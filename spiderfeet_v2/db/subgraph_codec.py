"""Dual-form subgraph codec: graph JSON ↔ TypeDB entity/relation form (R10-18 / AL2).

Canonical edge mapping: `.governance/project/SPEC010_EDGE_NAMING.md`
  had ↔ has_this · contains ↔ contains_this · listens-to ↔ listens_to_this
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from typedb.api.connection.driver import Driver
from typedb.api.connection.transaction import TransactionType

from spiderfeet.map.naming import entity_type_for_nugget_id
from spiderfeet.map.typeql_util import literal_string, run_read_exists, run_write, run_writes

# SPEC010_EDGE_NAMING.md §1
JSON_TO_TYPEQL: Mapping[str, str] = {
    "had": "has_this",
    "contains": "contains_this",
    "listens-to": "listens_to_this",
}
TYPEQL_TO_JSON: Mapping[str, str] = {v: k for k, v in JSON_TO_TYPEQL.items()}

NODE_ATTRS: Tuple[str, ...] = (
    "nugget_id",
    "nugget_instance_id",
    "nugget_type",
    "nugget_description",
    "nugget_data",
    "nugget_colour",
    "nugget_icon",
    "nugget_module",
    "nugget_source_data",
)

_SUBGRAPH_META = {
    "scan_result_graph": {"id_attr": "scan_result_id"},
    "project_context": {"id_attr": "project_context_id"},
    "temporary_subgraph": {"id_attr": "temporary_subgraph_id"},
    "target_context": {"id_attr": "target_context_id"},
}


class SubgraphCodecError(Exception):
    """Invalid graph JSON or dual-form persistence failure."""


def edge_relation_json(edge: Mapping[str, Any]) -> str:
    """Return corpus relation name (`had` / `contains` / `listens-to`)."""
    rel = edge.get("relation") or edge.get("type")
    if not rel:
        raise SubgraphCodecError(f"edge missing relation/type: {edge!r}")
    rel = str(rel)
    if rel not in JSON_TO_TYPEQL:
        raise SubgraphCodecError(
            f"unknown edge relation {rel!r}; allowed: {sorted(JSON_TO_TYPEQL)}"
        )
    return rel


def edge_endpoints(edge: Mapping[str, Any]) -> Tuple[str, str]:
    src = edge.get("source") or edge.get("from")
    tgt = edge.get("target") or edge.get("to")
    if not src or not tgt:
        raise SubgraphCodecError(f"edge missing source/target: {edge!r}")
    return str(src), str(tgt)


def normalize_graph(graph: Mapping[str, Any]) -> Dict[str, Any]:
    """Canonical nodes/edges ordering for equality checks and json_string storage."""
    if "nodes" not in graph or "edges" not in graph:
        raise SubgraphCodecError("graph must have 'nodes' and 'edges' arrays")
    nodes_out: List[Dict[str, Any]] = []
    for raw in graph["nodes"]:
        nid = raw.get("nugget_instance_id") or raw.get("id")
        if not nid:
            raise SubgraphCodecError(f"node missing nugget_instance_id/id: {raw!r}")
        if not raw.get("nugget_id"):
            raise SubgraphCodecError(f"node missing nugget_id: {raw!r}")
        node: Dict[str, Any] = {
            "id": str(nid),
            "nugget_instance_id": str(nid),
            "nugget_id": str(raw["nugget_id"]),
        }
        for attr in NODE_ATTRS:
            if attr in ("nugget_instance_id", "nugget_id"):
                continue
            if attr in raw and raw[attr] is not None:
                node[attr] = raw[attr]
        nodes_out.append(node)
    nodes_out.sort(key=lambda n: n["nugget_instance_id"])

    edges_out: List[Dict[str, Any]] = []
    for raw in graph["edges"]:
        src, tgt = edge_endpoints(raw)
        rel = edge_relation_json(raw)
        edges_out.append({"source": src, "target": tgt, "relation": rel})
    edges_out.sort(key=lambda e: (e["source"], e["target"], e["relation"]))
    return {"nodes": nodes_out, "edges": edges_out}


def canonical_json_string(graph: Mapping[str, Any]) -> str:
    return json.dumps(normalize_graph(graph), separators=(",", ":"), sort_keys=True)


def graphs_equal(a: Mapping[str, Any], b: Mapping[str, Any]) -> bool:
    return normalize_graph(a) == normalize_graph(b)


def _collect_strings(driver: Driver, database: str, query: str, column: str = "v") -> List[str]:
    out: List[str] = []
    with driver.transaction(database, TransactionType.READ) as tx:
        answer = tx.query(query).resolve()
        if not hasattr(answer, "as_concept_rows"):
            return out
        for row in answer.as_concept_rows():
            concept = row.get(column)
            if concept is None:
                continue
            value = concept.try_get_value()
            if value is not None:
                out.append(str(value))
    return out


def _nugget_exists(driver: Driver, database: str, instance_id: str) -> bool:
    return run_read_exists(
        driver,
        database,
        f"match $n isa nugget, has nugget_instance_id {literal_string(instance_id)};",
    )


def _upsert_nugget(driver: Driver, database: str, node: Mapping[str, Any]) -> None:
    instance_id = str(node["nugget_instance_id"])
    nugget_id = str(node["nugget_id"])
    entity_type = entity_type_for_nugget_id(nugget_id)
    if _nugget_exists(driver, database, instance_id):
        # Refresh attributes that are present on the node (skip id keys).
        for attr in NODE_ATTRS:
            if attr == "nugget_instance_id":
                continue
            if attr not in node or node[attr] is None:
                continue
            # clear then set
            has_it = run_read_exists(
                driver,
                database,
                f"match $n isa nugget, has nugget_instance_id {literal_string(instance_id)}, "
                f"has {attr} $v;",
            )
            if has_it:
                run_write(
                    driver,
                    database,
                    f"""
                    match
                      $n isa nugget, has nugget_instance_id {literal_string(instance_id)},
                        has {attr} $old;
                    delete
                      has $old of $n;
                    """,
                )
            run_write(
                driver,
                database,
                f"""
                match
                  $n isa nugget, has nugget_instance_id {literal_string(instance_id)};
                insert
                  $n has {attr} {literal_string(str(node[attr]))};
                """,
            )
        return

    has_parts = [
        f"has nugget_instance_id {literal_string(instance_id)}",
        f"has nugget_id {literal_string(nugget_id)}",
    ]
    for attr in NODE_ATTRS:
        if attr in ("nugget_instance_id", "nugget_id"):
            continue
        if attr not in node or node[attr] is None:
            continue
        has_parts.append(f"has {attr} {literal_string(str(node[attr]))}")
    run_write(
        driver,
        database,
        "insert\n  $n isa "
        + entity_type
        + ",\n    "
        + ",\n    ".join(has_parts)
        + ";\n",
    )


def _clear_subgraph_payload(
    driver: Driver, database: str, kind: str, id_attr: str, subgraph_id: str
) -> None:
    """Unlink + delete prior edge relations; unlink nuggets; clear json_string."""
    # Delete edges linked to this subgraph (edge instances belong to the payload).
    while run_read_exists(
        driver,
        database,
        f"""
        match
          $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
          $g links (edges: $e);
        """,
    ):
        run_write(
            driver,
            database,
            f"""
            match
              $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
              $g links (edges: $e);
            delete
              links (edges: $e) of $g;
              $e;
            """,
        )

    # Unlink nuggets (do not delete — may be shared / scan_step players).
    while run_read_exists(
        driver,
        database,
        f"""
        match
          $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
          $g links (nuggets: $n);
        """,
    ):
        run_write(
            driver,
            database,
            f"""
            match
              $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
              $g links (nuggets: $n);
            delete
              links (nuggets: $n) of $g;
            """,
        )

    if run_read_exists(
        driver,
        database,
        f"match $g isa {kind}, has {id_attr} {literal_string(subgraph_id)}, "
        f"has json_string $v;",
    ):
        run_write(
            driver,
            database,
            f"""
            match
              $g isa {kind}, has {id_attr} {literal_string(subgraph_id)},
                has json_string $old;
            delete
              has $old of $g;
            """,
        )


def store_viewer_json_string(
    driver: Driver,
    database: str,
    kind: str,
    subgraph_id: str,
    graph: Mapping[str, Any],
) -> Dict[str, Any]:
    """SPEC-017: persist temporary_subgraph as json_string only (viewer stamps kept).

    Remapped ``temporary--`` canvas ids must not be materialised as nugget entities.
    """
    if kind not in _SUBGRAPH_META:
        raise SubgraphCodecError(f"unknown subgraph kind: {kind}")
    id_attr = _SUBGRAPH_META[kind]["id_attr"]
    exists = run_read_exists(
        driver,
        database,
        f"match $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};",
    )
    if not exists:
        raise SubgraphCodecError(f"{kind} not found: {subgraph_id}")

    nodes = [dict(n) for n in (graph.get("nodes") or []) if isinstance(n, Mapping)]
    edges = [dict(e) for e in (graph.get("edges") or []) if isinstance(e, Mapping)]
    payload = {"nodes": nodes, "edges": edges}
    json_text = json.dumps(payload, separators=(",", ":"))

    # Clear prior json_string only (no dual-form unlink of remapped ids).
    if run_read_exists(
        driver,
        database,
        f"match $g isa {kind}, has {id_attr} {literal_string(subgraph_id)}, "
        f"has json_string $v;",
    ):
        run_write(
            driver,
            database,
            f"""
            match
              $g isa {kind}, has {id_attr} {literal_string(subgraph_id)},
                has json_string $old;
            delete
              has $old of $g;
            """,
        )
    run_write(
        driver,
        database,
        f"""
        match
          $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
        insert
          $g has json_string {literal_string(json_text)};
        """,
    )
    return payload


def store_dual_form(
    driver: Driver,
    database: str,
    kind: str,
    subgraph_id: str,
    graph: Mapping[str, Any],
) -> Dict[str, Any]:
    """Persist both json_string and in-graph nugget/edge form on an existing subgraph."""
    if kind not in _SUBGRAPH_META:
        raise SubgraphCodecError(f"unknown subgraph kind: {kind}")
    # SPEC-017 R17-02/R17-08: temporary rows are viewer json_string only.
    if kind == "temporary_subgraph":
        return store_viewer_json_string(driver, database, kind, subgraph_id, graph)

    id_attr = _SUBGRAPH_META[kind]["id_attr"]
    exists = run_read_exists(
        driver,
        database,
        f"match $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};",
    )
    if not exists:
        raise SubgraphCodecError(f"{kind} not found: {subgraph_id}")

    normalized = normalize_graph(graph)
    json_text = canonical_json_string(normalized)

    _clear_subgraph_payload(driver, database, kind, id_attr, subgraph_id)

    for node in normalized["nodes"]:
        _upsert_nugget(driver, database, node)

    # Link nuggets
    nugget_link_queries: List[str] = []
    for i, node in enumerate(normalized["nodes"]):
        nugget_link_queries.append(
            f"""
            match
              $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
              $n{i} isa nugget, has nugget_instance_id {literal_string(node["nugget_instance_id"])};
            insert
              $g links (nuggets: $n{i});
            """
        )
    run_writes(driver, database, nugget_link_queries)

    # Insert edges + link to subgraph
    edge_queries: List[str] = []
    for i, edge in enumerate(normalized["edges"]):
        typeql_rel = JSON_TO_TYPEQL[edge["relation"]]
        edge_queries.append(
            f"""
            match
              $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
              $src{i} isa nugget, has nugget_instance_id {literal_string(edge["source"])};
              $tgt{i} isa nugget, has nugget_instance_id {literal_string(edge["target"])};
            insert
              $e{i} isa {typeql_rel}, links (source: $src{i}, target: $tgt{i});
              $g links (edges: $e{i});
            """
        )
    run_writes(driver, database, edge_queries)

    run_write(
        driver,
        database,
        f"""
        match
          $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
        insert
          $g has json_string {literal_string(json_text)};
        """,
    )
    return normalized


def read_json_string(
    driver: Driver, database: str, kind: str, subgraph_id: str
) -> Optional[str]:
    if kind not in _SUBGRAPH_META:
        raise SubgraphCodecError(f"unknown subgraph kind: {kind}")
    id_attr = _SUBGRAPH_META[kind]["id_attr"]
    values = _collect_strings(
        driver,
        database,
        f"match $g isa {kind}, has {id_attr} {literal_string(subgraph_id)}, "
        f"has json_string $v;",
    )
    return values[0] if values else None


def load_graph_from_json_string(
    driver: Driver, database: str, kind: str, subgraph_id: str
) -> Optional[Dict[str, Any]]:
    text = read_json_string(driver, database, kind, subgraph_id)
    if text is None:
        return None
    return normalize_graph(json.loads(text))


def _read_node_attrs(
    driver: Driver, database: str, instance_id: str
) -> Dict[str, Any]:
    node: Dict[str, Any] = {
        "id": instance_id,
        "nugget_instance_id": instance_id,
    }
    for attr in NODE_ATTRS:
        if attr == "nugget_instance_id":
            continue
        values = _collect_strings(
            driver,
            database,
            f"match $n isa nugget, has nugget_instance_id {literal_string(instance_id)}, "
            f"has {attr} $v;",
        )
        if values:
            node[attr] = values[0]
    if "nugget_id" not in node:
        raise SubgraphCodecError(f"nugget missing nugget_id: {instance_id}")
    return node


def load_graph_from_typedb(
    driver: Driver, database: str, kind: str, subgraph_id: str
) -> Dict[str, Any]:
    """Reconstruct graph JSON from in-graph nuggets + semantic_link edges."""
    if kind not in _SUBGRAPH_META:
        raise SubgraphCodecError(f"unknown subgraph kind: {kind}")
    id_attr = _SUBGRAPH_META[kind]["id_attr"]
    exists = run_read_exists(
        driver,
        database,
        f"match $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};",
    )
    if not exists:
        raise SubgraphCodecError(f"{kind} not found: {subgraph_id}")

    instance_ids = _collect_strings(
        driver,
        database,
        f"""
        match
          $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
          $g links (nuggets: $n);
          $n has nugget_instance_id $v;
        """,
    )
    nodes = [_read_node_attrs(driver, database, iid) for iid in sorted(set(instance_ids))]

    edges: List[Dict[str, Any]] = []
    for typeql_rel, json_rel in TYPEQL_TO_JSON.items():
        with driver.transaction(database, TransactionType.READ) as tx:
            answer = tx.query(
                f"""
                match
                  $g isa {kind}, has {id_attr} {literal_string(subgraph_id)};
                  $g links (edges: $e);
                  $e isa {typeql_rel}, links (source: $src, target: $tgt);
                  $src has nugget_instance_id $sid;
                  $tgt has nugget_instance_id $tid;
                """
            ).resolve()
            if not hasattr(answer, "as_concept_rows"):
                continue
            for row in answer.as_concept_rows():
                sid_c = row.get("sid")
                tid_c = row.get("tid")
                if sid_c is None or tid_c is None:
                    continue
                sid = sid_c.try_get_value()
                tid = tid_c.try_get_value()
                if sid is None or tid is None:
                    continue
                edges.append(
                    {
                        "source": str(sid),
                        "target": str(tid),
                        "relation": json_rel,
                    }
                )

    return normalize_graph({"nodes": nodes, "edges": edges})


def load_dual_form(
    driver: Driver, database: str, kind: str, subgraph_id: str
) -> Dict[str, Any]:
    """Return both stored forms (json_string + reconstructed in-graph graph)."""
    graph_in = load_graph_from_typedb(driver, database, kind, subgraph_id)
    json_text = read_json_string(driver, database, kind, subgraph_id)
    graph_from_attr = (
        normalize_graph(json.loads(json_text)) if json_text is not None else None
    )
    return {
        "kind": kind,
        _SUBGRAPH_META[kind]["id_attr"]: subgraph_id,
        "json_string": json_text,
        "graph": graph_in,
        "graph_from_json_string": graph_from_attr,
    }
