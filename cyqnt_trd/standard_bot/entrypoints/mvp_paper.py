"""
Run one paper-execution cycle using the market-only standard bot MVP.
"""

from __future__ import annotations

import argparse
import json
import uuid

from ..core import DataQuery, MarketQuery, MonitorTrigger, QueryOptions, SignalPipelineSpec, TimeRange, TriggerType
from ..data import AlignmentPolicy
from ..data.adapters import BinanceRestMarketDataAdapter, HistoricalJsonMarketDataAdapter
from ..execution import LongOnlySinglePositionRule, MaxPositionFractionRule, PaperBrokerAdapter
from ..runtime import MarketOnlyPaperRunner, RunContext
from .common import build_strategy_pipeline, make_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one standard-bot paper execution cycle")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="1h")
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--market-type", choices=["spot", "futures"], default="spot")
    parser.add_argument(
        "--strategy",
        choices=["moving_average_cross", "price_moving_average", "rsi_reversion"],
        default="moving_average_cross",
    )
    parser.add_argument("--fast-window", type=int, default=5)
    parser.add_argument("--slow-window", type=int, default=20)
    parser.add_argument("--ma-period", type=int, default=5)
    parser.add_argument("--rsi-period", type=int, default=14)
    parser.add_argument("--oversold", type=float, default=30.0)
    parser.add_argument("--overbought", type=float, default=70.0)
    parser.add_argument("--entry-threshold", type=float, default=0.0)
    parser.add_argument("--initial-capital", type=float, default=10_000.0)
    parser.add_argument("--fee-bps", type=float, default=10.0)
    parser.add_argument("--slippage-bps", type=float, default=0.0)
    parser.add_argument("--tail-bars", type=int, default=120)
    parser.add_argument("--max-position-pct", type=float, default=0.95)
    parser.add_argument("--allow-pyramiding", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--input-json", default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.input_json:
        market_data = HistoricalJsonMarketDataAdapter(
            data_path=args.input_json,
            instrument_id=args.symbol.upper(),
            timeframe=args.interval,
        )
    else:
        market_data = BinanceRestMarketDataAdapter(market_type=args.market_type)

    registry = make_registry()
    risk_rules = [MaxPositionFractionRule(max_fraction=args.max_position_pct)]
    if not args.allow_pyramiding:
        risk_rules.append(LongOnlySinglePositionRule())

    runner = MarketOnlyPaperRunner(
        market_data=market_data,
        signal_registry=registry,
        broker=PaperBrokerAdapter(
            initial_cash=args.initial_capital,
            fee_bps=args.fee_bps,
            slippage_bps=args.slippage_bps,
        ),
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe=args.interval),
        risk_rules=risk_rules,
        snapshot_tail_bars=args.tail_bars,
    )

    context = RunContext(
        run_id=str(uuid.uuid4()),
        trigger=MonitorTrigger(trigger_type=TriggerType.MANUAL),
        data_query=DataQuery(
            market=MarketQuery(
                instruments=[args.symbol.upper()],
                timeframes=[args.interval],
                time_range=TimeRange(tail_bars=args.limit),
            ),
            options=QueryOptions(partial_ok=False),
        ),
        signal_pipeline=build_strategy_pipeline(
            strategy=args.strategy,
            symbol=args.symbol.upper(),
            interval=args.interval,
            fast_window=args.fast_window,
            slow_window=args.slow_window,
            entry_threshold=args.entry_threshold,
            ma_period=args.ma_period,
            rsi_period=args.rsi_period,
            oversold=args.oversold,
            overbought=args.overbought,
        ),
        dry_run=args.dry_run,
    )

    summary = runner.run(context)
    print(
        "run_id=%s status=%s signal_count=%s execution_reports=%s"
        % (summary.run_id, summary.status, summary.signal_count, len(summary.execution_reports))
    )
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
