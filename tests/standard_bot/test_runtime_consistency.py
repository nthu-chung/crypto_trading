from __future__ import annotations

import uuid

from cyqnt_trd.standard_bot.core import (
    Bar,
    BundleMeta,
    DataQuery,
    ExecutionIntent,
    MarketBundle,
    MarketQuery,
    MonitorTrigger,
    OrderType,
    QueryOptions,
    SignalContext,
    TimeRange,
    TradeSide,
    TriggerType,
)
from cyqnt_trd.standard_bot.data import AlignmentPolicy, HistoricalSnapshotAssembler
from cyqnt_trd.standard_bot.entrypoints.common import build_strategy_pipeline, make_registry
from cyqnt_trd.standard_bot.execution import MaxPositionFractionRule, PaperBrokerAdapter
from cyqnt_trd.standard_bot.runtime import MarketOnlyPaperRunner, RunContext


def _mtf_market_bundle() -> MarketBundle:
    bars_5m = []
    bars_1h = []
    close_values_5m = [100.0] * 12 + [120.0] * 12 + [150.0] * 12 + [80.0] * 12
    hour_closes = [100.0, 120.0, 150.0, 80.0]

    for index, close in enumerate(close_values_5m):
        close_ts = (index + 1) * 5 * 60_000
        open_ts = close_ts - 5 * 60_000
        bars_5m.append(
            Bar(
                open=close,
                high=close,
                low=close,
                close=close,
                volume=100.0,
                timestamp=close_ts,
                instrument_id="BTCUSDT",
                timeframe="5m",
                confirmed=True,
                extras={"open_time": open_ts, "close_time": close_ts},
            )
        )

    for index, close in enumerate(hour_closes):
        close_ts = (index + 1) * 60 * 60_000
        open_ts = close_ts - 60 * 60_000
        bars_1h.append(
            Bar(
                open=close,
                high=close,
                low=close,
                close=close,
                volume=1_200.0,
                timestamp=close_ts,
                instrument_id="BTCUSDT",
                timeframe="1h",
                confirmed=True,
                extras={"open_time": open_ts, "close_time": close_ts},
            )
        )

    return MarketBundle(
        bars={
            MarketBundle.key("BTCUSDT", "5m"): bars_5m,
            MarketBundle.key("BTCUSDT", "1h"): bars_1h,
        },
        meta=BundleMeta(data_source="fixture", fetched_at=bars_5m[-1].timestamp),
    )


def _mtf_latest_flip_bundle() -> MarketBundle:
    bars_5m = []
    bars_1h = []
    close_values_5m = [110.0] * 48
    hour_closes = [100.0, 100.0, 100.0, 140.0]

    for index, close in enumerate(close_values_5m):
        close_ts = (index + 1) * 5 * 60_000
        open_ts = close_ts - 5 * 60_000
        bars_5m.append(
            Bar(
                open=close,
                high=close,
                low=close,
                close=close,
                volume=100.0,
                timestamp=close_ts,
                instrument_id="BTCUSDT",
                timeframe="5m",
                confirmed=True,
                extras={"open_time": open_ts, "close_time": close_ts},
            )
        )

    for index, close in enumerate(hour_closes):
        close_ts = (index + 1) * 60 * 60_000
        open_ts = close_ts - 60 * 60_000
        bars_1h.append(
            Bar(
                open=close,
                high=close,
                low=close,
                close=close,
                volume=1_200.0,
                timestamp=close_ts,
                instrument_id="BTCUSDT",
                timeframe="1h",
                confirmed=True,
                extras={"open_time": open_ts, "close_time": close_ts},
            )
        )

    return MarketBundle(
        bars={
            MarketBundle.key("BTCUSDT", "5m"): bars_5m,
            MarketBundle.key("BTCUSDT", "1h"): bars_1h,
        },
        meta=BundleMeta(data_source="fixture_latest_flip", fetched_at=bars_5m[-1].timestamp),
    )


class _StaticMarketAdapter:
    def __init__(self, bundle: MarketBundle) -> None:
        self.bundle = bundle

    def fetch_market(self, market_query: MarketQuery) -> MarketBundle:  # noqa: ARG002
        return self.bundle


