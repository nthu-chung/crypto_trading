"""
Signal plugin registry for the standard bot MVP.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ..core import DataSnapshot, SignalBatch, SignalContext
from .interfaces import SignalState, StepSignalResult

REGISTRY_NAMESPACE = uuid.UUID("f9c7f231-6fe5-54a5-ab13-818ee51d4372")


@dataclass
class PipelineStepResult:
    batch: SignalBatch
    states: Dict[str, SignalState]


class SignalPluginRegistry:
    def __init__(self) -> None:
        self._plugins: Dict[str, Any] = {}
        self._config_factories: Dict[str, Callable[[dict], Any]] = {}

    def register(self, plugin: Any, config_factory: Callable[[dict], Any]) -> None:
        if plugin.plugin_id in self._plugins:
            raise ValueError("plugin '%s' is already registered" % plugin.plugin_id)
        self._plugins[plugin.plugin_id] = plugin
        self._config_factories[plugin.plugin_id] = config_factory

    def get(self, plugin_id: str) -> Any:
        if plugin_id not in self._plugins:
            raise KeyError("plugin '%s' is not registered" % plugin_id)
        return self._plugins[plugin_id]

    def make_invocation_key(self, plugin_id: str, config: dict) -> str:
        payload = json.dumps(config, sort_keys=True, separators=(",", ":"))
        return str(uuid.uuid5(REGISTRY_NAMESPACE, "%s|%s" % (plugin_id, payload)))

    def run_pipeline_step(
        self,
        snapshot: DataSnapshot,
        plugin_chain: List[Dict[str, Any]],
        *,
        previous_states: Optional[Dict[str, SignalState]] = None,
        context: Optional[SignalContext] = None,
    ) -> PipelineStepResult:
        previous_states = previous_states or {}
        merged = []
        next_states: Dict[str, SignalState] = {}

        for invocation in plugin_chain:
            plugin_id = invocation["plugin_id"]
            raw_config = invocation.get("config", {})
            plugin = self.get(plugin_id)
            config = self._config_factories[plugin_id](raw_config)
            invocation_key = self.make_invocation_key(plugin_id, raw_config)
            state = previous_states.get(invocation_key, plugin.initialize_state())
            result: StepSignalResult = plugin.step(
                snapshot=snapshot,
                state=state,
                config=config,
                context=context,
            )
            merged.extend(result.signals)
            if result.state is not None:
                next_states[invocation_key] = result.state

        batch_id = str(
            uuid.uuid5(
                REGISTRY_NAMESPACE,
                "%s|step|%s|%s"
                % (
                    snapshot.meta.snapshot_id,
                    ",".join(item["plugin_id"] for item in plugin_chain),
                    len(merged),
                ),
            )
        )
        return PipelineStepResult(
            batch=SignalBatch(signals=merged, batch_id=batch_id, created_at=int(time.time() * 1000)),
            states=next_states,
        )
