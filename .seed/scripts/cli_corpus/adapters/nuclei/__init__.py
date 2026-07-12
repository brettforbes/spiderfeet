"""Nuclei SPEC-004 adapter (`structured_native`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from adapters.nuclei.hooks import apply_nuclei_records
from core.graph_builder import GraphBuilder, nugget_node
from core.rule_engine import RuleEngine, load_rule_pack
from nuclei_structured import (
    NUCLEI_STRUCTURED_SCHEMA,
    dumps_nuclei_bundle,
    parse_nuclei_structured,
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
        doc = parse_nuclei_structured(structured)
    else:
        doc = structured
    doc = {**doc, "schema": doc.get("schema") or NUCLEI_STRUCTURED_SCHEMA}
    if "records" not in doc:
        raise ValueError("expected nuclei bundle with records[]")
    if target and not doc.get("target"):
        doc["target"] = target
    if command and not doc.get("command"):
        doc["command"] = command
    if "scan_data" not in doc:
        target_value = doc.get("target") or "nuclei"
        cmd = doc.get("command") or "nuclei"
        doc["scan_data"] = f"nuclei:{target_value}:{cmd}"
    return doc


def to_structured(
    raw: str | dict[str, Any],
    *,
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Normalize Nuclei JSON/JSONL into the approved `nuclei_finding_v1` bundle."""
    return _structured_doc(raw, target=target, command=command)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Nuclei records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str, *, target: str | None = None) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 11B hooks."""
    doc = _structured_doc(structured, target=target)
    rule_pack = load_rule_pack(RULES_DIR / "nuclei" / "mapping.yaml", shared_dir=RULES_DIR / "_shared")
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "nuclei", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_nuclei_records(builder, scan["id"], doc)
    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "nuclei") -> str:
    """Build Markdown report with 11B phrasing from narrative.yaml."""
    from core.narrative_profile import append_standard_appendix, load_narrative_profile

    profile = load_narrative_profile(RULES_DIR / "nuclei" / "narrative.yaml")
    phrasing = profile.get("phrasing") or {}
    nodes = graph.get("nodes") or []
    hosts = [n for n in nodes if n.get("nugget_id") == "HOST"]
    findings = [n for n in nodes if n.get("nugget_id") == "NUCLEI_FINDING"]
    templates = [n for n in nodes if n.get("nugget_id") == "NUCLEI_TEMPLATE"]

    lines = [
        f"# Nuclei scan narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        (phrasing.get("introduction") or "").strip()
        or (
            f"This report summarizes Nuclei vulnerability scan output with **{len(hosts)}** host(s), "
            f"**{len(findings)}** finding(s), and **{len(templates)}** template(s)."
        ),
        "",
        "## Hosts",
        "",
    ]
    for host in sorted(hosts, key=lambda n: str(n.get("nugget_data"))):
        lines.append(f"- `{host.get('nugget_data')}`")
    if not hosts:
        lines.append("- (none)")

    lines.extend(["", "## Findings", ""])
    for finding in sorted(findings, key=lambda n: str(n.get("nugget_data"))):
        lines.append(f"- `{finding.get('nugget_data')}`")
    if not findings:
        lines.append("- (none)")

    deferral = (phrasing.get("relation_deferral") or "").strip()
    if deferral:
        lines.extend(["", "## Relation notes", "", deferral, ""])

    append_standard_appendix(lines, graph)
    return "\n".join(lines).strip() + "\n"


def build_outputs(
    raw: str | dict[str, Any],
    *,
    scenario_key: str = "nuclei",
    target: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Nuclei capture."""
    structured = to_structured(raw, target=target, command=command)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_json": dumps_nuclei_bundle(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
