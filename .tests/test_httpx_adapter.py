"""Tests for the SPEC-004 Httpx structured-native adapter (D3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import httpx
from core.graph_builder import validate_graph
from core.rule_engine import load_rule_pack
from httpx_structured import build_httpx_bundle


def _httpx_bundle() -> dict:
    return build_httpx_bundle(
        [
            {
                "url": "https://www.k2am.com.au/",
                "input": "www.k2am.com.au",
                "host": "101.0.68.158",
                "port": "443",
                "scheme": "https",
                "status_code": 200,
                "title": "K2 Asset Management",
                "webserver": "Apache",
                "content_type": "text/html",
                "content_length": 12345,
                "method": "GET",
                "path": "/",
                "time": "120.5ms",
                "words": 321,
                "lines": 42,
                "failed": False,
                "timestamp": "2026-06-01T00:00:00Z",
                "tech": ["PHP", "Chart.js:2.4.0"],
                "a": ["101.0.68.158"],
                "knowledgebase": {"PageType": "nonerror", "pHash": 123},
            },
            {
                "url": "https://ksm.k2am.com.au/",
                "input": "ksm.k2am.com.au",
                "host": "104.18.34.21",
                "port": "443",
                "scheme": "https",
                "status_code": 409,
                "cdn": True,
                "cdn_name": "cloudflare",
                "cdn_type": "waf",
                "cname": ["unbouncepages.com"],
                "a": ["104.18.34.21", "172.64.153.235"],
                "knowledgebase": {"PageType": "error", "pHash": 456},
            },
        ],
        {
            "tool": "httpx",
            "target": "k2am.com.au",
            "subfinder_scenario": "corporate_k2am_passive_cs",
            "probe_profile": "status-code,title,tech-detect,server,cdn,ip",
            "host_input_count": 18,
            "command": "httpx -l hosts.txt -status-code -title -tech-detect -server -cdn -ip -json",
            "started_at": "2026-06-01T00:00:00+00:00",
            "duration_s": 1.0,
            "exit_code": 0,
            "scan_data": "httpx:k2am.com.au:httpx -l hosts.txt",
        },
    )


def test_httpx_rule_pack_loads_as_structured_native():
    rule_pack = load_rule_pack(RULES / "httpx" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "httpx"
    assert rule_pack.capture_family == "structured_native"


def test_httpx_adapter_builds_four_outputs():
    outputs = httpx.build_outputs(_httpx_bundle(), scenario_key="from_subfinder_k2am_passive")

    assert "www.k2am.com.au" in outputs["text"]
    assert outputs["structured"]["schema"] == "httpx_probe_v1"
    validate_graph(outputs["graph"])
    assert "## Appendix" in outputs["markdown_report"]


def test_httpx_h1_h2_h3_host_and_cdn_chains():
    graph = httpx.to_graph(_httpx_bundle())
    nodes = graph["nodes"]
    edges = graph["edges"]

    assert any(n["nugget_id"] == "HOST" and n["nugget_data"] == "101.0.68.158" for n in nodes)
    assert any(n["nugget_id"] == "CDN" and n["nugget_data"] == "104.18.34.21" for n in nodes)
    assert any(n["nugget_id"] == "NETWORKS" for n in nodes)
    assert any(n["nugget_id"] == "APPLICATIONS" for n in nodes)
    assert any(edge["relation"] == "listens-to" for edge in edges)
    assert all(edge["relation"] in {"contains", "had", "listens-to"} for edge in edges)


def test_httpx_h4_software_version_and_h5_cname():
    graph = httpx.to_graph(_httpx_bundle())
    nodes = graph["nodes"]

    assert any(n["nugget_id"] == "SOFTWARE_USED" and n["nugget_data"] == "Chart.js" for n in nodes)
    assert any(n["nugget_id"] == "SOFTWARE_VERSION" and n["nugget_data"] == "2.4.0" for n in nodes)
    assert any(n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "unbouncepages.com" for n in nodes)
    assert any(n["nugget_id"] == "CNAME_TARGET" and n["nugget_data"] == "unbouncepages.com" for n in nodes)


def test_httpx_h6_h7_probe_connected_and_http_liveness():
    graph = httpx.to_graph(_httpx_bundle())
    nodes = graph["nodes"]

    assert any(n["nugget_id"] == "PROBE_CONNECTED" and n["nugget_data"] == "true" for n in nodes)
    assert any(n["nugget_id"] == "PROBE_CONNECTED" and n["nugget_data"] == "false" for n in nodes)
    assert any(n["nugget_id"] == "HTTP_LIVENESS_STATUS" and n["nugget_data"] == "confirmed" for n in nodes)
    assert any(n["nugget_id"] == "HTTP_LIVENESS_STATUS" and n["nugget_data"] == "unconfirmed" for n in nodes)
    assert any(n["nugget_id"] == "UPSTREAM_SCENARIO_ID" for n in nodes)


def test_httpx_converter_delegates_to_adapter():
    from httpx_json_to_graph import httpx_to_graph

    raw = json.dumps(_httpx_bundle())
    graph = httpx_to_graph(raw, "k2am.com.au", "httpx -l hosts.txt -json")

    assert any(n["nugget_id"] == "HOST" for n in graph["nodes"])
    assert any(n["nugget_id"] == "CDN" for n in graph["nodes"])
    validate_graph(graph)
