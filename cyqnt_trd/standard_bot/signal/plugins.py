"""
MVP signal plugins for the standard bot architecture.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..core import (
    DataSnapshot,
    SignalBatch,
    SignalContext,
    SignalEnvelope,
    SignalKind,
    SignalProvenance,
    TradeSide,
)
from .interfaces import SignalState, StepSignalResult

SIGNAL_NAMESPACE = uuid.UUID("6d011acb-2b89-5dc5-bd38-fa9f903e6495")


def _now_ms() -> int:
    return int(time.time() * 1000)


def _mean(values: List[float]) -> float:
    return sum(values) / len(values)


def _normalize_strength(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return abs(numerator / denominator)


def _compute_rsi(closes: List[float], period: int) -> Optional[float]:
    if len(closes) < period + 1:
        return None
    relevant = closes[-(period + 1) :]
    gains = 0.0
    losses = 0.0
    for index in range(1, len(relevant)):
        delta = relevant[index] - relevant[index - 1]
        if delta > 0:
            gains += delta
        elif delta < 0:
            losses += -delta
    avg_gain = gains / period
    avg_loss = losses / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def _series_for(snapshot: DataSnapshot, instrument_id: str, timeframe: str):
    market = snapshot.require_market()
    return market.bars.get(market.key(instrument_id, timeframe), [])


@dataclass
class MovingAverageCrossConfig:
    instrument_id: str
    timeframe: str
    fast_window: int = 5
    slow_window: int = 20
    entry_threshold: float = 0.0
    time_horizon: str = "swing"

    def __post_init__(self) -> None:
        self.instrument_id = self.instrument_id.upper()
        if self.fast_window < 1:
            raise ValueError("fast_window must be >= 1")
        if self.slow_window <= self.fast_window:
            raise ValueError("slow_window must be greater than fast_window")
        if self.entry_threshold < 0:
            raise ValueError("entry_threshold must be >= 0")


@dataclass
class PriceMovingAverageConfig:
    instrument_id: str
    timeframe: str
    period: int = 5
    entry_threshold: float = 0.0
    time_horizon: str = "swing"

    def __post_init__(self) -> None:
        self.instrument_id = self.instrument_id.upper()
        if self.period < 2:
            raise ValueError("period must be >= 2")
        if self.entry_threshold < 0:
            raise ValueError("entry_threshold must be >= 0")


@dataclass
class RsiReversionConfig:
    instrument_id: str
    timeframe: str
    period: int = 14
    oversold: float = 30.0
    overbought: float = 70.0
    time_horizon: str = "mean_reversion"

    def __post_init__(self) -> None:
        self.instrument_id = self.instrument_id.upper()
        if self.period < 2:
            raise ValueError("period must be >= 2")
        if self.oversold <= 0 or self.oversold >= 100:
            raise ValueError("oversold must be within (0, 100)")
        if self.overbought <= 0 or self.overbought >= 100:
            raise ValueError("overbought must be within (0, 100)")
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be less than overbought")


class MovingAverageCrossPlugin:
    plugin_id = "moving_average_cross"
    plugin_version = "mvp/v1"

    def required_inputs(self) -> Dict[str, bool]:
        return {"market": True, "social": False, "onchain": False}

    def run(
        self,
        snapshot: DataSnapshot,
        config: MovingAverageCrossConfig,
        context: Optional[SignalContext] = None,
    ) -> SignalBatch:
        series = self._get_series(snapshot, config)
        if not series:
            return self._build_batch(snapshot, [])

        signals: List[SignalEnvelope] = []
        closes: List[float] = []
        for bar in series:
            closes.append(bar.close)
            signal = self._signal_for_window(
                closes=closes,
                timestamp=bar.timestamp,
                snapshot=snapshot,
                config=config,
                context=context,
            )
            if signal is not None:
                signals.append(signal)
        return self._build_batch(snapshot, signals)

    def initialize_state(self) -> SignalState:
        return SignalState(plugin_id=self.plugin_id, values={"cursor": None, "close_window": []})

    def step(
        self,
        snapshot: DataSnapshot,
        state: SignalState,
        config: MovingAverageCrossConfig,
        context: Optional[SignalContext] = None,
    ) -> StepSignalResult:
        series = self._get_series(snapshot, config)
        if not series:
            return StepSignalResult(state=state, signals=[])

        cursor = state.values.get("cursor")
        close_window = [float(value) for value in state.values.get("close_window", [])]
        emitted: List[SignalEnvelope] = []

        for bar in series:
            if cursor is not None and bar.timestamp <= cursor:
                continue
            close_window.append(float(bar.close))
            if len(close_window) > config.slow_window:
                close_window = close_window[-config.slow_window :]
            signal = self._signal_for_window(
                closes=close_window,
                timestamp=bar.timestamp,
                snapshot=snapshot,
                config=config,
                context=context,
            )
            if signal is not None:
                emitted.append(signal)
            cursor = bar.timestamp

        next_state = SignalState(
            plugin_id=self.plugin_id,
            values={"cursor": cursor, "close_window": close_window},
        )
        return StepSignalResult(state=next_state, signals=emitted)

    def _get_series(self, snapshot: DataSnapshot, config: MovingAverageCrossConfig):
        return _series_for(snapshot, config.instrument_id, config.timeframe)

    def _signal_for_window(
        self,
        *,
        closes: List[float],
        timestamp: int,
        snapshot: DataSnapshot,
        config: MovingAverageCrossConfig,
        context: Optional[SignalContext],
    ) -> Optional[SignalEnvelope]:
        if len(closes) < config.slow_window:
            return None

        fast_sma = _mean(closes[-config.fast_window :])
        slow_sma = _mean(closes[-config.slow_window :])
        if slow_sma == 0:
            return None

        spread = (fast_sma - slow_sma) / slow_sma
        if abs(spread) <= config.entry_threshold:
            return None

        side = TradeSide.BUY if spread > 0 else TradeSide.SELL
        signal_id = str(
            uuid.uuid5(
                SIGNAL_NAMESPACE,
                "%s|%s|%s|%s|%s"
                % (
                    snapshot.meta.snapshot_id,
                    config.instrument_id,
                    config.timeframe,
                    timestamp,
                    side.value,
                ),
            )
        )
        return SignalEnvelope(
            version="mvp/v1",
            signal_id=signal_id,
            kind=SignalKind.TRADE,
            instrument_id=config.instrument_id,
            side=side,
            strength=_normalize_strength(fast_sma - slow_sma, slow_sma),
            time_horizon=config.time_horizon,
            valid_until=snapshot.meta.decision_as_of,
            payload={
                "bar_timestamp": timestamp,
                "fast_sma": fast_sma,
                "slow_sma": slow_sma,
                "spread": spread,
                "blocked_instruments": [] if context is None else context.blacklist,
            },
            provenance=SignalProvenance(
                plugin_id=self.plugin_id,
                plugin_version=self.plugin_version,
                config_hash="%s|%s|%s|%s"
                % (
                    config.instrument_id,
                    config.timeframe,
                    config.fast_window,
                    config.slow_window,
                ),
                input_fingerprint=snapshot.meta.snapshot_id,
            ),
        )

    def _build_batch(self, snapshot: DataSnapshot, signals: List[SignalEnvelope]) -> SignalBatch:
        batch_id = str(
            uuid.uuid5(
                SIGNAL_NAMESPACE,
                "%s|%s|%s" % (self.plugin_id, snapshot.meta.snapshot_id, len(signals)),
            )
        )
        return SignalBatch(signals=signals, batch_id=batch_id, created_at=_now_ms())


class PriceMovingAveragePlugin:
    plugin_id = "price_moving_average"
    plugin_version = "mvp/v1"

    def required_inputs(self) -> Dict[str, bool]:
        return {"market": True, "social": False, "onchain": False}

    def run(
        self,
        snapshot: DataSnapshot,
        config: PriceMovingAverageConfig,
        context: Optional[SignalContext] = None,
    ) -> SignalBatch:
        series = _series_for(snapshot, config.instrument_id, config.timeframe)
        if not series:
            return self._build_batch(snapshot, [])

        closes: List[float] = []
        signals: List[SignalEnvelope] = []
        for bar in series:
            closes.append(float(bar.close))
            if len(closes) > config.period + 2:
                closes = closes[-(config.period + 2) :]
            signal = self._signal_for_window(
                closes=closes,
                timestamp=bar.timestamp,
                snapshot=snapshot,
                config=config,
                context=context,
            )
            if signal is not None:
                signals.append(signal)
        return self._build_batch(snapshot, signals)

    def initialize_state(self) -> SignalState:
        return SignalState(plugin_id=self.plugin_id, values={"cursor": None, "close_window": []})

    def step(
        self,
        snapshot: DataSnapshot,
        state: SignalState,
        config: PriceMovingAverageConfig,
        context: Optional[SignalContext] = None,
    ) -> StepSignalResult:
        series = _series_for(snapshot, config.instrument_id, config.timeframe)
        if not series:
            return StepSignalResult(state=state, signals=[])

        cursor = state.values.get("cursor")
        close_window = [float(value) for value in state.values.get("close_window", [])]
        emitted: List[SignalEnvelope] = []
        for bar in series:
            if cursor is not None and bar.timestamp <= cursor:
                continue
            close_window.append(float(bar.close))
            if len(close_window) > config.period + 2:
                close_window = close_window[-(config.period + 2) :]
            signal = self._signal_for_window(
                closes=close_window,
                timestamp=bar.timestamp,
                snapshot=snapshot,
                config=config,
                context=context,
            )
            if signal is not None:
                emitted.append(signal)
            cursor = bar.timestamp
        return StepSignalResult(
            state=SignalState(plugin_id=self.plugin_id, values={"cursor": cursor, "close_window": close_window}),
            signals=emitted,
        )

    def _signal_for_window(
        self,
        *,
        closes: List[float],
        timestamp: int,
        snapshot: DataSnapshot,
        config: PriceMovingAverageConfig,
        context: Optional[SignalContext],
    ) -> Optional[SignalEnvelope]:
        if len(closes) < config.period + 2:
            return None

        current_price = closes[-1]
        prev_price = closes[-2]
        current_ma = _mean(closes[-config.period - 1 : -1])
        prev_ma = _mean(closes[-config.period - 2 : -2])
        if current_ma == 0 or prev_ma == 0:
            return None

        upward_cross = prev_price <= prev_ma and current_price > current_ma
        downward_cross = prev_price >= prev_ma and current_price < current_ma
        if not upward_cross and not downward_cross:
            return None

        spread = (current_price - current_ma) / current_ma
        if abs(spread) <= config.entry_threshold:
            return None

        side = TradeSide.BUY if upward_cross else TradeSide.SELL
        signal_id = str(
            uuid.uuid5(
                SIGNAL_NAMESPACE,
                "%s|%s|%s|%s|%s"
                % (
                    snapshot.meta.snapshot_id,
                    config.instrument_id,
                    config.timeframe,
                    timestamp,
                    side.value,
                ),
            )
        )
        return SignalEnvelope(
            version="mvp/v1",
            signal_id=signal_id,
            kind=SignalKind.TRADE,
            instrument_id=config.instrument_id,
            side=side,
            strength=_normalize_strength(current_price - current_ma, current_ma),
            time_horizon=config.time_horizon,
            valid_until=snapshot.meta.decision_as_of,
            payload={
                "bar_timestamp": timestamp,
                "current_price": current_price,
                "current_ma": current_ma,
                "prev_price": prev_price,
                "prev_ma": prev_ma,
                "spread": spread,
                "blocked_instruments": [] if context is None else context.blacklist,
            },
            provenance=SignalProvenance(
                plugin_id=self.plugin_id,
                plugin_version=self.plugin_version,
                config_hash="%s|%s|%s" % (config.instrument_id, config.timeframe, config.period),
                input_fingerprint=snapshot.meta.snapshot_id,
            ),
        )

    def _build_batch(self, snapshot: DataSnapshot, signals: List[SignalEnvelope]) -> SignalBatch:
        batch_id = str(
            uuid.uuid5(
                SIGNAL_NAMESPACE,
                "%s|%s|%s" % (self.plugin_id, snapshot.meta.snapshot_id, len(signals)),
            )
        )
        return SignalBatch(signals=signals, batch_id=batch_id, created_at=_now_ms())


class RsiReversionPlugin:
    plugin_id = "rsi_reversion"
    plugin_version = "mvp/v1"

    def required_inputs(self) -> Dict[str, bool]:
        return {"market": True, "social": False, "onchain": False}

    def run(
        self,
        snapshot: DataSnapshot,
        config: RsiReversionConfig,
        context: Optional[SignalContext] = None,
    ) -> SignalBatch:
        series = _series_for(snapshot, config.instrument_id, config.timeframe)
        if not series:
            return self._build_batch(snapshot, [])

        closes: List[float] = []
        signals: List[SignalEnvelope] = []
        for bar in series:
            closes.append(float(bar.close))
            if len(closes) > config.period + 1:
                closes = closes[-(config.period + 1) :]
            signal = self._signal_for_window(
                closes=closes,
                timestamp=bar.timestamp,
                snapshot=snapshot,
                config=config,
                context=context,
            )
            if signal is not None:
                signals.append(signal)
        return self._build_batch(snapshot, signals)

    def initialize_state(self) -> SignalState:
        return SignalState(plugin_id=self.plugin_id, values={"cursor": None, "close_window": []})

    def step(
        self,
        snapshot: DataSnapshot,
        state: SignalState,
        config: RsiReversionConfig,
        context: Optional[SignalContext] = None,
    ) -> StepSignalResult:
        series = _series_for(snapshot, config.instrument_id, config.timeframe)
        if not series:
            return StepSignalResult(state=state, signals=[])

        cursor = state.values.get("cursor")
        close_window = [float(value) for value in state.values.get("close_window", [])]
        emitted: List[SignalEnvelope] = []
        for bar in series:
            if cursor is not None and bar.timestamp <= cursor:
                continue
            close_window.append(float(bar.close))
            if len(close_window) > config.period + 1:
                close_window = close_window[-(config.period + 1) :]
            signal = self._signal_for_window(
                closes=close_window,
                timestamp=bar.timestamp,
                snapshot=snapshot,
                config=config,
                context=context,
            )
            if signal is not None:
                emitted.append(signal)
            cursor = bar.timestamp

        return StepSignalResult(
            state=SignalState(plugin_id=self.plugin_id, values={"cursor": cursor, "close_window": close_window}),
            signals=emitted,
        )

    def _signal_for_window(
        self,
        *,
        closes: List[float],
        timestamp: int,
        snapshot: DataSnapshot,
        config: RsiReversionConfig,
        context: Optional[SignalContext],
    ) -> Optional[SignalEnvelope]:
        rsi = _compute_rsi(closes, config.period)
        if rsi is None:
            return None
        if rsi < config.oversold:
            side = TradeSide.BUY
            strength = (config.oversold - rsi) / max(config.oversold, 1e-9)
        elif rsi > config.overbought:
            side = TradeSide.SELL
            strength = (rsi - config.overbought) / max(100.0 - config.overbought, 1e-9)
        else:
            return None

        signal_id = str(
            uuid.uuid5(
                SIGNAL_NAMESPACE,
                "%s|%s|%s|%s|%s"
                % (
                    snapshot.meta.snapshot_id,
                    config.instrument_id,
                    config.timeframe,
                    timestamp,
                    side.value,
                ),
            )
        )
        return SignalEnvelope(
            version="mvp/v1",
            signal_id=signal_id,
            kind=SignalKind.TRADE,
            instrument_id=config.instrument_id,
            side=side,
            strength=float(strength),
            time_horizon=config.time_horizon,
            valid_until=snapshot.meta.decision_as_of,
            payload={
                "bar_timestamp": timestamp,
                "rsi": rsi,
                "oversold": config.oversold,
                "overbought": config.overbought,
                "blocked_instruments": [] if context is None else context.blacklist,
            },
            provenance=SignalProvenance(
                plugin_id=self.plugin_id,
                plugin_version=self.plugin_version,
                config_hash="%s|%s|%s|%s|%s"
                % (
                    config.instrument_id,
                    config.timeframe,
                    config.period,
                    config.oversold,
                    config.overbought,
                ),
                input_fingerprint=snapshot.meta.snapshot_id,
            ),
        )

    def _build_batch(self, snapshot: DataSnapshot, signals: List[SignalEnvelope]) -> SignalBatch:
        batch_id = str(
            uuid.uuid5(
                SIGNAL_NAMESPACE,
                "%s|%s|%s" % (self.plugin_id, snapshot.meta.snapshot_id, len(signals)),
            )
        )
        return SignalBatch(signals=signals, batch_id=batch_id, created_at=_now_ms())


def register_builtin_plugins(registry) -> None:
    registry.register(MovingAverageCrossPlugin(), lambda raw: MovingAverageCrossConfig(**raw))
    registry.register(PriceMovingAveragePlugin(), lambda raw: PriceMovingAverageConfig(**raw))
    registry.register(RsiReversionPlugin(), lambda raw: RsiReversionConfig(**raw))
