from __future__ import annotations

from cyqnt_trd.standard_bot.core import Bar, BundleMeta, MarketBundle
from cyqnt_trd.standard_bot.data import AlignmentPolicy, HistoricalSnapshotAssembler
from cyqnt_trd.standard_bot.signal import (
    PriceMovingAverageConfig,
    PriceMovingAveragePlugin,
    RsiReversionConfig,
    RsiReversionPlugin,
)


def _snapshot_from_closes(close_values: list[float]):
    bars = []
    for index, close in enumerate(close_values):
        ts = (index + 1) * 60_000
        bars.append(
            Bar(
                open=close,
                high=close,
                low=close,
                close=close,
                volume=10.0,
                timestamp=ts,
                instrument_id="BTCUSDT",
                timeframe="1m",
                confirmed=True,
                extras={"open_time": ts - 60_000, "close_time": ts},
            )
        )
    bundle = MarketBundle(
        bars={MarketBundle.key("BTCUSDT", "1m"): bars},
        meta=BundleMeta(data_source="fixture", fetched_at=bars[-1].timestamp),
    )
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        tail_bars=len(close_values),
    ).build(bundle)
    return snapshots[-1]


def test_price_moving_average_plugin_emits_buy_on_upward_cross() -> None:
    snapshot = _snapshot_from_closes([10.0, 9.0, 8.0, 7.0, 8.0, 11.0])
    plugin = PriceMovingAveragePlugin()
    batch = plugin.run(
        snapshot=snapshot,
        config=PriceMovingAverageConfig(
            instrument_id="BTCUSDT",
            timeframe="1m",
            period=3,
        ),
    )

    assert batch.signals
    assert batch.signals[-1].side.value == "buy"


def test_rsi_reversion_plugin_emits_buy_when_oversold() -> None:
    snapshot = _snapshot_from_closes([100.0, 95.0, 90.0, 85.0, 80.0, 75.0, 70.0, 68.0])
    plugin = RsiReversionPlugin()
    batch = plugin.run(
        snapshot=snapshot,
        config=RsiReversionConfig(
            instrument_id="BTCUSDT",
            timeframe="1m",
            period=5,
            oversold=35.0,
            overbought=70.0,
        ),
    )

    assert batch.signals
    assert batch.signals[-1].side.value == "buy"
