"""Read queries against spiderfeet-map (inventory and force-graph export)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from typedb.api.connection.driver import Driver
from typedb.api.connection.transaction import TransactionType

from spiderfeet.map import typeql_util


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
  $osint links ({role}: $nug);
  $nug isa nugget,
    has nugget_id $nid,
    has nugget_description $desc,
    has nugget_colour $colour;
"""
    if limit is not None:
        pipeline += f"offset 0;\nlimit {int(limit)};\n"
    pipeline += """
fetch {
  "module_id": $mid,
  "service_name": $name,
  "service_state": $state,
  "nugget_id": $nid,
  "nugget_description": $desc,
  "nugget_colour": $colour
};
"""
    return pipeline


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
                )
            if nid not in nodes:
                nodes[nid] = ForceGraphNode(
                    id=nid,
                    kind="nugget",
                    label=str(row.get("nugget_description") or nid),
                    colour=row.get("nugget_colour"),
                )
            links.append(ForceGraphLink(source=mid, target=nid, role=role))

    return ForceGraphExport(nodes=list(nodes.values()), links=links)
