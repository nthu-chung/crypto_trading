"""
Probe batch-vs-runtime signal consistency on the latest live snapshot.
"""

from __future__ import annotations

import argparse
import json
import uuid

from ..config import load_env_file
from ..core import (
    DataQuery,
    MarketQuery,
    MonitorTrigger,
    QueryOptions,
    SignalContext,
    TimeRange,
    TriggerType,
)
from ..data import AlignmentPolicy, HistoricalSnapshotAssembler
from ..data.adapters import BinanceRestMarketDataAdapter
from ..execution import (
    BinanceFuturesMainnetBrokerAdapter,
    BinanceFuturesTestnetBrokerAdapter,
    InstrumentWhitelistRule,
    MaxAbsoluteNotionalRule,
    MaxPositionFractionRule,
    PaperBrokerAdapter,
)
from ..runtime import MarketOnlyPaperRunner, RunContext
from .common import build_strategy_pipeline, make_registry

TESTNET_FUTURES_KLINES_URL = "https://testnet.binancefuture.com/fapi/v1/klines"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check latest batch-vs-runtime signal consistency")
    parser.add_argument(
        "--broker",
        choices=["paper", "binance_futures_testnet", "binance_futures_mainnet"],
        default="paper",
    )
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="5m")
    parser.add_argument("--secondary-interval", default="1h")
    parser.add_argument("--limit", type=int, default=240)
    parser.add_argument("--market-type", choices=["spot", "futures"], default="futures")
    parser.add_argument(
        "--strategy",
        choices=[
            "moving_average_cross",
            "price_moving_average",
            "rsi_reversion",
            "donchian_breakout",
            "adx_trend_strength",
            "atr_breakout",
            "bollinger_mean_reversion",
            "macd_trend_follow",
            "multi_timeframe_ma_spread",
        ],
        default="multi_timeframe_ma_spread",
    )
    parser.add_argument("--fast-window", type=int, default=5)
    parser.add_argument("--slow-window", type=int, default=20)
    parser.add_argument("--ma-period", type=int, default=5)
    parser.add_argument("--rsi-period", type=int, default=14)
    parser.add_argument("--oversold", type=float, default=30.0)
    parser.add_argument("--overbought", type=float, default=70.0)
    parser.add_argument("--donchian-window", type=int, default=20)
    parser.add_argument("--breakout-buffer-bps", type=float, default=0.0)
    parser.add_argument("--adx-period", type=int, default=14)
    parser.add_argument("--adx-threshold", type=float, default=25.0)
    parser.add_argument("--atr-ma-period", type=int, default=20)
    parser.add_argument("--atr-period", type=int, default=14)
    parser.add_argument("--atr-multiplier", type=float, default=2.0)
    parser.add_argument("--bollinger-period", type=int, default=20)
    parser.add_argument("--bollinger-stddev-multiplier", type=float, default=2.0)
    parser.add_argument("--macd-fast-period", type=int, default=12)
    parser.add_argument("--macd-slow-period", type=int, default=26)
    parser.add_argument("--macd-signal-period", type=int, default=9)
    parser.add_argument("--macd-histogram-threshold", type=float, default=0.0)
    parser.add_argument("--entry-threshold", type=float, default=0.0)
    parser.add_argument("--primary-ma-period", type=int, default=20)
    parser.add_argument("--reference-ma-period", type=int, default=20)
    parser.add_argument("--spread-threshold-bps", type=float, default=0.0)
    parser.add_argument("--initial-capital", type=float, default=10_000.0)
    parser.add_argument("--fee-bps", type=float, default=10.0)
    parser.add_argument("--slippage-bps", type=float, default=0.0)
    parser.add_argument("--max-position-pct", type=float, default=0.95)
    parser.add_argument("--mainnet-max-notional", type=float, default=100.0)
    parser.add_argument("--mainnet-symbol-whitelist", nargs="+", default=["BTCUSDT"])
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _signal_payload(signal):
    if signal is None:
        return None
    return {
        "signal_id": signal.signal_id,
        "instrument_id": signal.instrument_id,
        "side": None if signal.side is None else signal.side.value,
        "strength": signal.strength,
        "payload": signal.payload,
        "provenance": {
            "plugin_id": signal.provenance.plugin_id,
            "plugin_version": signal.provenance.plugin_version,
            "config_hash": signal.provenance.config_hash,
            "input_fingerprint": signal.provenance.input_fingerprint,
        },
    }


