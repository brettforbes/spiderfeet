"""Context export mark + append-unique merge (SPEC-010 AM3 / R10-22).

Per 12B v1:
- ``context.export: scan_graph`` marks a step's scan_result_graph for merge
  into the temporary (workflow) context.
- ``none`` / omitted does not export the graph (vars may still flow).
- Merge is append-unique: nodes by id, edges by ``(source, target, relation)``.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Set, Tuple

EXPORT_SCAN_GRAPH = "scan_graph"
EXPORT_NONE = "none"

# Metadata key stamped onto a scan_result_graph / graph envelope when marked.
EXPORT_MARK_KEY = "context_export"
EXPORT_TO_TEMPORARY_KEY = "export_to_temporary_context"

NodeId = str
EdgeKey = Tuple[str, str, str]


def empty_context() -> Dict[str, List[Dict[str, Any]]]:
    """Return an empty temporary/project context graph."""
    return {"nodes": [], "edges": []}


def step_context_export(step: Mapping[str, Any]) -> str:
    """Return the step's ``context.export`` value (``scan_graph`` or ``none``)."""
    ctx = step.get("context") or {}
    export = ctx.get("export") if isinstance(ctx, Mapping) else None
    if export == EXPORT_SCAN_GRAPH:
        return EXPORT_SCAN_GRAPH
    return EXPORT_NONE


def step_exports_scan_graph(step: Mapping[str, Any]) -> bool:
    """True when the step marks its scan_result_graph for temporary-context export."""
    return step_context_export(step) == EXPORT_SCAN_GRAPH


def node_id(node: Mapping[str, Any]) -> Optional[str]:
    """Canonical node identity: ``id`` or ``nugget_instance_id``."""
    nid = node.get("id") or node.get("nugget_instance_id")
    return str(nid) if nid else None


def edge_key(edge: Mapping[str, Any]) -> Optional[EdgeKey]:
    """Canonical edge identity: ``(source, target, relation)``."""
    src = edge.get("source") or edge.get("from")
    tgt = edge.get("target") or edge.get("to")
    rel = edge.get("relation") or edge.get("type")
    if not src or not tgt or not rel:
        return None
    return (str(src), str(tgt), str(rel))


def mark_scan_result_for_export(
    scan_result_graph: Mapping[str, Any],
    step: Mapping[str, Any],
) -> Dict[str, Any]:
    """Stamp export metadata on a scan_result_graph envelope from the step DSL.

    Does not mutate the input. Always sets ``context_export`` to the effective
    export mode and ``export_to_temporary_context`` to a boolean. Node/edge
    arrays are copied by reference (shallow) when present.
    """
    export = step_context_export(step)
    out: Dict[str, Any] = dict(scan_result_graph)
    out[EXPORT_MARK_KEY] = export
    out[EXPORT_TO_TEMPORARY_KEY] = export == EXPORT_SCAN_GRAPH
    return out


def is_marked_for_export(scan_result_graph: Mapping[str, Any]) -> bool:
    """True when a marked graph should merge into the temporary context."""
    if EXPORT_TO_TEMPORARY_KEY in scan_result_graph:
        return bool(scan_result_graph[EXPORT_TO_TEMPORARY_KEY])
    return scan_result_graph.get(EXPORT_MARK_KEY) == EXPORT_SCAN_GRAPH


def merge_graph(
    context: MutableMapping[str, Any],
    scan_graph: Mapping[str, Any],
) -> Dict[str, List[Dict[str, Any]]]:
    """Append-unique merge of ``scan_graph`` into ``context`` (mutates context).

    - Nodes unique by ``id`` / ``nugget_instance_id``
    - Edges unique by ``(source, target, relation)`` (also accepts from/to/type)
    """
    if "nodes" not in context or context["nodes"] is None:
        context["nodes"] = []
    if "edges" not in context or context["edges"] is None:
        context["edges"] = []

    nodes: List[Dict[str, Any]] = context["nodes"]
    edges: List[Dict[str, Any]] = context["edges"]

    seen_nodes: Set[str] = set()
    for n in nodes:
        nid = node_id(n)
        if nid:
            seen_nodes.add(nid)

    for n in scan_graph.get("nodes") or []:
        if not isinstance(n, Mapping):
            continue
        nid = node_id(n)
        if not nid or nid in seen_nodes:
            continue
        nodes.append(dict(n))
        seen_nodes.add(nid)

    seen_edges: Set[EdgeKey] = set()
    for e in edges:
        key = edge_key(e)
        if key:
            seen_edges.add(key)

    for e in scan_graph.get("edges") or []:
        if not isinstance(e, Mapping):
            continue
        key = edge_key(e)
        if not key or key in seen_edges:
            continue
        # Normalise stored edge shape for downstream consumers.
        edges.append({"source": key[0], "target": key[1], "relation": key[2]})
        # Preserve extra edge attrs when present.
        for k, v in e.items():
            if k in ("source", "target", "relation", "from", "to", "type"):
                continue
            edges[-1][k] = v
        seen_edges.add(key)

    return {"nodes": nodes, "edges": edges}


def merge_graphs(
    *graphs: Mapping[str, Any],
    base: Optional[MutableMapping[str, Any]] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """Merge zero or more graphs append-unique into ``base`` (or a new context)."""
    context: MutableMapping[str, Any] = base if base is not None else empty_context()
    for g in graphs:
        merge_graph(context, g)
    return {"nodes": list(context["nodes"]), "edges": list(context["edges"])}


def apply_context_export(
    context: MutableMapping[str, Any],
    step: Mapping[str, Any],
    scan_graph: Mapping[str, Any],
    *,
    scan_result_graph: Optional[MutableMapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Mark the scan result (optional) and merge into context when export is on.

    Returns ``{"exported": bool, "marked": <envelope>, "context": <nodes/edges>}``.
    """
    marked = mark_scan_result_for_export(scan_graph, step)
    if scan_result_graph is not None:
        scan_result_graph[EXPORT_MARK_KEY] = marked[EXPORT_MARK_KEY]
        scan_result_graph[EXPORT_TO_TEMPORARY_KEY] = marked[EXPORT_TO_TEMPORARY_KEY]

    exported = False
    if step_exports_scan_graph(step):
        merge_graph(context, scan_graph)
        exported = True

    return {
        "exported": exported,
        "marked": marked,
        "context": {"nodes": list(context.get("nodes") or []), "edges": list(context.get("edges") or [])},
    }


def export_steps(steps: Iterable[Mapping[str, Any]]) -> List[str]:
    """Return step ids whose ``context.export`` is ``scan_graph``."""
    out: List[str] = []
    for step in steps:
        if step_exports_scan_graph(step):
            sid = step.get("id")
            if sid:
                out.append(str(sid))
    return out
