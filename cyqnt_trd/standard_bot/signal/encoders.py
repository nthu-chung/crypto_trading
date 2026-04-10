"""
Thin Python-side encoders for signal kernels.

The roadmap asks for `DataSnapshot -> arrays` to stay outside the numerical
kernel. This module keeps that boundary explicit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from ..core import Bar, DataSnapshot


@dataclass
class EncodedCloseSeries:
    timestamps: np.ndarray
    closes: np.ndarray
    bars: List[Bar]


def series_for(snapshot: DataSnapshot, instrument_id: str, timeframe: str) -> List[Bar]:
    market = snapshot.require_market()
    return market.bars.get(market.key(instrument_id, timeframe), [])


def encode_close_series(snapshot: DataSnapshot, instrument_id: str, timeframe: str) -> EncodedCloseSeries:
    bars = series_for(snapshot, instrument_id, timeframe)
    if not bars:
        return EncodedCloseSeries(
            timestamps=np.zeros(0, dtype=np.int64),
            closes=np.zeros(0, dtype=np.float64),
            bars=[],
        )
    timestamps = np.asarray([int(bar.timestamp) for bar in bars], dtype=np.int64)
    closes = np.asarray([float(bar.close) for bar in bars], dtype=np.float64)
    return EncodedCloseSeries(timestamps=timestamps, closes=closes, bars=bars)
