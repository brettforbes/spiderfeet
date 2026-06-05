"""Tests tab catalog API (Stage 4 — R2-04-03 / R2-04-04)."""

from __future__ import annotations

from typing import Dict, List, Optional

from typedb.common.exception import TypeDBDriverException

from spiderfeet.api.schemas import (
    RouteCatalogItem,
    TestsModuleDetail,
    TestsModuleSummary,
    TestsSummaryResponse,
)
from spiderfeet.map.config import load_connection_config
from spiderfeet.map.connection import driver_session, ping
from spiderfeet.map.route_states import fetch_route_states, overlay_route_state
from spiderfeet.map.routes_catalog import (
    catalog_summary,
    list_module_summaries,
    module_catalog,
)


def _typedb_route_states() -> Optional[Dict[str, str]]:
    cfg = load_connection_config()
    if not ping(cfg):
        return None
    try:
        with driver_session(cfg) as driver:
            return fetch_route_states(driver, cfg.database)
    except TypeDBDriverException:
        return None


def _state_counts(states: Optional[Dict[str, str]], route_count: int) -> Dict[str, int]:
    if not states:
        return {
            "not_started": route_count,
            "in_test": 0,
            "favourite": 0,
            "unique": 0,
            "error": 0,
            "dominated": 0,
        }
    counts = {
        "not_started": 0,
        "in_test": 0,
        "favourite": 0,
        "unique": 0,
        "error": 0,
        "dominated": 0,
    }
    known = set(states.values())
    for state in known:
        key = state.replace("-", "_")
        if key in counts:
            counts[key] = sum(1 for v in states.values() if v == state)
    counted = sum(counts.values()) - counts["not_started"]
    counts["not_started"] = max(0, route_count - counted)
    return counts


def tests_summary() -> TestsSummaryResponse:
    summary = catalog_summary()
    states = _typedb_route_states()
    state_counts = _state_counts(states, summary["route_count"])
    return TestsSummaryResponse(
        module_count=summary["module_count"],
        route_count=summary["route_count"],
        consumption_group_count=summary["consumption_group_count"],
        typedb_connected=states is not None,
        route_states=state_counts,
    )


def list_modules(
    *,
    search: Optional[str] = None,
    consumption_group: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> List[TestsModuleSummary]:
    modules = list_module_summaries(
        search=search,
        consumption_group=consumption_group,
    )
    page = modules[offset : offset + limit]
    states = _typedb_route_states()
    return [
        TestsModuleSummary(
            module_id=m.module_id,
            name=m.name,
            summary=m.summary,
            consumption_group=m.consumption_group,
            access_tier=m.access_tier,
            route_count=m.route_count,
            routes_tested=_count_tested_routes(m.module_id, states),
        )
        for m in page
    ]


def _count_tested_routes(module_id: str, states: Optional[Dict[str, str]]) -> int:
    if not states:
        return 0
    suffix = f"-via-{module_id}"
    return sum(
        1
        for name, state in states.items()
        if name.endswith(suffix) and state != "not-started"
    )


def get_module(module_id: str) -> Optional[TestsModuleDetail]:
    catalog = module_catalog(module_id)
    if catalog is None:
        return None
    states = _typedb_route_states()
    routes = [
        RouteCatalogItem(
            route_name=r.route_name,
            consumed_nugget_id=r.consumed_nugget_id,
            produced_nugget_id=r.produced_nugget_id,
            route_state=overlay_route_state(r.route_name, states),
        )
        for r in catalog.routes
    ]
    return TestsModuleDetail(
        module_id=catalog.module_id,
        name=catalog.name,
        summary=catalog.summary,
        consumption_group=catalog.consumption_group,
        access_tier=catalog.access_tier,
        route_seed_nugget=catalog.route_seed_nugget,
        route_count=len(routes),
        routes=routes,
    )