def test_futures_paper_broker_supports_short_flip() -> None:
    broker = PaperBrokerAdapter(initial_cash=1_000.0, fee_bps=0.0, account_mode="futures")

    sell_report = broker.place_order(
        ExecutionIntent(
            intent_id="sell-open-short",
            instrument_id="BTCUSDT",
            side=TradeSide.SELL,
            order_type=OrderType.MARKET,
            quantity=5.0,
            risk_hints={"market_price": 100.0},
        )
    )
    assert sell_report.status.value == "filled"
    assert broker.sync_account().positions[0].side == "short"

    buy_report = broker.place_order(
        ExecutionIntent(
            intent_id="buy-flip-long",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            quantity=10.0,
            risk_hints={"market_price": 90.0},
        )
    )
    assert buy_report.status.value == "filled"
    account = broker.sync_account()
    assert account.positions[0].side == "long"
    assert account.positions[0].quantity == 5.0
    assert account.balances["USDT"] == 1050.0


def test_multi_timeframe_runtime_matches_batch_signal_and_opens_short() -> None:
    bundle = _mtf_latest_flip_bundle()
    registry = make_registry()
    pipeline = build_strategy_pipeline(
        strategy="multi_timeframe_ma_spread",
        symbol="BTCUSDT",
        interval="5m",
        secondary_interval="1h",
        fast_window=5,
        slow_window=20,
        entry_threshold=0.0,
        ma_period=5,
        rsi_period=14,
        oversold=30.0,
        overbought=70.0,
        primary_ma_period=3,
        reference_ma_period=2,
        spread_threshold_bps=0.0,
    )
    policy = AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="5m")
    snapshots = HistoricalSnapshotAssembler(policy=policy, tail_bars=60).build(bundle)
    previous_snapshot = snapshots[-2]
    latest_snapshot = snapshots[-1]
    broker = PaperBrokerAdapter(initial_cash=10_000.0, fee_bps=0.0, account_mode="futures")
    account_snapshot = broker.sync_account()
    signal_context = SignalContext(
        account_snapshot=account_snapshot,
        previous_positions={item.instrument_id: item.quantity for item in account_snapshot.positions},
    )
    previous_batch = registry.run_pipeline_batch(previous_snapshot, pipeline.plugin_chain, context=signal_context)
    latest_batch = registry.run_pipeline_batch(latest_snapshot, pipeline.plugin_chain, context=signal_context)
    batch_delta = [
        signal
        for signal in latest_batch.trade_signals()
        if int(signal.payload["bar_timestamp"]) > int(previous_snapshot.meta.decision_as_of)
    ]
    assert previous_batch.trade_signals()
    batch_signal = batch_delta[-1]

    runner = MarketOnlyPaperRunner(
        market_data=_StaticMarketAdapter(bundle),
        signal_registry=registry,
        broker=broker,
        policy=policy,
        risk_rules=[MaxPositionFractionRule(max_fraction=0.95)],
        snapshot_tail_bars=60,
    )
    summary = runner.run(
        RunContext(
            run_id=str(uuid.uuid4()),
            trigger=MonitorTrigger(trigger_type=TriggerType.MANUAL),
            data_query=DataQuery(
                market=MarketQuery(
                    instruments=["BTCUSDT"],
                    timeframes=["5m", "1h"],
                    time_range=TimeRange(tail_bars=60),
                ),
                options=QueryOptions(partial_ok=False),
            ),
            signal_pipeline=pipeline,
            signal_context=signal_context,
            dry_run=False,
        )
    )

    assert summary.status == "ok"
    assert summary.signal_count >= 1
    assert summary.signals
    runtime_signal = summary.signals[-1]
    assert runtime_signal.side == batch_signal.side
    assert runtime_signal.payload["bar_timestamp"] == batch_signal.payload["bar_timestamp"]
    assert runtime_signal.payload["target_position"] == -1
    assert len(summary.execution_reports) == 1
    assert summary.execution_reports[0].status.value == "filled"
    account = broker.sync_account()
    assert account.positions[0].side == "short"
