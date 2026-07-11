"""SPEC-004 bridge from CLI adapters to production sfp_* modules (R4-01-09).

Thin wrappers should call these helpers instead of re-implementing graph rules.
"""

from __future__ import annotations

from typing import Any


def nmap_graph_from_xml(raw_xml: str, *, target: str | None = None, command: str | None = None) -> dict[str, Any]:
    """Return nugget graph from Nmap XML via the SPEC-004 nmap adapter."""
    from adapters import nmap as nmap_adapter

    del target, command
    structured = nmap_adapter.to_structured(raw_xml)
    return nmap_adapter.to_graph(structured)


def nerva_graph_from_bundle(raw: str | dict[str, Any], *, command: str | None = None) -> dict[str, Any]:
    """Return nugget graph from Nerva JSON/JSONL via the SPEC-004 nerva adapter."""
    from adapters import nerva as nerva_adapter

    structured = nerva_adapter.to_structured(raw, command=command)
    return nerva_adapter.to_graph(structured)


def graph_entity_events(graph: dict[str, Any]) -> list[tuple[str, str]]:
    """Draft flatten: yield (nugget_id, nugget_data) for ENTITY nodes only."""
    events: list[tuple[str, str]] = []
    for node in graph.get("nodes") or []:
        if node.get("nugget_type") != "ENTITY":
            continue
        nugget_id = node.get("nugget_id")
        data = node.get("nugget_data")
        if nugget_id and data:
            events.append((str(nugget_id), str(data)))
    return events
