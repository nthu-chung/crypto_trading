from __future__ import annotations

import json
from pathlib import Path

from cyqnt_trd.standard_bot.config import BinanceMainnetCredentials, load_env_file
from cyqnt_trd.standard_bot.core import ExecutionIntent, OrderType, TradeSide
from cyqnt_trd.standard_bot.execution import InstrumentWhitelistRule, MaxAbsoluteNotionalRule
from cyqnt_trd.standard_bot.execution.binance_futures_mainnet import (
    BinanceFuturesMainnetBrokerAdapter,
)
from cyqnt_trd.standard_bot.execution.binance_futures_testnet import (
    BinanceFuturesTestnetBrokerAdapter,
)
from cyqnt_trd.standard_bot.execution.idempotency import build_client_tag
import requests


def test_load_env_file_supports_export_prefix(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "export BINANCE_TESTNET_API_KEY=test_key\nexport BINANCE_TESTNET_API_SECRET='test_secret'\n",
        encoding="utf-8",
    )

    loaded = load_env_file(str(env_file), override=True)

    assert loaded["BINANCE_TESTNET_API_KEY"] == "test_key"
    assert loaded["BINANCE_TESTNET_API_SECRET"] == "test_secret"


def test_binance_testnet_broker_quantizes_notional_order() -> None:
    broker = BinanceFuturesTestnetBrokerAdapter(api_key="k", api_secret="s")
    broker._exchange_filters["BTCUSDT"] = {"step_size": 0.001, "min_qty": 0.001, "min_notional": 5.0}

    quantity = broker._resolve_quantity(
        ExecutionIntent(
            intent_id="test-intent",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            notional=123.45,
            risk_hints={"market_price": 100.0},
        )
    )

    assert quantity == 1.234


def test_build_client_tag_is_deterministic_and_short() -> None:
    first = build_client_tag("run-123", "intent-abc")
    second = build_client_tag("run-123", "intent-abc")

    assert first == second
    assert len(first) <= 36


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload)

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError("http error", response=self)

    def json(self) -> dict:
        return self._payload


class _DuplicateThenFetchSession:
    def __init__(self) -> None:
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if method == "POST" and url.endswith("/fapi/v1/order"):
            return _FakeResponse(400, {"code": -4111, "msg": "Duplicate order sent."})
        if method == "GET" and url.endswith("/fapi/v1/order"):
            return _FakeResponse(
                200,
                {
                    "orderId": 123,
                    "symbol": "BTCUSDT",
                    "status": "FILLED",
                    "clientOrderId": kwargs["params"]["origClientOrderId"],
                    "avgPrice": "70000.0",
                    "executedQty": "0.002",
                },
            )
        raise AssertionError("unexpected request: %s %s" % (method, url))


def test_binance_broker_recovers_duplicate_client_order_id() -> None:
    broker = BinanceFuturesTestnetBrokerAdapter(
        api_key="k",
        api_secret="s",
        session=_DuplicateThenFetchSession(),
    )
    broker._exchange_filters["BTCUSDT"] = {"step_size": 0.001, "min_qty": 0.001, "min_notional": 5.0}

    report = broker.place_order(
        ExecutionIntent(
            intent_id="intent-1",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            notional=140.0,
            client_tag="fixed-client-tag",
            risk_hints={"market_price": 70000.0},
        )
    )

    assert report.status.value == "filled"
    assert report.external_ids["client_order_id"] == "fixed-client-tag"


def test_load_mainnet_credentials_supports_primary_and_fallback_names(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "BINANCE_API_KEY=main_key\nBINANCE_SECRET_KEY=main_secret\n",
        encoding="utf-8",
    )

    credentials = BinanceMainnetCredentials.from_env(str(env_file))

    assert credentials.api_key == "main_key"
    assert credentials.api_secret == "main_secret"


def test_binance_mainnet_broker_uses_mainnet_base_url_and_account_id() -> None:
    class _SyncSession:
        def request(self, method, url, **kwargs):
            if method == "GET" and url.endswith("/fapi/v2/balance"):
                return _FakeResponse(200, [{"asset": "USDT", "availableBalance": "1000"}])
            if method == "GET" and url.endswith("/fapi/v2/positionRisk"):
                return _FakeResponse(200, [])
            raise AssertionError("unexpected request: %s %s" % (method, url))

    broker = BinanceFuturesMainnetBrokerAdapter(api_key="k", api_secret="s", session=_SyncSession())
    account = broker.sync_account()

    assert broker.base_url == "https://fapi.binance.com"
    assert account.account_id == "binance_futures_mainnet"
    assert account.extras["environment"] == "mainnet"


def test_instrument_whitelist_rule_rejects_unknown_symbol() -> None:
    reason = InstrumentWhitelistRule(instruments=["BTCUSDT"]).validate(
        ExecutionIntent(
            intent_id="intent",
            instrument_id="ETHUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            notional=10.0,
        ),
        None,
    )

    assert reason == "instrument_not_whitelisted"


def test_max_absolute_notional_rule_rejects_large_order() -> None:
    reason = MaxAbsoluteNotionalRule(max_notional=50.0).validate(
        ExecutionIntent(
            intent_id="intent",
            instrument_id="BTCUSDT",
            side=TradeSide.BUY,
            order_type=OrderType.MARKET,
            notional=100.0,
        ),
        None,
    )

    assert reason == "max_absolute_notional_exceeded"
