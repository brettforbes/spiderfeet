"""Httpx SPEC-004 adapter (`structured_native`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from adapters.httpx.hooks import apply_httpx_records
from core.graph_builder import GraphBuilder, nugget_node
from core.rule_engine import RuleEngine, load_rule_pack
from httpx_structured import (
    HTTPX_STRUCTURED_SCHEMA,
    dumps_httpx_bundle,
    parse_httpx_structured,
    structured_to_text,
)

CAPTURE_FAMILY: Literal["structured_native"] = "structured_native"
RULES_DIR = Path(__file__).resolve().parents[2] / "rules"


def _structured_doc(
    structured: dict[str, Any] | str,
    *,
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = parse_httpx_structured(structured)
    else:
        doc = structured
    doc = {**doc, "schema": doc.get("schema") or HTTPX_STRUCTURED_SCHEMA}
    if "records" not in doc:
        raise ValueError("expected httpx bundle with records[]")
    if target and not doc.get("target"):
        doc["target"] = target
    if command and not doc.get("command"):
        doc["command"] = command
    if "scan_data" not in doc:
        target_value = doc.get("target") or "httpx"
        cmd = doc.get("command") or "httpx"
        doc["scan_data"] = f"httpx:{target_value}:{cmd}"
    return doc


def to_structured(
    raw: str | dict[str, Any],
    *,
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Normalize Httpx JSON/JSONL into the approved `httpx_probe_v1` bundle."""
    return _structured_doc(raw, target=target, command=command)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Httpx records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str, *, target: str | None = None) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 10 H0-H7 hooks."""
    doc = _structured_doc(structured, target=target)
    rule_pack = load_rule_pack(RULES_DIR / "httpx" / "mapping.yaml", shared_dir=RULES_DIR / "_shared")
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "httpx", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_httpx_records(builder, scan["id"], doc)
    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "httpx") -> str:
    from core.narrative_engine import render_narrative

    return render_narrative(graph, tool="httpx", scenario_key=scenario_key)


def build_outputs(
    raw: str | dict[str, Any],
    *,
    scenario_key: str = "httpx",
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Httpx capture."""
    structured = to_structured(raw, target=target, command=command)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_json": dumps_httpx_bundle(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
