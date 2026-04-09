"""
Paper execution components for the standard bot MVP.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ..core import (
    AccountPosition,
    AccountSnapshot,
    ExecutionIntent,
    ExecutionReport,
    ExecutionStatus,
    Fill,
    TradeSide,
)

PAPER_NAMESPACE = uuid.UUID("6cc0ce80-a23e-54a5-9aaf-d68650cd4b03")


def _now_ms() -> int:
    return int(time.time() * 1000)


@dataclass
class PaperBrokerAdapter:
    """
    Minimal paper broker for market-only long/flat execution.
    """

    account_id: str = "paper"
    base_currency: str = "USDT"
    initial_cash: float = 10_000.0
    fee_bps: float = 10.0
    slippage_bps: float = 0.0
    balances: Dict[str, float] = field(default_factory=dict)
    positions: Dict[str, AccountPosition] = field(default_factory=dict)
    reports: List[ExecutionReport] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.base_currency not in self.balances:
            self.balances[self.base_currency] = float(self.initial_cash)

    def place_order(self, intent: ExecutionIntent) -> ExecutionReport:
        market_price = self._resolve_price(intent)
        if market_price is None or market_price <= 0:
            return self._reject(intent, "missing_market_price")

        fill_price = self._apply_slippage(market_price, intent.side)
        quantity = self._resolve_quantity(intent, fill_price)
        if quantity is None or quantity <= 0:
            return self._reject(intent, "missing_quantity")

        if intent.side == TradeSide.BUY:
            return self._execute_buy(intent, fill_price, quantity)
        if intent.side == TradeSide.SELL:
            return self._execute_sell(intent, fill_price, quantity)
        return self._reject(intent, "unsupported_side")

    def cancel_order(self, intent_id: str) -> ExecutionReport:
        report = ExecutionReport(
            intent_id=intent_id,
            status=ExecutionStatus.CANCELLED,
            external_ids={"broker": "paper"},
        )
        self.reports.append(report)
        return report

    def sync_account(self) -> AccountSnapshot:
        return AccountSnapshot(
            account_id=self.account_id,
            balances={key: float(value) for key, value in self.balances.items()},
            positions=[
                AccountPosition(
                    instrument_id=position.instrument_id,
                    quantity=float(position.quantity),
                    avg_entry_price=position.avg_entry_price,
                    side=position.side,
                )
                for position in self.positions.values()
                if position.quantity > 0
            ],
            fetched_at=_now_ms(),
        )

    def _resolve_price(self, intent: ExecutionIntent) -> Optional[float]:
        if intent.price is not None:
            return float(intent.price)
        market_price = intent.risk_hints.get("market_price")
        if market_price is None:
            market_price = intent.risk_hints.get("reference_price")
        return None if market_price is None else float(market_price)

    def _apply_slippage(self, price: float, side: TradeSide) -> float:
        delta = self.slippage_bps / 10_000.0
        if side == TradeSide.BUY:
            return price * (1.0 + delta)
        if side == TradeSide.SELL:
            return price * (1.0 - delta)
        return price

    def _resolve_quantity(self, intent: ExecutionIntent, price: float) -> Optional[float]:
        if intent.quantity is not None:
            return float(intent.quantity)
        if intent.notional is not None and price > 0:
            return float(intent.notional) / price
        return None

    def _execute_buy(self, intent: ExecutionIntent, price: float, quantity: float) -> ExecutionReport:
        cash = float(self.balances.get(self.base_currency, 0.0))
        gross = quantity * price
        fee = gross * self.fee_bps / 10_000.0
        total_cost = gross + fee
        if total_cost > cash + 1e-9:
            return self._reject(intent, "insufficient_cash")

        self.balances[self.base_currency] = cash - total_cost
        current = self.positions.get(intent.instrument_id)
        next_qty = quantity if current is None else current.quantity + quantity
        avg_entry = price
        if current is not None and current.avg_entry_price is not None and next_qty > 0:
            avg_entry = ((current.quantity * current.avg_entry_price) + gross) / next_qty
        self.positions[intent.instrument_id] = AccountPosition(
            instrument_id=intent.instrument_id,
            quantity=next_qty,
            avg_entry_price=avg_entry,
            side="long",
        )
        return self._filled(intent, price=price, quantity=quantity, fee=fee)

    def _execute_sell(self, intent: ExecutionIntent, price: float, quantity: float) -> ExecutionReport:
        current = self.positions.get(intent.instrument_id)
        if current is None or current.quantity <= 0:
            return self._reject(intent, "no_position")
        if quantity > current.quantity + 1e-9:
            return self._reject(intent, "insufficient_position")

        gross = quantity * price
        fee = gross * self.fee_bps / 10_000.0
        self.balances[self.base_currency] = float(self.balances.get(self.base_currency, 0.0)) + gross - fee

        remaining = current.quantity - quantity
        if remaining <= 1e-9:
            self.positions.pop(intent.instrument_id, None)
        else:
            self.positions[intent.instrument_id] = AccountPosition(
                instrument_id=intent.instrument_id,
                quantity=remaining,
                avg_entry_price=current.avg_entry_price,
                side="long",
            )
        return self._filled(intent, price=price, quantity=quantity, fee=fee)

    def _filled(self, intent: ExecutionIntent, *, price: float, quantity: float, fee: float) -> ExecutionReport:
        report = ExecutionReport(
            intent_id=intent.intent_id,
            status=ExecutionStatus.FILLED,
            external_ids={
                "broker": "paper",
                "paper_fill_id": str(uuid.uuid5(PAPER_NAMESPACE, "%s|%s|%s" % (intent.intent_id, price, quantity))),
            },
            fills=[Fill(price=price, quantity=quantity, fee=fee, filled_at=_now_ms())],
        )
        self.reports.append(report)
        return report

    def _reject(self, intent: ExecutionIntent, reason: str) -> ExecutionReport:
        report = ExecutionReport(
            intent_id=intent.intent_id,
            status=ExecutionStatus.REJECTED,
            external_ids={"broker": "paper"},
            reason=reason,
        )
        self.reports.append(report)
        return report
