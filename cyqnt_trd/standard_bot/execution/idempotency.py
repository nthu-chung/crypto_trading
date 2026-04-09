"""
Helpers for execution idempotency.
"""

from __future__ import annotations

import hashlib


def build_client_tag(run_id: str, intent_id: str, *, prefix: str = "stdbot") -> str:
    """
    Build a deterministic Binance-safe client order id.
    """

    run_part = run_id.replace("-", "")[:8]
    digest = hashlib.sha256(("%s|%s" % (run_id, intent_id)).encode("utf-8")).hexdigest()[:16]
    return ("%s-%s-%s" % (prefix, run_part, digest))[:36]
