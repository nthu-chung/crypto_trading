"""
Shared helpers for standard bot CLI entrypoints.
"""

from __future__ import annotations

import argparse

from ..core import TimeRange
from ..core import SignalPipelineSpec
from ..data.adapters import BinanceRestMarketDataAdapter, HistoricalJsonMarketDataAdapter
from ..data.downloader import HistoricalBinanceDownloader
from ..data.historical import HistoricalParquetMarketDataAdapter, LocalFirstMarketDataAdapter
from ..signal import SignalPluginRegistry, register_builtin_plugins


def make_registry() -> SignalPluginRegistry:
    registry = SignalPluginRegistry()
    register_builtin_plugins(registry)
    return registry


def add_historical_data_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--input-json", default=None)
    parser.add_argument("--historical-dir", default="data/historical")
    parser.add_argument("--storage-timeframe", default="1m")
    parser.add_argument("--start-ts", type=int, default=None)
    parser.add_argument("--end-ts", type=int, default=None)
    parser.add_argument("--download-missing", action="store_true")
    parser.add_argument("--allow-remote-api", action="store_true")
    return parser


def build_time_range(*, limit: int, start_ts: int | None, end_ts: int | None) -> TimeRange:
    if start_ts is not None or end_ts is not None:
        return TimeRange(start_ts=start_ts, end_ts=end_ts)
    return TimeRange(tail_bars=limit)


def build_market_data_adapter(
    *,
    args: argparse.Namespace,
    symbol: str,
    timeframe: str,
):
    if getattr(args, "input_json", None):
        return HistoricalJsonMarketDataAdapter(
            data_path=args.input_json,
            instrument_id=symbol.upper(),
            timeframe=timeframe,
        )

    local_adapter = HistoricalParquetMarketDataAdapter(
        data_root=args.historical_dir,
        market_type=args.market_type,
        resample_source_timeframe=args.storage_timeframe,
    )
    remote_adapter = None
    if getattr(args, "allow_remote_api", False):
        remote_adapter = BinanceRestMarketDataAdapter(market_type=args.market_type)
    downloader = None
    if getattr(args, "download_missing", False):
        downloader = HistoricalBinanceDownloader(
            data_root=args.historical_dir,
            market_type=args.market_type,
        )
    return LocalFirstMarketDataAdapter(
        local_adapter=local_adapter,
        storage_timeframe=args.storage_timeframe,
        remote_adapter=remote_adapter,
        downloader=downloader,
    )


def build_strategy_pipeline(
    *,
    strategy: str,
    symbol: str,
    interval: str,
    secondary_interval: str = "1h",
    fast_window: int,
    slow_window: int,
    entry_threshold: float,
    ma_period: int,
    rsi_period: int,
    oversold: float,
    overbought: float,
    primary_ma_period: int = 20,
    reference_ma_period: int = 20,
    spread_threshold_bps: float = 0.0,
) -> SignalPipelineSpec:
    if strategy == "moving_average_cross":
        plugin_spec = {
            "plugin_id": "moving_average_cross",
            "config": {
                "instrument_id": symbol,
                "timeframe": interval,
                "fast_window": fast_window,
                "slow_window": slow_window,
                "entry_threshold": entry_threshold,
            },
        }
    elif strategy == "price_moving_average":
        plugin_spec = {
            "plugin_id": "price_moving_average",
            "config": {
                "instrument_id": symbol,
                "timeframe": interval,
                "period": ma_period,
                "entry_threshold": entry_threshold,
            },
        }
    elif strategy == "rsi_reversion":
        plugin_spec = {
            "plugin_id": "rsi_reversion",
            "config": {
                "instrument_id": symbol,
                "timeframe": interval,
                "period": rsi_period,
                "oversold": oversold,
                "overbought": overbought,
            },
        }
    elif strategy == "multi_timeframe_ma_spread":
        plugin_spec = {
            "plugin_id": "multi_timeframe_ma_spread",
            "config": {
                "instrument_id": symbol,
                "primary_timeframe": interval,
                "reference_timeframe": secondary_interval,
                "primary_ma_period": primary_ma_period,
                "reference_ma_period": reference_ma_period,
                "spread_threshold_bps": spread_threshold_bps,
            },
        }
    else:
        raise ValueError("unsupported strategy '%s'" % strategy)

    return SignalPipelineSpec(plugin_chain=[plugin_spec])
