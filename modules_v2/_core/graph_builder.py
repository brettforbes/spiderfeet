"""Shared helpers for CLI corpus nugget graph construction."""

from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_DNS, uuid5

REPO_ROOT = Path(__file__).resolve().parents[2]
NUGGETS_PATH = REPO_ROOT / ".docs" / "analysis" / "nuggets.json"
NUGGETS_EXTENSION_PATH = REPO_ROOT / ".docs" / "analysis" / "nuggets_extension.json"

# SpiderFeet ontology instance-id seed.
ONTOLOGY_NAMESPACE = uuid5(NAMESPACE_DNS, "OS Threat, OS Intel Ontology")

DEFAULT_TYPE_COLOURS = {
    "ENTITY": "#3B82F6",
    "DESCRIPTOR": "#F59E0B",
    "DATA": "#14B8A6",
    "SUBENTITY": "#F97316",
    "INTERNAL": "#8B5CF6",
    "CATEGORY": "#14B8A6",
}


@lru_cache(maxsize=1)
def load_nugget_templates() -> dict[str, dict[str, Any]]:
    templates: dict[str, dict[str, Any]] = {}
    for path in (NUGGETS_PATH, NUGGETS_EXTENSION_PATH):
        if not path.is_file():
            continue
        for record in json.loads(path.read_text(encoding="utf-8")):
            nugget_id = record.get("nugget_id")
            if nugget_id:
                templates[nugget_id] = record
    return templates


def nugget_instance_id(nugget_id: str, data: str) -> str:
    """Stable node id: uuid5(ontology_seed, nugget_data) scoped by nugget archetype."""
    return f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, data)}"


def nugget_node(
    nugget_id: str,
    data: str,
    *,
    nugget_type: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Build a node dict; resolve type/description/colour from the nugget catalogue when present."""
    template = load_nugget_templates().get(nugget_id, {})
    resolved_type = nugget_type or template.get("nugget_type") or "ENTITY"
    resolved_desc = (
        description
        or template.get("nugget_description")
        or nugget_id.replace("_", " ").title()
    )
    iid = nugget_instance_id(nugget_id, data)
    node: dict[str, Any] = {
        "id": iid,
        "nugget_instance_id": iid,
        "nugget_id": nugget_id,
        "nugget_type": resolved_type,
        "nugget_description": resolved_desc,
        "nugget_data": data,
    }
    colour = template.get("nugget_colour") or DEFAULT_TYPE_COLOURS.get(resolved_type)
    if colour:
        node["nugget_colour"] = colour
    return node


class GraphBuilder:
    """Accumulate nodes and edges; one node per nugget_id + data identity."""

    def __init__(self) -> None:
        self._nodes: dict[str, dict[str, Any]] = {}
        self._edges: list[dict[str, str]] = []
        self._edge_keys: set[tuple[str, str, str]] = set()

    def add_node(self, node: dict[str, Any]) -> dict[str, Any]:
        node_id = node["id"]
        existing = self._nodes.get(node_id)
        if existing is not None:
            return existing
        self._nodes[node_id] = node
        return node

    def add_edge(self, source: str, target: str, relation: str) -> None:
        key = (source, target, relation)
        if key in self._edge_keys:
            return
        self._edge_keys.add(key)
        self._edges.append({"source": source, "target": target, "relation": relation})

    def build(self, *, validate: bool = True) -> dict[str, Any]:
        graph = {"nodes": list(self._nodes.values()), "edges": list(self._edges)}
        if validate:
            validate_graph(graph)
        return graph


def validate_graph(graph: dict[str, Any]) -> list[str]:
    """Return validation errors; raise ValueError when the graph is invalid."""
    errors: list[str] = []
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []

    id_counts = Counter(node["id"] for node in nodes)
    duplicate_ids = [node_id for node_id, count in id_counts.items() if count > 1]
    if duplicate_ids:
        errors.append(f"duplicate node ids: {duplicate_ids[:8]}")

    data_counts = Counter((node["nugget_id"], node.get("nugget_data", "")) for node in nodes)
    duplicate_data = [pair for pair, count in data_counts.items() if count > 1]
    if duplicate_data:
        errors.append(f"duplicate nugget_id+data: {duplicate_data[:8]}")

    node_ids = set(id_counts)
    connected: set[str] = set()
    for edge in edges:
        source = edge.get("source", "")
        target = edge.get("target", "")
        connected.add(source)
        connected.add(target)
        if source not in node_ids:
            errors.append(f"edge source missing node: {source}")
        if target not in node_ids:
            errors.append(f"edge target missing node: {target}")

    for node in nodes:
        node_id = node["id"]
        if node_id not in connected:
            nugget_id = node.get("nugget_id", "?")
            errors.append(f"orphan node {nugget_id}: {node_id}")

    if errors:
        raise ValueError("; ".join(errors))
    return []


# Backward-compatible alias
validate_graph_connectivity = validate_graph
