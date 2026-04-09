"""
Interfaces for runtime / monitor orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Protocol

from ..core import DataQuery, MonitorTrigger, RunSummary, SignalContext, SignalPipelineSpec


@dataclass
class RunContext:
    run_id: str
    trigger: MonitorTrigger
    data_query: DataQuery
    signal_pipeline: Optional[SignalPipelineSpec] = None
    signal_context: SignalContext = field(default_factory=SignalContext)
    dry_run: bool = True
    extras: Dict[str, object] = field(default_factory=dict)


class Runner(Protocol):
    def run(self, context: RunContext) -> RunSummary:
        ...


class TriggerAdapter(Protocol):
    def build_context(self, trigger: MonitorTrigger) -> RunContext:
        ...
