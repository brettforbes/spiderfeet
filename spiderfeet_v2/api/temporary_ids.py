"""Strip widget temporary_id tags before persisting temporary context (R10-25)."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, MutableMapping, Optional


def _canonical_node_id(node: Mapping[str, Any]) -> Optional[str]:
    nid = node.get("nugget_instance_id") or node.get("id")
    return str(nid) if nid else None


def strip_temporary_ids(graph: Mapping[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """Return a graph with ``temporary_id`` removed and edges remapped.

    The Temporary Subgraph Viewer tags nodes with ``temporary_id``
    (``temporary--<uuid>``) and rewrites edge endpoints to those tags so
    overlapping scan graphs stay discrete in the UI. Before persistence the
    server must:

    1. build ``temporary_id → nugget_instance_id`` (or ``id``)
    2. remap edge ``source``/``target`` (also ``from``/``to``) via that map
    3. drop ``temporary_id`` from every node

    The server never stores ``temporary_id``.
    """
    temp_to_canonical: Dict[str, str] = {}
    clean_nodes: List[Dict[str, Any]] = []

    for raw in graph.get("nodes") or []:
        if not isinstance(raw, Mapping):
            continue
        node: Dict[str, Any] = dict(raw)
        tid = node.pop("temporary_id", None)
        canonical = _canonical_node_id(node)
        if tid and canonical:
            temp_to_canonical[str(tid)] = canonical
        if canonical:
            node["id"] = canonical
            node.setdefault("nugget_instance_id", canonical)
        clean_nodes.append(node)

    def _remap(value: Any) -> Any:
        if value is None:
            return None
        key = str(value)
        return temp_to_canonical.get(key, value)

    clean_edges: List[Dict[str, Any]] = []
    for raw in graph.get("edges") or []:
        if not isinstance(raw, Mapping):
            continue
        edge: Dict[str, Any] = dict(raw)
        src = _remap(edge.get("source") if "source" in edge else edge.get("from"))
        tgt = _remap(edge.get("target") if "target" in edge else edge.get("to"))
        rel = edge.get("relation") or edge.get("type")
        out: Dict[str, Any] = {}
        # Preserve extra keys but force canonical endpoints + relation name.
        for k, v in edge.items():
            if k in ("source", "from", "target", "to", "relation", "type"):
                continue
            out[k] = v
        if src is not None:
            out["source"] = src
        if tgt is not None:
            out["target"] = tgt
        if rel is not None:
            out["relation"] = rel
        clean_edges.append(out)

    return {"nodes": clean_nodes, "edges": clean_edges}


def assert_no_temporary_ids(graph: Mapping[str, Any]) -> None:
    """Raise ValueError if any temporary_id remains (post-strip invariant)."""
    for node in graph.get("nodes") or []:
        if isinstance(node, MutableMapping) and "temporary_id" in node:
            raise ValueError("temporary_id must not be persisted")
        if isinstance(node, Mapping) and node.get("temporary_id"):
            raise ValueError("temporary_id must not be persisted")
