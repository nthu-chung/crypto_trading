"""Packaged strategy case bundles for cyqnt-trd.

These bundles are lightweight reference assets that travel with the package:
- a catalog of curated strategy cases
- per-case metadata
- normalized presets that describe how a case maps into standard_bot
- concise READMEs for humans and agents

They are intentionally separate from executable plugins. Some cases already map
well to current standard_bot plugins, while others remain conceptual bundles
that still need dedicated implementation work.
"""

from __future__ import annotations

import json
import pkgutil
from typing import Dict, List


def _load_bytes(relative_path: str) -> bytes:
    data = pkgutil.get_data(__name__, relative_path)
    if data is None:
        raise FileNotFoundError("Packaged strategy case asset not found: %s" % relative_path)
    return data


def _load_json(relative_path: str) -> Dict[str, object]:
    return json.loads(_load_bytes(relative_path).decode("utf-8"))


def _load_text(relative_path: str) -> str:
    return _load_bytes(relative_path).decode("utf-8")


def load_catalog() -> Dict[str, object]:
    """Load the packaged strategy case catalog."""
    return _load_json("catalog.json")


def list_case_ids() -> List[str]:
    """Return curated case ids in stable catalog order."""
    catalog = load_catalog()
    return [entry["case_id"] for entry in catalog.get("cases", [])]


def load_case(case_id: str) -> Dict[str, object]:
    """Load structured metadata for a packaged strategy case."""
    return _load_json("cases/%s/case.json" % case_id)


def load_case_preset(case_id: str) -> Dict[str, object]:
    """Load the packaged preset for a strategy case."""
    return _load_json("cases/%s/preset.json" % case_id)


def load_case_readme(case_id: str) -> str:
    """Load the human-readable README for a strategy case."""
    return _load_text("cases/%s/README.md" % case_id)


__all__ = [
    "list_case_ids",
    "load_catalog",
    "load_case",
    "load_case_preset",
    "load_case_readme",
]
