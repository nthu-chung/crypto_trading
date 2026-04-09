"""
Shared helpers for standard bot CLI entrypoints.
"""

from __future__ import annotations

from ..core import SignalPipelineSpec
from ..signal import SignalPluginRegistry, register_builtin_plugins


def make_registry() -> SignalPluginRegistry:
    registry = SignalPluginRegistry()
    register_builtin_plugins(registry)
    return registry


def build_strategy_pipeline(
    *,
    strategy: str,
    symbol: str,
    interval: str,
    fast_window: int,
    slow_window: int,
    entry_threshold: float,
    ma_period: int,
    rsi_period: int,
    oversold: float,
    overbought: float,
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
    else:
        raise ValueError("unsupported strategy '%s'" % strategy)

    return SignalPipelineSpec(plugin_chain=[plugin_spec])
