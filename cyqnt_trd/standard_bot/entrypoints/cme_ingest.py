"""
Ingest CME futures OHLCV CSV files into standard_bot local parquet.
"""

from __future__ import annotations

import argparse

from ..data.cme import ingest_cme_csv_to_parquet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest CME OHLCV CSV into local parquet")
    parser.add_argument("--csv", required=True, help="Path to CME/broker/exported OHLCV CSV")
    parser.add_argument("--symbol", default="MNQ", help="Normalized instrument id, e.g. MNQ")
    parser.add_argument("--interval", default="1m", help="CSV bar timeframe, e.g. 1m, 5m, 15m")
    parser.add_argument("--historical-dir", default="data/historical")
    parser.add_argument("--timestamp-column", default="timestamp")
    parser.add_argument("--timezone", default="UTC")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = ingest_cme_csv_to_parquet(
        csv_path=args.csv,
        data_root=args.historical_dir,
        instrument_id=args.symbol,
        timeframe=args.interval,
        timestamp_column=args.timestamp_column,
        timezone=args.timezone,
    )
    print(
        "ingested_cme_csv symbol=%s interval=%s rows=%s path=%s"
        % (result.instrument_id, result.timeframe, result.row_count, result.path)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
