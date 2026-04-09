"""
Concrete data adapters for the standard bot MVP.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import requests

from ..core import Bar, BundleMeta, MarketBundle, MarketQuery


_SPOT_KLINES_URL = "https://api.binance.com/api/v3/uiKlines"
_FUTURES_KLINES_URL = "https://fapi.binance.com/fapi/v1/klines"


def _series_key(instrument_id: str, timeframe: str) -> str:
    return MarketBundle.key(instrument_id, timeframe)


def _parse_kline_row(instrument_id: str, timeframe: str, row: list) -> Bar:
    open_time = int(row[0])
    close_time = int(row[6])
    return Bar(
        open=float(row[1]),
        high=float(row[2]),
        low=float(row[3]),
        close=float(row[4]),
        volume=float(row[5]),
        quote_volume=float(row[7]) if len(row) > 7 else None,
        timestamp=close_time,
        instrument_id=instrument_id.upper(),
        timeframe=timeframe,
        confirmed=True,
        extras={
            "open_time": open_time,
            "close_time": close_time,
            "trades": int(row[8]) if len(row) > 8 else None,
        },
    )


@dataclass
class BinanceRestMarketDataAdapter:
    market_type: str = "spot"
    timeout: int = 30
    base_url_override: Optional[str] = None

    @property
    def base_url(self) -> str:
        if self.base_url_override:
            return self.base_url_override
        return _FUTURES_KLINES_URL if self.market_type == "futures" else _SPOT_KLINES_URL

    def fetch_market(self, market_query: MarketQuery) -> MarketBundle:
        series: Dict[str, List[Bar]] = {}
        fetched_at = int(time.time() * 1000)

        for instrument_id in market_query.instruments:
            for timeframe in market_query.timeframes:
                rows = self._fetch_klines(instrument_id, timeframe, market_query)
                bars = [_parse_kline_row(instrument_id, timeframe, row) for row in rows]
                series[_series_key(instrument_id, timeframe)] = bars

        return MarketBundle(
            bars=series,
            meta=BundleMeta(
                data_source="binance_%s_rest" % self.market_type,
                fetched_at=fetched_at,
            ),
        )

    def _fetch_klines(self, instrument_id: str, timeframe: str, market_query: MarketQuery) -> list:
        params = {
            "symbol": instrument_id.upper(),
            "interval": timeframe,
        }
        if market_query.time_range.tail_bars is not None:
            params["limit"] = int(market_query.time_range.tail_bars)
        if market_query.time_range.start_ts is not None:
            params["startTime"] = int(market_query.time_range.start_ts)
        if market_query.time_range.end_ts is not None:
            params["endTime"] = int(market_query.time_range.end_ts)

        response = requests.get(self.base_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


@dataclass
class HistoricalJsonMarketDataAdapter:
    data_path: str
    instrument_id: Optional[str] = None
    timeframe: Optional[str] = None

    def fetch_market(self, market_query: MarketQuery) -> MarketBundle:
        payload = json.loads(Path(self.data_path).read_text(encoding="utf-8"))
        rows = payload["data"] if isinstance(payload, dict) and "data" in payload else payload
        instrument_id = (self.instrument_id or payload.get("symbol") or market_query.instruments[0]).upper()
        timeframe = self.timeframe or payload.get("interval") or market_query.timeframes[0]
        bars = [self._row_to_bar(instrument_id, timeframe, row) for row in rows]
        filtered = self._filter_bars(bars, market_query)
        return MarketBundle(
            bars={_series_key(instrument_id, timeframe): filtered},
            meta=BundleMeta(
                data_source="historical_json",
                fetched_at=int(time.time() * 1000),
            ),
        )

    def _row_to_bar(self, instrument_id: str, timeframe: str, row: dict) -> Bar:
        close_time = int(row["close_time"])
        open_time = int(row.get("open_time", close_time))
        return Bar(
            open=float(row["open_price"]),
            high=float(row["high_price"]),
            low=float(row["low_price"]),
            close=float(row["close_price"]),
            volume=float(row["volume"]),
            quote_volume=float(row.get("quote_volume", 0.0)) if row.get("quote_volume") is not None else None,
            timestamp=close_time,
            instrument_id=instrument_id,
            timeframe=timeframe,
            confirmed=True,
            extras={"open_time": open_time, "close_time": close_time},
        )

    def _filter_bars(self, bars: list[Bar], market_query: MarketQuery) -> list[Bar]:
        filtered = bars
        if market_query.time_range.start_ts is not None:
            filtered = [bar for bar in filtered if bar.timestamp >= market_query.time_range.start_ts]
        if market_query.time_range.end_ts is not None:
            filtered = [bar for bar in filtered if bar.timestamp <= market_query.time_range.end_ts]
        if market_query.time_range.tail_bars is not None:
            filtered = filtered[-market_query.time_range.tail_bars :]
        return filtered
