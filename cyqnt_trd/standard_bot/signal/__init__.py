"""
Signal layer exports for the standard bot architecture.
"""

from .interfaces import (
    BatchSignalPlugin,
    IncrementalSignalPlugin,
    SignalComposer,
    SignalPlugin,
    SignalState,
    StepSignalResult,
)
from .encoders import EncodedCloseSeries, encode_close_series, series_for
from .numba_kernels import NUMBA_AVAILABLE
from .plugins import (
    DonchianBreakoutConfig,
    DonchianBreakoutPlugin,
    MovingAverageCrossConfig,
    MovingAverageCrossPlugin,
    MultiTimeframeMaSpreadConfig,
    MultiTimeframeMaSpreadPlugin,
    PriceMovingAverageConfig,
    PriceMovingAveragePlugin,
    RsiReversionConfig,
    RsiReversionPlugin,
    register_builtin_plugins,
)
from .registry import PipelineStepResult, SignalPluginRegistry

__all__ = [
    "BatchSignalPlugin",
    "DonchianBreakoutConfig",
    "DonchianBreakoutPlugin",
    "EncodedCloseSeries",
    "IncrementalSignalPlugin",
    "MovingAverageCrossConfig",
    "MovingAverageCrossPlugin",
    "MultiTimeframeMaSpreadConfig",
    "MultiTimeframeMaSpreadPlugin",
    "NUMBA_AVAILABLE",
    "PipelineStepResult",
    "PriceMovingAverageConfig",
    "PriceMovingAveragePlugin",
    "RsiReversionConfig",
    "RsiReversionPlugin",
    "SignalComposer",
    "SignalPlugin",
    "SignalPluginRegistry",
    "SignalState",
    "StepSignalResult",
    "encode_close_series",
    "register_builtin_plugins",
    "series_for",
]
