"""Tests tab catalog API (Stage 4 — R2-04-03 / R2-04-04)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from typedb.common.exception import TypeDBDriverException

from spiderfeet.api.schemas import (
    ModuleTestItem,
    TestsModuleDetail,
    TestsModuleSummary,
    TestsPlanItem,
    TestsPlanResponse,
    TestsSummaryResponse,
)
from spiderfeet.map.config import load_connection_config
from spiderfeet.map.connection import driver_session, ping
from spiderfeet.map.route_states import fetch_route_states, overlay_test_state
from spiderfeet.map.routes_catalog import (
    catalog_summary,
    expand_module_tests_for_service,
    list_module_summaries,
    load_osint_services,
    module_catalog,
)
from spiderfeet.map.subscriptions import subscription_status
from spiderfeet.map.test_targets import sample_target_for_module, seed_metadata_for_module


def _configured_modules(runtime_config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return (runtime_config or {}).get("__modules__", {}) or {}


def _service_lookup() -> Dict[str, Dict[str, Any]]:
    return {str(svc.get("module_id") or ""): svc for svc in load_osint_services()}


def _typedb_route_states() -> Optional[Dict[str, str]]:
    cfg = load_connection_config()
    if not ping(cfg):
        return None
    try:
        with driver_session(cfg) as driver:
            return fetch_route_states(driver, cfg.database)
    except TypeDBDriverException:
        return None


def _state_counts(states: Optional[Dict[str, str]], test_count: int) -> Dict[str, int]:
    if not states:
        return {
            "not_started": test_count,
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
    for svc in load_osint_services():
        for test in expand_module_tests_for_service(svc):
            state = overlay_test_state(test.route_names, states)
            key = state.replace("-", "_")
            if key in counts:
                counts[key] += 1
            else:
                counts["not_started"] += 1

    counted = sum(counts.values())
    if counted < test_count:
        counts["not_started"] += test_count - counted
    elif counted > test_count:
        counts["not_started"] = max(0, test_count - (counted - counts["not_started"]))
    return counts


def tests_summary() -> TestsSummaryResponse:
    summary = catalog_summary()
    states = _typedb_route_states()
    state_counts = _state_counts(states, summary["test_count"])
    return TestsSummaryResponse(
        module_count=summary["module_count"],
        test_count=summary["test_count"],
        route_count=summary["route_count"],
        consumption_group_count=summary["consumption_group_count"],
        typedb_connected=states is not None,
        test_states=state_counts,
        route_states=state_counts,
    )


def _count_tests_run(module_id: str, states: Optional[Dict[str, str]]) -> int:
    if not states:
        return 0
    count = 0
    for svc in load_osint_services():
        if svc.get("module_id") != module_id:
            continue
        for test in expand_module_tests_for_service(svc):
            if overlay_test_state(test.route_names, states) != "not-started":
                count += 1
        break
    return count


def list_modules(
    *,
    search: Optional[str] = None,
    consumption_group: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    runtime_config: Optional[Dict[str, Any]] = None,
) -> List[TestsModuleSummary]:
    modules = list_module_summaries(
        search=search,
        consumption_group=consumption_group,
    )
    page = modules[offset : offset + limit]
    states = _typedb_route_states()
    services = _service_lookup()
    configured = _configured_modules(runtime_config)
    return [
        _module_summary_row(m, services, configured, states)
        for m in page
    ]


def _module_summary_row(
    m: Any,
    services: Dict[str, Dict[str, Any]],
    configured: Dict[str, Any],
    states: Optional[Dict[str, str]],
) -> TestsModuleSummary:
    svc = services.get(m.module_id, {})
    tier, requires_key, has_key, _skip = subscription_status(svc, configured)
    return TestsModuleSummary(
        module_id=m.module_id,
        name=m.name,
        summary=m.summary,
        consumption_group=m.consumption_group,
        access_tier=m.access_tier,
        subscription_tier=tier,
        requires_api_key=requires_key,
        has_api_key=has_key,
        test_count=m.test_count,
        route_count=m.route_count,
        tests_run=_count_tests_run(m.module_id, states),
        routes_tested=_count_tests_run(m.module_id, states),
    )


def test_plan(
    *,
    search: Optional[str] = None,
    consumption_group: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
    runtime_config: Optional[Dict[str, Any]] = None,
) -> TestsPlanResponse:
    """Flat executable test list for the current module filter (one API round-trip)."""
    modules = list_module_summaries(
        search=search,
        consumption_group=consumption_group,
    )
    page = modules[offset : offset + limit]
    module_ids = {m.module_id for m in page}
    items: List[TestsPlanItem] = []
    configured = _configured_modules(runtime_config)

    for svc in load_osint_services():
        module_id = svc.get("module_id", "")
        if module_id not in module_ids:
            continue
        route_seed_nugget = svc.get("route_seed_nugget")
        tier, requires_api_key, has_api_key, skip_reason = subscription_status(svc, configured)
        for test in expand_module_tests_for_service(svc):
            meta = seed_metadata_for_module(module_id, test.consumed_nugget_id)
            items.append(
                TestsPlanItem(
                    test_id=test.test_id,
                    module_id=module_id,
                    consumed_nugget_id=test.consumed_nugget_id,
                    input_value=sample_target_for_module(
                        module_id,
                        test.consumed_nugget_id,
                        route_seed_nugget,
                    ),
                    subscription_tier=tier,
                    requires_api_key=requires_api_key,
                    has_api_key=has_api_key,
                    skip_reason=skip_reason,
                    fixture_kind=meta["fixture_kind"],
                    seed_validated=meta["seed_validated"],
                )
            )
    return TestsPlanResponse(
        items=items,
        module_count=len(page),
        test_count=len(items),
    )


def get_module(module_id: str) -> Optional[TestsModuleDetail]:
    catalog = module_catalog(module_id)
    if catalog is None:
        return None
    states = _typedb_route_states()
    tests = []
    for t in catalog.tests:
        meta = seed_metadata_for_module(catalog.module_id, t.consumed_nugget_id)
        tests.append(
            ModuleTestItem(
                test_id=t.test_id,
                consumed_nugget_id=t.consumed_nugget_id,
                test_state=overlay_test_state(t.route_names, states),
                input_value=sample_target_for_module(
                    catalog.module_id,
                    t.consumed_nugget_id,
                    catalog.route_seed_nugget,
                ),
                fixture_kind=meta["fixture_kind"],
                seed_validated=meta["seed_validated"],
            )
        )
    return TestsModuleDetail(
        module_id=catalog.module_id,
        name=catalog.name,
        summary=catalog.summary,
        consumption_group=catalog.consumption_group,
        access_tier=catalog.access_tier,
        route_seed_nugget=catalog.route_seed_nugget,
        test_count=len(tests),
        route_count=catalog.route_count,
        tests=tests,
    )
