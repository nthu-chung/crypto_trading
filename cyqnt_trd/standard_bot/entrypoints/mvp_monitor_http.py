"""
Minimal HTTP monitor for the standard bot runtime.
"""

from __future__ import annotations

import argparse
import json
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

from ..config import load_env_file
from ..core import DataQuery, MarketQuery, MonitorTrigger, QueryOptions, TimeRange, TriggerType
from ..data import AlignmentPolicy
from ..data.adapters import BinanceRestMarketDataAdapter
from ..execution import (
    BinanceFuturesTestnetBrokerAdapter,
    LongOnlySinglePositionRule,
    MaxPositionFractionRule,
    PaperBrokerAdapter,
)
from ..runtime import MarketOnlyPaperRunner, RunContext
from .common import build_strategy_pipeline, make_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the standard bot monitor over HTTP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--broker", choices=["paper", "binance_futures_testnet"], default="paper")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--interval", default="1h")
    parser.add_argument("--limit", type=int, default=120)
    parser.add_argument("--market-type", choices=["spot", "futures"], default="futures")
    parser.add_argument("--initial-capital", type=float, default=10_000.0)
    parser.add_argument("--fee-bps", type=float, default=10.0)
    parser.add_argument("--slippage-bps", type=float, default=0.0)
    parser.add_argument("--max-position-pct", type=float, default=0.95)
    return parser


def make_runner(args):
    load_env_file(args.env_file)
    if args.broker == "binance_futures_testnet":
        broker = BinanceFuturesTestnetBrokerAdapter(env_path=args.env_file)
    else:
        broker = PaperBrokerAdapter(
            initial_cash=args.initial_capital,
            fee_bps=args.fee_bps,
            slippage_bps=args.slippage_bps,
        )
    return MarketOnlyPaperRunner(
        market_data=BinanceRestMarketDataAdapter(market_type=args.market_type),
        signal_registry=make_registry(),
        broker=broker,
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe=args.interval),
        risk_rules=[
            MaxPositionFractionRule(max_fraction=args.max_position_pct),
            LongOnlySinglePositionRule(),
        ],
        snapshot_tail_bars=args.limit,
    )


def handler_factory(args, *, runner_override=None):
    runner = runner_override or make_runner(args)

    class MonitorHandler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path != "/health":
                self._send(404, {"error": "not_found"})
                return
            self._send(200, {"ok": True})

        def do_POST(self):  # noqa: N802
            if self.path != "/run":
                self._send(404, {"error": "not_found"})
                return
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            try:
                payload = json.loads(body.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._send(400, {"error": "invalid_json"})
                return
            try:
                symbol = str(payload.get("symbol", "BTCUSDT")).upper()
                interval = str(payload.get("interval", args.interval))
                strategy = str(payload.get("strategy", "moving_average_cross"))
                limit = int(payload.get("limit", args.limit))
                signal_only = bool(payload.get("signal_only", False))
                dry_run = bool(payload.get("dry_run", args.broker == "paper"))

                context = RunContext(
                    run_id=str(payload.get("run_id") or uuid.uuid4()),
                    trigger=MonitorTrigger(
                        trigger_type=TriggerType.HTTP,
                        payload=payload,
                        instruments_override=[symbol],
                        signal_only=signal_only,
                    ),
                    data_query=DataQuery(
                        market=MarketQuery(
                            instruments=[symbol],
                            timeframes=[interval],
                            time_range=TimeRange(tail_bars=limit),
                        ),
                        options=QueryOptions(partial_ok=False),
                    ),
                    signal_pipeline=build_strategy_pipeline(
                        strategy=strategy,
                        symbol=symbol,
                        interval=interval,
                        fast_window=int(payload.get("fast_window", 5)),
                        slow_window=int(payload.get("slow_window", 20)),
                        entry_threshold=float(payload.get("entry_threshold", 0.0)),
                        ma_period=int(payload.get("ma_period", 5)),
                        rsi_period=int(payload.get("rsi_period", 14)),
                        oversold=float(payload.get("oversold", 30.0)),
                        overbought=float(payload.get("overbought", 70.0)),
                    ),
                    dry_run=dry_run,
                )
                summary = runner.run(context)
            except Exception as exc:  # noqa: BLE001
                self._send(500, {"error": "run_failed", "detail": str(exc)})
                return

            self._send(200, summary_to_payload(summary))

        def log_message(self, format, *args_):  # noqa: A003
            return

        def _send(self, status_code: int, payload):
            encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    return MonitorHandler


def summary_to_payload(summary) -> dict:
    return {
        "run_id": summary.run_id,
        "status": summary.status,
        "signal_count": summary.signal_count,
        "errors": summary.errors,
        "execution_reports": [
            {
                "intent_id": report.intent_id,
                "status": report.status.value,
                "reason": report.reason,
                "external_ids": report.external_ids,
                "fills": [fill.__dict__ for fill in report.fills],
            }
            for report in summary.execution_reports
        ],
    }


def main() -> int:
    args = build_parser().parse_args()
    server = ThreadingHTTPServer((args.host, args.port), handler_factory(args))
    print("monitor_listening=http://%s:%s broker=%s" % (args.host, args.port, args.broker))
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