def _last_trade_signal(batch):
    trade_signals = batch.trade_signals()
    return trade_signals[-1] if trade_signals else None


def _signals_consistent(batch_signal, step_signal) -> bool:
    if batch_signal is None and step_signal is None:
        return True
    if batch_signal is None or step_signal is None:
        return False
    batch_bar = batch_signal.payload.get("bar_timestamp")
    step_bar = step_signal.payload.get("bar_timestamp")
    return (
        batch_signal.instrument_id == step_signal.instrument_id
        and batch_signal.side == step_signal.side
        and batch_bar == step_bar
        and abs(float(batch_signal.strength) - float(step_signal.strength)) <= 1e-9
        and batch_signal.provenance.config_hash == step_signal.provenance.config_hash
    )


def _batch_delta_trade_signals(batch, previous_decision_as_of: int | None):
    if previous_decision_as_of is None:
        return batch.trade_signals()
    signals = []
    for signal in batch.trade_signals():
        bar_timestamp = signal.payload.get("bar_timestamp")
        if bar_timestamp is not None and int(bar_timestamp) > int(previous_decision_as_of):
            signals.append(signal)
    return signals


def main() -> int:
    args = build_parser().parse_args()
    load_env_file(args.env_file)

    registry = make_registry()
    pipeline = build_strategy_pipeline(
        strategy=args.strategy,
        symbol=args.symbol.upper(),
        interval=args.interval,
        secondary_interval=args.secondary_interval,
        fast_window=args.fast_window,
        slow_window=args.slow_window,
        entry_threshold=args.entry_threshold,
        ma_period=args.ma_period,
        rsi_period=args.rsi_period,
        oversold=args.oversold,
        overbought=args.overbought,
        donchian_window=args.donchian_window,
        breakout_buffer_bps=args.breakout_buffer_bps,
        adx_period=args.adx_period,
        adx_threshold=args.adx_threshold,
        atr_ma_period=args.atr_ma_period,
        atr_period=args.atr_period,
        atr_multiplier=args.atr_multiplier,
        bollinger_period=args.bollinger_period,
        bollinger_stddev_multiplier=args.bollinger_stddev_multiplier,
        macd_fast_period=args.macd_fast_period,
        macd_slow_period=args.macd_slow_period,
        macd_signal_period=args.macd_signal_period,
        macd_histogram_threshold=args.macd_histogram_threshold,
        primary_ma_period=args.primary_ma_period,
        reference_ma_period=args.reference_ma_period,
        spread_threshold_bps=args.spread_threshold_bps,
    )
    timeframes = [args.interval]
    if args.strategy == "multi_timeframe_ma_spread" and args.secondary_interval not in timeframes:
        timeframes.append(args.secondary_interval)

    market_data = BinanceRestMarketDataAdapter(
        market_type=args.market_type,
        base_url_override=TESTNET_FUTURES_KLINES_URL
        if args.broker == "binance_futures_testnet" and args.market_type == "futures"
        else None,
    )
    if args.broker == "binance_futures_testnet":
        broker = BinanceFuturesTestnetBrokerAdapter(env_path=args.env_file)
    elif args.broker == "binance_futures_mainnet":
        broker = BinanceFuturesMainnetBrokerAdapter(env_path=args.env_file)
    else:
        broker = PaperBrokerAdapter(
            initial_cash=args.initial_capital,
            fee_bps=args.fee_bps,
            slippage_bps=args.slippage_bps,
            account_mode="futures" if args.market_type == "futures" else "spot",
        )

    market_bundle = market_data.fetch_market(
        MarketQuery(
            instruments=[args.symbol.upper()],
            timeframes=timeframes,
            time_range=TimeRange(tail_bars=args.limit),
        )
    )
    policy = AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe=args.interval)
    snapshots = HistoricalSnapshotAssembler(policy=policy, tail_bars=args.limit).build(market_bundle)
    if not snapshots:
        print(json.dumps({"error": "no_snapshots_built"}, ensure_ascii=False, indent=2))
        return 1

    latest_snapshot = snapshots[-1]
    previous_snapshot = snapshots[-2] if len(snapshots) > 1 else None
    account_snapshot = broker.sync_account()
    signal_context = SignalContext(
        account_snapshot=account_snapshot,
        previous_positions={item.instrument_id: item.quantity for item in account_snapshot.positions},
    )
    previous_batch = None
    if previous_snapshot is not None:
        previous_batch = registry.run_pipeline_batch(
            previous_snapshot,
            pipeline.plugin_chain,
            context=signal_context,
        )
    batch_result = registry.run_pipeline_batch(
        latest_snapshot,
        pipeline.plugin_chain,
        context=signal_context,
    )
    states = {}
    for snapshot in snapshots[:-1]:
        step_result = registry.run_pipeline_step(
            snapshot,
            pipeline.plugin_chain,
            previous_states=states,
            context=signal_context,
        )
        states = step_result.states
    latest_step = registry.run_pipeline_step(
        latest_snapshot,
        pipeline.plugin_chain,
        previous_states=states,
        context=signal_context,
    )

    runner = MarketOnlyPaperRunner(
        market_data=market_data,
        signal_registry=registry,
        broker=broker,
        policy=policy,
        risk_rules=(
            [MaxPositionFractionRule(max_fraction=args.max_position_pct)]
            + (
                [
                    InstrumentWhitelistRule(instruments=args.mainnet_symbol_whitelist),
                    MaxAbsoluteNotionalRule(max_notional=args.mainnet_max_notional),
                ]
                if args.broker == "binance_futures_mainnet"
                else []
            )
        ),
        snapshot_tail_bars=args.limit,
    )
    summary = runner.run(
        RunContext(
            run_id=str(uuid.uuid4()),
            trigger=MonitorTrigger(trigger_type=TriggerType.MANUAL, signal_only=True),
            data_query=DataQuery(
                market=MarketQuery(
                    instruments=[args.symbol.upper()],
                    timeframes=timeframes,
                    time_range=TimeRange(tail_bars=args.limit),
                ),
                options=QueryOptions(partial_ok=False),
            ),
            signal_pipeline=pipeline,
            signal_context=signal_context,
            dry_run=True,
        )
    )

    previous_decision_as_of = None if previous_snapshot is None else previous_snapshot.meta.decision_as_of
    batch_delta_signals = _batch_delta_trade_signals(batch_result, previous_decision_as_of)
    batch_signal = batch_delta_signals[-1] if batch_delta_signals else None
    step_signal = _last_trade_signal(latest_step.batch)
    runtime_signal = summary.signals[-1] if summary.signals else None
    consistent = _signals_consistent(batch_signal, step_signal) and _signals_consistent(batch_signal, runtime_signal)
    payload = {
        "consistent": consistent,
        "strategy": args.strategy,
        "symbol": args.symbol.upper(),
        "interval": args.interval,
        "secondary_interval": args.secondary_interval if args.strategy == "multi_timeframe_ma_spread" else None,
        "decision_as_of": latest_snapshot.meta.decision_as_of,
        "batch_delta_signal_count": len(batch_delta_signals),
        "batch_signal": _signal_payload(batch_signal),
        "step_signal": _signal_payload(step_signal),
        "runtime_signal": _signal_payload(runtime_signal),
        "summary": {
            "run_id": summary.run_id,
            "status": summary.status,
            "signal_count": summary.signal_count,
            "errors": summary.errors,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if consistent else 1


if __name__ == "__main__":
    raise SystemExit(main())
