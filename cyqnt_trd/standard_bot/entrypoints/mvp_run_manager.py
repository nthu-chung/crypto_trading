"""
Manage local background runs for standard bot demo/runtime commands.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..runtime.run_manager import LocalRunManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage standard bot background runs")
    parser.add_argument("--runs-dir", default=".standard_bot_runs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_demo = subparsers.add_parser("start-testnet-ma-demo", help="Start the testnet MA demo in the background")
    start_demo.add_argument("--env-file", default=".env")
    start_demo.add_argument("--symbol", default=None)
    start_demo.add_argument("--candidates", default="XRPUSDT,SOLUSDT,BNBUSDT,ETHUSDT")
    start_demo.add_argument("--interval", default="1m")
    start_demo.add_argument("--period", type=int, default=3)
    start_demo.add_argument("--duration-minutes", type=int, default=10)
    start_demo.add_argument("--notional", type=float, default=10.0)
    start_demo.add_argument("--tail-bars", type=int, default=40)
    start_demo.add_argument("--sleep-offset-seconds", type=float, default=2.0)
    start_demo.add_argument("--run-id", default=None)
    start_demo.add_argument("--log-path", default=None)

    start_monitor = subparsers.add_parser("start-monitor", help="Start the HTTP monitor in the background")
    start_monitor.add_argument(
        "--broker",
        choices=["paper", "binance_futures_testnet", "binance_futures_mainnet"],
        default="paper",
    )
    start_monitor.add_argument("--env-file", default=".env")
    start_monitor.add_argument("--host", default="127.0.0.1")
    start_monitor.add_argument("--port", type=int, default=8787)
    start_monitor.add_argument("--interval", default="1h")
    start_monitor.add_argument("--limit", type=int, default=120)
    start_monitor.add_argument("--market-type", choices=["spot", "futures"], default="futures")
    start_monitor.add_argument("--initial-capital", type=float, default=10_000.0)
    start_monitor.add_argument("--fee-bps", type=float, default=10.0)
    start_monitor.add_argument("--slippage-bps", type=float, default=0.0)
    start_monitor.add_argument("--max-position-pct", type=float, default=0.95)
    start_monitor.add_argument("--secondary-interval", default="1h")
    start_monitor.add_argument("--allow-mainnet-live", action="store_true")
    start_monitor.add_argument("--mainnet-max-notional", type=float, default=100.0)
    start_monitor.add_argument("--mainnet-symbol-whitelist", nargs="+", default=["BTCUSDT"])
    start_monitor.add_argument("--run-id", default=None)
    start_monitor.add_argument("--log-path", default=None)

    list_parser = subparsers.add_parser("list", help="List managed runs")
    list_parser.add_argument("--all", action="store_true")

    status_parser = subparsers.add_parser("status", help="Show one managed run")
    status_parser.add_argument("--run-id", required=True)

    stop_parser = subparsers.add_parser("stop", help="Gracefully stop a managed run")
    stop_parser.add_argument("--run-id", required=True)
    stop_parser.add_argument("--timeout-seconds", type=float, default=5.0)

    kill_parser = subparsers.add_parser("kill", help="Force kill a managed run")
    kill_parser.add_argument("--run-id", required=True)
    kill_parser.add_argument("--timeout-seconds", type=float, default=2.0)

    return parser


def _manager(args: argparse.Namespace) -> LocalRunManager:
    return LocalRunManager(root_dir=args.runs_dir)


def _print_record(record) -> None:
    print(json.dumps(record.to_dict(), ensure_ascii=False, indent=2))


def _demo_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "cyqnt_trd.standard_bot.entrypoints.mvp_testnet_ma_demo",
        "--env-file",
        args.env_file,
        "--candidates",
        args.candidates,
        "--interval",
        args.interval,
        "--period",
        str(args.period),
        "--duration-minutes",
        str(args.duration_minutes),
        "--notional",
        str(args.notional),
        "--tail-bars",
        str(args.tail_bars),
        "--sleep-offset-seconds",
        str(args.sleep_offset_seconds),
    ]
    if args.symbol:
        command.extend(["--symbol", args.symbol.upper()])
    return command


def _monitor_command(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http",
        "--broker",
        args.broker,
        "--env-file",
        args.env_file,
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--interval",
        args.interval,
        "--limit",
        str(args.limit),
        "--market-type",
        args.market_type,
        "--initial-capital",
        str(args.initial_capital),
        "--fee-bps",
        str(args.fee_bps),
        "--slippage-bps",
        str(args.slippage_bps),
        "--max-position-pct",
        str(args.max_position_pct),
        "--secondary-interval",
        args.secondary_interval,
    ]
    if args.allow_mainnet_live:
        command.append("--allow-mainnet-live")
    command.extend(["--mainnet-max-notional", str(args.mainnet_max_notional)])
    if args.mainnet_symbol_whitelist:
        command.extend(["--mainnet-symbol-whitelist", *args.mainnet_symbol_whitelist])
    return command


def main() -> int:
    args = build_parser().parse_args()
    manager = _manager(args)
    project_root = str(Path(__file__).resolve().parents[3])

    if args.command == "start-testnet-ma-demo":
        record = manager.start_command(
            profile="testnet_ma_demo",
            command=_demo_command(args),
            workdir=project_root,
            run_id=args.run_id,
            log_path=args.log_path,
            tags={
                "interval": args.interval,
                "period": args.period,
                "duration_minutes": args.duration_minutes,
            },
        )
        _print_record(record)
        return 0

    if args.command == "start-monitor":
        record = manager.start_command(
            profile="monitor_http",
            command=_monitor_command(args),
            workdir=project_root,
            run_id=args.run_id,
            log_path=args.log_path,
            tags={
                "broker": args.broker,
                "host": args.host,
                "port": args.port,
            },
        )
        _print_record(record)
        return 0

    if args.command == "list":
        records = manager.list_runs(refresh=True)
        if not args.all:
            records = [record for record in records if record.status not in {"exited", "stopped", "killed"}]
        print(json.dumps([record.to_dict() for record in records], ensure_ascii=False, indent=2))
        return 0

    if args.command == "status":
        _print_record(manager.get_run(args.run_id, refresh=True))
        return 0

    if args.command == "stop":
        _print_record(manager.stop(args.run_id, timeout_seconds=args.timeout_seconds))
        return 0

    if args.command == "kill":
        _print_record(manager.kill(args.run_id, timeout_seconds=args.timeout_seconds))
        return 0

    raise ValueError("unsupported command: %s" % args.command)


if __name__ == "__main__":
    raise SystemExit(main())
