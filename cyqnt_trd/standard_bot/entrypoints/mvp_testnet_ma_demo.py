"""
Run a 10-minute MA-based trading demo on Binance futures testnet.
"""

from __future__ import annotations

import argparse
import json
import os
import signal as signal_module
import time
import uuid
from pathlib import Path
from typing import Optional

from ..config import load_env_file
from ..core import ExecutionIntent, MarketQuery, OrderType, TimeRange, TradeSide
from ..data import AlignmentPolicy, HistoricalSnapshotAssembler
from ..data.adapters import BinanceRestMarketDataAdapter
from ..execution import BinanceFuturesTestnetBrokerAdapter
from ..signal import PriceMovingAverageConfig, PriceMovingAveragePlugin

TESTNET_FUTURES_KLINES_URL = "https://testnet.binancefuture.com/fapi/v1/klines"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run an MA-based demo loop on Binance futures testnet")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--symbol", default=None)
    parser.add_argument("--candidates", default="XRPUSDT,SOLUSDT,BNBUSDT,ETHUSDT")
    parser.add_argument("--interval", default="1m")
    parser.add_argument("--period", type=int, default=3)
    parser.add_argument("--duration-minutes", type=int, default=10)
    parser.add_argument("--notional", type=float, default=10.0)
    parser.add_argument("--tail-bars", type=int, default=40)
    parser.add_argument("--log-path", default=None)
    parser.add_argument("--sleep-offset-seconds", type=float, default=2.0)
    return parser


def _now_ms() -> int:
    return int(time.time() * 1000)


def _managed_run_id() -> Optional[str]:
    return os.getenv("STANDARD_BOT_MANAGED_RUN_ID")


def _log(event: dict, *, sink):
    managed_run_id = _managed_run_id()
    if managed_run_id and "managed_run_id" not in event:
        event = dict(event)
        event["managed_run_id"] = managed_run_id
    line = json.dumps(event, ensure_ascii=False)
    print(line, flush=True)
    if sink is not None:
        sink.write(line + "\n")
        sink.flush()


def _position_for_symbol(account_snapshot, symbol: str):
    for position in account_snapshot.positions:
        if position.instrument_id == symbol and position.quantity > 0:
            return position
    return None


def _latest_signal_for_symbol(adapter, plugin, config, symbol: str, interval: str, tail_bars: int):
    bundle = adapter.fetch_market(
        MarketQuery(
            instruments=[symbol],
            timeframes=[interval],
            time_range=TimeRange(tail_bars=tail_bars),
        )
    )
    snapshots = HistoricalSnapshotAssembler(
        policy=AlignmentPolicy(policy_id="bar_close_v1", primary_timeframe=interval),
        tail_bars=tail_bars,
    ).build(bundle)
    if not snapshots:
        return None, None
    snapshot = snapshots[-1]
    batch = plugin.run(snapshot, config)
    signal = batch.signals[-1] if batch.signals else None
    return snapshot, signal


def _choose_symbol(args, broker, adapter, plugin):
    account = broker.sync_account()
    blocked = {position.instrument_id for position in account.positions if position.quantity > 0}
    candidates = [item.strip().upper() for item in args.candidates.split(",") if item.strip()]
    if args.symbol:
        candidates = [args.symbol.upper()] + [item for item in candidates if item != args.symbol.upper()]

    best = None
    for symbol in candidates:
        if symbol in blocked:
            continue
        config = PriceMovingAverageConfig(instrument_id=symbol, timeframe=args.interval, period=args.period)
        snapshot, signal = _latest_signal_for_symbol(adapter, plugin, config, symbol, args.interval, args.tail_bars)
        if signal is None:
            continue
        strength = float(signal.strength)
        if best is None or strength > best["strength"]:
            best = {
                "symbol": symbol,
                "snapshot": snapshot,
                "signal": signal,
                "strength": strength,
                "config": config,
            }

    if best is None:
        raise RuntimeError("no_demo_symbol_with_signal")
    return best


def _build_order(symbol: str, side: TradeSide, *, notional=None, quantity=None, reduce_only=False, suffix=""):
    return ExecutionIntent(
        intent_id=str(uuid.uuid4()),
        instrument_id=symbol,
        side=side,
        order_type=OrderType.MARKET,
        notional=notional,
        quantity=quantity,
        reduce_only=reduce_only,
        client_tag=("demo-%s-%s" % (suffix or side.value, uuid.uuid4().hex[:18]))[:36],
    )


def _sleep_to_next_bar(offset_seconds: float):
    now = time.time()
    seconds = 60 - (now % 60) + offset_seconds
    if seconds < 0:
        seconds += 60
    time.sleep(seconds)


