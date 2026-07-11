"""Compatibility shim for the SPEC-004 core graph builder."""

from __future__ import annotations

from pathlib import Path
import sys

_CLI_CORPUS = Path(__file__).resolve().parent
if str(_CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(_CLI_CORPUS))

from core.graph_builder import (
    DEFAULT_TYPE_COLOURS,
    ONTOLOGY_NAMESPACE,
    GraphBuilder,
    load_nugget_templates,
    nugget_instance_id,
    nugget_node,
    validate_graph,
    validate_graph_connectivity,
)

__all__ = [
    "DEFAULT_TYPE_COLOURS",
    "ONTOLOGY_NAMESPACE",
    "GraphBuilder",
    "load_nugget_templates",
    "nugget_instance_id",
    "nugget_node",
    "validate_graph",
    "validate_graph_connectivity",
]
