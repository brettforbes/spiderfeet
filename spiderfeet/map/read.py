"""Read queries against spiderfeet-map (inventory and force-graph export)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Dict, List, Optional, Set, Tuple

from typedb.api.connection.driver import Driver
from typedb.api.connection.transaction import TransactionType

from spiderfeet.map import typeql_util
from spiderfeet.map.constants import OSINT_SERVICES_JSON


@dataclass
class MapInventory:
    nugget_count: int = 0
    service_count: int = 0
    link_count: int = 0


@dataclass
class ForceGraphNode:
    id: str
    kind: str
    label: str
    colour: Optional[str] = None
    service_state: Optional[str] = None
    fixture_category: Optional[str] = None
    icon: Optional[str] = None
    fav_icon: Optional[str] = None


@dataclass
class ForceGraphLink:
    source: str
    target: str
    role: str


@dataclass
class ForceGraphExport:
    nodes: List[ForceGraphNode] = field(default_factory=list)
    links: List[ForceGraphLink] = field(default_factory=list)


def _fetch_documents(driver: Driver, database: str, query: str) -> List[Dict[str, Any]]:
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        if not hasattr(answer, "as_concept_documents"):
            return []
        return list(answer.as_concept_documents())


def get_inventory(driver: Driver, database: str) -> MapInventory:
    nuggets = typeql_util.run_read_scalar(
        driver, database, "match $n isa nugget; reduce $c = count;"
    )
    services = typeql_util.run_read_scalar(
        driver, database, "match $s isa osint-service; reduce $c = count;"
    )
    links = typeql_util.run_read_scalar(
        driver,
        database,
        (
            "match $osint isa osint-service; "
            "{ $osint links (consumed: $nug); } or { $osint links (produced: $nug); }; "
            "$nug isa nugget; reduce $c = count;"
        ),
    )
    return MapInventory(
        nugget_count=nuggets or 0,
        service_count=services or 0,
        link_count=links or 0,
    )


def _link_fetch_query(role: str, limit: Optional[int]) -> str:
    pipeline = f"""
match
  $osint isa osint-service,
    has module_id $mid,
    has name $name,
    has service_state $state;
try {{
  $osint has fixture_category $fixture;
}};
  $osint links ({role}: $nug);
  $nug isa nugget,
    has nugget_id $nid,
    has nugget_description $desc,
    has nugget_colour $colour;
try {{
  $nug has nugget_icon $icon;
}};
"""
    if limit is not None:
        pipeline += f"offset 0;\nlimit {int(limit)};\n"
    pipeline += """
fetch {
  "module_id": $mid,
  "service_name": $name,
  "service_state": $state,
  "fixture_category": $fixture,
  "nugget_id": $nid,
  "nugget_description": $desc,
  "nugget_colour": $colour,
  "nugget_icon": $icon
};
"""
    return pipeline


@lru_cache(maxsize=1)
def _fav_icons_from_catalog() -> Dict[str, str]:
    """module_id → data_source.fav_icon from osint_services.json."""
    if not OSINT_SERVICES_JSON.is_file():
        return {}
    with OSINT_SERVICES_JSON.open(encoding="utf-8") as handle:
        rows = json.load(handle)
    out: Dict[str, str] = {}
    for row in rows:
        module_id = row.get("module_id")
        fav = (row.get("data_source") or {}).get("fav_icon")
        if module_id and fav:
            out[str(module_id)] = str(fav)
    return out


def _fetch_service_fav_icons(driver: Driver, database: str) -> Dict[str, str]:
    """module_id → fav_icon URL from TypeDB osint-source links."""
    query = """
match
  $osint isa osint-service,
    has module_id $mid;
  (service: $osint, source: $src) isa data-source;
  $src has fav_icon $fav;
fetch {
  "module_id": $mid,
  "fav_icon": $fav
};
"""
    icons: Dict[str, str] = {}
    for row in _fetch_documents(driver, database, query):
        mid = row.get("module_id")
        fav = row.get("fav_icon")
        if mid and fav:
            icons[str(mid)] = str(fav)
    return icons


def export_force_graph(
    driver: Driver,
    database: str,
    *,
    limit_per_role: Optional[int] = None,
) -> ForceGraphExport:
    """Build D3-friendly nodes/links from consumed and produced roles."""
    nodes: Dict[str, ForceGraphNode] = {}
    links: List[ForceGraphLink] = []
    seen_edges: Set[Tuple[str, str, str]] = set()

    for role in ("consumed", "produced"):
        for row in _fetch_documents(driver, database, _link_fetch_query(role, limit_per_role)):
            mid = str(row.get("module_id", ""))
            nid = str(row.get("nugget_id", ""))
            if not mid or not nid:
                continue
            edge_key = (mid, nid, role)
            if edge_key in seen_edges:
                continue
            seen_edges.add(edge_key)

            if mid not in nodes:
                nodes[mid] = ForceGraphNode(
                    id=mid,
                    kind="osint-service",
                    label=str(row.get("service_name") or mid),
                    service_state=str(row.get("service_state") or ""),
                    fixture_category=str(row.get("fixture_category") or "") or None,
                )
            if nid not in nodes:
                nodes[nid] = ForceGraphNode(
                    id=nid,
                    kind="nugget",
                    label=str(row.get("nugget_description") or nid),
                    colour=row.get("nugget_colour"),
                    icon=str(row.get("nugget_icon") or "") or None,
                )
            links.append(ForceGraphLink(source=mid, target=nid, role=role))

    catalog_fav = _fav_icons_from_catalog()
    typedb_fav = _fetch_service_fav_icons(driver, database)
    for node in nodes.values():
        if node.kind != "osint-service":
            continue
        node.fav_icon = typedb_fav.get(node.id) or catalog_fav.get(node.id)

    return ForceGraphExport(nodes=list(nodes.values()), links=links)
