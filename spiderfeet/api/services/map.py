"""Map API service layer (TypeDB read + bootstrap)."""

from __future__ import annotations

import logging
from typing import List, Optional, Union

from typedb.common.exception import TypeDBDriverException

from spiderfeet.api.schemas import (
    ForceGraphLinkModel,
    ForceGraphNodeModel,
    MapBootstrapResponse,
    MapConnectionInfo,
    MapConnectionPingResponse,
    MapForceGraphResponse,
    MapStatusResponse,
)
from spiderfeet.map.bootstrap import BootstrapReport, bootstrap_map, ensure_map_ready
from spiderfeet.map.config import TypeDBConfigError, load_connection_config
from spiderfeet.map.connection import database_exists, driver_session, ping
from spiderfeet.map.read import export_force_graph, get_inventory

logger = logging.getLogger(__name__)


def _addresses_list(addresses: Union[str, List[str]]) -> List[str]:
    if isinstance(addresses, str):
        return [addresses]
    return list(addresses)


def connection_info() -> MapConnectionInfo:
    cfg = load_connection_config()
    return MapConnectionInfo(
        database=cfg.database,
        addresses=_addresses_list(cfg.addresses),
        username=cfg.username,
        tls_enabled=cfg.tls_enabled,
        configured=True,
    )


def ping_connection() -> MapConnectionPingResponse:
    cfg = load_connection_config()
    return MapConnectionPingResponse(reachable=ping(cfg), database=cfg.database)


def map_status(*, auto_bootstrap: bool = True) -> MapStatusResponse:
    """Server connectivity plus map database readiness.

    ``reachable`` / ``server_reachable`` reflect the TypeDB server only.
    When the server is up but the map DB is missing, has no schema, or has no
    seed catalogue, bootstrap runs idempotently (same as ``POST /map/bootstrap``).
    """
    cfg = load_connection_config()
    server_reachable = ping(cfg)
    database_ready = False
    inventory = None
    bootstrapped = False

    if server_reachable and auto_bootstrap:
        try:
            bootstrapped = ensure_map_ready(cfg)
        except Exception as exc:
            logger.warning("Map auto-bootstrap failed: %s", exc)

    if server_reachable and database_exists(cfg):
        try:
            with driver_session(cfg) as driver:
                inv = get_inventory(driver, cfg.database)
            inventory = {
                "nugget_count": inv.nugget_count,
                "service_count": inv.service_count,
                "link_count": inv.link_count,
            }
            database_ready = inv.nugget_count > 0 and inv.service_count > 0
        except TypeDBDriverException:
            database_ready = False

    return MapStatusResponse(
        database=cfg.database,
        reachable=server_reachable,
        server_reachable=server_reachable,
        database_ready=database_ready,
        bootstrapped=bootstrapped,
        inventory=inventory,
    )


def run_bootstrap(*, reset: bool = False) -> MapBootstrapResponse:
    report = bootstrap_map(reset=reset)
    return MapBootstrapResponse.from_report(report)


def force_graph(*, limit_per_role: Optional[int] = None) -> MapForceGraphResponse:
    cfg = load_connection_config()
    if not ping(cfg):
        raise TypeDBConfigError(
            f"TypeDB server unreachable at {cfg.addresses}"
        )
    with driver_session(cfg) as driver:
        graph = export_force_graph(
            driver, cfg.database, limit_per_role=limit_per_role
        )
    return MapForceGraphResponse(
        nodes=[
            ForceGraphNodeModel(
                id=n.id,
                kind=n.kind,
                label=n.label,
                colour=n.colour,
                service_state=n.service_state,
                service_origin=n.service_origin,
                fixture_category=n.fixture_category,
                requires_api_key=n.requires_api_key,
                icon=n.icon,
                fav_icon=n.fav_icon,
            )
            for n in graph.nodes
        ],
        links=[
            ForceGraphLinkModel(source=l.source, target=l.target, role=l.role)
            for l in graph.links
        ],
    )
