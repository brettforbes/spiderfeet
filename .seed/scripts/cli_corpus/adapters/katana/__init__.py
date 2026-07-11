"""Katana SPEC-004 adapter (`structured_native`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from adapters.katana.hooks import apply_katana_records
from core.graph_builder import GraphBuilder, nugget_node
from core.rule_engine import RuleEngine, load_rule_pack
from katana_structured import (
    KATANA_STRUCTURED_SCHEMA,
    dumps_katana_bundle,
    parse_katana_structured,
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
        doc = parse_katana_structured(structured)
    else:
        doc = structured
    doc = {**doc, "schema": doc.get("schema") or KATANA_STRUCTURED_SCHEMA}
    if "records" not in doc:
        raise ValueError("expected katana bundle with records[]")
    if target and not doc.get("target"):
        doc["target"] = target
    if command and not doc.get("command"):
        doc["command"] = command
    if "scan_data" not in doc:
        target_value = doc.get("target") or "katana"
        cmd = doc.get("command") or "katana"
        doc["scan_data"] = f"katana:{target_value}:{cmd}"
    return doc


def to_structured(raw: str | dict[str, Any], *, target: str | None = None, command: str | None = None) -> dict[str, Any]:
    """Normalize Katana JSON/JSONL into the approved `katana_crawl_v1` bundle."""
    return _structured_doc(raw, target=target, command=command)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Katana records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str, *, target: str | None = None) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus Katana hooks."""
    doc = _structured_doc(structured, target=target)
    rule_pack = load_rule_pack(RULES_DIR / "katana" / "mapping.yaml", shared_dir=RULES_DIR / "_shared")
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "katana", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_katana_records(builder, scan["id"], doc)
    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "katana") -> str:
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}
    urls = [n for n in nodes if n.get("nugget_id") == "LINKED_URL_INTERNAL"]
    lines = [
        f"# Katana crawl narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        f"This report summarizes Katana crawl output with **{len(urls)}** discovered URL node(s).",
        "",
        "## URLs",
        "",
    ]
    for url in sorted(urls, key=lambda n: str(n.get("nugget_data"))):
        lines.append(f"- `{url.get('nugget_data')}`")
    if not urls:
        lines.append("- (none)")
    lines.extend(["", "## Appendix", "", "### Nodes", ""])
    for node in sorted(nodes, key=lambda n: (n.get("nugget_id", ""), n.get("nugget_data", ""))):
        lines.append(f"- `{node.get('nugget_id')}`: {node.get('nugget_data')}")
    lines.extend(["", "### Edges", ""])
    for edge in edges:
        src = by_id.get(edge.get("source"), {})
        tgt = by_id.get(edge.get("target"), {})
        lines.append(f"- `{src.get('nugget_id')}` `{edge.get('relation')}` `{tgt.get('nugget_id')}`")
    return "\n".join(lines).strip() + "\n"


def build_outputs(raw: str | dict[str, Any], *, scenario_key: str = "katana", target: str | None = None, command: str | None = None) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Katana capture."""
    structured = to_structured(raw, target=target, command=command)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_json": dumps_katana_bundle(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
