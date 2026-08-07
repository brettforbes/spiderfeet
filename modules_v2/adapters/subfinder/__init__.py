# -*- coding: utf-8 -*-
"""Subfinder structured-native adapter for modules_v2 (SPEC-010 / R10-15)."""

from __future__ import annotations

from typing import Any, Literal

from modules_v2._core.graph_builder import GraphBuilder, nugget_node
from modules_v2._core.narrative_engine import render_narrative
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2.adapters.subfinder.hooks import apply_subfinder_records
from modules_v2.adapters.subfinder.structured import (
    SUBFINDER_STRUCTURED_SCHEMA,
    dumps_subfinder_bundle,
    parse_subfinder_structured,
    structured_to_text,
)

CAPTURE_FAMILY: Literal["structured_native"] = "structured_native"


def _structured_doc(
    structured: dict[str, Any] | str,
    *,
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = parse_subfinder_structured(structured)
    else:
        doc = dict(structured)
    doc = {**doc, "schema": doc.get("schema") or SUBFINDER_STRUCTURED_SCHEMA}
    if "records" not in doc:
        raise ValueError("expected subfinder bundle with records[]")
    if target and not doc.get("target"):
        doc["target"] = target
    if command and (not doc.get("command") or doc.get("command") == "subfinder"):
        doc["command"] = command
    if "enumeration_mode" not in doc:
        has_ip = any(
            isinstance(record, dict) and record.get("ip") for record in doc.get("records") or []
        )
        doc["enumeration_mode"] = "active" if has_ip else "passive"
    if "scan_data" not in doc:
        target_value = doc.get("target") or "subfinder"
        cmd = doc.get("command") or "subfinder"
        doc["scan_data"] = f"subfinder:{target_value}:{cmd}"
    return doc


def to_structured(
    raw: str | dict[str, Any],
    *,
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Normalize Subfinder JSON/JSONL into the approved ``subfinder_host_v1`` bundle."""
    return _structured_doc(raw, target=target, command=command)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Subfinder records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str, *, target: str | None = None) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 09 S0-S6 hooks."""
    doc = _structured_doc(structured, target=target)
    rule_pack = load_rule_pack(mapping_path("subfinder"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "subfinder", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_subfinder_records(builder, scan["id"], doc)
    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "subfinder") -> str:
    return render_narrative(graph, tool="subfinder", scenario_key=scenario_key)


def build_outputs(
    raw: str | dict[str, Any],
    *,
    scenario_key: str = "subfinder",
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Subfinder capture."""
    structured = to_structured(raw, target=target, command=command)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_type": "json",
        "structured_json": dumps_subfinder_bundle(structured),
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
