"""
Binance USD-M futures testnet broker adapter.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import time
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_DOWN
from typing import Dict, List, Optional
from urllib.parse import urlencode

import requests

from ..config import BinanceTestnetCredentials
from ..core import (
    AccountPosition,
    AccountSnapshot,
    ExecutionIntent,
    ExecutionReport,
    ExecutionStatus,
    Fill,
    OrderType,
    TradeSide,
)


def _now_ms() -> int:
    return int(time.time() * 1000)


def _format_decimal(value: float) -> str:
    text = format(float(value), ".12f").rstrip("0").rstrip(".")
    return text or "0"


def _truncate_client_order_id(value: str) -> str:
    return value[:36]


@dataclass
class BinanceFuturesTestnetBrokerAdapter:
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    env_path: str = ".env"
    base_url: str = "https://testnet.binancefuture.com"
    recv_window: int = 5000
    timeout: int = 30
    session: requests.Session = field(default_factory=requests.Session)
    reports: List[ExecutionReport] = field(default_factory=list)
    _exchange_filters: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.api_key or not self.api_secret:
            credentials = BinanceTestnetCredentials.from_env(self.env_path)
            self.api_key = credentials.api_key
            self.api_secret = credentials.api_secret

    def place_order(self, intent: ExecutionIntent) -> ExecutionReport:
        client_order_id = _truncate_client_order_id(intent.client_tag or intent.intent_id)
        try:
            quantity = self._resolve_quantity(intent)
            if quantity is None or quantity <= 0:
                return self._reject(intent, "missing_quantity")

            params = {
                "symbol": intent.instrument_id,
                "side": "BUY" if intent.side == TradeSide.BUY else "SELL",
                "type": self._order_type_value(intent.order_type),
                "quantity": _format_decimal(quantity),
                "newClientOrderId": client_order_id,
            }
            if intent.reduce_only:
                params["reduceOnly"] = "true"
            if intent.time_in_force:
                params["timeInForce"] = intent.time_in_force
            if intent.price is not None:
                params["price"] = _format_decimal(float(intent.price))
            if intent.order_type == OrderType.MARKET:
                params["newOrderRespType"] = "RESULT"

            payload = self._signed_request("POST", "/fapi/v1/order", params)
            report = self._report_from_order_payload(intent, payload)
        except requests.HTTPError as exc:
            error_payload = self._response_json(exc.response)
            recovered = self._recover_duplicate_order(
                intent=intent,
                client_order_id=client_order_id,
                error_payload=error_payload,
            )
            if recovered is not None:
                report = recovered
            else:
                message = error_payload.get("msg") if isinstance(error_payload, dict) else None
                report = self._reject(intent, str(message or exc))
        except Exception as exc:  # noqa: BLE001
            report = self._reject(intent, str(exc))

        self.reports.append(report)
        return report

    def cancel_order(self, intent_id: str) -> ExecutionReport:
        params = {"origClientOrderId": _truncate_client_order_id(intent_id)}
        try:
            payload = self._signed_request("DELETE", "/fapi/v1/order", params)
            report = ExecutionReport(
                intent_id=intent_id,
                status=ExecutionStatus.CANCELLED,
                external_ids=self._external_ids(payload),
            )
        except Exception as exc:  # noqa: BLE001
            report = ExecutionReport(
                intent_id=intent_id,
                status=ExecutionStatus.REJECTED,
                reason=str(exc),
            )
        self.reports.append(report)
        return report

    def sync_account(self) -> AccountSnapshot:
        balances_payload = self._signed_request("GET", "/fapi/v2/balance", {})
        positions_payload = self._signed_request("GET", "/fapi/v2/positionRisk", {})

        balances = {
            item["asset"]: float(item.get("availableBalance", item.get("balance", 0.0)))
            for item in balances_payload
        }
        positions = []
        for item in positions_payload:
            quantity = float(item.get("positionAmt", 0.0))
            if abs(quantity) <= 1e-12:
                continue
            positions.append(
                AccountPosition(
                    instrument_id=item["symbol"],
                    quantity=abs(quantity),
                    avg_entry_price=float(item.get("entryPrice", 0.0)) or None,
                    side="long" if quantity > 0 else "short",
                )
            )

        return AccountSnapshot(
            account_id="binance_futures_testnet",
            balances=balances,
            positions=positions,
            fetched_at=_now_ms(),
            extras={"base_url": self.base_url},
        )

    def validate_order(self, intent: ExecutionIntent) -> Dict[str, object]:
        quantity = self._resolve_quantity(intent)
        if quantity is None or quantity <= 0:
            raise ValueError("missing_quantity")
        params = {
            "symbol": intent.instrument_id,
            "side": "BUY" if intent.side == TradeSide.BUY else "SELL",
            "type": self._order_type_value(intent.order_type),
            "quantity": _format_decimal(quantity),
            "newClientOrderId": _truncate_client_order_id(intent.client_tag or intent.intent_id),
        }
        if intent.reduce_only:
            params["reduceOnly"] = "true"
        if intent.time_in_force:
            params["timeInForce"] = intent.time_in_force
        if intent.price is not None:
            params["price"] = _format_decimal(float(intent.price))
        self._signed_request("POST", "/fapi/v1/order/test", params)
        return {"validated": True, "symbol": intent.instrument_id, "quantity": quantity}

    def _resolve_quantity(self, intent: ExecutionIntent) -> Optional[float]:
        if intent.quantity is not None:
            quantity = float(intent.quantity)
        elif intent.notional is not None:
            price = self._resolve_market_price(intent)
            if price is None or price <= 0:
                return None
            quantity = float(intent.notional) / price
        else:
            return None

        filters = self._symbol_filters(intent.instrument_id)
        step_size = filters.get("step_size")
        min_qty = filters.get("min_qty", 0.0)
        min_notional = filters.get("min_notional", 0.0)
        price = self._resolve_market_price(intent)
        if step_size and step_size > 0:
            quantity = float(
                Decimal(str(quantity)).quantize(Decimal(str(step_size)), rounding=ROUND_DOWN)
            )
            if step_size < 1:
                factor = Decimal("1") / Decimal(str(step_size))
                quantity = float((Decimal(str(quantity)) * factor).to_integral_value(rounding=ROUND_DOWN) / factor)
            else:
                quantity = float(math.floor(quantity / step_size) * step_size)

        if quantity < min_qty:
            raise ValueError("quantity_below_min_qty")
        if price is not None and quantity * price < min_notional:
            raise ValueError("notional_below_min_notional")
        return quantity

    def _resolve_market_price(self, intent: ExecutionIntent) -> Optional[float]:
        if intent.price is not None:
            return float(intent.price)
        hinted = intent.risk_hints.get("market_price") or intent.risk_hints.get("reference_price")
        if hinted is not None:
            return float(hinted)
        payload = self._public_request("GET", "/fapi/v1/ticker/price", {"symbol": intent.instrument_id})
        return float(payload["price"])

    def _symbol_filters(self, symbol: str) -> Dict[str, float]:
        if symbol in self._exchange_filters:
            return self._exchange_filters[symbol]

        payload = self._public_request("GET", "/fapi/v1/exchangeInfo", {})
        for symbol_info in payload.get("symbols", []):
            filters = {"step_size": 0.0, "min_qty": 0.0, "min_notional": 0.0}
            for item in symbol_info.get("filters", []):
                if item.get("filterType") == "LOT_SIZE":
                    filters["step_size"] = float(item.get("stepSize", 0.0))
                    filters["min_qty"] = float(item.get("minQty", 0.0))
                elif item.get("filterType") == "MIN_NOTIONAL":
                    filters["min_notional"] = float(item.get("notional", 0.0))
            self._exchange_filters[symbol_info["symbol"]] = filters

        return self._exchange_filters.get(symbol, {"step_size": 0.0, "min_qty": 0.0, "min_notional": 0.0})

    def _order_type_value(self, order_type: OrderType) -> str:
        mapping = {
            OrderType.MARKET: "MARKET",
            OrderType.LIMIT: "LIMIT",
            OrderType.STOP: "STOP",
            OrderType.STOP_LIMIT: "STOP_MARKET",
        }
        return mapping[order_type]

    def _signed_request(self, method: str, path: str, params: Dict[str, object]):
        base_params = dict(params)
        base_params["timestamp"] = _now_ms()
        base_params["recvWindow"] = self.recv_window
        query = urlencode(base_params, doseq=True)
        signature = hmac.new(
            str(self.api_secret).encode("utf-8"),
            query.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        payload = dict(base_params)
        payload["signature"] = signature
        return self._request(method, path, payload, signed=True)

    def _public_request(self, method: str, path: str, params: Dict[str, object]):
        return self._request(method, path, params, signed=False)

    def _request(self, method: str, path: str, params: Dict[str, object], *, signed: bool):
        headers = {"X-MBX-APIKEY": str(self.api_key)} if signed else {}
        kwargs = {"headers": headers, "timeout": self.timeout}
        if method.upper() in {"GET", "DELETE"}:
            kwargs["params"] = params
        else:
            kwargs["data"] = params
        response = self.session.request(method.upper(), "%s%s" % (self.base_url, path), **kwargs)
        response.raise_for_status()
        if not response.text.strip():
            return {}
        return response.json()

    def _recover_duplicate_order(
        self,
        *,
        intent: ExecutionIntent,
        client_order_id: str,
        error_payload: Dict[str, object],
    ) -> Optional[ExecutionReport]:
        message = str(error_payload.get("msg", "")).lower()
        if "duplicate" not in message:
            return None
        payload = self._signed_request(
            "GET",
            "/fapi/v1/order",
            {
                "symbol": intent.instrument_id,
                "origClientOrderId": client_order_id,
            },
        )
        return self._report_from_order_payload(intent, payload)

    def _report_from_order_payload(self, intent: ExecutionIntent, payload: Dict[str, object]) -> ExecutionReport:
        status = self._status_from_exchange_status(str(payload.get("status", "NEW")))
        fills = []
        executed_qty = float(payload.get("executedQty", 0.0) or 0.0)
        avg_price = float(payload.get("avgPrice", 0.0) or 0.0)
        if executed_qty > 0 and avg_price > 0:
            fills.append(Fill(price=avg_price, quantity=executed_qty, fee=0.0, filled_at=_now_ms()))

        return ExecutionReport(
            intent_id=intent.intent_id,
            status=status,
            external_ids=self._external_ids(payload),
            fills=fills,
            reason=payload.get("msg") if status == ExecutionStatus.REJECTED else None,
        )

    def _status_from_exchange_status(self, status: str) -> ExecutionStatus:
        mapping = {
            "NEW": ExecutionStatus.SUBMITTED,
            "PARTIALLY_FILLED": ExecutionStatus.PARTIAL,
            "FILLED": ExecutionStatus.FILLED,
            "CANCELED": ExecutionStatus.CANCELLED,
            "EXPIRED": ExecutionStatus.REJECTED,
            "REJECTED": ExecutionStatus.REJECTED,
        }
        return mapping.get(status, ExecutionStatus.SUBMITTED)

    def _external_ids(self, payload: Dict[str, object]) -> Dict[str, str]:
        items = {}
        if payload.get("orderId") is not None:
            items["order_id"] = str(payload["orderId"])
        if payload.get("clientOrderId") is not None:
            items["client_order_id"] = str(payload["clientOrderId"])
        if payload:
            items["raw"] = json.dumps(payload, ensure_ascii=False)
        return items

    def _response_json(self, response) -> Dict[str, object]:
        if response is None:
            return {}
        try:
            return response.json()
        except Exception:  # noqa: BLE001
            return {}

    def _reject(self, intent: ExecutionIntent, reason: str) -> ExecutionReport:
        return ExecutionReport(
            intent_id=intent.intent_id,
            status=ExecutionStatus.REJECTED,
            reason=reason,
        )
