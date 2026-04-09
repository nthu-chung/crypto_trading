"""
Execution layer exports for the standard bot architecture.
"""

from .binance_futures_testnet import BinanceFuturesTestnetBrokerAdapter
from .idempotency import build_client_tag
from .interfaces import BrokerAdapter, ExecutionPlanner, RiskRule
from .paper import PaperBrokerAdapter
from .rules import LongOnlySinglePositionRule, MaxPositionFractionRule

__all__ = [
    "BinanceFuturesTestnetBrokerAdapter",
    "BrokerAdapter",
    "ExecutionPlanner",
    "build_client_tag",
    "LongOnlySinglePositionRule",
    "MaxPositionFractionRule",
    "PaperBrokerAdapter",
    "RiskRule",
]
