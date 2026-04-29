"""
CME futures market-data helpers for the standard bot.

The production-safe path for CME remains local parquet. The downloader below is
an unauthenticated Yahoo chart adapter intended to bootstrap delayed continuous
futures research data into that local parquet format. Official CME / broker
exports can be normalized with ``ingest_cme_csv_to_parquet``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import quote

import pandas as pd
import requests

from .alignment import timeframe_to_ms
from .downloader import HistoricalDownloadResult
from .historical import build_history_path, ensure_pyarrow_available

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:  # pragma: no cover - exercised in environments without pyarrow
    pa = None
    pq = None


CME_MARKET_TYPE = "cme"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
YAHOO_CHART_FALLBACK_URL = "https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
HUGGINGFACE_NQ_1M_DATASET_ID = "mdelcristo/NQ-F_1min_OHLCV_Parquet"
HUGGINGFACE_NQ_1M_URL_TEMPLATE = (
    "https://huggingface.co/datasets/{dataset_id}/resolve/main/NQ_1min_{year}.parquet"
)
YFINANCE_INTERVAL_BY_TIMEFRAME = {
    "1m": "1m",
    "2m": "2m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "60m",
    "1d": "1d",
}
YAHOO_INTERVAL_BY_TIMEFRAME = {
    "1m": "1m",
    "2m": "2m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "60m",
    "1d": "1d",
}

CME_CONTRACT_SPECS = {
    "MNQ": {
        "provider_symbol": "MNQ=F",
        "exchange": "CME",
        "contract_name": "Micro E-mini Nasdaq-100",
        "contract_multiplier": 2.0,
        "tick_size": 0.25,
        "tick_value": 0.50,
        "currency": "USD",
    },
    "NQ": {
        "provider_symbol": "NQ=F",
        "exchange": "CME",
        "contract_name": "E-mini Nasdaq-100",
        "contract_multiplier": 20.0,
        "tick_size": 0.25,
        "tick_value": 5.00,
        "currency": "USD",
    },
}


def normalize_cme_instrument_id(instrument_id: str) -> str:
    return instrument_id.upper().replace("=F", "")


def cme_contract_spec(instrument_id: str) -> dict:
    normalized = normalize_cme_instrument_id(instrument_id)
    return dict(CME_CONTRACT_SPECS.get(normalized, {}))


def cme_contract_multiplier(instrument_id: str) -> float:
    return float(cme_contract_spec(instrument_id).get("contract_multiplier", 1.0))


def cme_provider_symbol(instrument_id: str, override: Optional[str] = None) -> str:
    if override:
        return override
    normalized = normalize_cme_instrument_id(instrument_id)
    spec = CME_CONTRACT_SPECS.get(normalized)
    if spec is not None:
        return str(spec["provider_symbol"])
    return "%s=F" % normalized


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
class YahooCmeChartDownloader:
    data_root: str
    timeout: int = 30
    session: Optional[requests.Session] = None
    base_url_template: str = YAHOO_CHART_URL
    fallback_url_template: str = YAHOO_CHART_FALLBACK_URL
    provider_symbol_override: Optional[str] = None
    user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )

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
        if timeframe not in YAHOO_INTERVAL_BY_TIMEFRAME:
            raise ValueError("Yahoo CME downloader does not support timeframe: %s" % timeframe)

        normalized_instrument = normalize_cme_instrument_id(instrument_id)
        chart = self._fetch_chart(
            instrument_id=normalized_instrument,
            timeframe=timeframe,
            start_ts=start_ts,
            end_ts=end_ts,
        )
        records = self._chart_to_records(
            instrument_id=normalized_instrument,
            timeframe=timeframe,
            chart=chart,
        )
        records = [
            row
            for row in records
            if int(row["close_time"]) >= int(start_ts) and int(row["close_time"]) <= int(end_ts)
        ]
        if not records:
            raise ValueError(
                "no CME chart rows returned for %s %s in [%s, %s]"
                % (normalized_instrument, timeframe, start_ts, end_ts)
            )

        target_path = build_history_path(
            self.data_root,
            CME_MARKET_TYPE,
            normalized_instrument,
            timeframe,
        )
        target_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = target_path.with_suffix(".parquet.tmp")
        if temp_path.exists():
            temp_path.unlink()

        table = pa.Table.from_pylist(records, schema=_parquet_schema())
        pq.write_table(table, str(temp_path), compression="zstd")
        os.replace(temp_path, target_path)
        return HistoricalDownloadResult(
            path=str(target_path),
            row_count=len(records),
            chunk_count=1,
            instrument_id=normalized_instrument,
            timeframe=timeframe,
            market_type=CME_MARKET_TYPE,
            start_ts=int(start_ts),
            end_ts=int(end_ts),
        )

    def _fetch_chart(
        self,
        *,
        instrument_id: str,
        timeframe: str,
        start_ts: int,
        end_ts: int,
    ) -> dict:
        provider_symbol = cme_provider_symbol(instrument_id, self.provider_symbol_override)
        params = {
            "period1": int(start_ts // 1000),
            "period2": int(end_ts // 1000),
            "interval": YAHOO_INTERVAL_BY_TIMEFRAME[timeframe],
            "includePrePost": "true",
            "events": "history",
        }
        headers = {"User-Agent": self.user_agent}
        session = self.session or requests
        url = self.base_url_template.format(symbol=quote(provider_symbol, safe=""))
        response = session.get(url, params=params, timeout=self.timeout, headers=headers)
        if response.status_code in {429, 502, 503, 504} and self.fallback_url_template:
            fallback_url = self.fallback_url_template.format(symbol=quote(provider_symbol, safe=""))
            response = session.get(fallback_url, params=params, timeout=self.timeout, headers=headers)
        response.raise_for_status()
        payload = response.json()
        result = payload.get("chart", {}).get("result") or []
        if not result:
            error = payload.get("chart", {}).get("error")
            raise ValueError("Yahoo CME chart returned no result: %s" % error)
        return result[0]

    def _chart_to_records(
        self,
        *,
        instrument_id: str,
        timeframe: str,
        chart: dict,
    ) -> list[dict]:
        timestamps = chart.get("timestamp") or []
        quote_payloads = chart.get("indicators", {}).get("quote") or []
        if not quote_payloads:
            return []
        quote_payload = quote_payloads[0]
        interval_ms = timeframe_to_ms(timeframe)
        multiplier = cme_contract_multiplier(instrument_id)
        records: list[dict] = []
        for index, timestamp_sec in enumerate(timestamps):
            open_value = self._value_at(quote_payload, "open", index)
            high_value = self._value_at(quote_payload, "high", index)
            low_value = self._value_at(quote_payload, "low", index)
            close_value = self._value_at(quote_payload, "close", index)
            if None in {open_value, high_value, low_value, close_value}:
                continue
            volume_value = self._value_at(quote_payload, "volume", index) or 0.0
            open_time = int(timestamp_sec) * 1000
            close_time = open_time + interval_ms - 1
            records.append(
                {
                    "open_time": open_time,
                    "close_time": close_time,
                    "open": float(open_value),
                    "high": float(high_value),
                    "low": float(low_value),
                    "close": float(close_value),
                    "volume": float(volume_value),
                    "quote_volume": float(close_value) * float(volume_value) * multiplier,
                    "trades": 0,
                    "instrument_id": instrument_id,
                    "timeframe": timeframe,
                    "confirmed": True,
                }
            )
        return records

    @staticmethod
    def _value_at(payload: dict, field_name: str, index: int) -> Optional[float]:
        values = payload.get(field_name) or []
        if index >= len(values):
            return None
        value = values[index]
        if value is None:
            return None
        return float(value)


def ingest_cme_csv_to_parquet(
    *,
    csv_path: str | Path,
    data_root: str,
    instrument_id: str,
    timeframe: str,
    timestamp_column: str = "timestamp",
    timezone: str = "UTC",
) -> HistoricalDownloadResult:
    ensure_pyarrow_available()
    normalized_instrument = normalize_cme_instrument_id(instrument_id)
    frame = pd.read_csv(csv_path)
    if timestamp_column not in frame.columns and "open_time" not in frame.columns:
        if {"date", "time"}.issubset({column.lower() for column in frame.columns}):
            lower_to_original = {column.lower(): column for column in frame.columns}
            frame[timestamp_column] = (
                frame[lower_to_original["date"]].astype(str)
                + " "
                + frame[lower_to_original["time"]].astype(str)
            )
        else:
            raise ValueError("CSV must contain timestamp/open_time or date+time columns")

    records = _normalize_cme_csv_frame(
        frame=frame,
        instrument_id=normalized_instrument,
        timeframe=timeframe,
        timestamp_column=timestamp_column,
        timezone=timezone,
    )
    if not records:
        raise ValueError("no rows parsed from CME CSV: %s" % csv_path)

    target_path = build_history_path(data_root, CME_MARKET_TYPE, normalized_instrument, timeframe)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(records, schema=_parquet_schema())
    pq.write_table(table, str(target_path), compression="zstd")
    return HistoricalDownloadResult(
        path=str(target_path),
        row_count=len(records),
        chunk_count=1,
        instrument_id=normalized_instrument,
        timeframe=timeframe,
        market_type=CME_MARKET_TYPE,
        start_ts=int(records[0]["open_time"]),
        end_ts=int(records[-1]["close_time"]),
    )


def download_huggingface_nq_1m_to_parquet(
    *,
    data_root: str,
    instrument_id: str = "MNQ",
    years: Iterable[int],
    dataset_id: str = HUGGINGFACE_NQ_1M_DATASET_ID,
    timeout: int = 120,
    session: Optional[requests.Session] = None,
    timezone: str = "UTC",
) -> HistoricalDownloadResult:
    """Download the free NQ 1m parquet dataset and store it as local CME bars.

    The dataset is NQ price/volume data. For MNQ research we intentionally keep
    the price series but normalize the contract metadata and quote volume using
    the target instrument's multiplier.
    """

    ensure_pyarrow_available()
    normalized_years = _normalize_huggingface_years(years)
    source_paths: list[Path] = []
    target_dir = Path(data_root) / CME_MARKET_TYPE / normalize_cme_instrument_id(instrument_id)
    scratch_dir = target_dir / "_downloads"
    scratch_dir.mkdir(parents=True, exist_ok=True)

    try:
        for year in normalized_years:
            source_paths.append(
                _download_huggingface_nq_year(
                    dataset_id=dataset_id,
                    year=year,
                    output_dir=scratch_dir,
                    timeout=timeout,
                    session=session,
                )
            )
        return ingest_huggingface_nq_parquets_to_parquet(
            source_paths=source_paths,
            data_root=data_root,
            instrument_id=instrument_id,
            timezone=timezone,
        )
    finally:
        for source_path in source_paths:
            source_path.unlink(missing_ok=True)
        if scratch_dir.exists() and not any(scratch_dir.iterdir()):
            scratch_dir.rmdir()


def ingest_huggingface_nq_parquets_to_parquet(
    *,
    source_paths: Iterable[str | Path],
    data_root: str,
    instrument_id: str = "MNQ",
    timezone: str = "UTC",
) -> HistoricalDownloadResult:
    ensure_pyarrow_available()
    normalized_instrument = normalize_cme_instrument_id(instrument_id)
    paths = [Path(path) for path in source_paths]
    if not paths:
        raise ValueError("at least one Hugging Face NQ parquet path is required")

    target_path = build_history_path(data_root, CME_MARKET_TYPE, normalized_instrument, "1m")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target_path.with_suffix(".parquet.tmp")
    if temp_path.exists():
        temp_path.unlink()

    schema = _parquet_schema()
    writer = None
    row_count = 0
    first_open_ts: Optional[int] = None
    last_close_ts: Optional[int] = None
    try:
        for source_path in paths:
            source_frame = pd.read_parquet(source_path)
            standard_frame = _normalize_huggingface_nq_frame(
                frame=source_frame,
                instrument_id=normalized_instrument,
                timezone=timezone,
            )
            if standard_frame.empty:
                continue
            table = pa.Table.from_pandas(standard_frame, schema=schema, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(str(temp_path), schema, compression="zstd")
            writer.write_table(table)
            row_count += int(table.num_rows)
            frame_first_open = int(standard_frame["open_time"].iloc[0])
            frame_last_close = int(standard_frame["close_time"].iloc[-1])
            first_open_ts = frame_first_open if first_open_ts is None else min(first_open_ts, frame_first_open)
            last_close_ts = frame_last_close if last_close_ts is None else max(last_close_ts, frame_last_close)
    finally:
        if writer is not None:
            writer.close()

    if row_count == 0:
        if temp_path.exists():
            temp_path.unlink()
        raise ValueError("no rows parsed from Hugging Face NQ parquet files")

    os.replace(temp_path, target_path)
    return HistoricalDownloadResult(
        path=str(target_path),
        row_count=row_count,
        chunk_count=len(paths),
        instrument_id=normalized_instrument,
        timeframe="1m",
        market_type=CME_MARKET_TYPE,
        start_ts=int(first_open_ts or 0),
        end_ts=int(last_close_ts or 0),
    )


def download_yfinance_cme_to_parquet(
    *,
    data_root: str,
    instrument_id: str,
    timeframe: str,
    period: str = "60d",
    provider_symbol_override: Optional[str] = None,
    timezone: str = "UTC",
    progress: bool = False,
) -> HistoricalDownloadResult:
    try:
        import yfinance as yf
    except ImportError as exc:  # pragma: no cover - exercised in envs without yfinance
        raise RuntimeError("yfinance is required for CME yfinance ingestion; install yfinance first") from exc

    if timeframe not in YFINANCE_INTERVAL_BY_TIMEFRAME:
        raise ValueError("yfinance CME downloader does not support timeframe: %s" % timeframe)

    provider_symbol = cme_provider_symbol(instrument_id, provider_symbol_override)
    frame = yf.download(
        provider_symbol,
        period=period,
        interval=YFINANCE_INTERVAL_BY_TIMEFRAME[timeframe],
        auto_adjust=False,
        progress=progress,
        threads=False,
    )
    if frame.empty:
        raise ValueError(
            "yfinance returned no rows for %s interval=%s period=%s"
            % (provider_symbol, timeframe, period)
        )
    return ingest_yfinance_cme_frame_to_parquet(
        frame=frame,
        data_root=data_root,
        instrument_id=instrument_id,
        timeframe=timeframe,
        timezone=timezone,
    )


def ingest_yfinance_cme_frame_to_parquet(
    *,
    frame: pd.DataFrame,
    data_root: str,
    instrument_id: str,
    timeframe: str,
    timezone: str = "UTC",
) -> HistoricalDownloadResult:
    ensure_pyarrow_available()
    normalized_instrument = normalize_cme_instrument_id(instrument_id)
    records_frame = _normalize_yfinance_cme_frame(
        frame=frame,
        instrument_id=normalized_instrument,
        timeframe=timeframe,
        timezone=timezone,
    )
    if records_frame.empty:
        raise ValueError("no rows parsed from yfinance CME frame")

    target_path = build_history_path(data_root, CME_MARKET_TYPE, normalized_instrument, timeframe)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pandas(records_frame, schema=_parquet_schema(), preserve_index=False)
    pq.write_table(table, str(target_path), compression="zstd")
    return HistoricalDownloadResult(
        path=str(target_path),
        row_count=int(table.num_rows),
        chunk_count=1,
        instrument_id=normalized_instrument,
        timeframe=timeframe,
        market_type=CME_MARKET_TYPE,
        start_ts=int(records_frame["open_time"].iloc[0]),
        end_ts=int(records_frame["close_time"].iloc[-1]),
    )


def _normalize_cme_csv_frame(
    *,
    frame: pd.DataFrame,
    instrument_id: str,
    timeframe: str,
    timestamp_column: str,
    timezone: str,
) -> list[dict]:
    column_map = {column.lower().strip(): column for column in frame.columns}
    required = ["open", "high", "low", "close"]
    missing = [column for column in required if column not in column_map]
    if missing:
        raise ValueError("CME CSV is missing OHLC columns: %s" % ", ".join(missing))

    if "open_time" in column_map:
        open_times = frame[column_map["open_time"]].astype("int64")
    else:
        timestamps = pd.to_datetime(frame[timestamp_column], utc=False)
        if timestamps.dt.tz is None:
            timestamps = timestamps.dt.tz_localize(timezone)
        timestamps = timestamps.dt.tz_convert("UTC")
        open_times = timestamps.map(lambda value: int(value.timestamp() * 1000)).astype("int64")

    interval_ms = timeframe_to_ms(timeframe)
    volume_column = column_map.get("volume")
    trades_column = column_map.get("trades")
    multiplier = cme_contract_multiplier(instrument_id)
    records: list[dict] = []
    working = frame.copy()
    working["_open_time"] = open_times
    working = working.sort_values("_open_time", kind="stable")
    for _, row in working.iterrows():
        open_time = int(row["_open_time"])
        close_value = float(row[column_map["close"]])
        volume = float(row[volume_column]) if volume_column is not None else 0.0
        records.append(
            {
                "open_time": open_time,
                "close_time": open_time + interval_ms - 1,
                "open": float(row[column_map["open"]]),
                "high": float(row[column_map["high"]]),
                "low": float(row[column_map["low"]]),
                "close": close_value,
                "volume": volume,
                "quote_volume": close_value * volume * multiplier,
                "trades": int(row[trades_column]) if trades_column is not None else 0,
                "instrument_id": instrument_id,
                "timeframe": timeframe,
                "confirmed": True,
            }
        )
    return records


def _normalize_huggingface_years(years: Iterable[int]) -> list[int]:
    normalized = sorted({int(year) for year in years})
    if not normalized:
        raise ValueError("at least one year is required")
    return normalized


def _download_huggingface_nq_year(
    *,
    dataset_id: str,
    year: int,
    output_dir: Path,
    timeout: int,
    session: Optional[requests.Session],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    target_path = output_dir / ("NQ_1min_%s.parquet" % int(year))
    temp_path = target_path.with_suffix(".parquet.tmp")
    url = HUGGINGFACE_NQ_1M_URL_TEMPLATE.format(dataset_id=dataset_id, year=int(year))
    client = session or requests
    with client.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with temp_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    os.replace(temp_path, target_path)
    return target_path


def _normalize_huggingface_nq_frame(
    *,
    frame: pd.DataFrame,
    instrument_id: str,
    timezone: str,
) -> pd.DataFrame:
    column_map = {column.lower().strip(): column for column in frame.columns}
    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [column for column in required if column not in column_map]
    if missing:
        raise ValueError("Hugging Face NQ parquet is missing columns: %s" % ", ".join(missing))

    working = frame.dropna(
        subset=[
            column_map["timestamp"],
            column_map["open"],
            column_map["high"],
            column_map["low"],
            column_map["close"],
        ]
    ).copy()
    if working.empty:
        return pd.DataFrame(columns=[field.name for field in _parquet_schema()])

    timestamps = pd.to_datetime(working[column_map["timestamp"]], utc=False)
    if timestamps.dt.tz is None:
        timestamps = timestamps.dt.tz_localize(timezone)
    timestamps = timestamps.dt.tz_convert("UTC")
    open_times = (
        pd.Series(timestamps.to_numpy(dtype="datetime64[ns]")).astype("int64") // 1_000_000
    ).astype("int64")
    close_values = working[column_map["close"]].astype("float64")
    volumes = working[column_map["volume"]].fillna(0.0).astype("float64")
    multiplier = cme_contract_multiplier(instrument_id)

    standard = pd.DataFrame(
        {
            "open_time": open_times.to_numpy(dtype="int64"),
            "close_time": (open_times + timeframe_to_ms("1m") - 1).to_numpy(dtype="int64"),
            "open": working[column_map["open"]].astype("float64").to_numpy(),
            "high": working[column_map["high"]].astype("float64").to_numpy(),
            "low": working[column_map["low"]].astype("float64").to_numpy(),
            "close": close_values.to_numpy(),
            "volume": volumes.to_numpy(),
            "quote_volume": (close_values * volumes * multiplier).to_numpy(),
            "trades": 0,
            "instrument_id": instrument_id,
            "timeframe": "1m",
            "confirmed": True,
        }
    )
    standard = standard.sort_values("open_time", kind="stable").reset_index(drop=True)
    return standard


def _normalize_yfinance_cme_frame(
    *,
    frame: pd.DataFrame,
    instrument_id: str,
    timeframe: str,
    timezone: str,
) -> pd.DataFrame:
    working = frame.copy()
    if isinstance(working.columns, pd.MultiIndex):
        working.columns = [str(column[0]).strip() for column in working.columns]
    else:
        working.columns = [str(column).strip() for column in working.columns]

    column_map = {column.lower().replace(" ", "_"): column for column in working.columns}
    required = ["open", "high", "low", "close"]
    missing = [column for column in required if column not in column_map]
    if missing:
        raise ValueError("yfinance CME frame is missing OHLC columns: %s" % ", ".join(missing))

    volume_column = column_map.get("volume")
    timestamp_column = column_map.get("timestamp") or column_map.get("datetime") or column_map.get("date")
    if timestamp_column is None:
        raw_timestamps = working.index
    else:
        raw_timestamps = working[timestamp_column]

    timestamps = pd.Series(pd.to_datetime(raw_timestamps, utc=False))
    if timestamps.dt.tz is None:
        timestamps = timestamps.dt.tz_localize(timezone)
    timestamps = timestamps.dt.tz_convert("UTC")
    open_times = (
        pd.Series(timestamps.to_numpy(dtype="datetime64[ns]")).astype("int64") // 1_000_000
    ).astype("int64")

    working["_open_time"] = open_times.to_numpy(dtype="int64")
    working = working.dropna(
        subset=[
            column_map["open"],
            column_map["high"],
            column_map["low"],
            column_map["close"],
        ]
    ).copy()
    if working.empty:
        return pd.DataFrame(columns=[field.name for field in _parquet_schema()])

    open_times = working["_open_time"].astype("int64").reset_index(drop=True)
    close_values = working[column_map["close"]].astype("float64").reset_index(drop=True)
    if volume_column is None:
        volumes = pd.Series([0.0] * len(working), dtype="float64")
    else:
        volumes = working[volume_column].fillna(0.0).astype("float64").reset_index(drop=True)
    multiplier = cme_contract_multiplier(instrument_id)
    interval_ms = timeframe_to_ms(timeframe)

    standard = pd.DataFrame(
        {
            "open_time": open_times.to_numpy(dtype="int64"),
            "close_time": (open_times + interval_ms - 1).to_numpy(dtype="int64"),
            "open": working[column_map["open"]].astype("float64").to_numpy(),
            "high": working[column_map["high"]].astype("float64").to_numpy(),
            "low": working[column_map["low"]].astype("float64").to_numpy(),
            "close": close_values.to_numpy(),
            "volume": volumes.to_numpy(),
            "quote_volume": (close_values * volumes * multiplier).to_numpy(),
            "trades": 0,
            "instrument_id": instrument_id,
            "timeframe": timeframe,
            "confirmed": True,
        }
    )
    return standard.sort_values("open_time", kind="stable").reset_index(drop=True)
