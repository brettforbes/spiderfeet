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
    "CrudStore",
    "CrudError",
    "SubgraphCodecError",
    "store_dual_form",
    "load_dual_form",
    "normalize_graph",
    "graphs_equal",
    "JSON_TO_TYPEQL",
    "TYPEQL_TO_JSON",
    "ProjectionStore",
    "ProjectionError",
    "project_json",
    "workflow_json",
    "scan_step_json",
    "meta_subgraph_json",
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
    if name in ("CrudStore", "CrudError"):
        from spiderfeet_v2.db import crud as _crud

        return getattr(_crud, name)
    if name in (
        "SubgraphCodecError",
        "store_dual_form",
        "load_dual_form",
        "normalize_graph",
        "graphs_equal",
        "JSON_TO_TYPEQL",
        "TYPEQL_TO_JSON",
    ):
        from spiderfeet_v2.db import subgraph_codec as _codec

        return getattr(_codec, name)
    if name in (
        "ProjectionStore",
        "ProjectionError",
        "project_json",
        "workflow_json",
        "scan_step_json",
        "meta_subgraph_json",
    ):
        from spiderfeet_v2.db import projections as _projections

        return getattr(_projections, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
