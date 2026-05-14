"""
Persistent Numba-kernel paper trading session.

Guarantees signal consistency with NumbaBacktestRunner by using the same kernel
and the same execution model (signal at bar-close → fill at next-bar-open).

The session is meant to be held in memory by a long-running daemon.  External
watchers query the session state via the ``state_snapshot()`` dict — reading
this dict never mutates session state and never triggers a re-run.

Key design invariants:
1. Same kernel as backtest → same signals.
2. Growing series: each tick appends one new bar, kernel re-runs over full series.
3. Pending execution: signal from bar[i] fills at bar[i+1] open — matches backtest.
4. State is in-memory; ``state_snapshot()`` is a read-only projection.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .numba_runner import (
    EncodedSeries,
    NumbaBacktestRunner,
    NumbaKernelSpec,
    BUILTIN_NUMBA_STRATEGIES,
)
from ..signal.numba_kernels import TARGET_KEEP, TARGET_LONG, TARGET_SHORT


SESSION_NAMESPACE = uuid.UUID("a7e8d1c4-5b3f-4e2a-9f1d-6c0e8b7a2d54")


@dataclass
class PaperFill:
    """One simulated fill."""

    fill_id: str
    timestamp_ms: int
    side: str  # "buy" or "sell"
    price: float
    quantity: float
    fee: float
    signal_bar_timestamp_ms: int
    action: str  # "open_long", "close_long", "open_short", "close_short", ...


@dataclass
class PaperPosition:
    """Current open position."""

    side: str  # "long" or "short"
    entry_price: float
    quantity: float
    opened_at_ms: int


@dataclass
class PendingOrder:
    """A trade pending execution at the next bar's open."""

    target_position: int  # TARGET_LONG=1, TARGET_SHORT=-1, 0=flat
    signal_bar_index: int
    signal_bar_timestamp_ms: int
    signal_strength: float


