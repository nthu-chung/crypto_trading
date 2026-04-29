"""
Ingest the free Hugging Face NQ 1m parquet dataset into standard CME storage.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ..data.cme import (
    HUGGINGFACE_NQ_1M_DATASET_ID,
    download_huggingface_nq_1m_to_parquet,
    ingest_huggingface_nq_parquets_to_parquet,
)


def _parse_years(value: str) -> list[int]:
    years: set[int] = set()
    for raw_part in value.split(","):
        part = raw_part.strip()
        if not part:
            continue
        if "-" in part:
            start_raw, end_raw = part.split("-", 1)
            start = int(start_raw.strip())
            end = int(end_raw.strip())
            if end < start:
                raise argparse.ArgumentTypeError("year range end must be >= start")
            years.update(range(start, end + 1))
        else:
            years.add(int(part))
    if not years:
        raise argparse.ArgumentTypeError("at least one year is required")
    return sorted(years)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download or ingest free NQ 1m parquet data as local CME/MNQ bars"
    )
    parser.add_argument("--symbol", default="MNQ")
    parser.add_argument("--historical-dir", default="data/cme_mnq")
    parser.add_argument("--years", type=_parse_years, default=[2025])
    parser.add_argument("--dataset-id", default=HUGGINGFACE_NQ_1M_DATASET_ID)
    parser.add_argument("--source-parquet", action="append", default=[])
    parser.add_argument("--timezone", default="UTC")
    parser.add_argument("--timeout", type=int, default=120)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.source_parquet:
        result = ingest_huggingface_nq_parquets_to_parquet(
            source_paths=[Path(path) for path in args.source_parquet],
            data_root=args.historical_dir,
            instrument_id=args.symbol,
            timezone=args.timezone,
        )
        source = "local"
    else:
        result = download_huggingface_nq_1m_to_parquet(
            data_root=args.historical_dir,
            instrument_id=args.symbol,
            years=args.years,
            dataset_id=args.dataset_id,
            timeout=args.timeout,
            timezone=args.timezone,
        )
        source = "huggingface"

    print(
        "ingested_hf_nq source=%s symbol=%s interval=%s years=%s rows=%s path=%s"
        % (
            source,
            result.instrument_id,
            result.timeframe,
            ",".join(str(year) for year in args.years),
            result.row_count,
            result.path,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
