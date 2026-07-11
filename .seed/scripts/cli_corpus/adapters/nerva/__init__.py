"""Nerva SPEC-004 adapter (`structured_native`)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from adapters.nerva.hooks import apply_nerva_records
from core.graph_builder import GraphBuilder, nugget_node
from core.rule_engine import RuleEngine, load_rule_pack
from nerva_structured import (
    NERVA_STRUCTURED_SCHEMA,
    dumps_nerva_bundle,
    parse_nerva_structured,
    structured_to_text,
)

CAPTURE_FAMILY: Literal["structured_native"] = "structured_native"
RULES_DIR = Path(__file__).resolve().parents[2] / "rules"


def _structured_doc(structured: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = parse_nerva_structured(structured)
    else:
        doc = structured
    if doc.get("schema") and doc.get("schema") != NERVA_STRUCTURED_SCHEMA:
        # Accept bundles that omit schema but always normalize.
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
    """Normalize Nerva JSON/JSONL into the approved `nerva_fingerprint_v1` bundle."""
    if isinstance(raw, dict):
        doc = _structured_doc(raw)
    else:
        doc = _structured_doc(raw)
    if command and not doc.get("command"):
        doc["command"] = command
    if command and doc.get("command") == "nerva":
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
    rule_pack = load_rule_pack(RULES_DIR / "nerva" / "mapping.yaml", shared_dir=RULES_DIR / "_shared")
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    tool = builder.add_node(nugget_node("SCAN_TOOL", "nerva", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan["id"], tool["id"], "had")
    apply_nerva_records(builder, scan["id"], doc)
    return builder.build()


def _load_narrative_profile() -> dict[str, Any]:
    import yaml

    path = RULES_DIR / "nerva" / "narrative.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "nerva") -> str:
    """Build Markdown report with CDN / indeterminate-origin phrasing from narrative.yaml."""
    profile = _load_narrative_profile()
    phrasing = profile.get("phrasing") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}
    systems = [n for n in nodes if n.get("nugget_id") in {"HOST", "CDN"}]
    cdn_nodes = [n for n in systems if n.get("nugget_id") == "CDN"]
    host_nodes = [n for n in systems if n.get("nugget_id") == "HOST"]
    suppressed = [n for n in nodes if n.get("nugget_id") == "ORIGIN_FINGERPRINT_SUPPRESSED"]
    vendors = sorted({n.get("nugget_data") for n in nodes if n.get("nugget_id") == "CDN_VENDOR"})

    lines = [
        f"# Nerva scan narrative — `{scenario_key}`",
        "",
        "## Introduction",
        "",
        (
            f"This report summarizes a Nerva fingerprint capture after Rulesets A/C/B "
            f"qualification. **{len(systems)}** system node(s) were emitted "
            f"({len(host_nodes)} HOST, {len(cdn_nodes)} CDN)."
        ),
        "",
        "## Systems",
        "",
    ]
    for system in systems:
        classification = next(
            (
                by_id[e["target"]].get("nugget_data")
                for e in edges
                if e.get("source") == system["id"]
                and e.get("relation") == "had"
                and by_id.get(e.get("target"), {}).get("nugget_id") == "HOST_CLASSIFICATION"
            ),
            None,
        )
        lines.append(
            f"- `{system.get('nugget_id')}` `{system.get('nugget_data')}`"
            + (f" — classification `{classification}`" if classification else "")
        )

    lines.extend(["", "## CDN / edge fronting", ""])
    if cdn_nodes:
        lines.append((phrasing.get("fronted_unknown") or "").strip())
        lines.append("")
        if vendors:
            lines.append(f"Detected vendor(s): **{', '.join(str(v) for v in vendors if v)}**.")
            lines.append("")
        lines.append(
            "Origin host count is **"
            + str(phrasing.get("indeterminate_origin_count") or "indeterminate")
            + "** — edge IP cardinality must not be treated as origin host count."
        )
        lines.append("")
    else:
        lines.append((phrasing.get("standard_host") or "No CDN fronting detected.").strip())
        lines.append("")

    if suppressed:
        lines.extend(
            [
                "## Origin fingerprint suppression",
                "",
                (phrasing.get("origin_fingerprint_suppressed") or "").strip(),
                "",
                f"Suppressed fingerprint markers present: **{len(suppressed)}**.",
                "",
            ]
        )

    services = [n for n in nodes if n.get("nugget_id") == "SERVICE"]
    lines.extend(["## Services", ""])
    if services:
        for service in services:
            lines.append(f"- `{service.get('nugget_data')}`")
    else:
        lines.append("- (none)")
    lines.append("")

    lines.extend(["## Appendix", "", "### Nodes", ""])
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
    scenario_key: str = "nerva",
    command: str | None = None,
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Nerva capture."""
    structured = to_structured(raw, command=command)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_json": dumps_nerva_bundle(structured),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
