"""Tests for SPEC-005 narrative engine v2."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from core.narrative_engine import (
    build_factual_intro,
    render_narrative,
    type_relation_mermaid,
    validate_narrative_coverage,
)


SAMPLE_GRAPH = {
    "nodes": [
        {"id": "s1", "nugget_id": "SCAN_RECORD", "nugget_data": "nmap:scanme:cmd"},
        {"id": "h1", "nugget_id": "HOST", "nugget_data": "scanme.nmap.org"},
        {"id": "ip1", "nugget_id": "IP_ADDRESS", "nugget_data": "45.33.32.156"},
    ],
    "edges": [
        {"source": "s1", "target": "h1", "relation": "contains"},
        {"source": "h1", "target": "ip1", "relation": "contains"},
    ],
}


def test_type_relation_mermaid_has_no_ip_literals():
    md = type_relation_mermaid(SAMPLE_GRAPH)
    assert "45.33.32.156" not in md
    assert "SCAN_RECORD" in md
    assert "IP_ADDRESS" in md
    assert "```mermaid" in md


def test_build_factual_intro_mentions_tool():
    intro = build_factual_intro(tool="nuclei", profile={"tool_name": "Nuclei"})
    assert "Nuclei" in intro
    assert "Scan" in intro or "scan" in intro.lower()


def test_render_narrative_nmap_preserves_quality_sections():
    md = render_narrative(SAMPLE_GRAPH, tool="nmap", scenario_key="tcp_top_ports_permissive")
    assert "## Introduction" in md
    assert "## Appendix" in md
    ok, missing = validate_narrative_coverage(SAMPLE_GRAPH, md)
    assert ok, missing


def test_render_narrative_generic_tool_has_appendix():
    md = render_narrative(SAMPLE_GRAPH, tool="httpx", scenario_key="from_subfinder_k2am_active")
    assert "## Introduction" in md
    assert "## Appendix" in md
    assert not re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", md.split("## Appendix")[0])
