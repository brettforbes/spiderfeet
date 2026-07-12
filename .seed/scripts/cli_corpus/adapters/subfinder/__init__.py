"""Subfinder SPEC-004 adapter (`structured_native`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from adapters.subfinder.hooks import apply_subfinder_records
from core.graph_builder import GraphBuilder, nugget_node
from core.rule_engine import RuleEngine, load_rule_pack
from subfinder_structured import (
    SUBFINDER_STRUCTURED_SCHEMA,
    dumps_subfinder_bundle,
    parse_subfinder_structured,
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
        doc = parse_subfinder_structured(structured)
    else:
        doc = structured
    doc = {**doc, "schema": doc.get("schema") or SUBFINDER_STRUCTURED_SCHEMA}
    if "records" not in doc:
        raise ValueError("expected subfinder bundle with records[]")
    if target and not doc.get("target"):
        doc["target"] = target
    if command and not doc.get("command"):
        doc["command"] = command
    if "enumeration_mode" not in doc:
        has_ip = any(isinstance(record, dict) and record.get("ip") for record in doc.get("records") or [])
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
    """Normalize Subfinder JSON/JSONL into the approved `subfinder_host_v1` bundle."""
    return _structured_doc(raw, target=target, command=command)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Subfinder records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str, *, target: str | None = None) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 09 S0-S6 hooks."""
    doc = _structured_doc(structured, target=target)
    rule_pack = load_rule_pack(
        RULES_DIR / "subfinder" / "mapping.yaml", shared_dir=RULES_DIR / "_shared"
    )
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "subfinder", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_subfinder_records(builder, scan["id"], doc)
    return builder.build()


def _load_narrative_profile() -> dict[str, Any]:
    import yaml

    path = RULES_DIR / "subfinder" / "narrative.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "subfinder") -> str:
    """Build Markdown report (stub profile; expanded in D6)."""
    profile = _load_narrative_profile()
    phrasing = profile.get("phrasing") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}
    domains = [n for n in nodes if n.get("nugget_id") == "DOMAIN_NAME"]
    ips = [n for n in nodes if n.get("nugget_id") == "IP_ADDRESS"]

    lines = [
        f"# Subfinder scan narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        (phrasing.get("introduction") or "").strip()
        or (
            f"This report summarizes Subfinder domain enumeration with **{len(domains)}** "
            f"domain node(s) and **{len(ips)}** resolved IP node(s)."
        ),
        "",
        "## Domains",
        "",
    ]
    if domains:
        for domain in sorted(domains, key=lambda n: str(n.get("nugget_data"))):
            lines.append(f"- `{domain.get('nugget_data')}`")
    else:
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
        "structured_json": dumps_subfinder_bundle(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
