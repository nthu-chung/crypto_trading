"""
Binance USD-M futures mainnet broker adapter.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..config import BinanceMainnetCredentials
from ..core import AccountSnapshot
from .binance_futures_testnet import BinanceFuturesTestnetBrokerAdapter


@dataclass
class BinanceFuturesMainnetBrokerAdapter(BinanceFuturesTestnetBrokerAdapter):
    base_url: str = "https://fapi.binance.com"

    def __post_init__(self) -> None:
        if not self.api_key or not self.api_secret:
            credentials = BinanceMainnetCredentials.from_env(self.env_path)
            self.api_key = credentials.api_key
            self.api_secret = credentials.api_secret

    def sync_account(self) -> AccountSnapshot:
        snapshot = super().sync_account()
        return AccountSnapshot(
            account_id="binance_futures_mainnet",
            balances=snapshot.balances,
            positions=snapshot.positions,
            fetched_at=snapshot.fetched_at,
            extras={**snapshot.extras, "environment": "mainnet"},
        )
