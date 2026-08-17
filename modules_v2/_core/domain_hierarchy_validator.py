"""SPEC-019 R19-22: apex DOMAIN_NAME must have a COMPANY contains parent."""

from __future__ import annotations

from typing import Any


def _norm_domain(value: str) -> str:
    return str(value or "").lower().rstrip(".")


def infer_apex_from_graph(graph: dict[str, Any]) -> str | None:
    """Infer scan apex from COMPANY -> DOMAIN_NAME contains edge when present."""
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    nodes_by_id = {n["id"]: n for n in nodes}
    for node in nodes:
        if node.get("nugget_id") != "COMPANY":
            continue
        for edge in edges:
            if edge.get("relation") != "contains" or edge.get("source") != node["id"]:
                continue
            child = nodes_by_id.get(edge.get("target", ""))
            if child and child.get("nugget_id") == "DOMAIN_NAME":
                return _norm_domain(str(child.get("nugget_data", "")))
    return None


def _contains_parent_id(edges: list[dict[str, Any]], node_id: str) -> str | None:
    for edge in edges:
        if edge.get("relation") == "contains" and edge.get("target") == node_id:
            return str(edge.get("source", ""))
    return None


def validate_apex_domain_company_parent(
    graph: dict[str, Any],
    *,
    apex: str | None = None,
) -> list[str]:
    """Return errors; raise ValueError when apex DOMAIN_NAME lacks COMPANY parent."""
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    nodes_by_id = {n["id"]: n for n in nodes}

    apex_norm = _norm_domain(apex) if apex else infer_apex_from_graph(graph)
    if not apex_norm:
        return []

    errors: list[str] = []
    for node in nodes:
        if node.get("nugget_id") != "DOMAIN_NAME":
            continue
        data = _norm_domain(str(node.get("nugget_data", "")))
        if data != apex_norm:
            continue
        parent_id = _contains_parent_id(edges, node["id"])
        if not parent_id:
            errors.append(
                f"apex DOMAIN_NAME {data!r} has no contains parent (expected COMPANY)"
            )
            continue
        parent = nodes_by_id.get(parent_id)
        if not parent or parent.get("nugget_id") != "COMPANY":
            errors.append(
                f"apex DOMAIN_NAME {data!r} parent is {parent.get('nugget_id') if parent else parent_id!r}, expected COMPANY"
            )

    if errors:
        raise ValueError("; ".join(errors))
    return []
