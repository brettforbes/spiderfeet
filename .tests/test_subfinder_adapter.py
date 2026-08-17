"""Tests for the SPEC-004 Subfinder structured-native adapter (D2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import subfinder
from core.graph_builder import validate_graph
from core.rule_engine import load_rule_pack
from subfinder_structured import build_subfinder_bundle


def _passive_bundle() -> dict:
    return build_subfinder_bundle(
        [
            {
                "host": "[www.k2am.com.au](https://www.k2am.com.au)",
                "input": "k2am.com.au",
                "mode": "passive",
                "sources": ["crtsh", "hackertarget"],
            },
            {
                "host": "owa.k2am.com.au",
                "input": "k2am.com.au",
                "mode": "passive",
                "sources": ["crtsh"],
            },
        ],
        {
            "tool": "subfinder",
            "target": "k2am.com.au",
            "enumeration_mode": "passive",
            "command": "subfinder -d k2am.com.au -oJ -cs",
            "started_at": "2026-06-01T00:00:00+00:00",
            "duration_s": 1.0,
            "exit_code": 0,
            "scan_data": "subfinder:k2am.com.au:subfinder -d k2am.com.au -oJ -cs",
        },
    )


def _active_bundle() -> dict:
    return build_subfinder_bundle(
        [
            {
                "host": "owa.k2am.com.au",
                "input": "k2am.com.au",
                "mode": "active",
                "ip": "59.100.198.94",
                "sources": ["dns"],
            },
            {
                "host": "smtp2.k2am.com.au",
                "input": "k2am.com.au",
                "mode": "active",
                "ip": "59.100.198.94",
                "sources": ["dns"],
            },
        ],
        {
            "tool": "subfinder",
            "target": "k2am.com.au",
            "enumeration_mode": "active",
            "command": "subfinder -d k2am.com.au -active -oJ -oI",
            "started_at": "2026-06-01T00:00:00+00:00",
            "duration_s": 1.0,
            "exit_code": 0,
            "scan_data": "subfinder:k2am.com.au:subfinder -d k2am.com.au -active -oJ -oI",
        },
    )


def test_subfinder_rule_pack_loads_as_structured_native():
    rule_pack = load_rule_pack(RULES / "subfinder" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "subfinder"
    assert rule_pack.capture_family == "structured_native"


def test_subfinder_adapter_builds_four_outputs():
    outputs = subfinder.build_outputs(_passive_bundle(), scenario_key="corporate_k2am_passive_cs")

    assert "www.k2am.com.au" in outputs["text"]
    assert outputs["structured"]["schema"] == "subfinder_host_v1"
    validate_graph(outputs["graph"])
    assert "## Appendix" in outputs["markdown_report"]


def test_subfinder_s0_s2_s3_s6_passive_domain_shape():
    graph = subfinder.to_graph(_passive_bundle())
    nodes = graph["nodes"]
    edges = graph["edges"]

    assert any(n["nugget_id"] == "COMPANY" for n in nodes)
    assert any(n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "k2am.com.au" for n in nodes)
    www = next(n for n in nodes if n["nugget_id"] == "SUBDOMAIN" and n["nugget_data"] == "www.k2am.com.au")
    linked = {
        (n["nugget_id"], n["nugget_data"])
        for n in nodes
        if any(edge["source"] == www["id"] and edge["target"] == n["id"] for edge in edges)
    }

    assert ("DISCOVERY_SOURCE", "crtsh") in linked
    assert ("DISCOVERY_SOURCE", "hackertarget") in linked
    assert ("DISCOVERY_MODE", "passive") in linked
    assert ("LIVENESS_STATUS", "unconfirmed") in linked


def test_subfinder_s4_active_ip_bridge_uses_allowed_relation():
    graph = subfinder.to_graph(_active_bundle())
    nodes = graph["nodes"]
    edges = graph["edges"]

    ip = next(
        n
        for n in nodes
        if n["nugget_id"] in {"IP_ADDRESS", "IPV4_ADDRESS"} and n["nugget_data"] == "59.100.198.94"
    )
    linked_domains = [
        edge["source"]
        for edge in edges
        if edge["target"] == ip["id"] and edge["relation"] == "had"
    ]
    assert len(linked_domains) == 2
    assert any(n["nugget_id"] == "CDN_REVIEW_NEEDED" for n in nodes)
    assert all(edge["relation"] in {"contains", "had", "listens-to"} for edge in edges)


def test_subfinder_converter_delegates_to_adapter():
    from subfinder_json_to_graph import subfinder_to_graph

    raw = json.dumps(_active_bundle())
    graph = subfinder_to_graph(raw, "k2am.com.au", "subfinder -d k2am.com.au -active -oJ -oI")

    assert any(n["nugget_id"] == "SUBDOMAIN" for n in graph["nodes"])
    assert any(n["nugget_id"] in {"IP_ADDRESS", "IPV4_ADDRESS"} for n in graph["nodes"])
    validate_graph(graph)
