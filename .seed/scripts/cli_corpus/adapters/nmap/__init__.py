"""Nmap SPEC-004 adapter (`structured_native`)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from adapters.nmap.hooks import apply_nmap_hosts
from adapters.nmap.intermediate import parse_nmap_xml
from core.graph_builder import GraphBuilder, nugget_node
from core.rule_engine import RuleEngine, load_rule_pack
from narrative_report import build_nmap_narrative_report

CAPTURE_FAMILY: Literal["structured_native"] = "structured_native"
RULES_DIR = Path(__file__).resolve().parents[2] / "rules"


def _structured_doc(structured: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(structured, str):
        doc = json.loads(structured)
    else:
        doc = structured
    if doc.get("schema") != "nmap_scan_v1":
        raise ValueError("expected schema nmap_scan_v1")
    return doc


def to_structured(xml_text: str) -> dict[str, Any]:
    """Normalize native Nmap XML into the intermediate `nmap_scan_v1` document."""
    return parse_nmap_xml(xml_text)


def to_text(structured: dict[str, Any] | str) -> str:
    """Derive a human-readable text pane from structured Nmap scan data."""
    doc = _structured_doc(structured)
    lines = [
        f"Nmap scan report for {doc.get('scan_target', 'unknown')}",
        f"Command: {doc.get('command', '')}",
    ]
    if doc.get("startstr"):
        lines.append(f"Started: {doc['startstr']}")
    finished = doc.get("finished") or {}
    if finished.get("summary"):
        lines.append(str(finished["summary"]))

    for host in doc.get("hosts") or []:
        lines.append("")
        hostnames = host.get("hostnames") or []
        label = hostnames[0] if hostnames else host.get("host_key", "unknown")
        lines.append(f"Host: {label} ({host.get('host_key')})")
        status = (host.get("status") or {}).get("state")
        if status:
            lines.append(f"Status: {status}")
        open_ports = [
            f"{port.get('portid')}/{port.get('protocol')} {port.get('state', '')}"
            for port in host.get("ports") or []
            if port.get("state") in {"open", "filtered", "closed"}
        ]
        if open_ports:
            lines.append("Ports:")
            lines.extend(f"  {entry}" for entry in open_ports[:50])
    return "\n".join(lines).strip() + "\n"


def _add_scan_tool_descriptor(builder: GraphBuilder, scan_id: str) -> None:
    node = builder.add_node(nugget_node("SCAN_TOOL", "nmap", nugget_type="DESCRIPTOR"))
    builder.add_edge(scan_id, node["id"], "had")


def to_graph(structured: dict[str, Any] | str) -> dict[str, Any]:
    """Build graph via rule-engine scan head plus 06B hooks."""
    doc = _structured_doc(structured)
    rule_pack = load_rule_pack(RULES_DIR / "nmap" / "mapping.yaml", shared_dir=RULES_DIR / "_shared")
    engine = RuleEngine(rule_pack)

    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    engine._add_mapped_descriptors(builder, doc, scan["id"])
    _add_scan_tool_descriptor(builder, scan["id"])
    apply_nmap_hosts(builder, scan["id"], doc)
    return builder.build()


def to_narrative(graph: dict[str, Any], *, scenario_key: str = "nmap") -> str:
    """Build the Markdown report pane for an Nmap graph."""
    return build_nmap_narrative_report(graph, scenario_key)


def build_outputs(
    xml_text: str,
    *,
    scenario_key: str = "nmap",
) -> dict[str, Any]:
    """Return the four SPEC-004 UI outputs for one Nmap XML capture."""
    structured = to_structured(xml_text)
    graph = to_graph(structured)
    return {
        "text": to_text(structured),
        "structured": structured,
        "structured_json": json.dumps(structured, indent=2, sort_keys=True),
        "graph": graph,
        "markdown_report": to_narrative(graph, scenario_key=scenario_key),
    }
