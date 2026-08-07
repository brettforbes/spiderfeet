# -*- coding: utf-8 -*-
"""Pius structured-native adapter for modules_v2 (SPEC-010 / R10-15)."""

from __future__ import annotations

from typing import Any, Literal

from modules_v2._core.graph_builder import GraphBuilder, nugget_node
from modules_v2._core.narrative_engine import render_narrative
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2.adapters.pius.hooks import apply_pius_records
from modules_v2.adapters.pius.structured import (
    PIUS_STRUCTURED_SCHEMA,
    dumps_pius_bundle,
    parse_pius_structured,
    structured_to_text,
)

CAPTURE_FAMILY: Literal["structured_native"] = "structured_native"


def _structured_doc(
    structured: dict[str, Any] | str,
    *,
    org: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = parse_pius_structured(structured)
    else:
        doc = dict(structured)
    doc = {**doc, "schema": doc.get("schema") or PIUS_STRUCTURED_SCHEMA}
    if org and not doc.get("org"):
        doc["org"] = org
    if command and (not doc.get("command") or doc.get("command") == "pius"):
        doc["command"] = command
    if "records" not in doc:
        raise ValueError("expected pius bundle with records[]")
    if "scan_data" not in doc:
        org_value = doc.get("org") or doc.get("target") or "pius"
        cmd = doc.get("command") or "pius"
        doc["scan_data"] = f"pius:{org_value}:{cmd}"
    return doc


def to_structured(
    raw: str | dict[str, Any],
    *,
    org: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Normalize Pius JSON/NDJSON into the approved ``pius_finding_v1`` bundle."""
    return _structured_doc(raw, org=org, command=command)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Pius records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str, *, org: str | None = None) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 08 hooks."""
    doc = _structured_doc(structured, org=org)
    rule_pack = load_rule_pack(mapping_path("pius"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "pius", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_pius_records(builder, scan["id"], doc)
    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "pius") -> str:
    return render_narrative(graph, tool="pius", scenario_key=scenario_key)


def build_outputs(
    raw: str | dict[str, Any],
    *,
    scenario_key: str = "pius",
    org: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Pius capture."""
    structured = to_structured(raw, org=org, command=command)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_type": "json",
        "structured_json": dumps_pius_bundle(structured),
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
