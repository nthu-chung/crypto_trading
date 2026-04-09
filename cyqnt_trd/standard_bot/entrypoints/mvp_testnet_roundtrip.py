"""
Run a small isolated round-trip trade on Binance futures testnet.
"""

from __future__ import annotations

import argparse
import json
import time
import uuid

from ..core import ExecutionIntent, OrderType, TradeSide
from ..execution import BinanceFuturesTestnetBrokerAdapter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a round-trip trade on Binance futures testnet")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--symbol", default="XRPUSDT")
    parser.add_argument("--side", choices=["buy", "sell"], default="buy")
    parser.add_argument("--notional", type=float, default=10.0)
    parser.add_argument("--sleep-seconds", type=float, default=1.0)
    return parser


def _position_for_symbol(account_snapshot, symbol: str):
    for position in account_snapshot.positions:
        if position.instrument_id == symbol and position.quantity > 0:
            return position
    return None


def _payload(report):
    return {
        "intent_id": report.intent_id,
        "status": report.status.value,
        "reason": report.reason,
        "external_ids": report.external_ids,
        "fills": [fill.__dict__ for fill in report.fills],
    }


def main() -> int:
    args = build_parser().parse_args()
    symbol = args.symbol.upper()
    broker = BinanceFuturesTestnetBrokerAdapter(env_path=args.env_file)

    before = broker.sync_account()
    existing = _position_for_symbol(before, symbol)
    if existing is not None:
        print(
            json.dumps(
                {
                    "error": "symbol_has_existing_position",
                    "symbol": symbol,
                    "quantity": existing.quantity,
                    "side": existing.side,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    open_side = TradeSide.BUY if args.side == "buy" else TradeSide.SELL
    close_side = TradeSide.SELL if open_side == TradeSide.BUY else TradeSide.BUY

    open_intent = ExecutionIntent(
        intent_id=str(uuid.uuid4()),
        instrument_id=symbol,
        side=open_side,
        order_type=OrderType.MARKET,
        notional=args.notional,
        client_tag="stdbot-open-%s" % uuid.uuid4().hex[:12],
    )
    open_report = broker.place_order(open_intent)
    if not open_report.fills:
        print(json.dumps({"error": "open_order_not_filled", "report": _payload(open_report)}, ensure_ascii=False, indent=2))
        return 1

    opened_qty = sum(fill.quantity for fill in open_report.fills)
    time.sleep(max(args.sleep_seconds, 0.0))

    close_intent = ExecutionIntent(
        intent_id=str(uuid.uuid4()),
        instrument_id=symbol,
        side=close_side,
        order_type=OrderType.MARKET,
        quantity=opened_qty,
        reduce_only=True,
        client_tag="stdbot-close-%s" % uuid.uuid4().hex[:11],
    )
    close_report = broker.place_order(close_intent)
    after = broker.sync_account()
    after_position = _position_for_symbol(after, symbol)

    payload = {
        "symbol": symbol,
        "open_report": _payload(open_report),
        "close_report": _payload(close_report),
        "final_position": None if after_position is None else after_position.__dict__,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if after_position is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
