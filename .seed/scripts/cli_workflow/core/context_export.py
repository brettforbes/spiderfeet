"""Merge scan graphs into workflow context."""

from __future__ import annotations

from typing import Any, Dict, List, MutableMapping, Set, Tuple


def merge_graph(
    context: MutableMapping[str, List[Dict[str, Any]]],
    scan_graph: Dict[str, Any],
) -> Dict[str, List[Dict[str, Any]]]:
    """Append unique nodes (by id) and edges (by source,target,relation)."""
    if "nodes" not in context:
        context["nodes"] = []
    if "edges" not in context:
        context["edges"] = []

    seen_nodes: Set[str] = set()
    for n in context["nodes"]:
        nid = n.get("id") or n.get("nugget_instance_id")
        if nid:
            seen_nodes.add(nid)

    for n in scan_graph.get("nodes") or []:
        nid = n.get("id") or n.get("nugget_instance_id")
        if not nid or nid in seen_nodes:
            continue
        context["nodes"].append(n)
        seen_nodes.add(nid)

    seen_edges: Set[Tuple[str, str, str]] = set()
    for e in context["edges"]:
        key = (e.get("source", ""), e.get("target", ""), e.get("relation", ""))
        seen_edges.add(key)

    for e in scan_graph.get("edges") or []:
        key = (e.get("source", ""), e.get("target", ""), e.get("relation", ""))
        if not key[0] or not key[1] or key in seen_edges:
            continue
        context["edges"].append(e)
        seen_edges.add(key)

    return dict(context)
