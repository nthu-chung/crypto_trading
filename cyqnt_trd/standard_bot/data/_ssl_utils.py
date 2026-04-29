"""
Helpers for resolving the CA bundle used by outbound HTTPS requests.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union


_LINUX_SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"


def resolve_ca_bundle() -> Union[str, bool]:
    """
    Resolve the CA bundle for HTTPS requests.

    Resolution order:
    1. Explicit deployment environment variables
    2. Linux system CA bundle
    3. certifi bundle when available
    4. requests default verification behavior
    """

    for env_var in ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "CURL_CA_BUNDLE"):
        value = os.environ.get(env_var, "").strip()
        if value and Path(value).exists():
            return value

    if Path(_LINUX_SYSTEM_CA).exists():
        return _LINUX_SYSTEM_CA

    try:
        import certifi

        return certifi.where()
    except ImportError:  # pragma: no cover - depends on environment packaging
        return True
