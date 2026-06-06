"""Route catalog from osint_services.json (Stage 4 — R2-04-03)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

from spiderfeet.map.constants import OSINT_SERVICES_JSON


@dataclass(frozen=True)
class RouteDefinition:
    route_name: str
    module_id: str
    consumed_nugget_id: str
    produced_nugget_id: str


@dataclass(frozen=True)
class ModuleTestDefinition:
    """One executable module test per consumed catalogue nugget."""

    test_id: str
    module_id: str
    consumed_nugget_id: str
    expected_produced_nugget_ids: Tuple[str, ...]
    route_names: Tuple[str, ...]


@dataclass
class ModuleRouteCatalog:
    module_id: str
    name: str
    summary: str
    consumption_group: str
    access_tier: str
    route_seed_nugget: Optional[str]
    route_count: int
    test_count: int = 0
    routes: List[RouteDefinition] = field(default_factory=list)
    tests: List[ModuleTestDefinition] = field(default_factory=list)


def route_name(consumed_nugget_id: str, produced_nugget_id: str, module_id: str) -> str:
    return f"{consumed_nugget_id}-to-{produced_nugget_id}-via-{module_id}"


def module_test_id(module_id: str, consumed_nugget_id: str) -> str:
    return f"{module_id}:{consumed_nugget_id}"


def expand_module_tests_for_service(svc: Dict[str, Any]) -> List[ModuleTestDefinition]:
    """One test per consumed nugget — a single scan may produce many nugget types."""
    module_id = svc.get("module_id", "")
    if not module_id:
        return []
    consumed = svc.get("consumed_nuggets") or []
    produced = tuple(svc.get("produced_nuggets") or [])
    tests: List[ModuleTestDefinition] = []
    for consumed_id in consumed:
        route_names = tuple(
            route_name(consumed_id, produced_id, module_id) for produced_id in produced
        )
        tests.append(
            ModuleTestDefinition(
                test_id=module_test_id(module_id, consumed_id),
                module_id=module_id,
                consumed_nugget_id=consumed_id,
                expected_produced_nugget_ids=produced,
                route_names=route_names,
            )
        )
    return tests


@lru_cache(maxsize=1)
def load_osint_services() -> Tuple[Dict[str, Any], ...]:
    with OSINT_SERVICES_JSON.open(encoding="utf-8") as handle:
        rows = json.load(handle)
    return tuple(rows)


@lru_cache(maxsize=1)
def osint_service_index() -> Dict[str, Dict[str, Any]]:
    return {str(svc.get("module_id") or ""): svc for svc in load_osint_services()}


def service_by_module_id(module_id: str) -> Optional[Dict[str, Any]]:
    return osint_service_index().get(module_id)


def expand_routes_for_service(svc: Dict[str, Any]) -> List[RouteDefinition]:
    module_id = svc.get("module_id", "")
    if not module_id:
        return []
    consumed = svc.get("consumed_nuggets") or []
    produced = svc.get("produced_nuggets") or []
    routes: List[RouteDefinition] = []
    for consumed_id in consumed:
        for produced_id in produced:
            routes.append(
                RouteDefinition(
                    route_name=route_name(consumed_id, produced_id, module_id),
                    module_id=module_id,
                    consumed_nugget_id=consumed_id,
                    produced_nugget_id=produced_id,
                )
            )
    return routes


def all_route_definitions() -> List[RouteDefinition]:
    routes: List[RouteDefinition] = []
    for svc in load_osint_services():
        routes.extend(expand_routes_for_service(svc))
    return routes


def all_module_test_definitions() -> List[ModuleTestDefinition]:
    tests: List[ModuleTestDefinition] = []
    for svc in load_osint_services():
        tests.extend(expand_module_tests_for_service(svc))
    return tests


def module_catalog(module_id: str) -> Optional[ModuleRouteCatalog]:
    for svc in load_osint_services():
        if svc.get("module_id") != module_id:
            continue
        routes = expand_routes_for_service(svc)
        tests = expand_module_tests_for_service(svc)
        return ModuleRouteCatalog(
            module_id=module_id,
            name=str(svc.get("name") or module_id),
            summary=str(svc.get("summary") or ""),
            consumption_group=str(svc.get("consumption_group") or "other"),
            access_tier=str(svc.get("access_tier") or ""),
            route_seed_nugget=svc.get("route_seed_nugget"),
            route_count=len(routes),
            test_count=len(tests),
            routes=routes,
            tests=tests,
        )
    return None


def list_module_summaries(
    *,
    search: Optional[str] = None,
    consumption_group: Optional[str] = None,
) -> List[ModuleRouteCatalog]:
    needle = (search or "").strip().lower()
    group_filter = (consumption_group or "").strip().lower()
    summaries: List[ModuleRouteCatalog] = []
    for svc in load_osint_services():
        module_id = svc.get("module_id", "")
        if not module_id:
            continue
        if group_filter and str(svc.get("consumption_group", "")).lower() != group_filter:
            continue
        name = str(svc.get("name") or module_id)
        if needle and needle not in module_id.lower() and needle not in name.lower():
            continue
        routes = expand_routes_for_service(svc)
        tests = expand_module_tests_for_service(svc)
        summaries.append(
            ModuleRouteCatalog(
                module_id=module_id,
                name=name,
                summary=str(svc.get("summary") or ""),
                consumption_group=str(svc.get("consumption_group") or "other"),
                access_tier=str(svc.get("access_tier") or ""),
                route_seed_nugget=svc.get("route_seed_nugget"),
                route_count=len(routes),
                test_count=len(tests),
            )
        )
    summaries.sort(key=lambda m: m.module_id)
    return summaries


def catalog_summary() -> Dict[str, int]:
    modules = list_module_summaries()
    routes = all_route_definitions()
    tests = all_module_test_definitions()
    groups: Dict[str, int] = {}
    for module in modules:
        groups[module.consumption_group] = groups.get(module.consumption_group, 0) + 1
    return {
        "module_count": len(modules),
        "test_count": len(tests),
        "route_count": len(routes),
        "consumption_group_count": len(groups),
    }
