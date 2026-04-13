"""
Configuration helpers for the standard bot entrypoints.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


def load_env_file(path: str = ".env", *, override: bool = False) -> Dict[str, str]:
    """
    Load KEY=VALUE pairs from a simple shell-style env file.

    Supports lines such as ``export FOO=bar`` and keeps existing environment
    variables unless ``override=True`` is provided.
    """

    env_path = Path(path)
    loaded: Dict[str, str] = {}
    if not env_path.exists():
        return loaded

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith(("\"", "'")) and value.endswith(("\"", "'")) and len(value) >= 2:
            value = value[1:-1]
        if override or key not in os.environ:
            os.environ[key] = value
        loaded[key] = os.environ[key]

    return loaded


@dataclass
class BinanceTestnetCredentials:
    api_key: str
    api_secret: str

    @classmethod
    def from_env(cls, env_path: str = ".env") -> "BinanceTestnetCredentials":
        load_env_file(env_path)
        api_key = os.getenv("BINANCE_TESTNET_API_KEY", "").strip()
        api_secret = os.getenv("BINANCE_TESTNET_API_SECRET", "").strip()
        if not api_key or not api_secret:
            raise ValueError("BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET are required")
        return cls(api_key=api_key, api_secret=api_secret)


@dataclass
class BinanceMainnetCredentials:
    api_key: str
    api_secret: str

    @classmethod
    def from_env(cls, env_path: str = ".env") -> "BinanceMainnetCredentials":
        load_env_file(env_path)
        api_key = (
            os.getenv("BINANCE_MAINNET_API_KEY", "").strip()
            or os.getenv("BINANCE_API_KEY", "").strip()
        )
        api_secret = (
            os.getenv("BINANCE_MAINNET_API_SECRET", "").strip()
            or os.getenv("BINANCE_SECRET_KEY", "").strip()
        )
        if not api_key or not api_secret:
            raise ValueError(
                "BINANCE_MAINNET_API_KEY/BINANCE_API_KEY and "
                "BINANCE_MAINNET_API_SECRET/BINANCE_SECRET_KEY are required"
            )
        return cls(api_key=api_key, api_secret=api_secret)