def main() -> int:
    args = build_parser().parse_args()
    load_env_file(args.env_file)

    adapter = BinanceRestMarketDataAdapter(
        market_type="futures",
        base_url_override=TESTNET_FUTURES_KLINES_URL,
    )
    broker = BinanceFuturesTestnetBrokerAdapter(env_path=args.env_file)
    plugin = PriceMovingAveragePlugin()
    sink = None
    if args.log_path:
        Path(args.log_path).parent.mkdir(parents=True, exist_ok=True)
        sink = Path(args.log_path).open("a", encoding="utf-8")

    stop_requested = {"value": False, "signal": None}

    def _request_stop(sig, _frame):  # noqa: ANN001
        stop_requested["value"] = True
        stop_requested["signal"] = sig
        _log(
            {
                "event": "stop_requested",
                "signal": int(sig),
                "timestamp": _now_ms(),
            },
            sink=sink,
        )

    previous_sigterm = signal_module.getsignal(signal_module.SIGTERM)
    previous_sigint = signal_module.getsignal(signal_module.SIGINT)
    signal_module.signal(signal_module.SIGTERM, _request_stop)
    signal_module.signal(signal_module.SIGINT, _request_stop)

    selected = _choose_symbol(args, broker, adapter, plugin)
    symbol = selected["symbol"]
    config = selected["config"]
    state = plugin.initialize_state()

    _log(
        {
            "event": "demo_start",
            "symbol": symbol,
            "interval": args.interval,
            "period": args.period,
            "duration_minutes": args.duration_minutes,
            "notional": args.notional,
            "selected_signal_side": selected["signal"].side.value,
            "selected_signal_strength": selected["strength"],
        },
        sink=sink,
    )

    account = broker.sync_account()
    position = _position_for_symbol(account, symbol)
    initial_signal = selected["signal"]
    if position is None and initial_signal is not None:
        open_report = broker.place_order(
            _build_order(symbol, initial_signal.side, notional=args.notional, suffix="open-initial")
        )
        _log({"event": "initial_order", "report": _report_payload(open_report)}, sink=sink)

    end_at = time.time() + args.duration_minutes * 60
    cycle = 0
    try:
        while time.time() < end_at:
            if stop_requested["value"]:
                break
            cycle += 1
            snapshot, _ = _latest_signal_for_symbol(adapter, plugin, config, symbol, args.interval, args.tail_bars)
            if snapshot is None:
                _log({"event": "cycle_skip", "cycle": cycle, "reason": "no_snapshot"}, sink=sink)
                _sleep_to_next_bar(args.sleep_offset_seconds)
                continue

            step_result = plugin.step(snapshot, state, config)
            state = step_result.state
            latest_signal = step_result.signals[-1] if step_result.signals else None
            account = broker.sync_account()
            position = _position_for_symbol(account, symbol)

            event = {
                "event": "cycle",
                "cycle": cycle,
                "timestamp": _now_ms(),
                "symbol": symbol,
                "position": None if position is None else position.__dict__,
                "signal": None
                if latest_signal is None
                else {
                    "side": latest_signal.side.value,
                    "strength": latest_signal.strength,
                    "bar_timestamp": latest_signal.payload.get("bar_timestamp"),
                },
            }

            if latest_signal is not None:
                if position is None:
                    report = broker.place_order(
                        _build_order(symbol, latest_signal.side, notional=args.notional, suffix="open")
                    )
                    event["execution"] = _report_payload(report)
                elif position.side == "long" and latest_signal.side == TradeSide.SELL:
                    report = broker.place_order(
                        _build_order(
                            symbol,
                            TradeSide.SELL,
                            quantity=position.quantity,
                            reduce_only=True,
                            suffix="close-long",
                        )
                    )
                    event["execution"] = _report_payload(report)
                elif position.side == "short" and latest_signal.side == TradeSide.BUY:
                    report = broker.place_order(
                        _build_order(
                            symbol,
                            TradeSide.BUY,
                            quantity=position.quantity,
                            reduce_only=True,
                            suffix="close-short",
                        )
                    )
                    event["execution"] = _report_payload(report)

            _log(event, sink=sink)
            if stop_requested["value"]:
                break
            _sleep_to_next_bar(args.sleep_offset_seconds)
    finally:
        final_account = broker.sync_account()
        final_position = _position_for_symbol(final_account, symbol)
        if final_position is not None:
            close_side = TradeSide.SELL if final_position.side == "long" else TradeSide.BUY
            close_report = broker.place_order(
                _build_order(
                    symbol,
                    close_side,
                    quantity=final_position.quantity,
                    reduce_only=True,
                    suffix="final-close",
                )
            )
            _log({"event": "final_close", "report": _report_payload(close_report)}, sink=sink)
        _log(
            {
                "event": "demo_end",
                "symbol": symbol,
                "stop_signal": stop_requested["signal"],
                "final_position": None
                if _position_for_symbol(broker.sync_account(), symbol) is None
                else _position_for_symbol(broker.sync_account(), symbol).__dict__,
            },
            sink=sink,
        )
        if sink is not None:
            sink.close()
        signal_module.signal(signal_module.SIGTERM, previous_sigterm)
        signal_module.signal(signal_module.SIGINT, previous_sigint)

    return 0


def _report_payload(report):
    return {
        "intent_id": report.intent_id,
        "status": report.status.value,
        "reason": report.reason,
        "external_ids": report.external_ids,
        "fills": [fill.__dict__ for fill in report.fills],
    }


if __name__ == "__main__":
    raise SystemExit(main())
