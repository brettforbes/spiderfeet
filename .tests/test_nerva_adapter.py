"""Tests for the SPEC-004 Nerva structured-native adapter (C3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"
FIXTURE = CLI_CORPUS / "fixtures" / "nerva_correlation_seed07.json"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import nerva
from core.graph_builder import validate_graph
from core.rule_engine import load_rule_pack


def test_nerva_rule_pack_loads_as_structured_native():
    rule_pack = load_rule_pack(RULES / "nerva" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "nerva"
    assert rule_pack.capture_family == "structured_native"


def test_nerva_adapter_builds_four_outputs():
    raw = FIXTURE.read_text(encoding="utf-8")
    outputs = nerva.build_outputs(raw, scenario_key="seed07_appendix", command="nerva -l targets --json")

    assert "praetorian.com" in outputs["text"] or "scanme.nmap.org" in outputs["text"]
    assert outputs["structured"]["schema"] == "nerva_fingerprint_v1"
    assert outputs["structured"]["records"]
    validate_graph(outputs["graph"])
    assert "## Appendix" in outputs["markdown_report"]


def test_nerva_adapter_qualifies_praetorian_as_single_cdn():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    graph = nerva.to_graph(doc)
    cdn_nodes = [n for n in graph["nodes"] if n["nugget_id"] == "CDN"]
    praetorian_hosts = [
        n for n in graph["nodes"] if n["nugget_id"] == "HOST" and "praetorian" in str(n["nugget_data"])
    ]

    assert len(cdn_nodes) == 1
    assert cdn_nodes[0]["nugget_data"] == "praetorian.com"
    assert not praetorian_hosts
    assert any(n["nugget_id"] == "CDN_VENDOR" and n["nugget_data"] == "Cloudflare" for n in graph["nodes"])


def test_nerva_adapter_scanme_dual_stack_is_host_not_cdn():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    scanme_only = {
        "schema": "nerva_fingerprint_v1",
        "command": "nerva -t scanme.nmap.org --json",
        "records": [r for r in doc["records"] if r["host"] == "scanme.nmap.org"],
    }
    graph = nerva.to_graph(scanme_only)
    host_nodes = [n for n in graph["nodes"] if n["nugget_id"] == "HOST"]
    cdn_nodes = [n for n in graph["nodes"] if n["nugget_id"] == "CDN"]

    assert len(host_nodes) == 1
    assert not cdn_nodes
    assert any(n["nugget_id"] == "SERVICE" and n["nugget_data"] == "ssh" for n in graph["nodes"])


def test_nerva_adapter_suppresses_origin_fingerprints_when_fronted():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for record in doc["records"]:
        if record["host"] != "praetorian.com":
            continue
        metadata = record.setdefault("metadata", {})
        metadata["technologies"] = ["Cloudflare", "nginx", "checkpoint-gateway"]
        metadata["fingerprint_metadata"] = {
            "nginx": {"vendor": "F5", "product": "Nginx", "detection_method": "error_page"},
            "checkpoint-gateway": {"vendor": "Check Point", "product": "Security Gateway"},
        }
    graph = nerva.to_graph(doc)
    suppressed = [n for n in graph["nodes"] if n["nugget_id"] == "ORIGIN_FINGERPRINT_SUPPRESSED"]
    assert suppressed
    assert any(n["nugget_data"] == "True" for n in suppressed)


def test_cli_tool_to_graph_delegates_to_nerva_adapter():
    from cli_tool_to_graph import nerva_to_graph

    raw = FIXTURE.read_text(encoding="utf-8")
    graph = nerva_to_graph(raw, "targets", "nerva -l targets --json")
    assert any(n["nugget_id"] == "CDN" for n in graph["nodes"])
    assert any(n["nugget_id"] == "HOST" for n in graph["nodes"])
