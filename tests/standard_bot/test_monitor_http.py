from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from types import SimpleNamespace

from cyqnt_trd.standard_bot.core import RunSummary
from cyqnt_trd.standard_bot.entrypoints.mvp_monitor_http import handler_factory


class DummyRunner:
    def __init__(self, *, summary: RunSummary | None = None, error: Exception | None = None) -> None:
        self.summary = summary
        self.error = error
        self.contexts = []

    def run(self, context):
        self.contexts.append(context)
        if self.error is not None:
            raise self.error
        return self.summary


def _serve(runner):
    args = SimpleNamespace(
        broker="paper",
        interval="1h",
        limit=120,
        market_type="futures",
        env_file=".env",
        initial_capital=10_000.0,
        fee_bps=10.0,
        slippage_bps=0.0,
        max_position_pct=0.95,
    )
    server_cls = __import__("http.server", fromlist=["ThreadingHTTPServer"]).ThreadingHTTPServer
    server = server_cls(("127.0.0.1", 0), handler_factory(args, runner_override=runner))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _request(url: str, *, method: str = "GET", payload: dict | None = None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, method=method, data=data)
    request.add_header("Content-Type", "application/json")
    return urllib.request.urlopen(request, timeout=5)


def test_monitor_health_endpoint_returns_ok() -> None:
    runner = DummyRunner(summary=RunSummary(run_id="r1", status="ok", signal_count=0))
    server, thread = _serve(runner)
    try:
        with _request("http://127.0.0.1:%s/health" % server.server_port) as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert payload == {"ok": True}
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_monitor_run_endpoint_builds_context_and_returns_summary() -> None:
    runner = DummyRunner(summary=RunSummary(run_id="run-1", status="dry_run", signal_count=2))
    server, thread = _serve(runner)
    try:
        with _request(
            "http://127.0.0.1:%s/run" % server.server_port,
            method="POST",
            payload={
                "run_id": "provided-run-id",
                "symbol": "ETHUSDT",
                "interval": "15m",
                "strategy": "rsi_reversion",
                "signal_only": True,
                "dry_run": True,
                "limit": 60,
            },
        ) as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert payload["run_id"] == "run-1"
        assert payload["status"] == "dry_run"
        assert runner.contexts
        context = runner.contexts[0]
        assert context.run_id == "provided-run-id"
        assert context.trigger.instruments_override == ["ETHUSDT"]
        assert context.trigger.signal_only is True
        assert context.data_query.market.timeframes == ["15m"]
        assert context.signal_pipeline.plugin_chain[0]["plugin_id"] == "rsi_reversion"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_monitor_run_endpoint_rejects_invalid_json() -> None:
    runner = DummyRunner(summary=RunSummary(run_id="run-1", status="ok", signal_count=0))
    server, thread = _serve(runner)
    try:
        request = urllib.request.Request(
            "http://127.0.0.1:%s/run" % server.server_port,
            method="POST",
            data=b"{",
            headers={"Content-Type": "application/json"},
        )
        try:
            urllib.request.urlopen(request, timeout=5)
        except urllib.error.HTTPError as exc:
            payload = json.loads(exc.read().decode("utf-8"))
            assert exc.code == 400
            assert payload["error"] == "invalid_json"
        else:
            raise AssertionError("expected HTTPError")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_monitor_run_endpoint_returns_500_on_runner_error() -> None:
    runner = DummyRunner(error=RuntimeError("boom"))
    server, thread = _serve(runner)
    try:
        try:
            _request("http://127.0.0.1:%s/run" % server.server_port, method="POST", payload={"symbol": "BTCUSDT"})
        except urllib.error.HTTPError as exc:
            payload = json.loads(exc.read().decode("utf-8"))
            assert exc.code == 500
            assert payload["error"] == "run_failed"
            assert payload["detail"] == "boom"
        else:
            raise AssertionError("expected HTTPError")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
