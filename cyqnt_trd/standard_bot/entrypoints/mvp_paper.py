"""
Run one paper-execution cycle using the market-only standard bot MVP.
"""

from __future__ import annotations

import argparse
import json
import uuid

from ..core import DataQuery, MarketQuery, MonitorTrigger, QueryOptions, SignalPipelineSpec, TimeRange, TriggerType
from ..data import AlignmentPolicy
from ..execution import LongOnlySinglePositionRule, MaxPositionFractionRule, PaperBrokerAdapter
from ..runtime import MarketOnlyPaperRunner, RunContext
from .common import (
    add_historical_data_arguments,
    build_market_data_adapter,
    build_strategy_pipeline,
    build_time_range,
    make_registry,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one standard-bot paper execution cycle")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="1h")
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--market-type", choices=["spot", "futures"], default="spot")
    parser.add_argument("--strategy", default="moving_average_cross")
    parser.add_argument("--strategy-module", default=None, help="Python module to import for external strategy registration")
    parser.add_argument("--extra-params", default=None, help="JSON dict of extra strategy config params")
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
    parser.add_argument("--secondary-interval", default="1h")
    parser.add_argument("--primary-ma-period", type=int, default=20)
    parser.add_argument("--reference-ma-period", type=int, default=20)
    parser.add_argument("--spread-threshold-bps", type=float, default=0.0)
    parser.add_argument("--entry-threshold", type=float, default=0.0)
    parser.add_argument("--initial-capital", type=float, default=10_000.0)
    parser.add_argument("--fee-bps", type=float, default=10.0)
    parser.add_argument("--slippage-bps", type=float, default=0.0)
    parser.add_argument("--tail-bars", type=int, default=120)
    parser.add_argument("--max-position-pct", type=float, default=0.95)
    parser.add_argument("--allow-pyramiding", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return add_historical_data_arguments(parser)


def main() -> int:
    args = build_parser().parse_args()
    if args.strategy_module:
        import importlib
        importlib.import_module(args.strategy_module)
    extra_params = json.loads(args.extra_params) if args.extra_params else None
    if args.input_json and args.strategy == "multi_timeframe_ma_spread":
        raise SystemExit("input_json_mode_does_not_support_multi_timeframe_strategy")
    market_data = build_market_data_adapter(
        args=args,
        symbol=args.symbol.upper(),
        timeframe=args.interval,
    )

    registry = make_registry()
    risk_rules = [MaxPositionFractionRule(max_fraction=args.max_position_pct)]
    if not args.allow_pyramiding and args.strategy in {
        "moving_average_cross",
        "price_moving_average",
        "rsi_reversion",
    }:
        risk_rules.append(LongOnlySinglePositionRule())

    runner = MarketOnlyPaperRunner(
        market_data=market_data,
        signal_registry=registry,
        broker=PaperBrokerAdapter(
            initial_cash=args.initial_capital,
            fee_bps=args.fee_bps,
            slippage_bps=args.slippage_bps,
            account_mode="futures" if args.market_type == "futures" else "spot",
        ),
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe=args.interval),
        risk_rules=risk_rules,
        snapshot_tail_bars=args.tail_bars,
    )

    timeframes = [args.interval]
    if args.strategy == "multi_timeframe_ma_spread" and args.secondary_interval not in timeframes:
        timeframes.append(args.secondary_interval)

    context = RunContext(
        run_id=str(uuid.uuid4()),
        trigger=MonitorTrigger(trigger_type=TriggerType.MANUAL),
        data_query=DataQuery(
            market=MarketQuery(
                instruments=[args.symbol.upper()],
                timeframes=timeframes,
                time_range=build_time_range(limit=args.limit, start_ts=args.start_ts, end_ts=args.end_ts),
            ),
            options=QueryOptions(partial_ok=False),
        ),
        signal_pipeline=build_strategy_pipeline(
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
            extra_params=extra_params,
        ),
        dry_run=args.dry_run,
    )

    try:
        summary = runner.run(context)
    except FileNotFoundError as error:
        if args.download_missing and (args.start_ts is None or args.end_ts is None):
            raise SystemExit("--download-missing requires both --start-ts and --end-ts") from error
        raise SystemExit(
            "missing local historical parquet data; rerun with --download-missing or --allow-remote-api"
        ) from error
    print(
        "run_id=%s status=%s signal_count=%s execution_reports=%s"
        % (summary.run_id, summary.status, summary.signal_count, len(summary.execution_reports))
    )
    if summary.signals:
        last_signal = summary.signals[-1]
        payload = {
            "signal_id": last_signal.signal_id,
            "side": None if last_signal.side is None else last_signal.side.value,
            "strength": last_signal.strength,
            "payload": last_signal.payload,
        }
        print("last_signal=%s" % json.dumps(payload, ensure_ascii=False))
    if summary.execution_reports:
        last_report = summary.execution_reports[-1]
        payload = {
            "intent_id": last_report.intent_id,
            "status": last_report.status.value,
            "reason": last_report.reason,
            "fills": [fill.__dict__ for fill in last_report.fills],
        }
        print("last_report=%s" % json.dumps(payload, ensure_ascii=False))
    if summary.errors:
        print("errors=%s" % json.dumps(summary.errors, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
