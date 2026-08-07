"""TypeDB client + bootstrap for spiderfeet-actual (SPEC-010)."""

from typing import Any

__all__ = [
    "BootstrapReport",
    "bootstrap_actual",
    "ensure_actual_ready",
    "needs_actual_bootstrap",
    "TypeDBConnectionConfig",
    "load_connection_config",
    "open_driver",
    "ping",
    "driver_session",
]


def __getattr__(name: str) -> Any:
    if name in ("BootstrapReport", "bootstrap_actual", "ensure_actual_ready", "needs_actual_bootstrap"):
        from spiderfeet_v2.db import bootstrap as _bootstrap

        return getattr(_bootstrap, name)
    if name in ("TypeDBConnectionConfig", "load_connection_config"):
        from spiderfeet_v2.db import config as _config

        return getattr(_config, name)
    if name in ("open_driver", "ping", "driver_session"):
        from spiderfeet_v2.db import connection as _connection

        return getattr(_connection, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
