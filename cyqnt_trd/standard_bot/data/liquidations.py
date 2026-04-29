"""
Local storage helpers for Binance futures liquidation stream data.
"""

from __future__ import annotations

import asyncio
import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

import pandas as pd
import websockets

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:  # pragma: no cover - exercised in environments without pyarrow
    pa = None
    pq = None


_FUTURES_ALL_MARKET_FORCE_ORDERS_STREAM_URL = "wss://fstream.binance.com/ws/!forceOrder@arr"


def ensure_pyarrow_available() -> None:
    if pa is None or pq is None:
        raise RuntimeError("pyarrow is required for liquidation parquet storage; install pyarrow first")


def build_liquidation_path(data_root: str, market_type: str, instrument_id: str, timeframe: str) -> Path:
    return Path(data_root) / market_type / instrument_id.upper() / ("liquidation_%s.parquet" % timeframe)


def build_liquidation_raw_path(data_root: str, market_type: str, capture_id: str) -> Path:
    return Path(data_root) / market_type / "_raw" / ("force_orders_%s.jsonl" % capture_id)


def _liquidation_schema() -> "pa.Schema":
    ensure_pyarrow_available()
    return pa.schema(
        [
            ("timestamp", pa.int64()),
            ("instrument_id", pa.string()),
            ("timeframe", pa.string()),
            ("long_liq_count", pa.int64()),
            ("short_liq_count", pa.int64()),
            ("long_liq_qty", pa.float64()),
            ("short_liq_qty", pa.float64()),
            ("long_liq_notional_usd", pa.float64()),
            ("short_liq_notional_usd", pa.float64()),
            ("total_liq_notional_usd", pa.float64()),
            ("net_liq_notional_usd", pa.float64()),
            ("liq_imbalance_ratio", pa.float64()),
        ]
    )


def _raw_to_records(payload: object) -> List[dict]:
    if isinstance(payload, list):
        records = []
        for item in payload:
            records.extend(_raw_to_records(item))
        return records
    if not isinstance(payload, dict):
        return []
    order = payload.get("o")
    if not isinstance(order, dict):
        return []

    symbol = str(order.get("s") or "").upper()
    side = str(order.get("S") or "").upper()
    if not symbol or side not in {"BUY", "SELL"}:
        return []

    average_price = float(order.get("ap") or order.get("p") or 0.0)
    filled_qty = float(order.get("z") or order.get("q") or 0.0)
    notional = average_price * filled_qty
    return [
        {
            "event_time": int(payload.get("E") or order.get("T") or 0),
            "timestamp": int(order.get("T") or payload.get("E") or 0),
            "instrument_id": symbol,
            "side": side,
            "order_type": str(order.get("o") or ""),
            "time_in_force": str(order.get("f") or ""),
            "status": str(order.get("X") or ""),
            "price": float(order.get("p") or 0.0),
            "average_price": average_price,
            "last_filled_qty": float(order.get("l") or 0.0),
            "filled_qty": filled_qty,
            "notional_usd": notional,
        }
    ]


