"""
Historical Binance downloader with chunked requests and streaming parquet writes.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests

from .alignment import timeframe_to_ms
from .historical import build_history_path, ensure_pyarrow_available
from ._ssl_utils import resolve_ca_bundle
from .adapters import _FUTURES_KLINES_URL, _SPOT_KLINES_URL

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:  # pragma: no cover - exercised in environments without pyarrow
    pa = None
    pq = None


def _parquet_schema() -> "pa.Schema":
    ensure_pyarrow_available()
    return pa.schema(
        [
            ("open_time", pa.int64()),
            ("close_time", pa.int64()),
            ("open", pa.float64()),
            ("high", pa.float64()),
            ("low", pa.float64()),
            ("close", pa.float64()),
            ("volume", pa.float64()),
            ("quote_volume", pa.float64()),
            ("trades", pa.int64()),
            ("instrument_id", pa.string()),
            ("timeframe", pa.string()),
            ("confirmed", pa.bool_()),
        ]
    )


@dataclass
class HistoricalDownloadResult:
    path: str
    row_count: int
    chunk_count: int
    instrument_id: str
    timeframe: str
    market_type: str
    start_ts: int
    end_ts: int


@dataclass
class HistoricalBinanceDownloader:
    data_root: str
    market_type: str = "spot"
    timeout: int = 30
    chunk_limit: int = 1000
    request_pause_sec: float = 0.0
    base_url_override: Optional[str] = None
    session: Optional[requests.Session] = None

    @property
    def base_url(self) -> str:
        if self.base_url_override:
            return self.base_url_override
        return _FUTURES_KLINES_URL if self.market_type == "futures" else _SPOT_KLINES_URL

    def download(
        self,
        *,
        instrument_id: str,
        timeframe: str,
        start_ts: int,
        end_ts: int,
    ) -> HistoricalDownloadResult:
        ensure_pyarrow_available()
        if start_ts >= end_ts:
            raise ValueError("start_ts must be smaller than end_ts")

        target_path = build_history_path(self.data_root, self.market_type, instrument_id, timeframe)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = target_path.with_suffix(".parquet.tmp")
        if temp_path.exists():
            temp_path.unlink()

        interval_ms = timeframe_to_ms(timeframe)
        current_start = int(start_ts)
        row_count = 0
        chunk_count = 0
        writer = None
        schema = _parquet_schema()

        try:
            while current_start <= int(end_ts):
                rows = self._fetch_chunk(
                    instrument_id=instrument_id,
                    timeframe=timeframe,
                    start_ts=current_start,
                    end_ts=int(end_ts),
                )
                if not rows:
                    break

                records = []
                for row in rows:
                    open_time = int(row[0])
                    close_time = int(row[6])
                    if close_time < int(start_ts) or close_time > int(end_ts):
                        continue
                    records.append(
                        {
                            "open_time": open_time,
                            "close_time": close_time,
                            "open": float(row[1]),
                            "high": float(row[2]),
                            "low": float(row[3]),
                            "close": float(row[4]),
                            "volume": float(row[5]),
                            "quote_volume": float(row[7]) if len(row) > 7 else 0.0,
                            "trades": int(row[8]) if len(row) > 8 else 0,
                            "instrument_id": instrument_id.upper(),
                            "timeframe": timeframe,
                            "confirmed": True,
                        }
                    )

                if records:
                    table = pa.Table.from_pylist(records, schema=schema)
                    if writer is None:
                        writer = pq.ParquetWriter(str(temp_path), schema, compression="zstd")
                    writer.write_table(table)
                    row_count += len(records)
                    chunk_count += 1

                last_open_time = int(rows[-1][0])
                next_start = last_open_time + interval_ms
                if next_start <= current_start:
                    break
                current_start = next_start
                if self.request_pause_sec > 0:
                    time.sleep(self.request_pause_sec)
        finally:
            if writer is not None:
                writer.close()

        if row_count == 0:
            if temp_path.exists():
                temp_path.unlink()
            raise ValueError(
                "no klines returned for %s %s in [%s, %s]"
                % (instrument_id, timeframe, start_ts, end_ts)
            )

        os.replace(temp_path, target_path)
        return HistoricalDownloadResult(
            path=str(target_path),
            row_count=row_count,
            chunk_count=chunk_count,
            instrument_id=instrument_id.upper(),
            timeframe=timeframe,
            market_type=self.market_type,
            start_ts=int(start_ts),
            end_ts=int(end_ts),
        )

    def _fetch_chunk(self, *, instrument_id: str, timeframe: str, start_ts: int, end_ts: int) -> list:
        params = {
            "symbol": instrument_id.upper(),
            "interval": timeframe,
            "startTime": int(start_ts),
            "endTime": int(end_ts),
            "limit": int(self.chunk_limit),
        }
        session = self.session or requests
        response = session.get(
            self.base_url,
            params=params,
            timeout=self.timeout,
            verify=resolve_ca_bundle(),
        )
        response.raise_for_status()
        return response.json()
