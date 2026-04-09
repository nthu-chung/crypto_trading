"""
Interfaces for the standard bot execution layer.
"""

from __future__ import annotations

from typing import List, Optional, Protocol

from ..core import AccountSnapshot, ExecutionIntent, ExecutionReport, OrderType, SignalBatch


class RiskRule(Protocol):
    def validate(self, intent: ExecutionIntent, account_snapshot: Optional[AccountSnapshot]) -> Optional[str]:
        """
        Return ``None`` when the intent is allowed, otherwise return the reject reason.
        """
        ...


class BrokerAdapter(Protocol):
    def place_order(self, intent: ExecutionIntent) -> ExecutionReport:
        ...

    def cancel_order(self, intent_id: str) -> ExecutionReport:
        ...

    def sync_account(self) -> AccountSnapshot:
        ...


class ExecutionPlanner:
    """
    Default mapper from trade signals to execution intents.
    """

    def build_intents(self, signal_batch: SignalBatch) -> List[ExecutionIntent]:
        intents = []
        for signal in signal_batch.trade_signals():
            if signal.instrument_id is None or signal.side is None:
                continue
            raw_order_type = signal.payload.get("order_type", OrderType.MARKET)
            order_type = raw_order_type if isinstance(raw_order_type, OrderType) else OrderType(str(raw_order_type))
            intents.append(
                ExecutionIntent(
                    intent_id=signal.signal_id,
                    instrument_id=signal.instrument_id,
                    side=signal.side,
                    order_type=order_type,
                    quantity=signal.payload.get("quantity"),
                    notional=signal.payload.get("notional"),
                    price=signal.payload.get("price"),
                    source_signal_id=signal.signal_id,
                    risk_hints=signal.payload.get("risk_hints", {}),
                )
            )
        return intents
