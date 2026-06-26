"""Tests for template-driven narrative reports from semantic graphs (Ontology §4.3)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NARRATIVE_PATH = REPO_ROOT / ".seed/scripts/cli_corpus/narrative_report.py"
NMAP_GRAPH_PATH = (
    REPO_ROOT
    / ".docs/docs-for-cli-tools/nugget_structure/nmap_capstone_permissive_proposed_nuggets_edges.json"
)
NMAP_GENERATOR_PATH = REPO_ROOT / ".seed/scripts/cli_corpus/nmap_xml_to_graph.py"
NMAP_XML = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap/17_output_structured.xml"


def _load_module(path: Path, name: str):
    import sys

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _load_narrative():
    return _load_module(NARRATIVE_PATH, "narrative_report")


def _load_nmap_generator():
    return _load_module(NMAP_GENERATOR_PATH, "nmap_xml_to_graph")


def test_narrative_includes_required_sections():
    narrative = _load_narrative()
    graph = json.loads(NMAP_GRAPH_PATH.read_text(encoding="utf-8"))
    report = narrative.build_nmap_narrative_report(graph, "capstone_permissive")

    for heading in (
        "## Introduction",
        "## Scan",
        "## Host ",
        "## Conclusion",
        "## Appendix",
        "OS-Intel Scan",
        "```mermaid",
    ):
        assert heading in report


def test_narrative_covers_every_nugget_value():
    narrative = _load_narrative()
    graph = json.loads(NMAP_GRAPH_PATH.read_text(encoding="utf-8"))
    report = narrative.build_nmap_narrative_report(graph, "capstone_permissive")
    ok, missing = narrative.validate_narrative_coverage(graph, report)
    assert ok, f"missing values: {missing[:10]}"


def test_narrative_mentions_ssh_keys_and_http_title():
    narrative = _load_narrative()
    generator = _load_nmap_generator()
    graph = generator.nmap_xml_to_graph(NMAP_XML)
    report = narrative.build_nmap_narrative_report(graph, "nse_default_permissive")

    assert "SSH host key" in report or "SSH Key" in report
    assert "Go ahead and ScanMe!" in report


def test_minimal_graph_produces_scan_only_story():
    narrative = _load_narrative()
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
    report = narrative.build_nmap_narrative_report(graph, "minimal")
    ok, missing = narrative.validate_narrative_coverage(graph, report)
    assert ok, missing
    assert "## Scan" in report
    assert "example.com" in report
    assert "## Host " not in report


def test_describe_graph_delegates_to_narrative_engine():
    generator = _load_nmap_generator()
    graph = generator.nmap_xml_to_graph(NMAP_XML)
    report = generator.describe_graph(graph, "nse_default_permissive")
    assert report.startswith("# Nmap OSINT Scan Report")
    assert "## Appendix" in report
