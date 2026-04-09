"""
Run the standard bot MVP as a market-only historical backtest.
"""

from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

from ..core import BacktestRequest, MarketQuery, SignalPipelineSpec, TimeRange
from ..data import AlignmentPolicy
from ..data.adapters import BinanceRestMarketDataAdapter, HistoricalJsonMarketDataAdapter
from ..data.snapshot import HistoricalSnapshotAssembler
from .common import build_strategy_pipeline, make_registry
from ..simulation.runner import SnapshotBacktestRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the standard bot MVP backtest")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="1h")
    parser.add_argument("--limit", type=int, default=300)
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
    parser.add_argument("--initial-capital", type=float, default=10000.0)
    parser.add_argument("--commission-bps", type=float, default=10.0)
    parser.add_argument("--slippage-bps", type=float, default=0.0)
    parser.add_argument("--tail-bars", type=int, default=120)
    parser.add_argument("--input-json", default=None)
    parser.add_argument("--output-json", default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    policy = AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe=args.interval)
    market_query = MarketQuery(
        instruments=[args.symbol.upper()],
        timeframes=[args.interval],
        time_range=TimeRange(tail_bars=args.limit),
    )

    if args.input_json:
        adapter = HistoricalJsonMarketDataAdapter(
            data_path=args.input_json,
            instrument_id=args.symbol.upper(),
            timeframe=args.interval,
        )
    else:
        adapter = BinanceRestMarketDataAdapter(market_type=args.market_type)

    market_bundle = adapter.fetch_market(market_query)
    snapshots = HistoricalSnapshotAssembler(policy=policy, tail_bars=args.tail_bars).build(market_bundle)

    registry = make_registry()
    pipeline = build_strategy_pipeline(
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
    )

    request = BacktestRequest(
        request_id=str(uuid.uuid4()),
        instruments=[args.symbol.upper()],
        primary_timeframe=args.interval,
        start_ts=snapshots[0].meta.decision_as_of or snapshots[0].meta.assembled_at,
        end_ts=snapshots[-1].meta.decision_as_of or snapshots[-1].meta.assembled_at,
        signal_pipeline=pipeline,
        initial_capital=args.initial_capital,
        fee_model={"commission_bps": args.commission_bps},
        slippage_model={"slippage_bps": args.slippage_bps},
    )

    result = SnapshotBacktestRunner(signal_registry=registry).run(
        request=request,
        snapshots=snapshots,
    )

    trades = result.extras.get("trades", [])
    print(
        "run_id=%s snapshots=%s trades=%s total_return=%.6f final_equity=%.2f"
        % (
            result.extras.get("run_id"),
            int(result.metrics.get("snapshot_count", 0)),
            int(result.metrics.get("trade_count", 0)),
            float(result.total_return),
            float(result.metrics.get("final_equity", args.initial_capital)),
        )
    )
    if trades:
        print("last_trade=%s" % json.dumps(trades[-1], ensure_ascii=False))

    if args.output_json:
        payload = {
            "request_id": result.request_id,
            "total_return": result.total_return,
            "metrics": result.metrics,
            "equity_curve": [point.__dict__ for point in result.equity_curve],
            "trades": trades,
        }
        Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote_output=%s" % args.output_json)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
