"""Tests for shared-engine narrative reports from semantic graphs (SPEC-014 / Ontology §4.3)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
NMAP_GRAPH_PATH = (
    REPO_ROOT
    / ".docs/docs-for-cli-tools/nugget_structure/nmap_capstone_permissive_proposed_nuggets_edges.json"
)
NMAP_GENERATOR_PATH = CORPUS / "nmap_xml_to_graph.py"
NMAP_XML = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap/17_output_structured.xml"

if str(CORPUS) not in sys.path:
    sys.path.insert(0, str(CORPUS))

from core.narrative_engine import render_narrative  # noqa: E402
from narrative_report import validate_narrative_coverage  # noqa: E402


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_narrative_includes_required_sections():
    graph = json.loads(NMAP_GRAPH_PATH.read_text(encoding="utf-8"))
    report = render_narrative(graph, tool="nmap", scenario_key="capstone_permissive")

    for heading in (
        "## Introduction",
        "## Scan",
        "## Host",
        "## Conclusion",
        "## Appendix",
        "OS-Intel Scan",
        "```mermaid",
    ):
        assert heading in report


def test_narrative_covers_every_nugget_value():
    graph = json.loads(NMAP_GRAPH_PATH.read_text(encoding="utf-8"))
    report = render_narrative(graph, tool="nmap", scenario_key="capstone_permissive")
    ok, missing = validate_narrative_coverage(graph, report)
    assert ok, f"missing values: {missing[:10]}"


def test_narrative_mentions_ssh_keys_and_http_title():
    generator = _load_module(NMAP_GENERATOR_PATH, "nmap_xml_to_graph")
    graph = generator.nmap_xml_to_graph(NMAP_XML)
    report = render_narrative(graph, tool="nmap", scenario_key="nse_default_permissive")

    # Values must appear (SSH key material / HTTP title from NSE)
    assert "Go ahead and ScanMe!" in report
    assert any(token in report for token in ("ssh-ed25519", "ssh-rsa", "ECDSA", "RSA", "EDDSA", "DSA"))


def test_minimal_graph_produces_scan_only_story():
    graph = {
        "nodes": [
            {
                "id": "scan-1",
                "nugget_id": "SCAN_RECORD",
                "nugget_description": "Scan Record",
                "nugget_type": "ENTITY",
                "nugget_data": "scan:test",
                "data": "scan:test",
            },
            {
                "id": "scan-target",
                "nugget_id": "SCAN_TARGET",
                "nugget_description": "Scan Target",
                "nugget_type": "DESCRIPTOR",
                "nugget_data": "example.com",
                "data": "example.com",
            },
        ],
        "edges": [
            {"source": "scan-1", "target": "scan-target", "relation": "had"},
        ],
    }
    report = render_narrative(graph, tool="nmap", scenario_key="minimal")
    ok, missing = validate_narrative_coverage(graph, report)
    assert ok, missing
    assert "## Scan" in report
    assert "example.com" in report
    assert "## Host" not in report


def test_describe_graph_delegates_to_narrative_engine():
    generator = _load_module(NMAP_GENERATOR_PATH, "nmap_xml_to_graph")
    graph = generator.nmap_xml_to_graph(NMAP_XML)
    report = generator.describe_graph(graph, "nse_default_permissive")
    assert "scan narrative" in report.lower() or report.startswith("# Nmap")
    assert "## Appendix" in report
