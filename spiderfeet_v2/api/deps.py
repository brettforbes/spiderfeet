"""FastAPI dependencies for v2 stores (overridable in tests)."""

from __future__ import annotations

from typing import Optional

from spiderfeet_v2.db.config import TypeDBConnectionConfig, load_connection_config
from spiderfeet_v2.db.crud import CrudStore
from spiderfeet_v2.db.projections import ProjectionStore

# Test / DI override hooks (set to a store instance or factory).
_crud_override: Optional[CrudStore] = None
_projection_override: Optional[ProjectionStore] = None


def set_crud_store(store: Optional[CrudStore]) -> None:
    global _crud_override
    _crud_override = store


def set_projection_store(store: Optional[ProjectionStore]) -> None:
    global _projection_override
    _projection_override = store


def get_crud_store() -> CrudStore:
    if _crud_override is not None:
        return _crud_override
    return CrudStore.connect(load_connection_config())


def get_projection_store() -> ProjectionStore:
    if _projection_override is not None:
        return _projection_override
    return ProjectionStore.connect(load_connection_config())


def connection_config() -> TypeDBConnectionConfig:
    return load_connection_config()
