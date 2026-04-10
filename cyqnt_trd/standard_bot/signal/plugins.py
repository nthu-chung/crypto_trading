"""
Signal plugins backed by shared Numba kernels.

The public plugin interfaces remain Python-friendly, while all numerical
decision logic is routed through the same array kernels used by the fast
backtest path.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np

from ..core import (
    DataSnapshot,
    SignalBatch,
    SignalContext,
    SignalEnvelope,
    SignalKind,
    SignalProvenance,
    TradeSide,
)
from .encoders import encode_close_series, series_for
from .interfaces import SignalState, StepSignalResult
from .numba_kernels import (
    SIGNAL_BUY,
    SIGNAL_NONE,
    SIGNAL_SELL,
    moving_average_cross_signal_rows,
    multi_timeframe_ma_spread_signal_rows,
    price_moving_average_signal_rows,
    rsi_reversion_signal_rows,
)

SIGNAL_NAMESPACE = uuid.UUID("6d011acb-2b89-5dc5-bd38-fa9f903e6495")


def _now_ms() -> int:
    return int(time.time() * 1000)


def _signal_side(direction: int) -> TradeSide:
    return TradeSide.BUY if int(direction) == int(SIGNAL_BUY) else TradeSide.SELL


def _blocked_instruments(context: Optional[SignalContext]) -> List[str]:
    return [] if context is None else context.blacklist


def _config_hash(*parts: object) -> str:
    return "|".join(str(part) for part in parts)


def _build_batch(plugin_id: str, snapshot: DataSnapshot, signals: Sequence[SignalEnvelope]) -> SignalBatch:
    batch_id = str(
        uuid.uuid5(
            SIGNAL_NAMESPACE,
            "%s|%s|%s" % (plugin_id, snapshot.meta.snapshot_id, len(signals)),
        )
    )
    return SignalBatch(signals=list(signals), batch_id=batch_id, created_at=_now_ms())


def _build_signal(
    *,
    snapshot: DataSnapshot,
    plugin_id: str,
    plugin_version: str,
    instrument_id: str,
    timeframe: str,
    time_horizon: str,
    timestamp: int,
    direction: int,
    strength: float,
    payload: Dict[str, object],
    config_hash: str,
) -> SignalEnvelope:
    side = _signal_side(direction)
    signal_id = str(
        uuid.uuid5(
            SIGNAL_NAMESPACE,
            "%s|%s|%s|%s|%s"
            % (
                snapshot.meta.snapshot_id,
                instrument_id,
                timeframe,
                timestamp,
                side.value,
            ),
        )
    )
    return SignalEnvelope(
        version="numba/v1",
        signal_id=signal_id,
        kind=SignalKind.TRADE,
        instrument_id=instrument_id,
        side=side,
        strength=float(strength),
        time_horizon=time_horizon,
        valid_until=snapshot.meta.decision_as_of,
        payload=payload,
        provenance=SignalProvenance(
            plugin_id=plugin_id,
            plugin_version=plugin_version,
            config_hash=config_hash,
            input_fingerprint=snapshot.meta.snapshot_id,
        ),
    )


def _trim_window(values: List[float], max_length: int) -> List[float]:
    if len(values) <= max_length:
        return values
    return values[-max_length:]


def _with_target_position(payload: Dict[str, object], *, target_position: int) -> Dict[str, object]:
    normalized = dict(payload)
    normalized["target_position"] = int(target_position)
    risk_hints = dict(normalized.get("risk_hints", {}))
    risk_hints["target_position"] = int(target_position)
    normalized["risk_hints"] = risk_hints
    return normalized


def _long_only_target_position(direction: int) -> int:
    return 1 if int(direction) == int(SIGNAL_BUY) else 0


@dataclass
class MovingAverageCrossConfig:
    instrument_id: str
    timeframe: str
    fast_window: int = 5
    slow_window: int = 20
    entry_threshold: float = 0.0
    time_horizon: str = "swing"

    def __post_init__(self) -> None:
        self.instrument_id = self.instrument_id.upper()
        if self.fast_window < 1:
            raise ValueError("fast_window must be >= 1")
        if self.slow_window <= self.fast_window:
            raise ValueError("slow_window must be greater than fast_window")
        if self.entry_threshold < 0:
            raise ValueError("entry_threshold must be >= 0")


@dataclass
class PriceMovingAverageConfig:
    instrument_id: str
    timeframe: str
    period: int = 5
    entry_threshold: float = 0.0
    time_horizon: str = "swing"

    def __post_init__(self) -> None:
        self.instrument_id = self.instrument_id.upper()
        if self.period < 2:
            raise ValueError("period must be >= 2")
        if self.entry_threshold < 0:
            raise ValueError("entry_threshold must be >= 0")


@dataclass
class RsiReversionConfig:
    instrument_id: str
    timeframe: str
    period: int = 14
    oversold: float = 30.0
    overbought: float = 70.0
    time_horizon: str = "mean_reversion"

    def __post_init__(self) -> None:
        self.instrument_id = self.instrument_id.upper()
        if self.period < 2:
            raise ValueError("period must be >= 2")
        if self.oversold <= 0 or self.oversold >= 100:
            raise ValueError("oversold must be within (0, 100)")
        if self.overbought <= 0 or self.overbought >= 100:
            raise ValueError("overbought must be within (0, 100)")
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be less than overbought")


@dataclass
class MultiTimeframeMaSpreadConfig:
    instrument_id: str
    primary_timeframe: str
    reference_timeframe: str
    primary_ma_period: int = 20
    reference_ma_period: int = 20
    spread_threshold_bps: float = 0.0
    time_horizon: str = "intraday"

    def __post_init__(self) -> None:
        self.instrument_id = self.instrument_id.upper()
        if self.primary_ma_period < 1:
            raise ValueError("primary_ma_period must be >= 1")
        if self.reference_ma_period < 1:
            raise ValueError("reference_ma_period must be >= 1")
        if self.spread_threshold_bps < 0:
            raise ValueError("spread_threshold_bps must be >= 0")


class MovingAverageCrossPlugin:
    plugin_id = "moving_average_cross"
    plugin_version = "numba/v1"

    def required_inputs(self) -> Dict[str, bool]:
        return {"market": True, "social": False, "onchain": False}

    def run(
        self,
        snapshot: DataSnapshot,
        config: MovingAverageCrossConfig,
        context: Optional[SignalContext] = None,
    ) -> SignalBatch:
        encoded = encode_close_series(snapshot, config.instrument_id, config.timeframe)
        if encoded.closes.size == 0:
            return _build_batch(self.plugin_id, snapshot, [])
        directions, strengths, fast_values, slow_values, spreads = moving_average_cross_signal_rows(
            encoded.closes,
            config.fast_window,
            config.slow_window,
            config.entry_threshold,
        )
        signals = []
        config_hash = _config_hash(
            config.instrument_id,
            config.timeframe,
            config.fast_window,
            config.slow_window,
        )
        blocked = _blocked_instruments(context)
        for index, direction in enumerate(directions):
            if int(direction) == int(SIGNAL_NONE):
                continue
            signals.append(
                _build_signal(
                    snapshot=snapshot,
                    plugin_id=self.plugin_id,
                    plugin_version=self.plugin_version,
                    instrument_id=config.instrument_id,
                    timeframe=config.timeframe,
                    time_horizon=config.time_horizon,
                    timestamp=int(encoded.timestamps[index]),
                    direction=int(direction),
                    strength=float(strengths[index]),
                    payload=_with_target_position(
                        {
                            "bar_timestamp": int(encoded.timestamps[index]),
                            "fast_sma": float(fast_values[index]),
                            "slow_sma": float(slow_values[index]),
                            "spread": float(spreads[index]),
                            "blocked_instruments": blocked,
                        },
                        target_position=_long_only_target_position(int(direction)),
                    ),
                    config_hash=config_hash,
                )
            )
        return _build_batch(self.plugin_id, snapshot, signals)

    def initialize_state(self) -> SignalState:
        return SignalState(plugin_id=self.plugin_id, values={"cursor": None, "close_window": []})

    def step(
        self,
        snapshot: DataSnapshot,
        state: SignalState,
        config: MovingAverageCrossConfig,
        context: Optional[SignalContext] = None,
    ) -> StepSignalResult:
        bars = series_for(snapshot, config.instrument_id, config.timeframe)
        if not bars:
            return StepSignalResult(state=state, signals=[])
        cursor = state.values.get("cursor")
        close_window = [float(value) for value in state.values.get("close_window", [])]
        emitted: List[SignalEnvelope] = []
        blocked = _blocked_instruments(context)
        config_hash = _config_hash(
            config.instrument_id,
            config.timeframe,
            config.fast_window,
            config.slow_window,
        )

        for bar in bars:
            if cursor is not None and bar.timestamp <= cursor:
                continue
            close_window.append(float(bar.close))
            close_window = _trim_window(close_window, config.slow_window)
            closes = np.asarray(close_window, dtype=np.float64)
            directions, strengths, fast_values, slow_values, spreads = moving_average_cross_signal_rows(
                closes,
                config.fast_window,
                config.slow_window,
                config.entry_threshold,
            )
            last_index = closes.shape[0] - 1
            if last_index >= 0 and int(directions[last_index]) != int(SIGNAL_NONE):
                emitted.append(
                    _build_signal(
                        snapshot=snapshot,
                        plugin_id=self.plugin_id,
                        plugin_version=self.plugin_version,
                        instrument_id=config.instrument_id,
                        timeframe=config.timeframe,
                        time_horizon=config.time_horizon,
                        timestamp=int(bar.timestamp),
                        direction=int(directions[last_index]),
                        strength=float(strengths[last_index]),
                        payload=_with_target_position(
                            {
                                "bar_timestamp": int(bar.timestamp),
                                "fast_sma": float(fast_values[last_index]),
                                "slow_sma": float(slow_values[last_index]),
                                "spread": float(spreads[last_index]),
                                "blocked_instruments": blocked,
                            },
                            target_position=_long_only_target_position(int(directions[last_index])),
                        ),
                        config_hash=config_hash,
                    )
                )
            cursor = bar.timestamp
        return StepSignalResult(
            state=SignalState(
                plugin_id=self.plugin_id,
                values={"cursor": cursor, "close_window": close_window},
            ),
            signals=emitted,
        )


class PriceMovingAveragePlugin:
    plugin_id = "price_moving_average"
    plugin_version = "numba/v1"

    def required_inputs(self) -> Dict[str, bool]:
        return {"market": True, "social": False, "onchain": False}

    def run(
        self,
        snapshot: DataSnapshot,
        config: PriceMovingAverageConfig,
        context: Optional[SignalContext] = None,
    ) -> SignalBatch:
        encoded = encode_close_series(snapshot, config.instrument_id, config.timeframe)
        if encoded.closes.size == 0:
            return _build_batch(self.plugin_id, snapshot, [])
        directions, strengths, current_ma_values, prev_ma_values, spreads = price_moving_average_signal_rows(
            encoded.closes,
            config.period,
            config.entry_threshold,
        )
        signals = []
        config_hash = _config_hash(config.instrument_id, config.timeframe, config.period)
        blocked = _blocked_instruments(context)
        for index, direction in enumerate(directions):
            if int(direction) == int(SIGNAL_NONE):
                continue
            current_price = float(encoded.closes[index])
            prev_price = float(encoded.closes[index - 1]) if index > 0 else current_price
            signals.append(
                _build_signal(
                    snapshot=snapshot,
                    plugin_id=self.plugin_id,
                    plugin_version=self.plugin_version,
                    instrument_id=config.instrument_id,
                    timeframe=config.timeframe,
                    time_horizon=config.time_horizon,
                    timestamp=int(encoded.timestamps[index]),
                    direction=int(direction),
                    strength=float(strengths[index]),
                    payload=_with_target_position(
                        {
                            "bar_timestamp": int(encoded.timestamps[index]),
                            "current_price": current_price,
                            "current_ma": float(current_ma_values[index]),
                            "prev_price": prev_price,
                            "prev_ma": float(prev_ma_values[index]),
                            "spread": float(spreads[index]),
                            "blocked_instruments": blocked,
                        },
                        target_position=_long_only_target_position(int(direction)),
                    ),
                    config_hash=config_hash,
                )
            )
        return _build_batch(self.plugin_id, snapshot, signals)

    def initialize_state(self) -> SignalState:
        return SignalState(plugin_id=self.plugin_id, values={"cursor": None, "close_window": []})

    def step(
        self,
        snapshot: DataSnapshot,
        state: SignalState,
        config: PriceMovingAverageConfig,
        context: Optional[SignalContext] = None,
    ) -> StepSignalResult:
        bars = series_for(snapshot, config.instrument_id, config.timeframe)
        if not bars:
            return StepSignalResult(state=state, signals=[])
        cursor = state.values.get("cursor")
        close_window = [float(value) for value in state.values.get("close_window", [])]
        emitted: List[SignalEnvelope] = []
        blocked = _blocked_instruments(context)
        config_hash = _config_hash(config.instrument_id, config.timeframe, config.period)

        for bar in bars:
            if cursor is not None and bar.timestamp <= cursor:
                continue
            close_window.append(float(bar.close))
            close_window = _trim_window(close_window, config.period + 2)
            closes = np.asarray(close_window, dtype=np.float64)
            directions, strengths, current_ma_values, prev_ma_values, spreads = price_moving_average_signal_rows(
                closes,
                config.period,
                config.entry_threshold,
            )
            last_index = closes.shape[0] - 1
            if last_index >= 0 and int(directions[last_index]) != int(SIGNAL_NONE):
                current_price = float(closes[last_index])
                prev_price = float(closes[last_index - 1]) if last_index > 0 else current_price
                emitted.append(
                    _build_signal(
                        snapshot=snapshot,
                        plugin_id=self.plugin_id,
                        plugin_version=self.plugin_version,
                        instrument_id=config.instrument_id,
                        timeframe=config.timeframe,
                        time_horizon=config.time_horizon,
                        timestamp=int(bar.timestamp),
                        direction=int(directions[last_index]),
                        strength=float(strengths[last_index]),
                        payload=_with_target_position(
                            {
                                "bar_timestamp": int(bar.timestamp),
                                "current_price": current_price,
                                "current_ma": float(current_ma_values[last_index]),
                                "prev_price": prev_price,
                                "prev_ma": float(prev_ma_values[last_index]),
                                "spread": float(spreads[last_index]),
                                "blocked_instruments": blocked,
                            },
                            target_position=_long_only_target_position(int(directions[last_index])),
                        ),
                        config_hash=config_hash,
                    )
                )
            cursor = bar.timestamp
        return StepSignalResult(
            state=SignalState(
                plugin_id=self.plugin_id,
                values={"cursor": cursor, "close_window": close_window},
            ),
            signals=emitted,
        )


class RsiReversionPlugin:
    plugin_id = "rsi_reversion"
    plugin_version = "numba/v1"

    def required_inputs(self) -> Dict[str, bool]:
        return {"market": True, "social": False, "onchain": False}

    def run(
        self,
        snapshot: DataSnapshot,
        config: RsiReversionConfig,
        context: Optional[SignalContext] = None,
    ) -> SignalBatch:
        encoded = encode_close_series(snapshot, config.instrument_id, config.timeframe)
        if encoded.closes.size == 0:
            return _build_batch(self.plugin_id, snapshot, [])
        directions, strengths, rsi_values = rsi_reversion_signal_rows(
            encoded.closes,
            config.period,
            config.oversold,
            config.overbought,
        )
        signals = []
        blocked = _blocked_instruments(context)
        config_hash = _config_hash(
            config.instrument_id,
            config.timeframe,
            config.period,
            config.oversold,
            config.overbought,
        )
        for index, direction in enumerate(directions):
            if int(direction) == int(SIGNAL_NONE):
                continue
            signals.append(
                _build_signal(
                    snapshot=snapshot,
                    plugin_id=self.plugin_id,
                    plugin_version=self.plugin_version,
                    instrument_id=config.instrument_id,
                    timeframe=config.timeframe,
                    time_horizon=config.time_horizon,
                    timestamp=int(encoded.timestamps[index]),
                    direction=int(direction),
                    strength=float(strengths[index]),
                    payload=_with_target_position(
                        {
                            "bar_timestamp": int(encoded.timestamps[index]),
                            "rsi": float(rsi_values[index]),
                            "oversold": float(config.oversold),
                            "overbought": float(config.overbought),
                            "blocked_instruments": blocked,
                        },
                        target_position=_long_only_target_position(int(direction)),
                    ),
                    config_hash=config_hash,
                )
            )
        return _build_batch(self.plugin_id, snapshot, signals)

    def initialize_state(self) -> SignalState:
        return SignalState(plugin_id=self.plugin_id, values={"cursor": None, "close_window": []})

    def step(
        self,
        snapshot: DataSnapshot,
        state: SignalState,
        config: RsiReversionConfig,
        context: Optional[SignalContext] = None,
    ) -> StepSignalResult:
        bars = series_for(snapshot, config.instrument_id, config.timeframe)
        if not bars:
            return StepSignalResult(state=state, signals=[])
        cursor = state.values.get("cursor")
        close_window = [float(value) for value in state.values.get("close_window", [])]
        emitted: List[SignalEnvelope] = []
        blocked = _blocked_instruments(context)
        config_hash = _config_hash(
            config.instrument_id,
            config.timeframe,
            config.period,
            config.oversold,
            config.overbought,
        )

        for bar in bars:
            if cursor is not None and bar.timestamp <= cursor:
                continue
            close_window.append(float(bar.close))
            close_window = _trim_window(close_window, config.period + 1)
            closes = np.asarray(close_window, dtype=np.float64)
            directions, strengths, rsi_values = rsi_reversion_signal_rows(
                closes,
                config.period,
                config.oversold,
                config.overbought,
            )
            last_index = closes.shape[0] - 1
            if last_index >= 0 and int(directions[last_index]) != int(SIGNAL_NONE):
                emitted.append(
                    _build_signal(
                        snapshot=snapshot,
                        plugin_id=self.plugin_id,
                        plugin_version=self.plugin_version,
                        instrument_id=config.instrument_id,
                        timeframe=config.timeframe,
                        time_horizon=config.time_horizon,
                        timestamp=int(bar.timestamp),
                        direction=int(directions[last_index]),
                        strength=float(strengths[last_index]),
                        payload=_with_target_position(
                            {
                                "bar_timestamp": int(bar.timestamp),
                                "rsi": float(rsi_values[last_index]),
                                "oversold": float(config.oversold),
                                "overbought": float(config.overbought),
                                "blocked_instruments": blocked,
                            },
                            target_position=_long_only_target_position(int(directions[last_index])),
                        ),
                        config_hash=config_hash,
                    )
                )
            cursor = bar.timestamp

        return StepSignalResult(
            state=SignalState(
                plugin_id=self.plugin_id,
                values={"cursor": cursor, "close_window": close_window},
            ),
            signals=emitted,
        )


class MultiTimeframeMaSpreadPlugin:
    plugin_id = "multi_timeframe_ma_spread"
    plugin_version = "numba/v1"

    def required_inputs(self) -> Dict[str, bool]:
        return {"market": True, "social": False, "onchain": False}

    def run(
        self,
        snapshot: DataSnapshot,
        config: MultiTimeframeMaSpreadConfig,
        context: Optional[SignalContext] = None,
    ) -> SignalBatch:
        primary_encoded = encode_close_series(snapshot, config.instrument_id, config.primary_timeframe)
        secondary_encoded = encode_close_series(snapshot, config.instrument_id, config.reference_timeframe)
        if primary_encoded.closes.size == 0 or secondary_encoded.closes.size == 0:
            return _build_batch(self.plugin_id, snapshot, [])

        directions, strengths, primary_ma_values, secondary_ma_values, spread_bps_values = multi_timeframe_ma_spread_signal_rows(
            primary_encoded.timestamps,
            primary_encoded.closes,
            secondary_encoded.timestamps,
            secondary_encoded.closes,
            config.primary_ma_period,
            config.reference_ma_period,
            config.spread_threshold_bps,
        )
        blocked = _blocked_instruments(context)
        config_hash = _config_hash(
            config.instrument_id,
            config.primary_timeframe,
            config.reference_timeframe,
            config.primary_ma_period,
            config.reference_ma_period,
            config.spread_threshold_bps,
        )
        signals = []
        previous_direction = SIGNAL_NONE
        for index, direction in enumerate(directions):
            if int(direction) == int(SIGNAL_NONE):
                previous_direction = SIGNAL_NONE
                continue
            if int(direction) == int(previous_direction):
                previous_direction = direction
                continue
            signals.append(
                _build_signal(
                    snapshot=snapshot,
                    plugin_id=self.plugin_id,
                    plugin_version=self.plugin_version,
                    instrument_id=config.instrument_id,
                    timeframe=config.primary_timeframe,
                    time_horizon=config.time_horizon,
                    timestamp=int(primary_encoded.timestamps[index]),
                    direction=int(direction),
                    strength=float(strengths[index]),
                    payload=_with_target_position(
                        {
                            "bar_timestamp": int(primary_encoded.timestamps[index]),
                            "primary_timeframe": config.primary_timeframe,
                            "reference_timeframe": config.reference_timeframe,
                            "primary_ma": float(primary_ma_values[index]),
                            "reference_ma": float(secondary_ma_values[index]),
                            "spread_bps": float(spread_bps_values[index]),
                            "blocked_instruments": blocked,
                        },
                        target_position=1 if int(direction) == int(SIGNAL_BUY) else -1,
                    ),
                    config_hash=config_hash,
                )
            )
            previous_direction = direction
        return _build_batch(self.plugin_id, snapshot, signals)

    def initialize_state(self) -> SignalState:
        return SignalState(
            plugin_id=self.plugin_id,
            values={
                "primary_cursor": None,
                "reference_cursor": None,
                "last_direction": int(SIGNAL_NONE),
                "primary_timestamp_window": [],
                "primary_close_window": [],
                "reference_timestamp_window": [],
                "reference_close_window": [],
            },
        )

    def step(
        self,
        snapshot: DataSnapshot,
        state: SignalState,
        config: MultiTimeframeMaSpreadConfig,
        context: Optional[SignalContext] = None,
    ) -> StepSignalResult:
        primary_bars = series_for(snapshot, config.instrument_id, config.primary_timeframe)
        reference_bars = series_for(snapshot, config.instrument_id, config.reference_timeframe)
        if not primary_bars or not reference_bars:
            return StepSignalResult(state=state, signals=[])

        primary_cursor = state.values.get("primary_cursor")
        reference_cursor = state.values.get("reference_cursor")
        last_direction = int(state.values.get("last_direction", int(SIGNAL_NONE)))
        primary_timestamp_window = [int(value) for value in state.values.get("primary_timestamp_window", [])]
        primary_close_window = [float(value) for value in state.values.get("primary_close_window", [])]
        reference_timestamp_window = [int(value) for value in state.values.get("reference_timestamp_window", [])]
        reference_close_window = [float(value) for value in state.values.get("reference_close_window", [])]
        emitted: List[SignalEnvelope] = []
        blocked = _blocked_instruments(context)
        config_hash = _config_hash(
            config.instrument_id,
            config.primary_timeframe,
            config.reference_timeframe,
            config.primary_ma_period,
            config.reference_ma_period,
            config.spread_threshold_bps,
        )

        for primary_bar in primary_bars:
            if primary_cursor is not None and primary_bar.timestamp <= primary_cursor:
                continue
            for reference_bar in reference_bars:
                if reference_bar.timestamp > primary_bar.timestamp:
                    break
                if reference_cursor is not None and reference_bar.timestamp <= reference_cursor:
                    continue
                reference_timestamp_window.append(int(reference_bar.timestamp))
                reference_close_window.append(float(reference_bar.close))
                if len(reference_timestamp_window) > config.reference_ma_period + 1:
                    reference_timestamp_window = reference_timestamp_window[-(config.reference_ma_period + 1) :]
                reference_close_window = _trim_window(reference_close_window, config.reference_ma_period + 1)
                reference_cursor = reference_bar.timestamp

            primary_timestamp_window.append(int(primary_bar.timestamp))
            primary_close_window.append(float(primary_bar.close))
            if len(primary_timestamp_window) > config.primary_ma_period + 1:
                primary_timestamp_window = primary_timestamp_window[-(config.primary_ma_period + 1) :]
            primary_close_window = _trim_window(primary_close_window, config.primary_ma_period + 1)
            full_primary_timestamps = np.asarray(primary_timestamp_window, dtype=np.int64)
            full_primary_closes = np.asarray(primary_close_window, dtype=np.float64)
            full_reference_timestamps = np.asarray(reference_timestamp_window, dtype=np.int64)
            full_reference_closes = np.asarray(reference_close_window, dtype=np.float64)

            directions, strengths, primary_ma_values, secondary_ma_values, spread_bps_values = multi_timeframe_ma_spread_signal_rows(
                full_primary_timestamps,
                full_primary_closes,
                full_reference_timestamps,
                full_reference_closes,
                config.primary_ma_period,
                config.reference_ma_period,
                config.spread_threshold_bps,
            )
            last_index = full_primary_closes.shape[0] - 1
            if last_index >= 0 and int(directions[last_index]) != int(SIGNAL_NONE):
                if int(directions[last_index]) != int(last_direction):
                    emitted.append(
                        _build_signal(
                            snapshot=snapshot,
                            plugin_id=self.plugin_id,
                            plugin_version=self.plugin_version,
                            instrument_id=config.instrument_id,
                            timeframe=config.primary_timeframe,
                            time_horizon=config.time_horizon,
                            timestamp=int(primary_bar.timestamp),
                            direction=int(directions[last_index]),
                            strength=float(strengths[last_index]),
                            payload=_with_target_position(
                                {
                                    "bar_timestamp": int(primary_bar.timestamp),
                                    "primary_timeframe": config.primary_timeframe,
                                    "reference_timeframe": config.reference_timeframe,
                                    "primary_ma": float(primary_ma_values[last_index]),
                                    "reference_ma": float(secondary_ma_values[last_index]),
                                    "spread_bps": float(spread_bps_values[last_index]),
                                    "blocked_instruments": blocked,
                                },
                                target_position=1 if int(directions[last_index]) == int(SIGNAL_BUY) else -1,
                            ),
                            config_hash=config_hash,
                        )
                    )
                    last_direction = int(directions[last_index])
            elif last_index >= 0:
                last_direction = int(SIGNAL_NONE)
            primary_cursor = primary_bar.timestamp

        return StepSignalResult(
            state=SignalState(
                plugin_id=self.plugin_id,
                values={
                    "primary_cursor": primary_cursor,
                    "reference_cursor": reference_cursor,
                    "last_direction": last_direction,
                    "primary_timestamp_window": primary_timestamp_window,
                    "primary_close_window": primary_close_window,
                    "reference_timestamp_window": reference_timestamp_window,
                    "reference_close_window": reference_close_window,
                },
            ),
            signals=emitted,
        )


def register_builtin_plugins(registry) -> None:
    registry.register(MovingAverageCrossPlugin(), lambda raw: MovingAverageCrossConfig(**raw))
    registry.register(PriceMovingAveragePlugin(), lambda raw: PriceMovingAverageConfig(**raw))
    registry.register(RsiReversionPlugin(), lambda raw: RsiReversionConfig(**raw))
    registry.register(MultiTimeframeMaSpreadPlugin(), lambda raw: MultiTimeframeMaSpreadConfig(**raw))
