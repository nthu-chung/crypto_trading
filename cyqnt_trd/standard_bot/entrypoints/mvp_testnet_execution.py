"""
Execution-only CLI for Binance futures testnet.
"""

from __future__ import annotations

import argparse
import json
import uuid

from ..core import ExecutionIntent, OrderType, TradeSide
from ..execution import BinanceFuturesTestnetBrokerAdapter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run execution-only actions against Binance futures testnet")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--sync-account", action="store_true")
    parser.add_argument("--validate-order", action="store_true")
    parser.add_argument("--place-order", action="store_true")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--side", choices=["buy", "sell"], default="buy")
    parser.add_argument("--order-type", choices=["market", "limit"], default="market")
    parser.add_argument("--quantity", type=float, default=None)
    parser.add_argument("--notional", type=float, default=None)
    parser.add_argument("--price", type=float, default=None)
    parser.add_argument("--reduce-only", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        broker = BinanceFuturesTestnetBrokerAdapter(env_path=args.env_file)

        if args.sync_account or (not args.validate_order and not args.place_order):
            account = broker.sync_account()
            payload = {
                "account_id": account.account_id,
                "balances": account.balances,
                "positions": [position.__dict__ for position in account.positions],
                "fetched_at": account.fetched_at,
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0

        intent = ExecutionIntent(
            intent_id=str(uuid.uuid4()),
            instrument_id=args.symbol.upper(),
            side=TradeSide.BUY if args.side == "buy" else TradeSide.SELL,
            order_type=OrderType.MARKET if args.order_type == "market" else OrderType.LIMIT,
            quantity=args.quantity,
            notional=args.notional,
            price=args.price,
            reduce_only=args.reduce_only,
        )

        if args.validate_order:
            payload = broker.validate_order(intent)
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0

        if args.place_order:
            report = broker.place_order(intent)
            payload = {
                "intent_id": report.intent_id,
                "status": report.status.value,
                "reason": report.reason,
                "external_ids": report.external_ids,
                "fills": [fill.__dict__ for fill in report.fills],
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
