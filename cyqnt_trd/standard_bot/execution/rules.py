"""
Baseline risk rules for the standard bot execution layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from ..core import AccountSnapshot, ExecutionIntent, TradeSide


@dataclass
class MaxPositionFractionRule:
    """
    Reject directional intents that exceed a configurable fraction of available cash.
    """

    max_fraction: float = 0.95
    base_currency: str = "USDT"

    def validate(self, intent: ExecutionIntent, account_snapshot: Optional[AccountSnapshot]) -> Optional[str]:
        if account_snapshot is None or intent.reduce_only:
            return None
        if not 0 < self.max_fraction <= 1:
            return "invalid_max_fraction"

        market_price = intent.risk_hints.get("market_price")
        available_cash = float(account_snapshot.balances.get(self.base_currency, 0.0))
        if available_cash <= 0:
            return "insufficient_cash"

        requested_notional = intent.risk_hints.get("requested_position_notional", intent.notional)
        if requested_notional is None and intent.quantity is not None and market_price is not None:
            requested_notional = float(intent.quantity) * float(market_price)
        if requested_notional is None:
            return "risk_missing_notional"

        if float(requested_notional) > available_cash * self.max_fraction + 1e-9:
            return "max_position_fraction_exceeded"
        return None


@dataclass
class LongOnlySinglePositionRule:
    """
    Prevent duplicate buy intents while an instrument is already held.
    """

    def validate(self, intent: ExecutionIntent, account_snapshot: Optional[AccountSnapshot]) -> Optional[str]:
        if intent.side != TradeSide.BUY or account_snapshot is None:
            return None
        for position in account_snapshot.positions:
            if position.instrument_id == intent.instrument_id and position.quantity > 0:
                return "position_exists"
        return None


@dataclass
class InstrumentWhitelistRule:
    """
    Restrict execution to an explicit instrument allowlist.
    """

    instruments: Sequence[str]

    def validate(self, intent: ExecutionIntent, account_snapshot: Optional[AccountSnapshot]) -> Optional[str]:  # noqa: ARG002
        allowed = {item.upper() for item in self.instruments}
        if not allowed:
            return "empty_instrument_whitelist"
        if intent.instrument_id.upper() not in allowed:
            return "instrument_not_whitelisted"
        return None


@dataclass
class MaxAbsoluteNotionalRule:
    """
    Bound a single order's notional exposure in quote currency.
    """

    max_notional: float

    def validate(self, intent: ExecutionIntent, account_snapshot: Optional[AccountSnapshot]) -> Optional[str]:  # noqa: ARG002
        if intent.reduce_only:
            return None
        if self.max_notional <= 0:
            return "invalid_max_notional"
        market_price = intent.risk_hints.get("market_price") or intent.risk_hints.get("reference_price")
        requested_notional = intent.risk_hints.get("requested_position_notional", intent.notional)
        if requested_notional is None and intent.quantity is not None and market_price is not None:
            requested_notional = float(intent.quantity) * float(market_price)
        if requested_notional is None:
            return "risk_missing_notional"
        if float(requested_notional) > float(self.max_notional) + 1e-9:
            return "max_absolute_notional_exceeded"
        return None
