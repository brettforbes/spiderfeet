"""Tests for SPEC-004 sfp_adapter_bridge (Epic E2)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
NMAP_XML = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap/17_output_structured.xml"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import nmap as nmap_adapter
from core.graph_builder import validate_graph
from sfp_adapter_bridge import graph_entity_events, nmap_graph_from_xml


def test_nmap_bridge_matches_adapter_graph():
    raw = NMAP_XML.read_text(encoding="utf-8")
    target = "scanme.nmap.org"
    command = "nmap -sT -A -T3 -p 22,80,443 -oX - scanme.nmap.org"

    bridged = nmap_graph_from_xml(raw, target=target, command=command)
    direct = nmap_adapter.to_graph(nmap_adapter.to_structured(raw))

    assert bridged == direct
    validate_graph(bridged)
    assert any(n["nugget_id"] == "HOST" for n in bridged["nodes"])


def test_graph_entity_events_extracts_entities_only():
    graph = {
        "nodes": [
            {"nugget_id": "HOST", "nugget_data": "example.com", "nugget_type": "ENTITY"},
            {"nugget_id": "HTTP_TITLE", "nugget_data": "Welcome", "nugget_type": "DESCRIPTOR"},
        ],
        "edges": [],
    }
    assert graph_entity_events(graph) == [("HOST", "example.com")]