class NumbaLivePaperSession:
    """
    Persistent in-memory paper trading session backed by a Numba kernel.

    Usage::

        session = NumbaLivePaperSession(
            strategy_id="ema_rsi_cross",
            symbol="BTCUSDT",
            config={"fast_window": 2, "slow_window": 5, ...},
            initial_capital=10000.0,
        )

        # On each new confirmed bar:
        session.tick(bar)  # bar is a dict with OHLCV + timestamp

        # Query state (read-only, no side effects):
        snapshot = session.state_snapshot()
    """

    def __init__(
        self,
        *,
        strategy_id: str,
        symbol: str,
        config: Dict[str, Any],
        initial_capital: float = 10_000.0,
        fee_bps: float = 10.0,
        slippage_bps: float = 0.0,
        market_type: str = "futures",
        contract_multiplier: float = 1.0,
        max_bar_volume_fraction: float = 0.10,
    ) -> None:
        # --- Validate: multi_timeframe not supported in live mode ---
        if strategy_id == "multi_timeframe_ma_spread":
            raise ValueError(
                "multi_timeframe_ma_spread is not supported in live paper mode; "
                "it requires synchronized dual-timeframe data"
            )

        # --- Validate strategy is registered ---
        if strategy_id in BUILTIN_NUMBA_STRATEGIES:
            self._spec: Optional[NumbaKernelSpec] = None
            self._is_builtin = True
        else:
            registered = NumbaBacktestRunner.registered_kernels()
            if strategy_id not in registered:
                raise ValueError(
                    "strategy '%s' is not registered; call "
                    "NumbaBacktestRunner.register_kernel() first" % strategy_id
                )
            self._spec = registered[strategy_id]
            self._is_builtin = False

        self.strategy_id = strategy_id
        self.symbol = symbol
        self.config = dict(config)
        self.market_type = market_type
        self.contract_multiplier = contract_multiplier
        self.max_bar_volume_fraction = max_bar_volume_fraction

        # --- Financial state ---
        self.initial_capital = float(initial_capital)
        self.cash = float(initial_capital)
        self.fee_bps = float(fee_bps)
        self.slippage_bps = float(slippage_bps)
        self.position: Optional[PaperPosition] = None
        self.position_qty: float = 0.0  # signed: +long, -short

        # --- Bar history (growing) ---
        self._timestamps: List[int] = []
        self._open_times: List[int] = []
        self._opens: List[float] = []
        self._highs: List[float] = []
        self._lows: List[float] = []
        self._closes: List[float] = []
        self._volumes: List[float] = []
        self._quote_volumes: List[float] = []
        self._oi_change_bps: List[float] = []
        self._funding_rate_bps: List[float] = []
        self._long_liq_notional_usd: List[float] = []
        self._short_liq_notional_usd: List[float] = []

        # --- Signal & execution state ---
        self._pending_order: Optional[PendingOrder] = None
        self._last_target: int = 0  # current target position direction
        self._target_history: List[int] = []  # target at each bar

        # --- Trade log ---
        self.trade_log: List[PaperFill] = []
        self._tick_count: int = 0
        self._session_id = str(uuid.uuid4())

        # --- Runner instance (shared for builtin and custom kernels) ---
        self._runner = NumbaBacktestRunner()

    # ─────────────────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────────────────

    def tick(self, bar: Dict[str, Any]) -> Optional[PaperFill]:
        """
        Process one new confirmed bar.

        Steps (in order to match backtest execution model):
        1. Execute any pending order at this bar's open price.
        2. Append bar to history.
        3. Run kernel over full history.
        4. If latest target differs from current position → create pending order.

        Returns a PaperFill if an execution happened, else None.
        """
        fill = None

        # Step 1: Execute pending order at this bar's open
        if self._pending_order is not None:
            open_price = float(bar["open"])
            volume = float(bar.get("volume", 1e12))
            quote_volume = float(bar.get("quote_volume", open_price * volume))
            fill = self._execute_pending(
                open_price=open_price,
                bar_timestamp_ms=int(bar["timestamp"]),
                volume=volume,
                quote_volume=quote_volume,
            )
            self._pending_order = None

        # Step 2: Append bar to history
        self._append_bar(bar)
        self._tick_count += 1

        # Step 3: Run kernel over full history
        target_at_this_bar, strength = self._compute_latest_target()
        self._target_history.append(target_at_this_bar)

        # Step 4: If target changed, create pending order for next bar
        if target_at_this_bar != TARGET_KEEP:
            current_direction = self._position_direction()
            target_direction = int(target_at_this_bar)
            if target_direction != current_direction:
                self._pending_order = PendingOrder(
                    target_position=target_direction,
                    signal_bar_index=len(self._timestamps) - 1,
                    signal_bar_timestamp_ms=int(bar["timestamp"]),
                    signal_strength=strength,
                )
                self._last_target = target_direction

        return fill

    def warm_up(self, bar: Dict[str, Any]) -> None:
        """
        Load one historical bar for indicator context without trading.

        Warm-up bars exist only so the kernel has enough lookback history when
        live polling starts. They must never execute pending orders and must
        never create a pending order that can fill on the first live bar.
        """
        self._append_bar(bar)
        self._tick_count += 1

        target_at_this_bar, _strength = self._compute_latest_target()
        self._target_history.append(target_at_this_bar)

        self._pending_order = None
        self._last_target = self._position_direction()

    def has_pending_order(self) -> bool:
        """Check if there's a trade waiting to execute at the next bar."""
        return self._pending_order is not None

    @property
    def equity(self) -> float:
        """Current equity = cash + position mark-to-market."""
        if not self._closes:
            return self.cash
        last_price = self._closes[-1]
        return self.cash + self.position_qty * last_price * self.contract_multiplier

    @property
    def pnl_usd(self) -> float:
        return self.equity - self.initial_capital

    @property
    def pnl_pct(self) -> float:
        if self.initial_capital == 0:
            return 0.0
        return self.pnl_usd / self.initial_capital

    def state_snapshot(self) -> Dict[str, Any]:
        """
        Read-only state projection compatible with watcher state.json format.

        Calling this method does NOT trigger any re-computation or mutation.
        """
        position_dict = None
        if self.position is not None:
            position_dict = {
                "side": self.position.side,
                "entry_price": self.position.entry_price,
                "qty": self.position.quantity,
                "notional": self.position.entry_price * self.position.quantity,
            }

        latest_signal = None
        if self._pending_order is not None:
            side = "long" if self._pending_order.target_position == 1 else (
                "short" if self._pending_order.target_position == -1 else "close"
            )
            latest_signal = {
                "signal_id": str(uuid.uuid5(
                    SESSION_NAMESPACE,
                    "%s|%s|%d" % (self._session_id, side, self._pending_order.signal_bar_timestamp_ms),
                )),
                "side": side,
                "strength": self._pending_order.signal_strength,
                "source": "numba_kernel",
                "pending": True,
            }
        elif self.trade_log:
            last_trade = self.trade_log[-1]
            latest_signal = {
                "signal_id": last_trade.fill_id,
                "side": last_trade.side,
                "strength": 0.0,
                "source": "numba_kernel",
                "pending": False,
            }

        return {
            "session_id": self._session_id,
            "strategy": self.strategy_id,
            "symbol": self.symbol,
            "market_type": self.market_type,
            "params": self.config,
            "initial_capital": self.initial_capital,
            "session_start_equity": self.initial_capital,
            "current_equity": round(self.equity, 4),
            "pnl_usd": round(self.pnl_usd, 4),
            "pnl": round(self.pnl_pct, 6),
            "position": position_dict,
            "latest_signal": latest_signal,
            "has_pending_order": self._pending_order is not None,
            "tick_count": self._tick_count,
            "bar_count": len(self._timestamps),
            "trade_count": len(self.trade_log),
            "trade_log": [self._fill_to_dict(f) for f in self.trade_log[-50:]],
            "last_bar_timestamp": self._timestamps[-1] if self._timestamps else None,
            "current_price": self._closes[-1] if self._closes else None,
            "last_update_ts": int(time.time()),
        }

    def checkpoint_state(self) -> Dict[str, Any]:
        """
        Serialize the full in-memory session so a daemon restart can resume.

        Unlike state_snapshot(), this captures internal runtime state such as bar
        history, pending orders, and cash so the next process can continue the
        exact same paper session instead of starting from scratch.
        """
        return {
            "format_version": 1,
            "session_id": self._session_id,
            "strategy_id": self.strategy_id,
            "symbol": self.symbol,
            "config": dict(self.config),
            "initial_capital": self.initial_capital,
            "cash": self.cash,
            "fee_bps": self.fee_bps,
            "slippage_bps": self.slippage_bps,
            "market_type": self.market_type,
            "contract_multiplier": self.contract_multiplier,
            "max_bar_volume_fraction": self.max_bar_volume_fraction,
            "position_qty": self.position_qty,
            "position": self._position_to_dict(self.position),
            "pending_order": self._pending_to_dict(self._pending_order),
            "last_target": self._last_target,
            "tick_count": self._tick_count,
            "target_history": list(self._target_history),
            "bars": {
                "timestamps": list(self._timestamps),
                "open_times": list(self._open_times),
                "opens": list(self._opens),
                "highs": list(self._highs),
                "lows": list(self._lows),
                "closes": list(self._closes),
                "volumes": list(self._volumes),
                "quote_volumes": list(self._quote_volumes),
                "oi_change_bps": list(self._oi_change_bps),
                "funding_rate_bps": list(self._funding_rate_bps),
                "long_liq_notional_usd": list(self._long_liq_notional_usd),
                "short_liq_notional_usd": list(self._short_liq_notional_usd),
            },
            "trade_log": [self._fill_to_checkpoint_dict(fill) for fill in self.trade_log],
        }

    @classmethod
    def from_checkpoint(cls, payload: Dict[str, Any]) -> "NumbaLivePaperSession":
        """Restore a session previously created by checkpoint_state()."""
        if int(payload.get("format_version", 0)) != 1:
            raise ValueError("unsupported live paper checkpoint format")

        session = cls(
            strategy_id=str(payload["strategy_id"]),
            symbol=str(payload["symbol"]),
            config=dict(payload["config"]),
            initial_capital=float(payload["initial_capital"]),
            fee_bps=float(payload["fee_bps"]),
            slippage_bps=float(payload["slippage_bps"]),
            market_type=str(payload.get("market_type", "futures")),
            contract_multiplier=float(payload.get("contract_multiplier", 1.0)),
            max_bar_volume_fraction=float(payload.get("max_bar_volume_fraction", 0.10)),
        )

        session._session_id = str(payload["session_id"])
        session.cash = float(payload["cash"])
        session.position_qty = float(payload.get("position_qty", 0.0))
        session.position = cls._position_from_dict(payload.get("position"))
        session._pending_order = cls._pending_from_dict(payload.get("pending_order"))
        session._last_target = int(payload.get("last_target", 0))
        session._tick_count = int(payload.get("tick_count", 0))
        session._target_history = [int(v) for v in payload.get("target_history", [])]

        bars = payload.get("bars", {})
        session._timestamps = [int(v) for v in bars.get("timestamps", [])]
        session._open_times = [int(v) for v in bars.get("open_times", [])]
        session._opens = [float(v) for v in bars.get("opens", [])]
        session._highs = [float(v) for v in bars.get("highs", [])]
        session._lows = [float(v) for v in bars.get("lows", [])]
        session._closes = [float(v) for v in bars.get("closes", [])]
        session._volumes = [float(v) for v in bars.get("volumes", [])]
        session._quote_volumes = [float(v) for v in bars.get("quote_volumes", [])]
        session._oi_change_bps = [float(v) for v in bars.get("oi_change_bps", [])]
        session._funding_rate_bps = [float(v) for v in bars.get("funding_rate_bps", [])]
        session._long_liq_notional_usd = [float(v) for v in bars.get("long_liq_notional_usd", [])]
        session._short_liq_notional_usd = [float(v) for v in bars.get("short_liq_notional_usd", [])]
        session.trade_log = [
            cls._fill_from_checkpoint_dict(item) for item in payload.get("trade_log", [])
        ]
        return session

    # ─────────────────────────────────────────────────────────────────────
    # Internal: bar management
    # ─────────────────────────────────────────────────────────────────────

    def _append_bar(self, bar: Dict[str, Any]) -> None:
        self._timestamps.append(int(bar["timestamp"]))
        self._open_times.append(int(bar.get("open_time", bar["timestamp"])))
        self._opens.append(float(bar["open"]))
        self._highs.append(float(bar["high"]))
        self._lows.append(float(bar["low"]))
        self._closes.append(float(bar["close"]))
        self._volumes.append(float(bar.get("volume", 0.0)))
        self._quote_volumes.append(float(bar.get("quote_volume", 0.0)))
        self._oi_change_bps.append(float(bar.get("oi_change_bps", 0.0)))
        self._funding_rate_bps.append(float(bar.get("funding_rate_bps", 0.0)))
        self._long_liq_notional_usd.append(float(bar.get("long_liq_notional_usd", 0.0)))
        self._short_liq_notional_usd.append(float(bar.get("short_liq_notional_usd", 0.0)))

    def _build_encoded_series(self) -> EncodedSeries:
        """Build numpy arrays from accumulated bar lists."""
        return EncodedSeries(
            timestamps=np.asarray(self._timestamps, dtype=np.int64),
            open_times=np.asarray(self._open_times, dtype=np.int64),
            opens=np.asarray(self._opens, dtype=np.float64),
            highs=np.asarray(self._highs, dtype=np.float64),
            lows=np.asarray(self._lows, dtype=np.float64),
            closes=np.asarray(self._closes, dtype=np.float64),
            volumes=np.asarray(self._volumes, dtype=np.float64),
            quote_volumes=np.asarray(self._quote_volumes, dtype=np.float64),
            oi_change_bps=np.asarray(self._oi_change_bps, dtype=np.float64),
            funding_rate_bps=np.asarray(self._funding_rate_bps, dtype=np.float64),
            long_liq_notional_usd=np.asarray(self._long_liq_notional_usd, dtype=np.float64),
            short_liq_notional_usd=np.asarray(self._short_liq_notional_usd, dtype=np.float64),
        )

    # ─────────────────────────────────────────────────────────────────────
    # Internal: kernel execution
    # ─────────────────────────────────────────────────────────────────────

    def _compute_latest_target(self) -> Tuple[int, float]:
        """
        Run kernel over full series, return (target_at_last_bar, strength).

        Uses the EXACT same code path as NumbaBacktestRunner._build_signal_targets
        to guarantee signal consistency.
        """
        series = self._build_encoded_series()

        if self._is_builtin:
            target_updates, strengths = self._runner._build_signal_targets(
                strategy_id=self.strategy_id,
                raw_config=self.config,
                market_bundle=None,  # not needed for single-timeframe builtins
                primary_series=series,
                instrument_id=self.symbol,
            )
        else:
            # Custom kernel — same path as _build_custom_signal_targets
            target_updates, strengths = self._runner._build_custom_signal_targets(
                strategy_id=self.strategy_id,
                raw_config=self.config,
                primary_series=series,
            )

        # Return the target at the last bar
        last_idx = len(self._timestamps) - 1
        target = int(target_updates[last_idx])
        strength = float(strengths[last_idx])
        return target, strength

    # ─────────────────────────────────────────────────────────────────────
    # Internal: execution (matches backtest execution model)
    # ─────────────────────────────────────────────────────────────────────

    def _execute_pending(
        self,
        *,
        open_price: float,
        bar_timestamp_ms: int,
        volume: float,
        quote_volume: float,
    ) -> Optional[PaperFill]:
        """
        Execute pending order at the given bar's open price.

        Matches the execution model in simulate_target_positions_next_open:
        - Target position computed from equity at execution time
        - Liquidity cap from bar volume
        - Slippage applied
        - Fees charged
        """
        pending = self._pending_order
        if pending is None:
            return None

        target_pos = pending.target_position
        multiplier = self.contract_multiplier

        # Compute target quantity (matches backtest logic exactly)
        equity_ref = self.cash + self.position_qty * open_price * multiplier
        if equity_ref < 0.0:
            equity_ref = 0.0

        if target_pos == 1:  # TARGET_LONG
            target_qty = equity_ref / (open_price * multiplier)
        elif target_pos == -1:  # TARGET_SHORT
            target_qty = -equity_ref / (open_price * multiplier)
        else:  # flat
            target_qty = 0.0

        # Compute delta
        delta_qty = target_qty - self.position_qty

        # Liquidity cap (same as backtest)
        if self.max_bar_volume_fraction > 0.0 and open_price > 0.0:
            base_cap = max(volume, 0.0) * self.max_bar_volume_fraction
            if quote_volume > 0.0:
                quote_cap = (quote_volume * self.max_bar_volume_fraction) / (open_price * multiplier)
                if quote_cap < base_cap:
                    base_cap = quote_cap
            available = max(base_cap, 0.0)
            if delta_qty > available:
                delta_qty = available
            elif delta_qty < -available:
                delta_qty = -available

        if abs(delta_qty) < 1e-12:
            return None

        # Slippage (same as backtest)
        slip = self.slippage_bps / 10_000.0
        if delta_qty > 0.0:
            fill_price = open_price * (1.0 + slip)
        else:
            fill_price = open_price * (1.0 - slip)

        # Fee
        fee = abs(delta_qty) * fill_price * multiplier * (self.fee_bps / 10_000.0)

        # Execute
        old_position_qty = self.position_qty
        self.cash -= delta_qty * fill_price * multiplier + fee
        self.position_qty += delta_qty
        if abs(self.position_qty) < 1e-12:
            self.position_qty = 0.0

        # Determine action label
        action = self._action_label(old_qty=old_position_qty, new_qty=self.position_qty)

        # Update position object
        if self.position_qty > 0:
            self.position = PaperPosition(
                side="long",
                entry_price=fill_price,
                quantity=abs(self.position_qty),
                opened_at_ms=bar_timestamp_ms,
            )
        elif self.position_qty < 0:
            self.position = PaperPosition(
                side="short",
                entry_price=fill_price,
                quantity=abs(self.position_qty),
                opened_at_ms=bar_timestamp_ms,
            )
        else:
            self.position = None

        # Record fill
        fill_id = str(uuid.uuid5(
            SESSION_NAMESPACE,
            "%s|%d|%s|%.8f" % (self._session_id, bar_timestamp_ms, action, fill_price),
        ))
        side = "buy" if delta_qty > 0 else "sell"

        paper_fill = PaperFill(
            fill_id=fill_id,
            timestamp_ms=bar_timestamp_ms,
            side=side,
            price=fill_price,
            quantity=abs(delta_qty),
            fee=fee,
            signal_bar_timestamp_ms=pending.signal_bar_timestamp_ms,
            action=action,
        )
        self.trade_log.append(paper_fill)
        return paper_fill

    def _position_direction(self) -> int:
        """Return current position direction: 1=long, -1=short, 0=flat."""
        if self.position_qty > 1e-12:
            return 1
        elif self.position_qty < -1e-12:
            return -1
        return 0

    @staticmethod
    def _action_label(*, old_qty: float, new_qty: float) -> str:
        old_dir = 1 if old_qty > 1e-12 else (-1 if old_qty < -1e-12 else 0)
        new_dir = 1 if new_qty > 1e-12 else (-1 if new_qty < -1e-12 else 0)

        if old_dir == 0 and new_dir == 1:
            return "open_long"
        if old_dir == 0 and new_dir == -1:
            return "open_short"
        if old_dir == 1 and new_dir == 0:
            return "close_long"
        if old_dir == -1 and new_dir == 0:
            return "close_short"
        if old_dir == -1 and new_dir == 1:
            return "flip_to_long"
        if old_dir == 1 and new_dir == -1:
            return "flip_to_short"
        return "rebalance"

    @staticmethod
    def _fill_to_dict(fill: PaperFill) -> Dict[str, Any]:
        return {
            "fill_id": fill.fill_id,
            "ts": fill.timestamp_ms // 1000,
            "side": fill.side,
            "price": fill.price,
            "qty": fill.quantity,
            "fee": fill.fee,
            "action": fill.action,
            "signal_bar_ts": fill.signal_bar_timestamp_ms,
        }

    @staticmethod
    def _fill_to_checkpoint_dict(fill: PaperFill) -> Dict[str, Any]:
        return {
            "fill_id": fill.fill_id,
            "timestamp_ms": fill.timestamp_ms,
            "side": fill.side,
            "price": fill.price,
            "quantity": fill.quantity,
            "fee": fill.fee,
            "signal_bar_timestamp_ms": fill.signal_bar_timestamp_ms,
            "action": fill.action,
        }

    @staticmethod
    def _fill_from_checkpoint_dict(payload: Dict[str, Any]) -> PaperFill:
        return PaperFill(
            fill_id=str(payload["fill_id"]),
            timestamp_ms=int(payload["timestamp_ms"]),
            side=str(payload["side"]),
            price=float(payload["price"]),
            quantity=float(payload["quantity"]),
            fee=float(payload["fee"]),
            signal_bar_timestamp_ms=int(payload["signal_bar_timestamp_ms"]),
            action=str(payload["action"]),
        )

    @staticmethod
    def _position_to_dict(position: Optional[PaperPosition]) -> Optional[Dict[str, Any]]:
        if position is None:
            return None
        return {
            "side": position.side,
            "entry_price": position.entry_price,
            "quantity": position.quantity,
            "opened_at_ms": position.opened_at_ms,
        }

    @staticmethod
    def _position_from_dict(payload: Optional[Dict[str, Any]]) -> Optional[PaperPosition]:
        if payload is None:
            return None
        return PaperPosition(
            side=str(payload["side"]),
            entry_price=float(payload["entry_price"]),
            quantity=float(payload["quantity"]),
            opened_at_ms=int(payload["opened_at_ms"]),
        )

    @staticmethod
    def _pending_to_dict(pending: Optional[PendingOrder]) -> Optional[Dict[str, Any]]:
        if pending is None:
            return None
        return {
            "target_position": pending.target_position,
            "signal_bar_index": pending.signal_bar_index,
            "signal_bar_timestamp_ms": pending.signal_bar_timestamp_ms,
            "signal_strength": pending.signal_strength,
        }

    @staticmethod
    def _pending_from_dict(payload: Optional[Dict[str, Any]]) -> Optional[PendingOrder]:
        if payload is None:
            return None
        return PendingOrder(
            target_position=int(payload["target_position"]),
            signal_bar_index=int(payload["signal_bar_index"]),
            signal_bar_timestamp_ms=int(payload["signal_bar_timestamp_ms"]),
            signal_strength=float(payload["signal_strength"]),
        )
