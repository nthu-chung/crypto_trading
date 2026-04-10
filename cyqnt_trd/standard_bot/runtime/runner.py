"""
Market-only runtime runner backed by the standard bot protocols.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Optional

from ..core import AccountPosition, ExecutionIntent, RunSummary, SignalKind, SignalPipelineSpec, TradeSide
from ..data import AlignmentPolicy, HistoricalSnapshotAssembler
from ..data.interfaces import MarketDataAdapter
from ..execution import BrokerAdapter, ExecutionPlanner, RiskRule, build_client_tag
from .interfaces import RunContext
from ..signal import SignalPluginRegistry
from ..signal.interfaces import SignalState


class MarketOnlyPaperRunner:
    """
    Reuses the step-based signal pipeline to drive one paper-execution cycle.
    """

    def __init__(
        self,
        *,
        market_data: MarketDataAdapter,
        signal_registry: SignalPluginRegistry,
        broker: BrokerAdapter,
        policy: AlignmentPolicy,
        risk_rules: Optional[List[RiskRule]] = None,
        execution_planner: Optional[ExecutionPlanner] = None,
        snapshot_tail_bars: int = 120,
        default_buy_fraction: float = 0.95,
    ) -> None:
        self.market_data = market_data
        self.signal_registry = signal_registry
        self.broker = broker
        self.policy = policy
        self.risk_rules = risk_rules or []
        self.execution_planner = execution_planner or ExecutionPlanner()
        self.snapshot_tail_bars = snapshot_tail_bars
        self.default_buy_fraction = default_buy_fraction
        self._plugin_states: Dict[str, SignalState] = {}

    def run(self, context: RunContext) -> RunSummary:
        if context.data_query.market is None:
            return RunSummary(
                run_id=context.run_id,
                status="error",
                signal_count=0,
                errors=["market_query_required"],
            )

        signal_pipeline = context.signal_pipeline or context.extras.get("signal_pipeline")
        if not isinstance(signal_pipeline, SignalPipelineSpec):
            return RunSummary(
                run_id=context.run_id,
                status="error",
                signal_count=0,
                errors=["signal_pipeline_required"],
            )

        request_policy = self.policy
        if context.data_query.market.timeframes:
            request_policy = replace(
                self.policy,
                primary_timeframe=context.data_query.market.timeframes[0],
            )

        market_bundle = self.market_data.fetch_market(context.data_query.market)
        snapshots = HistoricalSnapshotAssembler(
            policy=request_policy,
            tail_bars=self.snapshot_tail_bars,
        ).build(market_bundle)
        if not snapshots:
            return RunSummary(
                run_id=context.run_id,
                status="error",
                signal_count=0,
                errors=["no_snapshots_built"],
            )

        warm_snapshots = snapshots[:-1] if not self._plugin_states and len(snapshots) > 1 else []
        for warm_snapshot in warm_snapshots:
            warm_step = self.signal_registry.run_pipeline_step(
                warm_snapshot,
                signal_pipeline.plugin_chain,
                previous_states=self._plugin_states,
                context=context.signal_context,
            )
            self._plugin_states = warm_step.states

        latest_snapshot = snapshots[-1]
        account_snapshot = self.broker.sync_account()
        signal_context = replace(
            context.signal_context,
            account_snapshot=account_snapshot,
            previous_positions={item.instrument_id: item.quantity for item in account_snapshot.positions},
        )
        step_result = self.signal_registry.run_pipeline_step(
            latest_snapshot,
            signal_pipeline.plugin_chain,
            previous_states=self._plugin_states,
            context=signal_context,
        )
        self._plugin_states = step_result.states

        intents = self.execution_planner.build_intents(step_result.batch)
        intents = self._materialize_intents(
            intents,
            account_snapshot,
            latest_snapshot,
            context.run_id,
            request_policy.primary_timeframe,
        )

        reports = []
        errors = []
        for intent in intents:
            reject_reason = self._validate_intent(intent, account_snapshot)
            if reject_reason is not None:
                errors.append("%s:%s" % (intent.intent_id, reject_reason))
                continue
            if context.dry_run or context.trigger.signal_only:
                continue
            report = self.broker.place_order(intent)
            reports.append(report)
            if report.status.value == "rejected" and report.reason:
                errors.append("%s:%s" % (intent.intent_id, report.reason))
            else:
                account_snapshot = self.broker.sync_account()

        status = "ok" if not errors else "partial"
        if context.dry_run or context.trigger.signal_only:
            status = "dry_run"

        return RunSummary(
            run_id=context.run_id,
            status=status,
            signal_count=len([signal for signal in step_result.batch.signals if signal.kind == SignalKind.TRADE]),
            signals=step_result.batch.signals,
            execution_reports=reports,
            errors=errors,
        )

    def _materialize_intents(self, intents, account_snapshot, latest_snapshot, run_id: str, primary_timeframe: str):
        market = latest_snapshot.require_market()
        current_instrument = next(iter(market.bars.keys())).split("|", 1)[0]
        current_timeframe = primary_timeframe
        series = market.bars.get(market.key(current_instrument, current_timeframe), [])
        latest_price = series[-1].close if series else None

        position_map = {position.instrument_id: position for position in account_snapshot.positions}
        cash = float(account_snapshot.balances.get("USDT", 0.0))
        materialized = []
        for intent in intents:
            risk_hints = dict(intent.risk_hints)
            if latest_price is not None:
                risk_hints.setdefault("market_price", latest_price)
                risk_hints.setdefault("reference_price", latest_price)

            position = position_map.get(intent.instrument_id)
            target_position = self._target_position(risk_hints)
            quantity = intent.quantity
            notional = intent.notional
            reduce_only = intent.reduce_only

            if quantity is None and notional is None:
                resolved = self._resolve_default_sizing(
                    intent=intent,
                    target_position=target_position,
                    current_position=position,
                    latest_price=latest_price,
                    available_cash=cash,
                )
                if resolved is None:
                    continue
                quantity = resolved.get("quantity")
                notional = resolved.get("notional")
                reduce_only = bool(resolved.get("reduce_only", reduce_only))
                if "requested_position_notional" in resolved:
                    risk_hints.setdefault(
                        "requested_position_notional",
                        float(resolved["requested_position_notional"]),
                    )

            materialized.append(
                ExecutionIntent(
                    intent_id=intent.intent_id,
                    instrument_id=intent.instrument_id,
                    side=intent.side,
                    order_type=intent.order_type,
                    quantity=quantity,
                    notional=notional,
                    price=intent.price,
                    time_in_force=intent.time_in_force,
                    reduce_only=reduce_only,
                    client_tag=intent.client_tag or build_client_tag(run_id, intent.intent_id),
                    risk_hints=risk_hints,
                    source_signal_id=intent.source_signal_id,
                )
            )
        return materialized

    def _validate_intent(self, intent: ExecutionIntent, account_snapshot) -> Optional[str]:
        if intent.quantity is None and intent.notional is None:
            return "missing_size"
        if intent.side == TradeSide.BUY or intent.notional is not None:
            market_price = intent.risk_hints.get("market_price")
            if market_price is None and intent.price is None:
                return "missing_market_price"
        for rule in self.risk_rules:
            reject_reason = rule.validate(intent, account_snapshot)
            if reject_reason is not None:
                return reject_reason
        return None

    def _find_position(self, positions: List[AccountPosition], instrument_id: str) -> Optional[AccountPosition]:
        for position in positions:
            if position.instrument_id == instrument_id:
                return position
        return None

    def _target_position(self, risk_hints: Dict[str, object]) -> Optional[int]:
        raw_value = risk_hints.get("target_position")
        if raw_value is None:
            return None
        try:
            value = int(raw_value)
        except (TypeError, ValueError):
            return None
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0

    def _position_direction(self, position: Optional[AccountPosition]) -> int:
        if position is None or position.quantity <= 0:
            return 0
        return -1 if position.side == "short" else 1

    def _resolve_default_sizing(
        self,
        *,
        intent: ExecutionIntent,
        target_position: Optional[int],
        current_position: Optional[AccountPosition],
        latest_price: Optional[float],
        available_cash: float,
    ) -> Optional[Dict[str, float | bool]]:
        current_direction = self._position_direction(current_position)
        desired_notional = available_cash * self.default_buy_fraction
        if target_position == 0:
            if current_position is None:
                return None
            return {"quantity": float(current_position.quantity), "reduce_only": True}

        if target_position in {-1, 1}:
            if current_direction == target_position:
                return None
            if latest_price is None or latest_price <= 0 or desired_notional <= 0:
                return None
            desired_quantity = desired_notional / latest_price
            if current_direction == 0:
                return {
                    "notional": desired_notional,
                    "requested_position_notional": desired_notional,
                }
            return {
                "quantity": float(current_position.quantity) + desired_quantity,
                "requested_position_notional": desired_notional,
            }

        if intent.side == TradeSide.SELL and current_direction > 0 and current_position is not None:
            return {"quantity": float(current_position.quantity), "reduce_only": True}
        if intent.side == TradeSide.BUY and current_direction < 0 and current_position is not None:
            return {"quantity": float(current_position.quantity), "reduce_only": True}
        if intent.side == TradeSide.BUY and desired_notional > 0:
            return {"notional": desired_notional}
        return None