def _bucket_close_time(timestamp: int, timeframe_ms: int) -> int:
    bucket_open = (int(timestamp) // int(timeframe_ms)) * int(timeframe_ms)
    return bucket_open + int(timeframe_ms) - 1


def aggregate_force_order_records(
    records: Sequence[dict],
    *,
    timeframe: str,
    instrument_ids: Optional[Iterable[str]] = None,
    timeframe_ms: int,
) -> Dict[str, pd.DataFrame]:
    if not records:
        return {}

    allowed = None
    if instrument_ids:
        allowed = {str(symbol).upper() for symbol in instrument_ids}

    rows: List[dict] = []
    for record in records:
        instrument_id = str(record["instrument_id"]).upper()
        if allowed is not None and instrument_id not in allowed:
            continue
        timestamp = int(record["timestamp"])
        side = str(record["side"]).upper()
        notional_usd = float(record["notional_usd"])
        qty = float(record["filled_qty"])
        rows.append(
            {
                "bucket_close_time": _bucket_close_time(timestamp, timeframe_ms),
                "instrument_id": instrument_id,
                "long_liq_count": 1 if side == "SELL" else 0,
                "short_liq_count": 1 if side == "BUY" else 0,
                "long_liq_qty": qty if side == "SELL" else 0.0,
                "short_liq_qty": qty if side == "BUY" else 0.0,
                "long_liq_notional_usd": notional_usd if side == "SELL" else 0.0,
                "short_liq_notional_usd": notional_usd if side == "BUY" else 0.0,
            }
        )

    if not rows:
        return {}

    frame = pd.DataFrame(rows)
    aggregated = (
        frame.groupby(["instrument_id", "bucket_close_time"], sort=True, as_index=False)
        .agg(
            {
                "long_liq_count": "sum",
                "short_liq_count": "sum",
                "long_liq_qty": "sum",
                "short_liq_qty": "sum",
                "long_liq_notional_usd": "sum",
                "short_liq_notional_usd": "sum",
            }
        )
        .rename(columns={"bucket_close_time": "timestamp"})
    )
    aggregated["timeframe"] = timeframe
    aggregated["total_liq_notional_usd"] = (
        aggregated["long_liq_notional_usd"] + aggregated["short_liq_notional_usd"]
    )
    aggregated["net_liq_notional_usd"] = (
        aggregated["short_liq_notional_usd"] - aggregated["long_liq_notional_usd"]
    )
    total = aggregated["total_liq_notional_usd"].replace(0.0, pd.NA)
    aggregated["liq_imbalance_ratio"] = (
        aggregated["net_liq_notional_usd"] / total
    ).fillna(0.0)

    results: Dict[str, pd.DataFrame] = {}
    for instrument_id, symbol_frame in aggregated.groupby("instrument_id", sort=True):
        results[str(instrument_id)] = symbol_frame.sort_values("timestamp", kind="stable").reset_index(drop=True)
    return results


def enrich_market_frame_with_liquidations(
    frame: pd.DataFrame,
    *,
    liquidations_root: Optional[str],
    market_type: str,
    instrument_id: str,
    timeframe: str,
) -> pd.DataFrame:
    if frame.empty or not liquidations_root or market_type != "futures":
        return frame

    path = build_liquidation_path(liquidations_root, market_type, instrument_id, timeframe)
    if not path.exists():
        return frame

    ensure_pyarrow_available()
    liq_frame = pq.read_table(str(path)).to_pandas()
    if liq_frame.empty:
        return frame

    liq_frame = liq_frame.sort_values("timestamp", kind="stable").reset_index(drop=True)
    enriched = pd.merge_asof(
        frame.sort_values("close_time", kind="stable").reset_index(drop=True),
        liq_frame[
            [
                "timestamp",
                "long_liq_count",
                "short_liq_count",
                "long_liq_qty",
                "short_liq_qty",
                "long_liq_notional_usd",
                "short_liq_notional_usd",
                "total_liq_notional_usd",
                "net_liq_notional_usd",
                "liq_imbalance_ratio",
            ]
        ].sort_values("timestamp", kind="stable"),
        left_on="close_time",
        right_on="timestamp",
        direction="backward",
    )
    return enriched.drop(columns=["timestamp"], errors="ignore")


@dataclass
class LiquidationCaptureResult:
    capture_id: str
    market_type: str
    timeframe: str
    raw_path: str
    raw_row_count: int
    aggregate_paths: Dict[str, str] = field(default_factory=dict)
    aggregate_row_counts: Dict[str, int] = field(default_factory=dict)


@dataclass
class HistoricalBinanceLiquidationRecorder:
    data_root: str
    market_type: str = "futures"
    stream_url: str = _FUTURES_ALL_MARKET_FORCE_ORDERS_STREAM_URL

    async def _collect_force_orders(
        self,
        *,
        duration_sec: int,
    ) -> List[dict]:
        if duration_sec <= 0:
            raise ValueError("duration_sec must be > 0")

        deadline = time.time() + float(duration_sec)
        records: List[dict] = []
        async with websockets.connect(
            self.stream_url,
            ping_interval=20,
            ping_timeout=20,
            max_size=2**20,
        ) as websocket:
            while time.time() < deadline:
                timeout = max(0.25, deadline - time.time())
                try:
                    raw_message = await asyncio.wait_for(websocket.recv(), timeout=timeout)
                except asyncio.TimeoutError:
                    break
                payload = json.loads(raw_message)
                records.extend(_raw_to_records(payload))
        return records

    def record_and_store(
        self,
        *,
        duration_sec: int,
        timeframe: str,
        timeframe_ms: int,
        instrument_ids: Optional[Sequence[str]] = None,
    ) -> LiquidationCaptureResult:
        if self.market_type != "futures":
            raise ValueError("liquidation recorder currently supports futures only")

        capture_id = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        records = asyncio.run(self._collect_force_orders(duration_sec=duration_sec))
        raw_path = build_liquidation_raw_path(self.data_root, self.market_type, capture_id)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        with raw_path.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, sort_keys=True))
                handle.write("\n")

        aggregate_paths: Dict[str, str] = {}
        aggregate_row_counts: Dict[str, int] = {}
        symbol_frames = aggregate_force_order_records(
            records,
            timeframe=timeframe,
            instrument_ids=instrument_ids,
            timeframe_ms=timeframe_ms,
        )
        ensure_pyarrow_available()
        schema = _liquidation_schema()
        for instrument_id, symbol_frame in symbol_frames.items():
            target_path = build_liquidation_path(self.data_root, self.market_type, instrument_id, timeframe)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            table = pa.Table.from_pandas(
                symbol_frame[
                    [
                        "timestamp",
                        "instrument_id",
                        "timeframe",
                        "long_liq_count",
                        "short_liq_count",
                        "long_liq_qty",
                        "short_liq_qty",
                        "long_liq_notional_usd",
                        "short_liq_notional_usd",
                        "total_liq_notional_usd",
                        "net_liq_notional_usd",
                        "liq_imbalance_ratio",
                    ]
                ],
                schema=schema,
                preserve_index=False,
            )
            pq.write_table(table, str(target_path))
            aggregate_paths[instrument_id] = str(target_path)
            aggregate_row_counts[instrument_id] = int(len(symbol_frame))

        return LiquidationCaptureResult(
            capture_id=capture_id,
            market_type=self.market_type,
            timeframe=timeframe,
            raw_path=str(raw_path),
            raw_row_count=len(records),
            aggregate_paths=aggregate_paths,
            aggregate_row_counts=aggregate_row_counts,
        )
