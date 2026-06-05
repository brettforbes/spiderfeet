"""Load injectable TypeDB connection settings from JSON."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from spiderfeet.map.constants import DEFAULT_CONFIG_PATH, EXAMPLE_CONFIG_PATH


class TypeDBConfigError(Exception):
    """Connection config is missing or invalid."""


@dataclass(frozen=True)
class TypeDBConnectionConfig:
    """Operator-supplied TypeDB connection (no secrets in repo)."""

    addresses: Union[str, List[str]]
    username: str
    password: str
    database: str
    tls_enabled: bool = False
    root_ca_path: Optional[str] = None

    @classmethod
    def from_dict(cls, raw: Dict[str, Any]) -> "TypeDBConnectionConfig":
        addresses = raw.get("addresses", raw.get("address", "127.0.0.1:1729"))
        username = raw.get("username", "admin")
        password = raw.get("password", "")
        if not password:
            raise TypeDBConfigError("password is required in TypeDB connection config")
        database = raw.get("database", raw.get("database_name", "spiderfeet-map"))
        tls = raw.get("tls", {}) or {}
        tls_enabled = bool(tls.get("enabled", raw.get("tls_enabled", False)))
        root_ca_path = tls.get("root_ca_path") or raw.get("root_ca_path")
        return cls(
            addresses=addresses,
            username=username,
            password=password,
            database=str(database),
            tls_enabled=tls_enabled,
            root_ca_path=root_ca_path,
        )


def resolve_config_path(path: Optional[Path] = None) -> Path:
    """Resolve config file: explicit path, env override, or default."""
    if path is not None:
        return path
    env_path = os.environ.get("SPIDERFEET_TYPEDB_CONFIG")
    if env_path:
        return Path(env_path)
    return DEFAULT_CONFIG_PATH


def load_connection_config(path: Optional[Path] = None) -> TypeDBConnectionConfig:
    """Load connection JSON; raises TypeDBConfigError when missing."""
    config_path = resolve_config_path(path)
    if not config_path.is_file():
        hint = (
            f"Copy {EXAMPLE_CONFIG_PATH.name} to {config_path.name} "
            f"(or set SPIDERFEET_TYPEDB_CONFIG)."
        )
        raise TypeDBConfigError(f"TypeDB config not found: {config_path}. {hint}")
    with config_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise TypeDBConfigError(f"Expected JSON object in {config_path}")
    return TypeDBConnectionConfig.from_dict(data)
