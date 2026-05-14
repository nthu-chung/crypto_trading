"""
Numba-backed historical backtest runner.

Design choices in this runner follow a conservative bar-based execution model:

- Signals are computed from confirmed historical bars only.
- A signal observed at bar-close ``t`` can only execute at the next bar open ``t+1``.
- Market-order style fills use taker fees plus configurable slippage / impact.
- Liquidity is capped by a fraction of the next bar's reported volume / quote volume.
- Funding can be charged per held bar for futures-style tests.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Dict, List, Sequence, Tuple

import numpy as np

from ..core import (
    BacktestRequest,
    BacktestResult,
    EquityPoint,
    MarketBundle,
    SignalBatch,
    SignalEnvelope,
    SignalKind,
    SignalProvenance,
    TradeSide,
)
from ..signal.numba_kernels import (
    adx_trend_strength_target_updates,
    atr_breakout_target_updates,
    bollinger_mean_reversion_target_updates,
    liquidation_reversal_target_updates,
    NUMBA_AVAILABLE,
    oi_funding_breakout_target_updates,
    TARGET_KEEP,
    TARGET_LONG,
    donchian_breakout_target_updates,
    macd_trend_follow_target_updates,
    moving_average_cross_target_updates,
    multi_timeframe_ma_spread_target_updates,
    price_moving_average_target_updates,
    rsi_reversion_target_updates,
)
from .execution_kernels import simulate_target_positions_next_open
from .metrics_kernels import compute_equity_statistics


SIMULATION_NAMESPACE = uuid.UUID("0bf7f6fd-3ca7-57aa-8266-4f22048d8bf8")
SIGNAL_NAMESPACE = uuid.UUID("6d011acb-2b89-5dc5-bd38-fa9f903e6495")

BUILTIN_NUMBA_STRATEGIES = {
    "adx_trend_strength",
    "atr_breakout",
    "bollinger_mean_reversion",
    "donchian_breakout",
    "macd_trend_follow",
    "moving_average_cross",
    "oi_funding_breakout",
    "liquidation_reversal",
    "price_moving_average",
    "rsi_reversion",
    "multi_timeframe_ma_spread",
}


@dataclass(frozen=True)
class NumbaKernelArgSpec:
    """One positional argument for a registered external Numba kernel.

    ``source`` supports:
    - ``series``: read ``name`` from the encoded primary market series
    - ``config``: read ``name`` from raw strategy config, with optional dtype/default
    - ``literal``: pass ``value`` as-is
    """

    source: str
    name: str = ""
    dtype: str = ""
    default: Any = None
    has_default: bool = False
    value: Any = None


@dataclass(frozen=True)
class NumbaKernelSpec:
    """Declarative adapter for externally registered Numba strategy kernels.

    The kernel must return ``(target_updates, strengths)`` arrays with the same
    length as the primary market series. Prefer ``arg_map`` for new strategies:
    it declares the exact positional arguments passed to ``kernel_fn``. The
    older ``input_fields`` + ``param_names`` form remains supported.
    """

    strategy_id: str
    kernel_fn: Callable
    input_fields: Tuple[str, ...]
    param_names: Tuple[str, ...] = ()
    arg_map: Tuple[NumbaKernelArgSpec, ...] = ()


@dataclass
class EncodedSeries:
    timestamps: np.ndarray
    open_times: np.ndarray
    opens: np.ndarray
    highs: np.ndarray
    lows: np.ndarray
    closes: np.ndarray
    volumes: np.ndarray
    quote_volumes: np.ndarray
    oi_change_bps: np.ndarray
    funding_rate_bps: np.ndarray
    long_liq_notional_usd: np.ndarray
    short_liq_notional_usd: np.ndarray

class NumbaBacktestRunner:
    _custom_kernels: ClassVar[Dict[str, NumbaKernelSpec]] = {}

    @classmethod
    def register_kernel(
        cls,
        strategy_id: str,
        kernel_fn: Callable,
        *,
        input_fields: Sequence[str] | None = None,
        param_names: Sequence[str] = (),
        arg_map: Sequence[Any] | None = None,
    ) -> NumbaKernelSpec:
        """Register an external Numba-compatible target-update kernel.

        External modules can call this at import time, then use the same
        ``BacktestRequest`` flow with ``plugin_id`` set to ``strategy_id``.
        New strategies should prefer ``arg_map`` so the kernel's exact
        positional arguments can be declared without a wrapper adapter.
        ``input_fields`` + ``param_names`` remains supported for compatibility.
        """
        normalized_strategy_id = str(strategy_id).strip()
        if not normalized_strategy_id:
            raise ValueError("strategy_id is required for custom numba kernels")
        if normalized_strategy_id in BUILTIN_NUMBA_STRATEGIES:
            raise ValueError("cannot register custom numba kernel over built-in strategy '%s'" % normalized_strategy_id)
        if not callable(kernel_fn):
            raise ValueError("kernel_fn must be callable")

        if arg_map is not None:
            normalized_arg_map = cls._normalize_arg_map(arg_map)
            normalized_input_fields = tuple(arg.name for arg in normalized_arg_map if arg.source == "series")
            normalized_param_names = tuple(arg.name for arg in normalized_arg_map if arg.source == "config")
        else:
            normalized_arg_map = ()
            normalized_input_fields = tuple(str(field).strip() for field in (input_fields or ()))
            normalized_param_names = tuple(str(param).strip() for param in param_names)
            if not normalized_input_fields:
                raise ValueError("input_fields must include at least one EncodedSeries field")
            if any(not field for field in normalized_input_fields):
                raise ValueError("input_fields cannot contain blank names")
            if any(not param for param in normalized_param_names):
                raise ValueError("param_names cannot contain blank names")

        spec = NumbaKernelSpec(
            strategy_id=normalized_strategy_id,
            kernel_fn=kernel_fn,
            input_fields=normalized_input_fields,
            param_names=normalized_param_names,
            arg_map=normalized_arg_map,
        )
        cls._custom_kernels[normalized_strategy_id] = spec
        return spec

    @classmethod
    def _normalize_arg_map(cls, arg_map: Sequence[Any]) -> Tuple[NumbaKernelArgSpec, ...]:
        normalized = tuple(cls._normalize_arg_spec(arg) for arg in arg_map)
        if not normalized:
            raise ValueError("arg_map must include at least one kernel argument")
        return normalized

    @classmethod
    def _normalize_arg_spec(cls, arg: Any) -> NumbaKernelArgSpec:
        if isinstance(arg, NumbaKernelArgSpec):
            return cls._validate_arg_spec(arg)

        if isinstance(arg, Mapping):
            source = str(arg.get("source", "")).strip().lower()
            name = str(arg.get("name", arg.get("field", ""))).strip()
            dtype = cls._normalize_dtype(arg.get("dtype", arg.get("type", "")))
            has_default = "default" in arg
            return cls._validate_arg_spec(
                NumbaKernelArgSpec(
                    source=source,
                    name=name,
                    dtype=dtype,
                    default=arg.get("default"),
                    has_default=has_default,
                    value=arg.get("value"),
                )
            )

        if isinstance(arg, tuple):
            if len(arg) < 2:
                raise ValueError("arg_map tuple entries must contain at least source and name/value")
            source = str(arg[0]).strip().lower()
            if source in {"literal", "const", "constant"}:
                return cls._validate_arg_spec(NumbaKernelArgSpec(source="literal", value=arg[1]))
            name = str(arg[1]).strip()
            dtype = cls._normalize_dtype(arg[2]) if len(arg) >= 3 else ""
            has_default = len(arg) >= 4
            default = arg[3] if has_default else None
            return cls._validate_arg_spec(
                NumbaKernelArgSpec(
                    source=source,
                    name=name,
                    dtype=dtype,
                    default=default,
                    has_default=has_default,
                )
            )

        raise ValueError("arg_map entries must be NumbaKernelArgSpec, dict, or tuple")

    @classmethod
    def _validate_arg_spec(cls, arg: NumbaKernelArgSpec) -> NumbaKernelArgSpec:
        source = arg.source.strip().lower()
        if source in {"input", "field"}:
            source = "series"
        elif source in {"param", "params", "parameter"}:
            source = "config"
        elif source in {"const", "constant"}:
            source = "literal"

        if source not in {"series", "config", "literal"}:
            raise ValueError("arg_map source must be 'series', 'config', or 'literal'")
        name = arg.name.strip() if arg.name else ""
        if source in {"series", "config"} and not name:
            raise ValueError("arg_map %s entries must include name/field" % source)

        return NumbaKernelArgSpec(
            source=source,
            name=name,
            dtype=cls._normalize_dtype(arg.dtype),
            default=arg.default,
            has_default=arg.has_default,
            value=arg.value,
        )

    @staticmethod
    def _normalize_dtype(dtype: Any) -> str:
        if dtype in (None, ""):
            return ""
        if dtype is int:
            return "int"
        if dtype is float:
            return "float"
        if dtype is bool:
            return "bool"
        if dtype is str:
            return "str"
        normalized = str(dtype).strip().lower()
        if normalized in {"integer", "int64", "int32"}:
            return "int"
        if normalized in {"float64", "float32", "double"}:
            return "float"
        if normalized in {"boolean"}:
            return "bool"
        if normalized in {"string"}:
            return "str"
        if normalized not in {"", "int", "float", "bool", "str"}:
            raise ValueError("unsupported arg_map dtype '%s'" % dtype)
        return normalized

    @staticmethod
    def _coerce_arg_value(value: Any, dtype: str) -> Any:
        if dtype == "int":
            return int(value)
        if dtype == "float":
            return float(value)
        if dtype == "bool":
            if isinstance(value, str):
                return value.strip().lower() in {"1", "true", "yes", "y", "on"}
            return bool(value)
        if dtype == "str":
            return str(value)
        return value

    @classmethod
    def unregister_kernel(cls, strategy_id: str) -> None:
        cls._custom_kernels.pop(strategy_id, None)

    @classmethod
    def clear_custom_kernels(cls) -> None:
        cls._custom_kernels.clear()

    @classmethod
    def list_custom_kernels(cls) -> Tuple[str, ...]:
        return tuple(sorted(cls._custom_kernels))

    @classmethod
    def registered_kernels(cls) -> Dict[str, NumbaKernelSpec]:
        return dict(cls._custom_kernels)

    def run(
        self,
        *,
        request: BacktestRequest,
        market_bundle: MarketBundle,
    ) -> BacktestResult:
        if not NUMBA_AVAILABLE:
            raise RuntimeError("numba is not installed; install it before using the numba backtest engine")

        strategy_id, raw_config = self._extract_strategy(request)
        series = self._encode_series(
            market_bundle=market_bundle,
            instrument_id=request.instruments[0],
            timeframe=request.primary_timeframe,
        )
        target_updates, strengths = self._build_signal_targets(
            strategy_id=strategy_id,
            raw_config=raw_config,
            market_bundle=market_bundle,
            primary_series=series,
            instrument_id=request.instruments[0],
        )

        taker_fee_bps = float(request.fee_model.get("taker_fee_bps", request.fee_model.get("commission_bps", 0.0)))
        slippage_bps = float(request.slippage_model.get("slippage_bps", 0.0))
        impact_slippage_bps = float(request.slippage_model.get("impact_slippage_bps", 0.0))
        max_bar_volume_fraction = float(request.slippage_model.get("max_bar_volume_fraction", 0.10))
        contract_multiplier = float(request.extras.get("contract_multiplier", 1.0))
        quantity_step = float(request.extras.get("quantity_step", 0.0))
        min_quantity = float(request.extras.get("min_quantity", 0.0))
        fixed_fee_per_contract = float(request.fee_model.get("fixed_fee_per_contract", 0.0))
        funding_rate_per_bar = float(request.fee_model.get("funding_rate_per_bar", 0.0))
        if "funding_bps_per_bar" in request.fee_model:
            funding_rate_per_bar = float(request.fee_model["funding_bps_per_bar"]) / 10_000.0

        (
            equity_values,
            cash_values,
            position_values,
            trade_actions,
            trade_quantities,
            trade_prices,
            trade_fee_values,
            funding_fee_values,
        ) = simulate_target_positions_next_open(
            series.opens,
            series.closes,
            series.volumes,
            series.quote_volumes,
            target_updates,
            int(TARGET_KEEP),
            float(request.initial_capital),
            taker_fee_bps,
            slippage_bps,
            impact_slippage_bps,
            funding_rate_per_bar,
            max_bar_volume_fraction,
            contract_multiplier,
            quantity_step,
            min_quantity,
            fixed_fee_per_contract,
        )

        trade_rows = self._build_trade_rows(
            request=request,
            series=series,
            target_updates=target_updates,
            trade_actions=trade_actions,
            trade_quantities=trade_quantities,
            trade_prices=trade_prices,
            trade_fee_values=trade_fee_values,
            position_values=position_values,
        )
        signal_batches = self._build_signal_batches(
            request=request,
            series=series,
            strategy_id=strategy_id,
            raw_config=raw_config,
            target_updates=target_updates,
            strengths=strengths,
        )

        initial = float(request.initial_capital)
        final_equity = float(equity_values[-1]) if len(equity_values) else initial
        total_return = (final_equity - initial) / initial if initial else 0.0
        drawdowns, max_drawdown, mean_bar_return, bar_return_volatility, sharpe_ratio = compute_equity_statistics(
            equity_values,
            self._periods_per_year(request.primary_timeframe),
        )
        equity_curve = self._build_equity_curve(series.timestamps, equity_values, cash_values, drawdowns)
        run_id = str(
            uuid.uuid5(
                SIMULATION_NAMESPACE,
                "%s|%s|%s|%s|numba"
                % (request.request_id, request.start_ts, request.end_ts, len(series.timestamps)),
            )
        )

        return BacktestResult(
            request_id=request.request_id,
            total_return=float(total_return),
            equity_curve=equity_curve,
            metrics={
                "snapshot_count": float(len(series.timestamps)),
                "trade_count": float(len(trade_rows)),
                "signal_count": float(len(signal_batches)),
                "final_equity": float(final_equity),
                "total_return": float(total_return),
                "max_drawdown": float(max_drawdown),
                "sharpe_ratio": float(sharpe_ratio),
                "mean_bar_return": float(mean_bar_return),
                "bar_return_volatility": float(bar_return_volatility),
                "ending_position_qty": float(position_values[-1]) if len(position_values) else 0.0,
            },
            signal_batches=signal_batches,
            extras={
                "run_id": run_id,
                "engine": "numba",
                "execution_assumption": "signal_at_bar_close_fill_next_bar_open",
                "trades": trade_rows,
                "liquidity_model": {
                    "max_bar_volume_fraction": max_bar_volume_fraction,
                    "quote_volume_used": True,
                    "contract_multiplier": contract_multiplier,
                    "quantity_step": quantity_step,
                    "min_quantity": min_quantity,
                },
                "fee_model": {
                    "taker_fee_bps": taker_fee_bps,
                    "fixed_fee_per_contract": fixed_fee_per_contract,
                    "funding_rate_per_bar": funding_rate_per_bar,
                    "total_funding_fees": float(np.sum(funding_fee_values)),
                },
                "slippage_model": {
                    "slippage_bps": slippage_bps,
                    "impact_slippage_bps": impact_slippage_bps,
                },
            },
        )

    def _extract_strategy(self, request: BacktestRequest) -> Tuple[str, dict]:
        plugin_chain = request.signal_pipeline.plugin_chain
        if len(plugin_chain) != 1:
            raise ValueError("numba backtest runner currently supports exactly one signal plugin")
        strategy_id = plugin_chain[0]["plugin_id"]
        raw_config = dict(plugin_chain[0].get("config", {}))
        if strategy_id not in BUILTIN_NUMBA_STRATEGIES and strategy_id not in self._custom_kernels:
            raise ValueError(
                "numba backtest runner does not support strategy '%s' yet; "
                "register external kernels with NumbaBacktestRunner.register_kernel(...)" % strategy_id
            )
        return strategy_id, raw_config

    def _encode_series(self, *, market_bundle: MarketBundle, instrument_id: str, timeframe: str) -> EncodedSeries:
        key = market_bundle.key(instrument_id, timeframe)
        bars = sorted(
            [bar for bar in market_bundle.bars.get(key, []) if bar.confirmed],
            key=lambda bar: bar.timestamp,
        )
        if not bars:
            raise ValueError("no confirmed bars found for %s" % key)

        timestamps = np.asarray([int(bar.timestamp) for bar in bars], dtype=np.int64)
        open_times = np.asarray(
            [int(bar.extras.get("open_time", bar.timestamp)) for bar in bars],
            dtype=np.int64,
        )
        opens = np.asarray([float(bar.open) for bar in bars], dtype=np.float64)
        highs = np.asarray([float(bar.high) for bar in bars], dtype=np.float64)
        lows = np.asarray([float(bar.low) for bar in bars], dtype=np.float64)
        closes = np.asarray([float(bar.close) for bar in bars], dtype=np.float64)
        volumes = np.asarray([float(bar.volume) for bar in bars], dtype=np.float64)
        quote_volumes = np.asarray(
            [
                float(bar.quote_volume)
                if bar.quote_volume is not None
                else float(bar.close * bar.volume)
                for bar in bars
            ],
            dtype=np.float64,
        )
        oi_change_bps = np.asarray(
            [
                float(bar.extras.get("oi_change_bps"))
                if bar.extras.get("oi_change_bps") is not None
                else np.nan
                for bar in bars
            ],
            dtype=np.float64,
        )
        funding_rate_bps = np.asarray(
            [
                float(bar.extras.get("funding_rate_bps"))
                if bar.extras.get("funding_rate_bps") is not None
                else np.nan
                for bar in bars
            ],
            dtype=np.float64,
        )
        long_liq_notional_usd = np.asarray(
            [
                float(bar.extras.get("long_liq_notional_usd"))
                if bar.extras.get("long_liq_notional_usd") is not None
                else 0.0
                for bar in bars
            ],
            dtype=np.float64,
        )
        short_liq_notional_usd = np.asarray(
            [
                float(bar.extras.get("short_liq_notional_usd"))
                if bar.extras.get("short_liq_notional_usd") is not None
                else 0.0
                for bar in bars
            ],
            dtype=np.float64,
        )
        return EncodedSeries(
            timestamps=timestamps,
            open_times=open_times,
            opens=opens,
            highs=highs,
            lows=lows,
            closes=closes,
            volumes=volumes,
            quote_volumes=quote_volumes,
            oi_change_bps=oi_change_bps,
            funding_rate_bps=funding_rate_bps,
            long_liq_notional_usd=long_liq_notional_usd,
            short_liq_notional_usd=short_liq_notional_usd,
        )

    def _build_signal_targets(
        self,
        *,
        strategy_id: str,
        raw_config: dict,
        market_bundle: MarketBundle,
        primary_series: EncodedSeries,
        instrument_id: str,
    ) -> Tuple[np.ndarray, np.ndarray]:
        if strategy_id == "donchian_breakout":
            return donchian_breakout_target_updates(
                primary_series.closes,
                primary_series.highs,
                primary_series.lows,
                int(raw_config["lookback_window"]),
                float(raw_config.get("breakout_buffer_bps", 0.0)),
            )
        if strategy_id == "oi_funding_breakout":
            return oi_funding_breakout_target_updates(
                primary_series.closes,
                primary_series.highs,
                primary_series.lows,
                primary_series.oi_change_bps,
                primary_series.funding_rate_bps,
                int(raw_config["lookback_window"]),
                float(raw_config.get("breakout_buffer_bps", 0.0)),
                float(raw_config.get("oi_threshold_bps", 0.0)),
                float(raw_config.get("max_funding_rate_bps", 100.0)),
            )
        if strategy_id == "liquidation_reversal":
            return liquidation_reversal_target_updates(
                primary_series.long_liq_notional_usd,
                primary_series.short_liq_notional_usd,
                float(raw_config.get("long_liquidation_threshold_usd", 100_000.0)),
                float(raw_config.get("short_liquidation_threshold_usd", 100_000.0)),
                float(raw_config.get("liquidation_imbalance_ratio", 0.60)),
            )
        if strategy_id == "adx_trend_strength":
            return adx_trend_strength_target_updates(
                primary_series.closes,
                primary_series.highs,
                primary_series.lows,
                int(raw_config["period"]),
                float(raw_config.get("adx_threshold", 25.0)),
            )
        if strategy_id == "atr_breakout":
            return atr_breakout_target_updates(
                primary_series.closes,
                primary_series.highs,
                primary_series.lows,
                int(raw_config["ma_period"]),
                int(raw_config["atr_period"]),
                float(raw_config.get("atr_multiplier", 2.0)),
            )
        if strategy_id == "bollinger_mean_reversion":
            return bollinger_mean_reversion_target_updates(
                primary_series.closes,
                int(raw_config["period"]),
                float(raw_config.get("stddev_multiplier", 2.0)),
            )
        if strategy_id == "macd_trend_follow":
            return macd_trend_follow_target_updates(
                primary_series.closes,
                int(raw_config["fast_period"]),
                int(raw_config["slow_period"]),
                int(raw_config["signal_period"]),
                float(raw_config.get("histogram_threshold", 0.0)),
            )
        if strategy_id == "moving_average_cross":
            return moving_average_cross_target_updates(
                primary_series.closes,
                int(raw_config["fast_window"]),
                int(raw_config["slow_window"]),
                float(raw_config.get("entry_threshold", 0.0)),
            )
        if strategy_id == "price_moving_average":
            return price_moving_average_target_updates(
                primary_series.closes,
                int(raw_config["period"]),
                float(raw_config.get("entry_threshold", 0.0)),
            )
        if strategy_id == "rsi_reversion":
            return rsi_reversion_target_updates(
                primary_series.closes,
                int(raw_config["period"]),
                float(raw_config["oversold"]),
                float(raw_config["overbought"]),
            )

        if strategy_id == "multi_timeframe_ma_spread":
            secondary_key = market_bundle.key(instrument_id, str(raw_config["reference_timeframe"]))
            secondary_bars = sorted(
                [bar for bar in market_bundle.bars.get(secondary_key, []) if bar.confirmed],
                key=lambda bar: bar.timestamp,
            )
            if not secondary_bars:
                raise ValueError("no confirmed secondary bars found for %s" % secondary_key)
            secondary_timestamps = np.asarray([int(bar.timestamp) for bar in secondary_bars], dtype=np.int64)
            secondary_closes = np.asarray([float(bar.close) for bar in secondary_bars], dtype=np.float64)
            return multi_timeframe_ma_spread_target_updates(
                primary_series.timestamps,
                primary_series.closes,
                secondary_timestamps,
                secondary_closes,
                int(raw_config["primary_ma_period"]),
                int(raw_config["reference_ma_period"]),
                float(raw_config.get("spread_threshold_bps", 0.0)),
            )

        if strategy_id in self._custom_kernels:
            return self._build_custom_signal_targets(
                strategy_id=strategy_id,
                raw_config=raw_config,
                primary_series=primary_series,
            )

        raise ValueError("unsupported numba strategy '%s'" % strategy_id)

    def _build_custom_signal_targets(
        self,
        *,
        strategy_id: str,
        raw_config: dict,
        primary_series: EncodedSeries,
    ) -> Tuple[np.ndarray, np.ndarray]:
        spec = self._custom_kernels[strategy_id]
        if spec.arg_map:
            kernel_args = self._build_custom_kernel_args_from_arg_map(
                strategy_id=strategy_id,
                spec=spec,
                raw_config=raw_config,
                primary_series=primary_series,
            )
        else:
            kernel_args = []
            for field_name in spec.input_fields:
                if not hasattr(primary_series, field_name):
                    raise ValueError(
                        "custom numba strategy '%s' requested unknown input field '%s'" % (strategy_id, field_name)
                    )
                kernel_args.append(getattr(primary_series, field_name))

            for param_name in spec.param_names:
                if param_name not in raw_config:
                    raise ValueError(
                        "custom numba strategy '%s' missing required config parameter '%s'" % (strategy_id, param_name)
                    )
                kernel_args.append(raw_config[param_name])

        result = spec.kernel_fn(*kernel_args)
        if not isinstance(result, tuple) or len(result) != 2:
            raise ValueError("custom numba strategy '%s' must return (target_updates, strengths)" % strategy_id)

        target_updates = np.asarray(result[0], dtype=np.int8)
        strengths = np.asarray(result[1], dtype=np.float64)
        expected_length = primary_series.closes.shape[0]
        if target_updates.shape[0] != expected_length or strengths.shape[0] != expected_length:
            raise ValueError(
                "custom numba strategy '%s' returned arrays with invalid lengths: expected %s" % (
                    strategy_id,
                    expected_length,
                )
            )
        return target_updates, strengths

    def _build_custom_kernel_args_from_arg_map(
        self,
        *,
        strategy_id: str,
        spec: NumbaKernelSpec,
        raw_config: dict,
        primary_series: EncodedSeries,
    ) -> List[Any]:
        kernel_args: List[Any] = []
        for arg in spec.arg_map:
            if arg.source == "series":
                if not hasattr(primary_series, arg.name):
                    raise ValueError(
                        "custom numba strategy '%s' requested unknown input field '%s'" % (strategy_id, arg.name)
                    )
                value = getattr(primary_series, arg.name)
            elif arg.source == "config":
                if arg.name in raw_config:
                    value = raw_config[arg.name]
                elif arg.has_default:
                    value = arg.default
                else:
                    raise ValueError(
                        "custom numba strategy '%s' missing required config parameter '%s'" % (strategy_id, arg.name)
                    )
                value = self._coerce_arg_value(value, arg.dtype)
            elif arg.source == "literal":
                value = self._coerce_arg_value(arg.value, arg.dtype)
            else:
                raise ValueError("custom numba strategy '%s' has unsupported arg source '%s'" % (strategy_id, arg.source))
            kernel_args.append(value)
        return kernel_args

    def _build_trade_rows(
        self,
        *,
        request: BacktestRequest,
        series: EncodedSeries,
        target_updates: np.ndarray,
        trade_actions: np.ndarray,
        trade_quantities: np.ndarray,
        trade_prices: np.ndarray,
        trade_fee_values: np.ndarray,
        position_values: np.ndarray,
    ) -> List[Dict]:
        instrument_id = request.instruments[0]
        trades: List[Dict] = []
        for index, action in enumerate(trade_actions):
            if action == 0:
                continue
            signal_bar_index = index - 1
            if signal_bar_index < 0:
                continue
            side = TradeSide.BUY if action > 0 else TradeSide.SELL
            signal_id = str(
                uuid.uuid5(
                    SIGNAL_NAMESPACE,
                    "%s|%s|%s|%s"
                    % (
                        request.request_id,
                        instrument_id,
                        int(series.timestamps[signal_bar_index]),
                        side.value,
                    ),
                )
            )
            post_position = float(position_values[index])
            if action > 0:
                pre_position = post_position - float(trade_quantities[index])
            else:
                pre_position = post_position + float(trade_quantities[index])
            action_label = "rebalance"
            if pre_position == 0.0 and post_position > 0.0:
                action_label = "open_long"
            elif pre_position == 0.0 and post_position < 0.0:
                action_label = "open_short"
            elif pre_position > 0.0 and post_position == 0.0:
                action_label = "close_long"
            elif pre_position < 0.0 and post_position == 0.0:
                action_label = "cover_short"
            elif pre_position < 0.0 and post_position > 0.0:
                action_label = "flip_to_long"
            elif pre_position > 0.0 and post_position < 0.0:
                action_label = "flip_to_short"
            trades.append(
                {
                    "timestamp": int(series.open_times[index]),
                    "decision_timestamp": int(series.timestamps[signal_bar_index]),
                    "instrument_id": instrument_id,
                    "side": side.value,
                    "price": float(trade_prices[index]),
                    "quantity": float(trade_quantities[index]),
                    "fee": float(trade_fee_values[index]),
                    "signal_id": signal_id,
                    "action": action_label,
                    "execution_model": "next_open",
                    "target_position": int(target_updates[signal_bar_index]) if signal_bar_index >= 0 else None,
                    "post_trade_position_qty": post_position,
                }
            )
        return trades

    def _build_signal_batches(
        self,
        *,
        request: BacktestRequest,
        series: EncodedSeries,
        strategy_id: str,
        raw_config: dict,
        target_updates: np.ndarray,
        strengths: np.ndarray,
    ) -> List[SignalBatch]:
        batches: List[SignalBatch] = []
        instrument_id = request.instruments[0]
        config_hash = "|".join("%s=%s" % (key, raw_config[key]) for key in sorted(raw_config))

        for index, target_update in enumerate(target_updates):
            if target_update == TARGET_KEEP:
                continue
            side = TradeSide.BUY if target_update == TARGET_LONG else TradeSide.SELL
            signal_id = str(
                uuid.uuid5(
                    SIGNAL_NAMESPACE,
                    "%s|%s|%s|%s"
                    % (
                        request.request_id,
                        instrument_id,
                        int(series.timestamps[index]),
                        side.value,
                    ),
                )
            )
            batch_id = str(
                uuid.uuid5(
                    SIGNAL_NAMESPACE,
                    "%s|%s|%s"
                    % (strategy_id, request.request_id, int(series.timestamps[index])),
                )
            )
            next_open_time = int(series.open_times[index + 1]) if index + 1 < len(series.open_times) else None
            signal = SignalEnvelope(
                version="numba/v1",
                signal_id=signal_id,
                kind=SignalKind.TRADE,
                instrument_id=instrument_id,
                side=side,
                strength=float(strengths[index]),
                time_horizon="swing",
                valid_until=int(series.timestamps[index]),
                payload={
                    "bar_timestamp": int(series.timestamps[index]),
                    "decision_price": float(series.closes[index]),
                    "execute_at_open_time": next_open_time,
                    "execution_model": "next_open",
                    "target_position": int(target_update),
                },
                provenance=SignalProvenance(
                    plugin_id=strategy_id,
                    plugin_version="numba/v1",
                    config_hash=config_hash,
                    input_fingerprint=request.request_id,
                ),
            )
            batches.append(
                SignalBatch(
                    signals=[signal],
                    batch_id=batch_id,
                    created_at=int(series.timestamps[index]),
                )
            )
        return batches

    def _periods_per_year(self, timeframe: str) -> float:
        if not timeframe or len(timeframe) < 2:
            return 0.0
        unit = timeframe[-1]
        try:
            size = float(timeframe[:-1])
        except ValueError:
            return 0.0
        if size <= 0.0:
            return 0.0
        if unit == "m":
            return 365.0 * 24.0 * 60.0 / size
        if unit == "h":
            return 365.0 * 24.0 / size
        if unit == "d":
            return 365.0 / size
        if unit == "w":
            return 365.0 / (7.0 * size)
        if unit == "M":
            return 12.0 / size
        return 0.0

    def _build_equity_curve(
        self,
        timestamps: np.ndarray,
        equity_values: np.ndarray,
        cash_values: np.ndarray,
        drawdowns: np.ndarray,
    ) -> List[EquityPoint]:
        if len(timestamps) == 0:
            return []
        points: List[EquityPoint] = []
        for index, timestamp in enumerate(timestamps):
            equity = float(equity_values[index])
            cash = float(cash_values[index])
            points.append(
                EquityPoint(
                    timestamp=int(timestamp),
                    equity=equity,
                    cash=cash,
                    drawdown=float(drawdowns[index]) if index < len(drawdowns) else 0.0,
                )
            )
        return points
