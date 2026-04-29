"""
Ingest recent CME futures K bars from yfinance into standard local parquet.
"""

from __future__ import annotations

import argparse

from ..data.cme import YFINANCE_INTERVAL_BY_TIMEFRAME, download_yfinance_cme_to_parquet


def _parse_intervals(values: list[str]) -> list[str]:
    intervals: list[str] = []
    for value in values:
        for part in value.split(","):
            interval = part.strip()
            if interval:
                intervals.append(interval)
    if not intervals:
        raise argparse.ArgumentTypeError("at least one interval is required")
    unsupported = [interval for interval in intervals if interval not in YFINANCE_INTERVAL_BY_TIMEFRAME]
    if unsupported:
        raise argparse.ArgumentTypeError(
            "unsupported yfinance interval(s): %s" % ", ".join(unsupported)
        )
    return intervals


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download yfinance CME K bars into local parquet")
    parser.add_argument("--symbol", default="MNQ")
    parser.add_argument("--provider-symbol", default=None)
    parser.add_argument("--interval", action="append", default=None)
    parser.add_argument("--period", default="60d")
    parser.add_argument("--historical-dir", default="data/yfinance_mnq")
    parser.add_argument("--timezone", default="UTC")
    parser.add_argument("--progress", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    intervals = _parse_intervals(args.interval or ["5m", "15m"])
    for interval in intervals:
        result = download_yfinance_cme_to_parquet(
            data_root=args.historical_dir,
            instrument_id=args.symbol,
            timeframe=interval,
            period=args.period,
            provider_symbol_override=args.provider_symbol,
            timezone=args.timezone,
            progress=args.progress,
        )
        print(
            "ingested_yfinance_cme symbol=%s interval=%s period=%s rows=%s path=%s"
            % (
                result.instrument_id,
                result.timeframe,
                args.period,
                result.row_count,
                result.path,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
