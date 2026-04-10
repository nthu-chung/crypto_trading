from __future__ import annotations

import uuid

import pytest

from cyqnt_trd.standard_bot.core import (
    DataQuery,
    ExecutionIntent,
    MarketQuery,
    MonitorTrigger,
    OrderType,
    QueryOptions,
    SignalPipelineSpec,
    TimeRange,
    TradeSide,
    TriggerType,
)
from cyqnt_trd.standard_bot.data import AlignmentPolicy
from cyqnt_trd.standard_bot.data.adapters import HistoricalJsonMarketDataAdapter
from cyqnt_trd.standard_bot.data.historical import HistoricalParquetMarketDataAdapter
from cyqnt_trd.standard_bot.execution import (
    LongOnlySinglePositionRule,
    MaxPositionFractionRule,
    PaperBrokerAdapter,
)
from cyqnt_trd.standard_bot.runtime import MarketOnlyPaperRunner, RunContext
from cyqnt_trd.standard_bot.signal import (
    MovingAverageCrossConfig,
    MovingAverageCrossPlugin,
    MultiTimeframeMaSpreadConfig,
    MultiTimeframeMaSpreadPlugin,
    SignalPluginRegistry,
)


def _make_context() -> RunContext:
    return RunContext(
        run_id=str(uuid.uuid4()),
        trigger=MonitorTrigger(trigger_type=TriggerType.MANUAL),
        data_query=DataQuery(
            market=MarketQuery(
                instruments=["BTCUSDT"],
                timeframes=["1m"],
                time_range=TimeRange(tail_bars=30),
            ),
            options=QueryOptions(partial_ok=False),
        ),
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
        dry_run=False,
    )


def test_paper_broker_round_trip_buy_then_sell() -> None:
    broker = PaperBrokerAdapter(initial_cash=1000.0, fee_bps=0.0)
    buy_report = broker.place_order(
        intent=ExecutionIntent(
            intent_id="buy-1",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            quantity=None,
            notional=500.0,
            price=None,
            risk_hints={"market_price": 100.0},
            source_signal_id="signal-buy",
        )
    )
    assert buy_report.status.value == "filled"
    assert broker.sync_account().balances["USDT"] == 500.0

    sell_report = broker.place_order(
        intent=ExecutionIntent(
            intent_id="sell-1",
            instrument_id="BTCUSDT",
            side=TradeSide.SELL,
            order_type=OrderType.MARKET,
            quantity=5.0,
            notional=None,
            price=None,
            risk_hints={"market_price": 120.0},
            source_signal_id="signal-sell",
        )
    )
    assert sell_report.status.value == "filled"
    assert broker.sync_account().balances["USDT"] == 1100.0


def test_market_only_paper_runner_executes_one_step_cycle(tmp_path) -> None:
    data_path = tmp_path / "bars.json"
    rows = []
    close_values = [100.0] * 20 + [110.0] * 4 + [120.0]
    for index, close in enumerate(close_values):
        ts = (index + 1) * 60_000
        rows.append(
            {
                "open_time": ts - 60_000,
                "close_time": ts,
                "open_price": close,
                "high_price": close,
                "low_price": close,
                "close_price": close,
                "volume": 10.0,
            }
        )
    data_path.write_text(__import__("json").dumps({"symbol": "BTCUSDT", "interval": "1m", "data": rows}), encoding="utf-8")

    registry = SignalPluginRegistry()
    registry.register(MovingAverageCrossPlugin(), lambda raw: MovingAverageCrossConfig(**raw))
    runner = MarketOnlyPaperRunner(
        market_data=HistoricalJsonMarketDataAdapter(str(data_path), instrument_id="BTCUSDT", timeframe="1m"),
        signal_registry=registry,
        broker=PaperBrokerAdapter(initial_cash=1000.0, fee_bps=0.0),
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="1m"),
        snapshot_tail_bars=20,
    )

    summary = runner.run(_make_context())

    assert summary.status == "ok"
    assert summary.signal_count >= 1
    assert len(summary.execution_reports) == 1
    assert summary.execution_reports[0].status.value == "filled"


