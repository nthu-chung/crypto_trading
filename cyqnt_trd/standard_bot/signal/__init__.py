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
from .plugins import (
    MovingAverageCrossConfig,
    MovingAverageCrossPlugin,
    PriceMovingAverageConfig,
    PriceMovingAveragePlugin,
    RsiReversionConfig,
    RsiReversionPlugin,
    register_builtin_plugins,
)
from .registry import PipelineStepResult, SignalPluginRegistry

__all__ = [
    "BatchSignalPlugin",
    "IncrementalSignalPlugin",
    "MovingAverageCrossConfig",
    "MovingAverageCrossPlugin",
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
    "register_builtin_plugins",
]
