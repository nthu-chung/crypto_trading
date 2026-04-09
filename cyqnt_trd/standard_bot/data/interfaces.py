"""
Interfaces for the standard bot data layer.
"""

from __future__ import annotations

from typing import Protocol

from ..core import DataQuery, DataSnapshot, MarketBundle, OnChainSignalBundle, SocialFeedBundle


class MarketDataAdapter(Protocol):
    def fetch_market(self, market_query) -> MarketBundle:
        ...


class SocialDataAdapter(Protocol):
    def fetch_social(self, social_query) -> SocialFeedBundle:
        ...


class OnChainDataAdapter(Protocol):
    def fetch_onchain(self, onchain_query) -> OnChainSignalBundle:
        ...


class SnapshotAssembler(Protocol):
    def assemble(self, query: DataQuery) -> DataSnapshot:
        ...
