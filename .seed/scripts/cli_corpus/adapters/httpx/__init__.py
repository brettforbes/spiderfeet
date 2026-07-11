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
    """Build Markdown report (stub profile; expanded in D6)."""
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}
    hosts = [n for n in nodes if n.get("nugget_id") == "HOST"]
    cdns = [n for n in nodes if n.get("nugget_id") == "CDN"]
    services = [n for n in nodes if n.get("nugget_id") == "SERVICE"]

    lines = [
        f"# Httpx scan narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        (
            f"This report summarizes Httpx live-web probe output with **{len(hosts)}** HOST, "
            f"**{len(cdns)}** CDN, and **{len(services)}** service node(s)."
        ),
        "",
        "## Systems",
        "",
    ]
    for node in sorted(hosts + cdns, key=lambda n: (n.get("nugget_id", ""), n.get("nugget_data", ""))):
        lines.append(f"- `{node.get('nugget_id')}` `{node.get('nugget_data')}`")
    if not hosts and not cdns:
        lines.append("- (none)")

    lines.extend(["", "## Appendix", "", "### Nodes", ""])
    for node in sorted(nodes, key=lambda n: (n.get("nugget_id", ""), n.get("nugget_data", ""))):
        lines.append(f"- `{node.get('nugget_id')}`: {node.get('nugget_data')}")
    lines.extend(["", "### Edges", ""])
    for edge in edges:
        src = by_id.get(edge.get("source"), {})
        tgt = by_id.get(edge.get("target"), {})
        lines.append(
            f"- `{src.get('nugget_id')}` `{edge.get('relation')}` `{tgt.get('nugget_id')}`"
        )
    return "\n".join(lines).strip() + "\n"


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
