"""TypeDB map endpoints (Stage 3b — R2-03-02)."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from spiderfeet.api.schemas import (
    MapBootstrapResponse,
    MapConnectionInfo,
    MapConnectionPingResponse,
    MapForceGraphResponse,
    MapStatusResponse,
)
from spiderfeet.api.services import map as map_service
from spiderfeet.map.config import TypeDBConfigError

router = APIRouter(prefix="/map", tags=["map"])


def _config_error(exc: TypeDBConfigError) -> HTTPException:
    return HTTPException(status_code=503, detail=str(exc))


@router.get("/connection", response_model=MapConnectionInfo)
def get_connection() -> MapConnectionInfo:
    """Return redacted TypeDB connection settings (no password)."""
    try:
        return map_service.connection_info()
    except TypeDBConfigError as exc:
        raise _config_error(exc) from exc


@router.post("/connection/ping", response_model=MapConnectionPingResponse)
def ping_connection() -> MapConnectionPingResponse:
    """Test connectivity to the configured TypeDB server."""
    try:
        return map_service.ping_connection()
    except TypeDBConfigError as exc:
        raise _config_error(exc) from exc


@router.get("/status", response_model=MapStatusResponse)
def map_status() -> MapStatusResponse:
    """Inventory counts and connectivity for spiderfeet-map."""
    try:
        return map_service.map_status()
    except TypeDBConfigError as exc:
        raise _config_error(exc) from exc


@router.post("/bootstrap", response_model=MapBootstrapResponse)
def bootstrap_map(
    reset: bool = Query(
        False,
        description="Drop and recreate the map database (development only)",
    ),
) -> MapBootstrapResponse:
    """Idempotent seed of schema, nuggets, services, and role links."""
    try:
        return map_service.run_bootstrap(reset=reset)
    except TypeDBConfigError as exc:
        raise _config_error(exc) from exc


@router.get("/graph", response_model=MapForceGraphResponse)
def force_graph(
    limit_per_role: Optional[int] = Query(
        None,
        ge=1,
        le=10000,
        description="Cap edges fetched per role (consumed / produced)",
    ),
) -> MapForceGraphResponse:
    """Export map as D3 force-graph nodes and links."""
    try:
        return map_service.force_graph(limit_per_role=limit_per_role)
    except TypeDBConfigError as exc:
        raise _config_error(exc) from exc
