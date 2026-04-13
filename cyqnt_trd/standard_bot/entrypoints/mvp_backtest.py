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
from ..data.snapshot import HistoricalSnapshotAssembler
from .common import (
    add_historical_data_arguments,
    build_market_data_adapter,
    build_strategy_pipeline,
    build_time_range,
    make_registry,
)
from ..simulation import NumbaBacktestRunner, SnapshotBacktestRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the standard bot MVP backtest")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="1h")
    parser.add_argument("--limit", type=int, default=300)
    parser.add_argument("--market-type", choices=["spot", "futures"], default="spot")
    parser.add_argument("--engine", choices=["python", "numba"], default="numba")
    parser.add_argument(
        "--strategy",
        choices=["moving_average_cross", "price_moving_average", "rsi_reversion", "donchian_breakout", "multi_timeframe_ma_spread"],
        default="moving_average_cross",
    )
    parser.add_argument("--secondary-interval", default="1h")
    parser.add_argument("--fast-window", type=int, default=5)
    parser.add_argument("--slow-window", type=int, default=20)
    parser.add_argument("--ma-period", type=int, default=5)
    parser.add_argument("--rsi-period", type=int, default=14)
    parser.add_argument("--oversold", type=float, default=30.0)
    parser.add_argument("--overbought", type=float, default=70.0)
    parser.add_argument("--donchian-window", type=int, default=20)
    parser.add_argument("--breakout-buffer-bps", type=float, default=0.0)
    parser.add_argument("--primary-ma-period", type=int, default=20)
    parser.add_argument("--reference-ma-period", type=int, default=20)
    parser.add_argument("--spread-threshold-bps", type=float, default=0.0)
    parser.add_argument("--entry-threshold", type=float, default=0.0)
    parser.add_argument("--initial-capital", type=float, default=10000.0)
    parser.add_argument("--commission-bps", type=float, default=10.0)
    parser.add_argument("--taker-fee-bps", type=float, default=None)
    parser.add_argument("--slippage-bps", type=float, default=0.0)
    parser.add_argument("--impact-slippage-bps", type=float, default=0.0)
    parser.add_argument("--funding-bps-per-bar", type=float, default=0.0)
    parser.add_argument("--max-bar-volume-fraction", type=float, default=0.10)
    parser.add_argument("--tail-bars", type=int, default=120)
    parser.add_argument("--output-json", default=None)
    return add_historical_data_arguments(parser)


def build_market_query(args: argparse.Namespace) -> MarketQuery:
    timeframes = [args.interval]
    if args.strategy == "multi_timeframe_ma_spread" and args.secondary_interval not in timeframes:
        timeframes.append(args.secondary_interval)
    return MarketQuery(
        instruments=[args.symbol.upper()],
        timeframes=timeframes,
        time_range=build_time_range(limit=args.limit, start_ts=args.start_ts, end_ts=args.end_ts),
    )


def load_market_bundle(args: argparse.Namespace, market_query: MarketQuery):
    adapter = build_market_data_adapter(
        args=args,
        symbol=args.symbol.upper(),
        timeframe=args.interval,
    )
    try:
        return adapter.fetch_market(market_query)
    except FileNotFoundError as error:
        if args.download_missing and (market_query.time_range.start_ts is None or market_query.time_range.end_ts is None):
            raise ValueError("--download-missing requires both --start-ts and --end-ts") from error
        raise RuntimeError(
            "missing local historical parquet data; rerun with --download-missing or --allow-remote-api"
        ) from error


def main() -> int:
    args = build_parser().parse_args()
    policy = AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe=args.interval)
    market_query = build_market_query(args)
    market_bundle = load_market_bundle(args, market_query)
    key = market_bundle.key(args.symbol.upper(), args.interval)
    bars = market_bundle.bars.get(key, [])
    if not bars:
        raise ValueError("no bars available for %s" % key)

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
        primary_ma_period=args.primary_ma_period,
        reference_ma_period=args.reference_ma_period,
        spread_threshold_bps=args.spread_threshold_bps,
    )

    request = BacktestRequest(
        request_id=str(uuid.uuid4()),
        instruments=[args.symbol.upper()],
        primary_timeframe=args.interval,
        start_ts=bars[0].timestamp,
        end_ts=bars[-1].timestamp,
        signal_pipeline=pipeline,
        initial_capital=args.initial_capital,
        fee_model={
            "commission_bps": args.commission_bps,
            "taker_fee_bps": args.taker_fee_bps if args.taker_fee_bps is not None else args.commission_bps,
            "funding_bps_per_bar": args.funding_bps_per_bar,
        },
        slippage_model={
            "slippage_bps": args.slippage_bps,
            "impact_slippage_bps": args.impact_slippage_bps,
            "max_bar_volume_fraction": args.max_bar_volume_fraction,
        },
        extras={
            "engine": args.engine,
            "execution_assumption": "signal_at_bar_close_fill_next_bar_open",
        },
    )

    if args.engine == "numba":
        result = NumbaBacktestRunner().run(
            request=request,
            market_bundle=market_bundle,
        )
    else:
        snapshots = HistoricalSnapshotAssembler(policy=policy, tail_bars=args.tail_bars).build(market_bundle)
        request.start_ts = snapshots[0].meta.decision_as_of or snapshots[0].meta.assembled_at
        request.end_ts = snapshots[-1].meta.decision_as_of or snapshots[-1].meta.assembled_at
        result = SnapshotBacktestRunner(signal_registry=registry).run(
            request=request,
            snapshots=snapshots,
        )

    trades = result.extras.get("trades", [])
    print(
        "engine=%s run_id=%s snapshots=%s trades=%s total_return=%.6f final_equity=%.2f"
        % (
            args.engine,
            result.extras.get("run_id"),
            int(result.metrics.get("snapshot_count", 0)),
            int(result.metrics.get("trade_count", 0)),
            float(result.total_return),
            float(result.metrics.get("final_equity", args.initial_capital)),
        )
    )
    if args.engine == "numba":
        print(
            "execution_model=signal_at_bar_close_fill_next_bar_open "
            "taker_fee_bps=%.4f funding_bps_per_bar=%.4f max_bar_volume_fraction=%.4f"
            % (
                float(request.fee_model.get("taker_fee_bps", 0.0)),
                float(request.fee_model.get("funding_bps_per_bar", 0.0)),
                float(request.slippage_model.get("max_bar_volume_fraction", 0.0)),
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
            "signal_batches": [
                {
                    "batch_id": batch.batch_id,
                    "created_at": batch.created_at,
                    "signals": [
                        {
                            "signal_id": signal.signal_id,
                            "instrument_id": signal.instrument_id,
                            "side": None if signal.side is None else signal.side.value,
                            "strength": signal.strength,
                            "payload": signal.payload,
                        }
                        for signal in batch.signals
                    ],
                }
                for batch in result.signal_batches
            ],
            "trades": trades,
            "extras": result.extras,
        }
        Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("wrote_output=%s" % args.output_json)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
