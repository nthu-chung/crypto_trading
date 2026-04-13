from __future__ import annotations

import uuid

import numpy as np
import pytest

from cyqnt_trd.standard_bot.core import (
    BacktestRequest,
    Bar,
    BundleMeta,
    MarketBundle,
    SignalPipelineSpec,
)
from cyqnt_trd.standard_bot.data import AlignmentPolicy, HistoricalSnapshotAssembler
from cyqnt_trd.standard_bot.signal import (
    DonchianBreakoutConfig,
    DonchianBreakoutPlugin,
    MovingAverageCrossConfig,
    MovingAverageCrossPlugin,
    RsiReversionConfig,
    RsiReversionPlugin,
    SignalPluginRegistry,
)
from cyqnt_trd.standard_bot.signal.numba_kernels import (
    TARGET_KEEP,
    donchian_breakout_target_updates,
    moving_average_cross_target_updates,
    rsi_reversion_target_updates,
)
from cyqnt_trd.standard_bot.simulation import NumbaBacktestRunner


def _market_bundle(
    opens: list[float],
    closes: list[float],
    *,
    highs: list[float] | None = None,
    lows: list[float] | None = None,
    volumes: list[float] | None = None,
    quote_volumes: list[float] | None = None,
) -> MarketBundle:
    bars = []
    volumes = volumes or [100.0] * len(opens)
    quote_volumes = quote_volumes or [opens[index] * volumes[index] for index in range(len(opens))]
    highs = highs or [max(opens[index], closes[index]) for index in range(len(opens))]
    lows = lows or [min(opens[index], closes[index]) for index in range(len(opens))]

    for index, (open_price, close_price) in enumerate(zip(opens, closes)):
        ts = (index + 1) * 60_000
        bars.append(
            Bar(
                open=open_price,
                high=highs[index],
                low=lows[index],
                close=close_price,
                volume=volumes[index],
                quote_volume=quote_volumes[index],
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


def _request(
    *,
    strategy: str,
    config: dict,
    initial_capital: float = 1000.0,
    fee_model: dict | None = None,
    slippage_model: dict | None = None,
) -> BacktestRequest:
    return BacktestRequest(
        request_id=str(uuid.uuid4()),
        instruments=["BTCUSDT"],
        primary_timeframe="1m",
        start_ts=60_000,
        end_ts=600_000,
        signal_pipeline=SignalPipelineSpec(plugin_chain=[{"plugin_id": strategy, "config": config}]),
        initial_capital=initial_capital,
        fee_model=fee_model or {"taker_fee_bps": 0.0},
        slippage_model=slippage_model or {"slippage_bps": 0.0, "max_bar_volume_fraction": 1.0},
    )


def test_numba_backtest_uses_next_bar_open_for_price_ma_fills() -> None:
    bundle = _market_bundle(
        opens=[100.0, 100.0, 100.0, 100.0, 200.0],
        closes=[100.0, 100.0, 100.0, 120.0, 130.0],
    )
    request = _request(
        strategy="price_moving_average",
        config={"instrument_id": "BTCUSDT", "timeframe": "1m", "period": 2, "entry_threshold": 0.0},
    )

    result = NumbaBacktestRunner().run(request=request, market_bundle=bundle)

    trades = result.extras["trades"]
    assert len(trades) == 1
    assert trades[0]["decision_timestamp"] == 240_000
    assert trades[0]["price"] == 200.0
    assert result.metrics["trade_count"] == 1.0


def test_numba_backtest_respects_liquidity_caps() -> None:
    bundle = _market_bundle(
        opens=[100.0, 100.0, 100.0, 100.0, 100.0],
        closes=[100.0, 100.0, 100.0, 120.0, 130.0],
        volumes=[100.0, 100.0, 100.0, 100.0, 1.0],
    )
    request = _request(
        strategy="price_moving_average",
        config={"instrument_id": "BTCUSDT", "timeframe": "1m", "period": 2, "entry_threshold": 0.0},
        slippage_model={"slippage_bps": 0.0, "max_bar_volume_fraction": 0.10},
    )

    result = NumbaBacktestRunner().run(request=request, market_bundle=bundle)

    trades = result.extras["trades"]
    assert len(trades) == 1
    assert trades[0]["quantity"] == pytest.approx(0.1)
    assert result.metrics["ending_position_qty"] == pytest.approx(0.1)


def test_numba_backtest_applies_taker_and_funding_fees() -> None:
    bundle = _market_bundle(
        opens=[100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
        closes=[100.0, 100.0, 100.0, 120.0, 120.0, 120.0],
    )
    request_no_cost = _request(
        strategy="price_moving_average",
        config={"instrument_id": "BTCUSDT", "timeframe": "1m", "period": 2, "entry_threshold": 0.0},
        fee_model={"taker_fee_bps": 0.0, "funding_bps_per_bar": 0.0},
        slippage_model={"slippage_bps": 0.0, "max_bar_volume_fraction": 1.0},
    )
    request_with_cost = _request(
        strategy="price_moving_average",
        config={"instrument_id": "BTCUSDT", "timeframe": "1m", "period": 2, "entry_threshold": 0.0},
        fee_model={"taker_fee_bps": 10.0, "funding_bps_per_bar": 25.0},
        slippage_model={"slippage_bps": 0.0, "max_bar_volume_fraction": 1.0},
    )

    result_no_cost = NumbaBacktestRunner().run(request=request_no_cost, market_bundle=bundle)
    result_with_cost = NumbaBacktestRunner().run(request=request_with_cost, market_bundle=bundle)

    assert result_with_cost.metrics["final_equity"] < result_no_cost.metrics["final_equity"]
    assert result_with_cost.extras["fee_model"]["total_funding_fees"] > 0.0
    assert result_with_cost.extras["trades"][0]["fee"] > 0.0


def test_numba_moving_average_cross_matches_incremental_plugin_decisions() -> None:
    closes = [100.0, 100.0, 110.0, 115.0, 90.0, 85.0]
    bundle = _market_bundle(opens=closes, closes=closes)
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        tail_bars=10,
    ).build(bundle)

    registry = SignalPluginRegistry()
    registry.register(MovingAverageCrossPlugin(), lambda raw: MovingAverageCrossConfig(**raw))
    step_states = {}
    step_decisions = []

    for snapshot in snapshots:
        result = registry.run_pipeline_step(
            snapshot,
            [
                {
                    "plugin_id": "moving_average_cross",
                    "config": {
                        "instrument_id": "BTCUSDT",
                        "timeframe": "1m",
                        "fast_window": 2,
                        "slow_window": 3,
                        "entry_threshold": 0.0,
                    },
                }
            ],
            previous_states=step_states,
        )
        step_states = result.states
        trade_signals = result.batch.trade_signals()
        if trade_signals:
            step_decisions.append((snapshot.meta.decision_as_of, trade_signals[-1].side.value))

    updates, _ = moving_average_cross_target_updates(
        np.asarray(closes, dtype=np.float64),
        2,
        3,
        0.0,
    )
    numba_decisions = []
    timestamps = [60_000, 120_000, 180_000, 240_000, 300_000, 360_000]
    for index, update in enumerate(updates):
        if update == TARGET_KEEP:
            continue
        numba_decisions.append((timestamps[index], "buy" if int(update) == 1 else "sell"))

    assert step_decisions == numba_decisions


def test_numba_runner_supports_moving_average_cross_backtests() -> None:
    bundle = _market_bundle(
        opens=[100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
        closes=[100.0, 100.0, 110.0, 115.0, 90.0, 85.0],
    )
    request = _request(
        strategy="moving_average_cross",
        config={
            "instrument_id": "BTCUSDT",
            "timeframe": "1m",
            "fast_window": 2,
            "slow_window": 3,
            "entry_threshold": 0.0,
        },
        slippage_model={"slippage_bps": 0.0, "max_bar_volume_fraction": 1.0},
    )

    result = NumbaBacktestRunner().run(request=request, market_bundle=bundle)

    assert result.metrics["signal_count"] >= 1.0
    assert "signal_at_bar_close_fill_next_bar_open" == result.extras["execution_assumption"]


def test_numba_rsi_reversion_matches_incremental_plugin_decisions() -> None:
    closes = [100.0, 99.0, 98.0, 97.0, 96.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0]
    bundle = _market_bundle(opens=closes, closes=closes)
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        tail_bars=20,
    ).build(bundle)

    registry = SignalPluginRegistry()
    registry.register(RsiReversionPlugin(), lambda raw: RsiReversionConfig(**raw))
    step_states = {}
    step_decisions = []

    for snapshot in snapshots:
        result = registry.run_pipeline_step(
            snapshot,
            [
                {
                    "plugin_id": "rsi_reversion",
                    "config": {
                        "instrument_id": "BTCUSDT",
                        "timeframe": "1m",
                        "period": 3,
                        "oversold": 30.0,
                        "overbought": 70.0,
                    },
                }
            ],
            previous_states=step_states,
        )
        step_states = result.states
        trade_signals = result.batch.trade_signals()
        if trade_signals:
            step_decisions.append((snapshot.meta.decision_as_of, trade_signals[-1].side.value))

    updates, _ = rsi_reversion_target_updates(
        np.asarray(closes, dtype=np.float64),
        3,
        30.0,
        70.0,
    )
    numba_decisions = []
    timestamps = [60_000 * (index + 1) for index in range(len(closes))]
    for index, update in enumerate(updates):
        if update == TARGET_KEEP:
            continue
        numba_decisions.append((timestamps[index], "buy" if int(update) == 1 else "sell"))

    assert step_decisions == numba_decisions


def test_numba_runner_supports_rsi_reversion_backtests() -> None:
    closes = [100.0, 99.0, 98.0, 97.0, 96.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0]
    bundle = _market_bundle(opens=closes, closes=closes)
    request = _request(
        strategy="rsi_reversion",
        config={
            "instrument_id": "BTCUSDT",
            "timeframe": "1m",
            "period": 3,
            "oversold": 30.0,
            "overbought": 70.0,
        },
        slippage_model={"slippage_bps": 0.0, "max_bar_volume_fraction": 1.0},
    )

    result = NumbaBacktestRunner().run(request=request, market_bundle=bundle)

    assert result.metrics["signal_count"] >= 1.0
    assert result.extras["execution_assumption"] == "signal_at_bar_close_fill_next_bar_open"


def test_numba_runner_reports_sharpe_and_bar_return_metrics() -> None:
    bundle = _market_bundle(
        opens=[100.0, 100.0, 100.0, 100.0, 102.0, 104.0, 106.0],
        closes=[100.0, 100.0, 110.0, 115.0, 118.0, 120.0, 122.0],
    )
    request = _request(
        strategy="moving_average_cross",
        config={
            "instrument_id": "BTCUSDT",
            "timeframe": "1m",
            "fast_window": 2,
            "slow_window": 3,
            "entry_threshold": 0.0,
        },
        slippage_model={"slippage_bps": 0.0, "max_bar_volume_fraction": 1.0},
    )

    result = NumbaBacktestRunner().run(request=request, market_bundle=bundle)

    assert "sharpe_ratio" in result.metrics
    assert "mean_bar_return" in result.metrics
    assert "bar_return_volatility" in result.metrics
    assert result.metrics["sharpe_ratio"] > 0.0


def test_numba_donchian_breakout_matches_incremental_plugin_decisions() -> None:
    closes = [100.0, 101.0, 102.0, 103.0, 104.0, 95.0, 90.0, 91.0, 92.0]
    bundle = _market_bundle(opens=closes, closes=closes)
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        tail_bars=20,
    ).build(bundle)

    registry = SignalPluginRegistry()
    registry.register(DonchianBreakoutPlugin(), lambda raw: DonchianBreakoutConfig(**raw))
    step_states = {}
    step_decisions = []

    for snapshot in snapshots:
        result = registry.run_pipeline_step(
            snapshot,
            [
                {
                    "plugin_id": "donchian_breakout",
                    "config": {
                        "instrument_id": "BTCUSDT",
                        "timeframe": "1m",
                        "lookback_window": 3,
                        "breakout_buffer_bps": 0.0,
                    },
                }
            ],
            previous_states=step_states,
        )
        step_states = result.states
        trade_signals = result.batch.trade_signals()
        if trade_signals:
            step_decisions.append((snapshot.meta.decision_as_of, trade_signals[-1].side.value))

    updates, _ = donchian_breakout_target_updates(
        np.asarray(closes, dtype=np.float64),
        np.asarray(closes, dtype=np.float64),
        np.asarray(closes, dtype=np.float64),
        3,
        0.0,
    )
    numba_decisions = []
    timestamps = [60_000 * (index + 1) for index in range(len(closes))]
    for index, update in enumerate(updates):
        if update == TARGET_KEEP:
            continue
        numba_decisions.append((timestamps[index], "buy" if int(update) == 1 else "sell"))

    assert step_decisions == numba_decisions


def test_numba_runner_supports_donchian_breakout_backtests() -> None:
    closes = [100.0, 101.0, 102.0, 103.0, 104.0, 95.0, 90.0, 91.0, 92.0]
    bundle = _market_bundle(opens=closes, closes=closes)
    request = _request(
        strategy="donchian_breakout",
        config={
            "instrument_id": "BTCUSDT",
            "timeframe": "1m",
            "lookback_window": 3,
            "breakout_buffer_bps": 0.0,
        },
        slippage_model={"slippage_bps": 0.0, "max_bar_volume_fraction": 1.0},
    )

    result = NumbaBacktestRunner().run(request=request, market_bundle=bundle)

    assert result.metrics["signal_count"] >= 2.0
    assert result.extras["execution_assumption"] == "signal_at_bar_close_fill_next_bar_open"
    trades = result.extras["trades"]
    assert trades[0]["action"] == "open_long"
    assert trades[-1]["action"] == "flip_to_short"
