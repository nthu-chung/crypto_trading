from __future__ import annotations

import uuid

from cyqnt_trd.standard_bot.core import (
    BacktestRequest,
    Bar,
    BundleMeta,
    MarketBundle,
    SignalPipelineSpec,
)
from cyqnt_trd.standard_bot.data import AlignmentPolicy, HistoricalSnapshotAssembler
from cyqnt_trd.standard_bot.signal import (
    MovingAverageCrossConfig,
    MovingAverageCrossPlugin,
    SignalPluginRegistry,
)
from cyqnt_trd.standard_bot.simulation import SnapshotBacktestRunner


def _market_bundle(close_values: list[float]) -> MarketBundle:
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
    return MarketBundle(
        bars={MarketBundle.key("BTCUSDT", "1m"): bars},
        meta=BundleMeta(data_source="fixture", fetched_at=bars[-1].timestamp),
    )


def test_historical_snapshot_assembler_builds_primary_timeframe_snapshots() -> None:
    bundle = _market_bundle([100.0, 101.0, 102.0, 103.0])
    assembler = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        tail_bars=3,
    )

    snapshots = assembler.build(bundle)

    assert len(snapshots) == 4
    assert snapshots[-1].meta.decision_as_of == 240_000
    latest_series = snapshots[-1].require_market().bars[MarketBundle.key("BTCUSDT", "1m")]
    assert len(latest_series) == 3
    assert latest_series[0].close == 101.0


def test_snapshot_backtest_runner_executes_market_only_mvp_flow() -> None:
    bundle = _market_bundle([100.0] * 20 + [110.0] * 5 + [90.0] * 5)
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        tail_bars=20,
    ).build(bundle)

    registry = SignalPluginRegistry()
    registry.register(MovingAverageCrossPlugin(), lambda raw: MovingAverageCrossConfig(**raw))

    request = BacktestRequest(
        request_id=str(uuid.uuid4()),
        instruments=["BTCUSDT"],
        primary_timeframe="1m",
        start_ts=snapshots[0].meta.decision_as_of or snapshots[0].meta.assembled_at,
        end_ts=snapshots[-1].meta.decision_as_of or snapshots[-1].meta.assembled_at,
        signal_pipeline=SignalPipelineSpec(
            plugin_chain=[
                {
                    "plugin_id": "moving_average_cross",
                    "config": {
                        "instrument_id": "BTCUSDT",
                        "timeframe": "1m",
                        "fast_window": 3,
                        "slow_window": 5,
                        "entry_threshold": 0.0,
                    },
                }
            ]
        ),
        initial_capital=1000.0,
        fee_model={"commission_bps": 0.0},
        slippage_model={"slippage_bps": 0.0},
    )

    result = SnapshotBacktestRunner(signal_registry=registry).run(
        request=request,
        snapshots=snapshots,
    )

    assert result.metrics["snapshot_count"] == float(len(snapshots))
    assert result.metrics["trade_count"] >= 1.0
    assert result.equity_curve
    assert "trades" in result.extras
