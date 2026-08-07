"""Acceptance invariant checks (SPEC-010 R10-30)."""

from __future__ import annotations

import json
from typing import Any, Dict, Mapping, Optional, Sequence


class AcceptanceError(AssertionError):
    """One or more acceptance invariants failed."""


FOUR_FORMS = (
    "text_form",
    "structured_form",
    "graph_form",
    "markdown_narrative_form",
)


def assert_no_ip_address_nodes(graph: Mapping[str, Any], *, label: str = "graph") -> None:
    bad = [
        n
        for n in (graph.get("nodes") or [])
        if isinstance(n, Mapping) and n.get("nugget_id") == "IP_ADDRESS"
    ]
    if bad:
        sample = [n.get("nugget_data") or n.get("id") for n in bad[:5]]
        raise AcceptanceError(
            f"{label}: found ambiguous IP_ADDRESS nugget(s) (AH incomplete): {sample}"
        )


def assert_no_orphan_nodes(graph: Mapping[str, Any], *, label: str = "graph") -> None:
    """Every node must appear in at least one edge when the graph has edges.

    Empty graphs (clean miss) are valid. Single-node graphs with no edges are
    treated as sparse-but-valid (no orphan set to check against edges).
    """
    nodes = [n for n in (graph.get("nodes") or []) if isinstance(n, Mapping)]
    edges = [e for e in (graph.get("edges") or []) if isinstance(e, Mapping)]
    if not nodes or not edges:
        return
    seen: set[str] = set()
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src:
            seen.add(str(src))
        if tgt:
            seen.add(str(tgt))
    orphans = []
    for node in nodes:
        nid = str(node.get("id") or node.get("nugget_instance_id") or "")
        if nid and nid not in seen:
            orphans.append(nid)
    if orphans:
        raise AcceptanceError(
            f"{label}: orphan node(s) not referenced by edges: {orphans[:8]}"
        )


def parse_graph_form(graph_form: Any) -> Dict[str, Any]:
    if graph_form is None:
        return {"nodes": [], "edges": []}
    if isinstance(graph_form, Mapping):
        return {
            "nodes": list(graph_form.get("nodes") or []),
            "edges": list(graph_form.get("edges") or []),
        }
    if isinstance(graph_form, str):
        text = graph_form.strip()
        if not text:
            return {"nodes": [], "edges": []}
        parsed = json.loads(text)
        if not isinstance(parsed, Mapping):
            raise AcceptanceError("graph_form JSON root must be an object")
        return {
            "nodes": list(parsed.get("nodes") or []),
            "edges": list(parsed.get("edges") or []),
        }
    raise AcceptanceError(f"unsupported graph_form type: {type(graph_form)!r}")


def assert_four_forms_present(
    scan_step: Mapping[str, Any], *, label: Optional[str] = None
) -> None:
    sid = label or scan_step.get("scan_instance_id") or "scan_step"
    missing = [k for k in FOUR_FORMS if not _nonempty(scan_step.get(k))]
    if missing:
        raise AcceptanceError(f"{sid}: missing four-form field(s): {missing}")


def assert_graph_invariants(
    graph: Mapping[str, Any], *, label: str = "graph"
) -> None:
    assert_no_ip_address_nodes(graph, label=label)
    assert_no_orphan_nodes(graph, label=label)


def assert_scan_step_artifacts(
    scan_step: Mapping[str, Any], *, require_forms: bool = True
) -> None:
    sid = str(scan_step.get("scan_instance_id") or "scan_step")
    if require_forms:
        assert_four_forms_present(scan_step, label=sid)
    graph = parse_graph_form(scan_step.get("graph_form"))
    assert_graph_invariants(graph, label=f"{sid}.graph_form")


def assert_queryable_json(payload: Any, *, label: str) -> Dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise AcceptanceError(f"{label}: expected JSON object, got {type(payload)!r}")
    return dict(payload)


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return True
    return True


def summarize_failures(errors: Sequence[BaseException]) -> str:
    if not errors:
        return ""
    return "\n".join(f"- {e}" for e in errors)
