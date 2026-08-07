# -*- coding: utf-8 -*-
"""Nerva structured-native adapter for modules_v2 (SPEC-010 / R10-15)."""

from __future__ import annotations

from typing import Any, Literal

from modules_v2._core.graph_builder import GraphBuilder, nugget_node
from modules_v2._core.narrative_engine import render_narrative
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2.adapters.nerva.hooks import apply_nerva_records
from modules_v2.adapters.nerva.structured import (
    NERVA_STRUCTURED_SCHEMA,
    dumps_nerva_bundle,
    parse_nerva_structured,
    structured_to_text,
)

CAPTURE_FAMILY: Literal["structured_native"] = "structured_native"


def _structured_doc(structured: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = parse_nerva_structured(structured)
    else:
        doc = dict(structured)
    if doc.get("schema") and doc.get("schema") != NERVA_STRUCTURED_SCHEMA:
        if "records" not in doc:
            raise ValueError(f"expected schema {NERVA_STRUCTURED_SCHEMA}")
    if "records" not in doc:
        raise ValueError("expected nerva bundle with records[]")
    doc = {**doc, "schema": NERVA_STRUCTURED_SCHEMA}
    if "command" not in doc:
        doc["command"] = doc.get("scan_command") or "nerva"
    if "scan_data" not in doc:
        target = doc.get("target") or "nerva"
        doc["scan_data"] = f"nerva:{target}:{doc.get('started_at') or doc['command']}"
    return doc


def to_structured(raw: str | dict[str, Any], *, command: str | None = None) -> dict[str, Any]:
    """Normalize Nerva JSON/JSONL into the approved ``nerva_fingerprint_v1`` bundle."""
    doc = _structured_doc(raw)
    if command and (not doc.get("command") or doc.get("command") == "nerva"):
        doc["command"] = command
        doc["scan_data"] = f"nerva:{doc.get('target') or 'nerva'}:{command}"
    return doc


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Nerva records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 07B hooks (N1 uses correlation_engine)."""
    doc = _structured_doc(structured)
    rule_pack = load_rule_pack(mapping_path("nerva"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "nerva", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_nerva_records(builder, scan["id"], doc)
    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "nerva") -> str:
    return render_narrative(graph, tool="nerva", scenario_key=scenario_key)


def build_outputs(
    raw: str | dict[str, Any],
    *,
    scenario_key: str = "nerva",
    command: str | None = None,
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Nerva capture."""
    structured = to_structured(raw, command=command)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_type": "json",
        "structured_json": dumps_nerva_bundle(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }


__all__ = [
    "CAPTURE_FAMILY",
    "build_outputs",
    "to_graph",
    "to_narrative",
    "to_structured",
    "to_text",
]
