"""
Numba-friendly signal kernels for market-only strategies.

The kernels in this module only consume historical arrays that are visible at
decision time. They intentionally avoid any look-ahead fields so the same math
can be reused by conservative backtests and, later, incremental runtimes.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np

try:
    from numba import njit

    NUMBA_AVAILABLE = True
except Exception:  # pragma: no cover - import fallback for environments without numba
    NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):  # type: ignore
        def decorator(func):
            return func

        return decorator


TARGET_SHORT = np.int8(-1)
TARGET_FLAT = np.int8(0)
TARGET_LONG = np.int8(1)
TARGET_KEEP = np.int8(2)
SIGNAL_SELL = np.int8(-1)
SIGNAL_NONE = np.int8(0)
SIGNAL_BUY = np.int8(1)


@njit(cache=True)
def moving_average_cross_signal_rows(
    closes: np.ndarray,
    fast_window: int,
    slow_window: int,
    entry_threshold: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    directions = np.full(closes.shape[0], SIGNAL_NONE, dtype=np.int8)
    strengths = np.zeros(closes.shape[0], dtype=np.float64)
    fast_values = np.zeros(closes.shape[0], dtype=np.float64)
    slow_values = np.zeros(closes.shape[0], dtype=np.float64)
    spreads = np.zeros(closes.shape[0], dtype=np.float64)
    if closes.shape[0] == 0 or fast_window < 1 or slow_window <= fast_window:
        return directions, strengths, fast_values, slow_values, spreads

    fast_sum = 0.0
    slow_sum = 0.0
    for index in range(closes.shape[0]):
        close_value = closes[index]
        fast_sum += close_value
        slow_sum += close_value
        if index >= fast_window:
            fast_sum -= closes[index - fast_window]
        if index >= slow_window:
            slow_sum -= closes[index - slow_window]
        if index + 1 < slow_window:
            continue

        slow_sma = slow_sum / slow_window
        if slow_sma == 0.0:
            continue

        fast_sma = fast_sum / fast_window
        fast_values[index] = fast_sma
        slow_values[index] = slow_sma
        spread = (fast_sma - slow_sma) / slow_sma
        spreads[index] = spread
        if spread > entry_threshold:
            directions[index] = SIGNAL_BUY
            strengths[index] = abs(spread)
        elif spread < -entry_threshold:
            directions[index] = SIGNAL_SELL
            strengths[index] = abs(spread)
    return directions, strengths, fast_values, slow_values, spreads


@njit(cache=True)
def moving_average_cross_target_updates(
    closes: np.ndarray,
    fast_window: int,
    slow_window: int,
    entry_threshold: float,
) -> Tuple[np.ndarray, np.ndarray]:
    directions, strengths, _, _, _ = moving_average_cross_signal_rows(
        closes,
        fast_window,
        slow_window,
        entry_threshold,
    )
    target_updates = np.full(closes.shape[0], TARGET_KEEP, dtype=np.int8)
    for index in range(closes.shape[0]):
        if directions[index] == SIGNAL_BUY:
            target_updates[index] = TARGET_LONG
        elif directions[index] == SIGNAL_SELL:
            target_updates[index] = TARGET_FLAT
    return target_updates, strengths


@njit(cache=True)
def price_moving_average_signal_rows(
    closes: np.ndarray,
    period: int,
    entry_threshold: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    directions = np.full(closes.shape[0], SIGNAL_NONE, dtype=np.int8)
    strengths = np.zeros(closes.shape[0], dtype=np.float64)
    current_ma_values = np.zeros(closes.shape[0], dtype=np.float64)
    prev_ma_values = np.zeros(closes.shape[0], dtype=np.float64)
    spreads = np.zeros(closes.shape[0], dtype=np.float64)
    if closes.shape[0] == 0 or period < 2:
        return directions, strengths, current_ma_values, prev_ma_values, spreads

    prefix = np.zeros(closes.shape[0] + 1, dtype=np.float64)
    for index in range(closes.shape[0]):
        prefix[index + 1] = prefix[index] + closes[index]

    for index in range(closes.shape[0]):
        if index < period + 1:
            continue

        current_price = closes[index]
        prev_price = closes[index - 1]
        current_ma = (prefix[index] - prefix[index - period]) / period
        prev_ma = (prefix[index - 1] - prefix[index - 1 - period]) / period
        current_ma_values[index] = current_ma
        prev_ma_values[index] = prev_ma
        if current_ma == 0.0 or prev_ma == 0.0:
            continue

        upward_cross = prev_price <= prev_ma and current_price > current_ma
        downward_cross = prev_price >= prev_ma and current_price < current_ma
        if not upward_cross and not downward_cross:
            continue

        spread = (current_price - current_ma) / current_ma
        spreads[index] = spread
        if abs(spread) <= entry_threshold:
            continue

        directions[index] = SIGNAL_BUY if upward_cross else SIGNAL_SELL
        strengths[index] = abs(spread)
    return directions, strengths, current_ma_values, prev_ma_values, spreads


@njit(cache=True)
def price_moving_average_target_updates(
    closes: np.ndarray,
    period: int,
    entry_threshold: float,
) -> Tuple[np.ndarray, np.ndarray]:
    directions, strengths, _, _, _ = price_moving_average_signal_rows(
        closes,
        period,
        entry_threshold,
    )
    target_updates = np.full(closes.shape[0], TARGET_KEEP, dtype=np.int8)
    for index in range(closes.shape[0]):
        if directions[index] == SIGNAL_BUY:
            target_updates[index] = TARGET_LONG
        elif directions[index] == SIGNAL_SELL:
            target_updates[index] = TARGET_FLAT
    return target_updates, strengths


@njit(cache=True)
def rsi_reversion_signal_rows(
    closes: np.ndarray,
    period: int,
    oversold: float,
    overbought: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    directions = np.full(closes.shape[0], SIGNAL_NONE, dtype=np.int8)
    strengths = np.zeros(closes.shape[0], dtype=np.float64)
    rsi_values = np.zeros(closes.shape[0], dtype=np.float64)
    if closes.shape[0] == 0 or period < 2:
        return directions, strengths, rsi_values

    for index in range(period, closes.shape[0]):
        gains = 0.0
        losses = 0.0
        for step in range(index - period + 1, index + 1):
            delta = closes[step] - closes[step - 1]
            if delta > 0.0:
                gains += delta
            elif delta < 0.0:
                losses += -delta

        avg_gain = gains / period
        avg_loss = losses / period
        if avg_loss == 0.0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))
        rsi_values[index] = rsi

        if rsi < oversold:
            directions[index] = SIGNAL_BUY
            strengths[index] = (oversold - rsi) / max(oversold, 1e-9)
        elif rsi > overbought:
            directions[index] = SIGNAL_SELL
            strengths[index] = (rsi - overbought) / max(100.0 - overbought, 1e-9)
    return directions, strengths, rsi_values


@njit(cache=True)
def multi_timeframe_ma_spread_signal_rows(
    primary_timestamps: np.ndarray,
    primary_closes: np.ndarray,
    secondary_timestamps: np.ndarray,
    secondary_closes: np.ndarray,
    primary_period: int,
    secondary_period: int,
    threshold_bps: float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    directions = np.full(primary_closes.shape[0], SIGNAL_NONE, dtype=np.int8)
    strengths = np.zeros(primary_closes.shape[0], dtype=np.float64)
    primary_ma_values = np.zeros(primary_closes.shape[0], dtype=np.float64)
    secondary_ma_aligned = np.zeros(primary_closes.shape[0], dtype=np.float64)
    spread_bps_values = np.zeros(primary_closes.shape[0], dtype=np.float64)
    if primary_closes.shape[0] == 0 or secondary_closes.shape[0] == 0:
        return directions, strengths, primary_ma_values, secondary_ma_aligned, spread_bps_values
    if primary_period < 1 or secondary_period < 1:
        return directions, strengths, primary_ma_values, secondary_ma_aligned, spread_bps_values

    primary_prefix = np.zeros(primary_closes.shape[0] + 1, dtype=np.float64)
    secondary_prefix = np.zeros(secondary_closes.shape[0] + 1, dtype=np.float64)
    for index in range(primary_closes.shape[0]):
        primary_prefix[index + 1] = primary_prefix[index] + primary_closes[index]
    for index in range(secondary_closes.shape[0]):
        secondary_prefix[index + 1] = secondary_prefix[index] + secondary_closes[index]

    secondary_cursor = -1
    threshold_ratio = threshold_bps / 10_000.0

    for primary_index in range(primary_closes.shape[0]):
        while secondary_cursor + 1 < secondary_timestamps.shape[0] and secondary_timestamps[secondary_cursor + 1] <= primary_timestamps[primary_index]:
            secondary_cursor += 1
        if primary_index + 1 < primary_period:
            continue
        if secondary_cursor + 1 < secondary_period:
            continue

        primary_ma = (primary_prefix[primary_index + 1] - primary_prefix[primary_index + 1 - primary_period]) / primary_period
        secondary_ma = (
            secondary_prefix[secondary_cursor + 1] - secondary_prefix[secondary_cursor + 1 - secondary_period]
        ) / secondary_period
        primary_ma_values[primary_index] = primary_ma
        secondary_ma_aligned[primary_index] = secondary_ma
        if secondary_ma == 0.0:
            continue

        spread_ratio = (primary_ma - secondary_ma) / secondary_ma
        spread_bps = spread_ratio * 10_000.0
        spread_bps_values[primary_index] = spread_bps
        if spread_ratio > threshold_ratio:
            directions[primary_index] = SIGNAL_BUY
            strengths[primary_index] = abs(spread_ratio)
        elif spread_ratio < -threshold_ratio:
            directions[primary_index] = SIGNAL_SELL
            strengths[primary_index] = abs(spread_ratio)
    return directions, strengths, primary_ma_values, secondary_ma_aligned, spread_bps_values


@njit(cache=True)
def multi_timeframe_ma_spread_target_updates(
    primary_timestamps: np.ndarray,
    primary_closes: np.ndarray,
    secondary_timestamps: np.ndarray,
    secondary_closes: np.ndarray,
    primary_period: int,
    secondary_period: int,
    threshold_bps: float,
) -> Tuple[np.ndarray, np.ndarray]:
    directions, strengths, _, _, _ = multi_timeframe_ma_spread_signal_rows(
        primary_timestamps,
        primary_closes,
        secondary_timestamps,
        secondary_closes,
        primary_period,
        secondary_period,
        threshold_bps,
    )
    target_updates = np.full(primary_closes.shape[0], TARGET_KEEP, dtype=np.int8)
    previous_direction = SIGNAL_NONE
    for index in range(primary_closes.shape[0]):
        current_direction = directions[index]
        if current_direction == SIGNAL_NONE:
            previous_direction = SIGNAL_NONE
            continue
        if current_direction == previous_direction:
            continue
        if current_direction == SIGNAL_BUY:
            target_updates[index] = TARGET_LONG
        elif current_direction == SIGNAL_SELL:
            target_updates[index] = TARGET_SHORT
        previous_direction = current_direction
    return target_updates, strengths
