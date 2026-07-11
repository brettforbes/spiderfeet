"""Tests for the SPEC-004 Katana structured-native adapter (D4)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import katana
from core.graph_builder import validate_graph
from core.rule_engine import load_rule_pack
from katana_structured import build_katana_bundle


def _katana_bundle() -> dict:
    return build_katana_bundle(
        [
            {
                "url": "https://www.k2am.com.au/about",
                "request": {"endpoint": "https://www.k2am.com.au/about", "method": "GET"},
                "response": {"status_code": 200},
            },
            {
                "url": "https://www.k2am.com.au/contact",
                "request": {"endpoint": "https://www.k2am.com.au/contact", "method": "GET"},
                "response": {"status_code": 301},
            },
        ],
        {
            "tool": "katana",
            "target": "k2am.com.au",
            "httpx_scenario": "from_subfinder_k2am_passive",
            "crawl_profile": "depth-2,fqdn-scope,concurrency-5",
            "url_input_count": 1,
            "command": "katana -list urls.txt -silent -j",
            "started_at": "2026-06-01T00:00:00+00:00",
            "duration_s": 1.0,
            "exit_code": 0,
            "scan_data": "katana:k2am.com.au:katana -list urls.txt -silent -j",
        },
    )


def test_katana_rule_pack_loads_as_structured_native():
    rule_pack = load_rule_pack(RULES / "katana" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "katana"
    assert rule_pack.capture_family == "structured_native"


def test_katana_adapter_builds_four_outputs():
    outputs = katana.build_outputs(_katana_bundle(), scenario_key="from_httpx_k2am_passive")

    assert "https://www.k2am.com.au/about" in outputs["text"]
    assert outputs["structured"]["schema"] == "katana_crawl_v1"
    validate_graph(outputs["graph"])
    assert "## Appendix" in outputs["markdown_report"]


def test_katana_adapter_preserves_url_domain_status_hierarchy():
    graph = katana.to_graph(_katana_bundle())
    nodes = graph["nodes"]

    assert any(n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "k2am.com.au" for n in nodes)
    assert any(n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "www.k2am.com.au" for n in nodes)
    assert any(n["nugget_id"] == "LINKED_URL_INTERNAL" and n["nugget_data"].endswith("/about") for n in nodes)
    assert any(n["nugget_id"] == "HTTP_STATUS_CODE" and n["nugget_data"] == "200" for n in nodes)
    assert any(n["nugget_id"] == "SCAN_CRAWL_PROFILE" for n in nodes)
    assert any(n["nugget_id"] == "UPSTREAM_SCENARIO_ID" for n in nodes)


def test_katana_converter_delegates_to_adapter():
    from katana_json_to_graph import katana_to_graph

    raw = json.dumps(_katana_bundle())
    graph = katana_to_graph(raw, "k2am.com.au", "katana -list urls.txt -silent -j")

    assert any(n["nugget_id"] == "LINKED_URL_INTERNAL" for n in graph["nodes"])
    validate_graph(graph)
