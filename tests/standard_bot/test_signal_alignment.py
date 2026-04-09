from __future__ import annotations

from dataclasses import dataclass

from cyqnt_trd.standard_bot.core import Bar, BundleMeta, MarketBundle
from cyqnt_trd.standard_bot.data import AlignmentPolicy, HistoricalSnapshotAssembler
from cyqnt_trd.standard_bot.signal import (
    MovingAverageCrossConfig,
    MovingAverageCrossPlugin,
    PriceMovingAverageConfig,
    PriceMovingAveragePlugin,
    RsiReversionConfig,
    RsiReversionPlugin,
)


def _snapshots(close_values: list[float]):
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
    return HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        tail_bars=len(close_values),
    ).build(bundle)


def _signal_signature(signal):
    if signal is None:
        return None
    return {
        "side": signal.side.value,
        "bar_timestamp": signal.payload["bar_timestamp"],
        "strength": round(float(signal.strength), 12),
    }


def _batch_step_alignment(plugin, config, close_values: list[float]) -> None:
    snapshots = _snapshots(close_values)
    state = plugin.initialize_state()
    previous_batch_count = 0

    for snapshot in snapshots:
        batch = plugin.run(snapshot, config)
        batch_emitted = None
        if len(batch.signals) > previous_batch_count:
            batch_emitted = batch.signals[-1]
        previous_batch_count = len(batch.signals)

        step_result = plugin.step(snapshot, state, config)
        state = step_result.state
        step_emitted = step_result.signals[-1] if step_result.signals else None

        assert _signal_signature(step_emitted) == _signal_signature(batch_emitted)


def test_moving_average_cross_batch_matches_step() -> None:
    _batch_step_alignment(
        MovingAverageCrossPlugin(),
        MovingAverageCrossConfig(
            instrument_id="BTCUSDT",
            timeframe="1m",
            fast_window=3,
            slow_window=5,
            entry_threshold=0.0,
        ),
        [100.0, 101.0, 102.0, 103.0, 110.0, 111.0, 109.0, 108.0, 100.0, 95.0],
    )


def test_price_moving_average_batch_matches_step() -> None:
    _batch_step_alignment(
        PriceMovingAveragePlugin(),
        PriceMovingAverageConfig(
            instrument_id="BTCUSDT",
            timeframe="1m",
            period=3,
            entry_threshold=0.0,
        ),
        [10.0, 9.0, 8.0, 7.0, 8.0, 11.0, 12.0, 10.0, 8.0, 7.0],
    )


def test_rsi_reversion_batch_matches_step() -> None:
    _batch_step_alignment(
        RsiReversionPlugin(),
        RsiReversionConfig(
            instrument_id="BTCUSDT",
            timeframe="1m",
            period=5,
            oversold=35.0,
            overbought=70.0,
        ),
        [100.0, 96.0, 93.0, 88.0, 85.0, 81.0, 78.0, 84.0, 90.0, 96.0, 102.0],
    )