def test_market_only_paper_runner_supports_local_resampled_multi_timeframe_data(tmp_path) -> None:
    pyarrow = pytest.importorskip("pyarrow")
    pyarrow_parquet = pytest.importorskip("pyarrow.parquet")

    rows = []
    for index in range(180):
        open_time = index * 60_000
        close = 100.0 + float(index // 60) * 20.0 + float(index % 5)
        rows.append(
            {
                "open_time": open_time,
                "close_time": open_time + 59_999,
                "open": close,
                "high": close,
                "low": close,
                "close": close,
                "volume": 10.0,
                "quote_volume": 1000.0,
                "trades": 10,
                "instrument_id": "BTCUSDT",
                "timeframe": "1m",
                "confirmed": True,
            }
        )
    table = pyarrow.Table.from_pylist(rows)
    parquet_path = tmp_path / "futures" / "BTCUSDT"
    parquet_path.mkdir(parents=True, exist_ok=True)
    pyarrow_parquet.write_table(table, str(parquet_path / "1m.parquet"))

    registry = SignalPluginRegistry()
    registry.register(MultiTimeframeMaSpreadPlugin(), lambda raw: MultiTimeframeMaSpreadConfig(**raw))
    runner = MarketOnlyPaperRunner(
        market_data=HistoricalParquetMarketDataAdapter(
            data_root=str(tmp_path),
            market_type="futures",
            resample_source_timeframe="1m",
        ),
        signal_registry=registry,
        broker=PaperBrokerAdapter(initial_cash=1000.0, fee_bps=0.0, account_mode="futures"),
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe="5m"),
        snapshot_tail_bars=120,
    )
    context = RunContext(
        run_id=str(uuid.uuid4()),
        trigger=MonitorTrigger(trigger_type=TriggerType.MANUAL),
        data_query=DataQuery(
            market=MarketQuery(
                instruments=["BTCUSDT"],
                timeframes=["5m", "1h"],
                time_range=TimeRange(tail_bars=24),
            ),
            options=QueryOptions(partial_ok=False),
        ),
        signal_pipeline=SignalPipelineSpec(
            plugin_chain=[
                {
                    "plugin_id": "multi_timeframe_ma_spread",
                    "config": {
                        "instrument_id": "BTCUSDT",
                        "primary_timeframe": "5m",
                        "reference_timeframe": "1h",
                        "primary_ma_period": 3,
                        "reference_ma_period": 2,
                        "spread_threshold_bps": 0.0,
                    },
                }
            ]
        ),
        dry_run=True,
    )

    summary = runner.run(context)

    assert summary.status == "dry_run"
    assert summary.signal_count >= 0


def test_max_position_fraction_rule_rejects_oversized_buy() -> None:
    broker = PaperBrokerAdapter(initial_cash=1000.0, fee_bps=0.0)
    account_snapshot = broker.sync_account()
    rule = MaxPositionFractionRule(max_fraction=0.5)

    reject_reason = rule.validate(
        ExecutionIntent(
            intent_id="buy-oversized",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            notional=750.0,
            risk_hints={"market_price": 100.0},
        ),
        account_snapshot,
    )

    assert reject_reason == "max_position_fraction_exceeded"


def test_long_only_single_position_rule_rejects_duplicate_buy() -> None:
    broker = PaperBrokerAdapter(initial_cash=1000.0, fee_bps=0.0)
    broker.place_order(
        ExecutionIntent(
            intent_id="buy-existing",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            notional=500.0,
            risk_hints={"market_price": 100.0},
        )
    )
    rule = LongOnlySinglePositionRule()

    reject_reason = rule.validate(
        ExecutionIntent(
            intent_id="buy-duplicate",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            notional=100.0,
            risk_hints={"market_price": 100.0},
        ),
        broker.sync_account(),
    )

    assert reject_reason == "position_exists"
