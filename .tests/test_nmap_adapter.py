"""Tests for the SPEC-004 Nmap structured-native adapter."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"
NMAP_XML = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap/17_output_structured.xml"
CORPORATE_TOP_PORTS_XML = (
    REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap/21_output_structured.xml"
)

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import nmap
from core.graph_builder import validate_graph
from core.rule_engine import load_rule_pack


def test_nmap_rule_pack_loads_as_structured_native():
    rule_pack = load_rule_pack(RULES / "nmap" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "nmap"
    assert rule_pack.capture_family == "structured_native"
    assert rule_pack.scan_head.get("data_path") == "scan_data"


def test_nmap_adapter_builds_four_outputs():
    xml_text = NMAP_XML.read_text(encoding="utf-8")
    outputs = nmap.build_outputs(xml_text, scenario_key="adapter_nse_default")

    assert outputs["text"].startswith("Nmap scan report")
    assert outputs["structured"]["schema"] == "nmap_scan_v1"
    assert outputs["structured"]["hosts"]
    assert json.loads(outputs["structured_json"])["schema"] == "nmap_scan_v1"
    validate_graph(outputs["graph"])
    assert any(node["nugget_id"] == "HOST" for node in outputs["graph"]["nodes"])
    assert any(node["nugget_id"] == "SERVICE" for node in outputs["graph"]["nodes"])
    assert "## Appendix" in outputs["markdown_report"]


def test_nmap_adapter_emits_ssh_keys_and_multiple_os_candidates():
    xml_text = NMAP_XML.read_text(encoding="utf-8")
    graph = nmap.to_graph(nmap.to_structured(xml_text))
    nugget_ids = {node["nugget_id"] for node in graph["nodes"]}

    assert {"DSA", "RSA", "ECDSA", "EDDSA"}.issubset(nugget_ids)
    assert "HTTP_TITLE" in nugget_ids
    os_nodes = [node for node in graph["nodes"] if node["nugget_id"] == "OPERATING_SYSTEM"]
    assert len(os_nodes) >= 2


def test_nmap_adapter_links_services_to_ports():
    xml_text = CORPORATE_TOP_PORTS_XML.read_text(encoding="utf-8")
    graph = nmap.to_graph(nmap.to_structured(xml_text))
    nodes = {node["id"]: node for node in graph["nodes"]}
    listens = {
        (nodes[edge["source"]]["nugget_data"], nodes[edge["target"]]["nugget_data"])
        for edge in graph["edges"]
        if edge["relation"] == "listens-to"
        and nodes[edge["source"]]["nugget_id"] == "SERVICE"
        and nodes[edge["target"]]["nugget_id"] == "PORT"
    }

    assert len(listens) == 20
    assert ("https", "443") in listens
