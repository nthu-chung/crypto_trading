"""
Interfaces for the standard bot simulation layer.
"""

from __future__ import annotations

from typing import Optional, Protocol

from ..core import BacktestRequest, BacktestResult, DataSnapshot, ExecutionIntent, ExecutionReport


class FeeModel(Protocol):
    def estimate_fee(self, intent: ExecutionIntent, price: float, quantity: float) -> float:
        ...


class SlippageModel(Protocol):
    def adjust_price(self, snapshot: DataSnapshot, intent: ExecutionIntent) -> float:
        ...


class FillModel(Protocol):
    def fill(self, snapshot: DataSnapshot, intent: ExecutionIntent) -> ExecutionReport:
        ...


class BacktestEngine(Protocol):
    def run(self, request: BacktestRequest) -> BacktestResult:
        ...
