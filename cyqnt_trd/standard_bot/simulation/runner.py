"""
Snapshot-driven backtest runner for the MVP.
"""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional

from ..core import BacktestRequest, BacktestResult, EquityPoint, SignalContext, SignalKind, TradeSide
from ..signal.registry import SignalPluginRegistry

SIMULATION_NAMESPACE = uuid.UUID("0bf7f6fd-3ca7-57aa-8266-4f22048d8bf8")


class SnapshotBacktestRunner:
    def __init__(self, *, signal_registry: SignalPluginRegistry) -> None:
        self.signal_registry = signal_registry

    def run(
        self,
        *,
        request: BacktestRequest,
        snapshots: list,
        signal_context: Optional[SignalContext] = None,
    ) -> BacktestResult:
        ordered = sorted(
            snapshots,
            key=lambda snapshot: snapshot.meta.decision_as_of or snapshot.meta.assembled_at,
        )
        plugin_states: Dict[str, object] = {}
        trade_rows: List[Dict] = []
        equity_curve: List[EquityPoint] = []
        signal_batches = []

        cash = float(request.initial_capital)
        position_qty = 0.0
        position_entry = 0.0
        current_instrument = request.instruments[0]
        commission_bps = float(request.fee_model.get("commission_bps", 0.0))
        slippage_bps = float(request.slippage_model.get("slippage_bps", 0.0))

        for snapshot in ordered:
            step_result = self.signal_registry.run_pipeline_step(
                snapshot,
                request.signal_pipeline.plugin_chain,
                previous_states=plugin_states,
                context=signal_context,
            )
            plugin_states = step_result.states
            signal_batches.append(step_result.batch)
            timestamp = snapshot.meta.decision_as_of or snapshot.meta.assembled_at

            market = snapshot.require_market()
            primary_key = market.key(current_instrument, request.primary_timeframe)
            series = market.bars.get(primary_key, [])
            if not series:
                continue
            latest_bar = series[-1]
            trade_signals = [signal for signal in step_result.batch.signals if signal.kind == SignalKind.TRADE]

            for signal in trade_signals:
                execution_price = latest_bar.close * (
                    1.0 + (slippage_bps / 10_000.0 if signal.side == TradeSide.BUY else -slippage_bps / 10_000.0)
                )
                if signal.side == TradeSide.BUY and position_qty == 0:
                    qty = cash / execution_price if execution_price > 0 else 0.0
                    fee = qty * execution_price * commission_bps / 10_000.0
                    if qty > 0:
                        cash = cash - qty * execution_price - fee
                        position_qty = qty
                        position_entry = execution_price
                        trade_rows.append(
                            {
                                "timestamp": timestamp,
                                "instrument_id": signal.instrument_id,
                                "side": signal.side.value,
                                "price": execution_price,
                                "quantity": qty,
                                "fee": fee,
                                "signal_id": signal.signal_id,
                                "action": "entry",
                            }
                        )
                elif signal.side == TradeSide.SELL and position_qty > 0:
                    fee = position_qty * execution_price * commission_bps / 10_000.0
                    realized = position_qty * execution_price - fee
                    pnl = (execution_price - position_entry) * position_qty - fee
                    cash = cash + realized
                    trade_rows.append(
                        {
                            "timestamp": timestamp,
                            "instrument_id": signal.instrument_id,
                            "side": signal.side.value,
                            "price": execution_price,
                            "quantity": position_qty,
                            "fee": fee,
                            "signal_id": signal.signal_id,
                            "action": "exit",
                            "entry_price": position_entry,
                            "pnl": pnl,
                        }
                    )
                    position_qty = 0.0
                    position_entry = 0.0

            equity = cash + position_qty * latest_bar.close
            equity_curve.append(EquityPoint(timestamp=timestamp, equity=float(equity), cash=float(cash)))

        if ordered and position_qty > 0:
            final_snapshot = ordered[-1]
            market = final_snapshot.require_market()
            series = market.bars.get(market.key(current_instrument, request.primary_timeframe), [])
            final_bar = series[-1]
            exit_price = final_bar.close
            fee = position_qty * exit_price * commission_bps / 10_000.0
            pnl = (exit_price - position_entry) * position_qty - fee
            cash = cash + position_qty * exit_price - fee
            trade_rows.append(
                {
                    "timestamp": final_bar.timestamp,
                    "instrument_id": current_instrument,
                    "side": "sell",
                    "price": exit_price,
                    "quantity": position_qty,
                    "fee": fee,
                    "action": "forced_exit",
                    "entry_price": position_entry,
                    "pnl": pnl,
                }
            )
            if equity_curve:
                equity_curve[-1] = EquityPoint(
                    timestamp=equity_curve[-1].timestamp,
                    equity=float(cash),
                    cash=float(cash),
                )

        run_id = str(
            uuid.uuid5(
                SIMULATION_NAMESPACE,
                "%s|%s|%s|%s"
                % (request.request_id, request.start_ts, request.end_ts, len(ordered)),
            )
        )
        initial = float(request.initial_capital)
        final_equity = float(equity_curve[-1].equity) if equity_curve else initial
        total_return = (final_equity - initial) / initial if initial else 0.0

        return BacktestResult(
            request_id=request.request_id,
            total_return=float(total_return),
            equity_curve=equity_curve,
            metrics={
                "snapshot_count": float(len(ordered)),
                "trade_count": float(len(trade_rows)),
                "final_equity": float(final_equity),
                "total_return": float(total_return),
            },
            signal_batches=signal_batches,
            extras={"run_id": run_id, "trades": trade_rows},
        )
