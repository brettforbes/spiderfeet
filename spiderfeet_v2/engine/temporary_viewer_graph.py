"""Stamp scan graphs for Temporary Subgraph Viewer (SPEC-017 R17-02).

Per-node ``temporary_id`` is ``temporary--<uuidv4>`` so uuid5 nugget instance
ids can overlap across subgraphs on one canvas. TypeDB row id remains
``temporary-subgraph--<uuidv4>`` (separate).

Node membership label uses property ``source`` (= YAML scan_name).
Edge endpoints keep ``source``/``target``; membership uses ``scan_name``
(cannot reuse ``source`` on edges — that field is the endpoint).
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, MutableMapping, Optional
from uuid import uuid4


def new_temporary_subgraph_id() -> str:
    return f"temporary-subgraph--{uuid4()}"


def new_temporary_node_id() -> str:
    return f"temporary--{uuid4()}"


def stamp_viewer_graph(
    scan_graph: Mapping[str, Any],
    *,
    scan_name: str,
) -> Dict[str, List[Dict[str, Any]]]:
    """Return a deep-copied graph with temporary ids + membership stamps."""
    id_map: Dict[str, str] = {}
    nodes_out: List[Dict[str, Any]] = []

    for raw in scan_graph.get("nodes") or []:
        if not isinstance(raw, Mapping):
            continue
        node: Dict[str, Any] = dict(raw)
        canonical = str(node.get("nugget_instance_id") or node.get("id") or "")
        if not canonical:
            continue
        tid = new_temporary_node_id()
        id_map[canonical] = tid
        # Preserve ontology identity; canvas identity is temporary_id.
        node["nugget_instance_id"] = canonical
        node["id"] = tid
        node["temporary_id"] = tid
        node["source"] = scan_name
        nodes_out.append(node)

    def _remap(value: Any) -> Any:
        if value is None:
            return None
        key = str(value)
        return id_map.get(key, value)

    edges_out: List[Dict[str, Any]] = []
    for raw in scan_graph.get("edges") or []:
        if not isinstance(raw, Mapping):
            continue
        edge: Dict[str, Any] = dict(raw)
        src = _remap(edge.get("source") if "source" in edge else edge.get("from"))
        tgt = _remap(edge.get("target") if "target" in edge else edge.get("to"))
        out: Dict[str, Any] = {}
        for k, v in edge.items():
            if k in ("source", "from", "target", "to"):
                continue
            out[k] = v
        if src is not None:
            out["source"] = src
        if tgt is not None:
            out["target"] = tgt
        out["scan_name"] = scan_name
        edges_out.append(out)

    return {"nodes": nodes_out, "edges": edges_out}


def viewer_json_string(graph: Mapping[str, Any]) -> str:
    """Serialize viewer graph preserving temporary_id / source / scan_name."""
    import json

    nodes = list(graph.get("nodes") or [])
    edges = list(graph.get("edges") or [])
    return json.dumps({"nodes": nodes, "edges": edges}, separators=(",", ":"))


def step_scan_name(step: Mapping[str, Any]) -> str:
    sid = step.get("id")
    return str(sid).strip() if sid else "unknown_step"


def step_scan_description(step: Mapping[str, Any]) -> Optional[str]:
    desc = step.get("description")
    if desc is None:
        return None
    text = str(desc).strip()
    return text or None
