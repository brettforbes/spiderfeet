"""Pius SPEC-004 adapter (`structured_native`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from adapters.pius.hooks import apply_pius_records
from core.graph_builder import GraphBuilder, nugget_node
from core.rule_engine import RuleEngine, load_rule_pack
from pius_structured import (
    PIUS_STRUCTURED_SCHEMA,
    dumps_pius_bundle,
    parse_pius_structured,
    structured_to_text,
)

CAPTURE_FAMILY: Literal["structured_native"] = "structured_native"
RULES_DIR = Path(__file__).resolve().parents[2] / "rules"


def _structured_doc(
    structured: dict[str, Any] | str,
    *,
    org: str | None = None,
    command: str | None = None,
) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = parse_pius_structured(structured)
    else:
        doc = structured
    doc = {**doc, "schema": doc.get("schema") or PIUS_STRUCTURED_SCHEMA}
    if org and not doc.get("org"):
        doc["org"] = org
    if command and not doc.get("command"):
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
    """Normalize Pius JSON/NDJSON into the approved `pius_finding_v1` bundle."""
    return _structured_doc(raw, org=org, command=command)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive the Text pane from structured Pius records."""
    doc = _structured_doc(structured)
    return structured_to_text(doc.get("records") or [])


def to_graph(structured: dict[str, Any] | str, *, org: str | None = None) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 08 hooks."""
    doc = _structured_doc(structured, org=org)
    rule_pack = load_rule_pack(RULES_DIR / "pius" / "mapping.yaml", shared_dir=RULES_DIR / "_shared")
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "pius", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_pius_records(builder, scan["id"], doc)
    return builder.build()


def _load_narrative_profile() -> dict[str, Any]:
    import yaml

    path = RULES_DIR / "pius" / "narrative.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "pius") -> str:
    """Build Markdown report (stub profile; expanded in D6)."""
    profile = _load_narrative_profile()
    phrasing = profile.get("phrasing") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}

    companies = [n for n in nodes if n.get("nugget_id") == "COMPANY_NAME"]
    domains = [n for n in nodes if n.get("nugget_id") == "DOMAIN_NAME"]
    affiliates = [n for n in nodes if n.get("nugget_id") == "AFFILIATE_COMPANY_NAME"]
    leads = [n for n in nodes if n.get("nugget_id") == "CANDIDATE_ENTITY"]

    lines = [
        f"# Pius scan narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        (phrasing.get("introduction") or "").strip()
        or (
            f"This report summarizes organizational attack-surface findings from a Pius capture. "
            f"**{len(domains)}** domain(s), **{len(affiliates)}** affiliate company record(s), "
            f"and **{len(leads)}** research lead(s) were emitted."
        ),
        "",
        "## Organization",
        "",
    ]
    if companies:
        for company in companies:
            lines.append(f"- `{company.get('nugget_data')}`")
    else:
        lines.append("- (no head company node)")

    lines.extend(["", "## Domains", ""])
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
        "structured_json": dumps_pius_bundle(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
