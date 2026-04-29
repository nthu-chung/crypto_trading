from __future__ import annotations

from cyqnt_trd.standard_bot.core import Bar, BundleMeta, MarketBundle
from cyqnt_trd.standard_bot.data import AlignmentPolicy, HistoricalSnapshotAssembler
from cyqnt_trd.standard_bot.signal import (
    LiquidationReversalConfig,
    LiquidationReversalPlugin,
    OiFundingBreakoutConfig,
    OiFundingBreakoutPlugin,
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


def test_oi_funding_breakout_plugin_emits_buy_on_confirmed_breakout() -> None:
    bars = []
    closes = [100.0, 101.0, 102.0, 103.0, 110.0]
    highs = [101.0, 102.0, 103.0, 104.0, 111.0]
    lows = [99.0, 100.0, 101.0, 102.0, 109.0]
    oi_changes = [0.0, 0.0, 50.0, 80.0, 120.0]
    funding_bps = [1.0, 1.0, 1.0, 1.0, 1.0]
    for index, close in enumerate(closes):
        ts = (index + 1) * 300_000
        bars.append(
            Bar(
                open=close,
                high=highs[index],
                low=lows[index],
                close=close,
                volume=10.0,
                timestamp=ts,
                instrument_id="BTCUSDT",
                timeframe="5m",
                confirmed=True,
                extras={
                    "open_time": ts - 300_000,
                    "close_time": ts,
                    "oi_change_bps": oi_changes[index],
                    "funding_rate_bps": funding_bps[index],
                },
            )
        )
    bundle = MarketBundle(
        bars={MarketBundle.key("BTCUSDT", "5m"): bars},
        meta=BundleMeta(data_source="fixture", fetched_at=bars[-1].timestamp),
    )
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="5m"),
        tail_bars=len(closes),
    ).build(bundle)
    snapshot = snapshots[-1]

    plugin = OiFundingBreakoutPlugin()
    batch = plugin.run(
        snapshot=snapshot,
        config=OiFundingBreakoutConfig(
            instrument_id="BTCUSDT",
            timeframe="5m",
            lookback_window=3,
            oi_threshold_bps=50.0,
            max_funding_rate_bps=5.0,
        ),
    )

    assert batch.signals
    assert batch.signals[-1].side.value == "buy"


def test_liquidation_reversal_plugin_emits_buy_after_long_liquidation_spike() -> None:
    bars = []
    long_liqs = [0.0, 0.0, 250_000.0, 0.0]
    short_liqs = [0.0, 0.0, 0.0, 0.0]
    for index in range(4):
        ts = (index + 1) * 300_000
        bars.append(
            Bar(
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.0,
                volume=10.0,
                timestamp=ts,
                instrument_id="BTCUSDT",
                timeframe="5m",
                confirmed=True,
                extras={
                    "open_time": ts - 300_000,
                    "close_time": ts,
                    "long_liq_notional_usd": long_liqs[index],
                    "short_liq_notional_usd": short_liqs[index],
                },
            )
        )
    bundle = MarketBundle(
        bars={MarketBundle.key("BTCUSDT", "5m"): bars},
        meta=BundleMeta(data_source="fixture", fetched_at=bars[-1].timestamp),
    )
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="5m"),
        tail_bars=4,
    ).build(bundle)

    plugin = LiquidationReversalPlugin()
    batch = plugin.run(
        snapshot=snapshots[-1],
        config=LiquidationReversalConfig(
            instrument_id="BTCUSDT",
            timeframe="5m",
            long_liquidation_threshold_usd=100_000.0,
            short_liquidation_threshold_usd=100_000.0,
            liquidation_imbalance_ratio=0.6,
        ),
    )

    assert batch.signals
    assert batch.signals[-1].side.value == "buy"
