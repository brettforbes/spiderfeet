"""Narrative coverage smoke tests for SPEC-004 D1-D5 structured-native adapters."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
FIXTURES = CLI_CORPUS / "fixtures"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import httpx, katana, nuclei, pius, subfinder
from narrative_report import validate_narrative_coverage
from nuclei_structured import build_nuclei_bundle, parse_ndjson
from pius_structured import build_pius_bundle, parse_ndjson as parse_pius_ndjson
from subfinder_structured import build_subfinder_bundle


def _pius_graph():
    records = parse_pius_ndjson((FIXTURES / "pius_linode_crt_sample.jsonl").read_text(encoding="utf-8"))
    bundle = build_pius_bundle(
        records,
        {
            "tool": "pius",
            "org": "Linode",
            "target": "linode.com",
            "command": "pius run --org Linode --domain linode.com --output ndjson",
            "scan_data": "pius:Linode:pius run --org Linode --domain linode.com --output ndjson",
        },
    )
    return pius.to_graph(bundle)


def _subfinder_graph():
    bundle = build_subfinder_bundle(
        [
            {
                "host": "owa.k2am.com.au",
                "input": "k2am.com.au",
                "mode": "passive",
                "sources": ["crtsh"],
            }
        ],
        {
            "tool": "subfinder",
            "target": "k2am.com.au",
            "enumeration_mode": "passive",
            "command": "subfinder -d k2am.com.au -oJ -cs",
            "scan_data": "subfinder:k2am.com.au:subfinder -d k2am.com.au -oJ -cs",
        },
    )
    return subfinder.to_graph(bundle)


def _httpx_graph():
    from httpx_structured import build_httpx_bundle

    bundle = build_httpx_bundle(
        [
            {
                "url": "https://www.k2am.com.au",
                "input": "https://www.k2am.com.au",
                "host": "www.k2am.com.au",
                "scheme": "https",
                "port": "443",
                "status_code": 200,
                "title": "Home",
            }
        ],
        {
            "tool": "httpx",
            "target": "k2am.com.au",
            "command": "httpx -l hosts.txt -json",
            "scan_data": "httpx:k2am.com.au:httpx -l hosts.txt -json",
        },
    )
    return httpx.to_graph(bundle)


def _katana_graph():
    from katana_structured import build_katana_bundle

    bundle = build_katana_bundle(
        [
            {
                "url": "https://www.k2am.com.au/about",
                "request": {"endpoint": "https://www.k2am.com.au/about", "method": "GET"},
                "response": {"status_code": 200},
            }
        ],
        {
            "tool": "katana",
            "target": "k2am.com.au",
            "command": "katana -list urls.txt -silent -j",
            "scan_data": "katana:k2am.com.au:katana -list urls.txt -silent -j",
        },
    )
    return katana.to_graph(bundle)


def _nuclei_graph():
    records = parse_ndjson((FIXTURES / "nuclei_cve_critical_sample.jsonl").read_text(encoding="utf-8"))
    bundle = build_nuclei_bundle(
        records,
        {
            "tool": "nuclei",
            "target": "app.example.com",
            "command": "nuclei -u https://app.example.com -silent -jsonl",
            "scan_data": "nuclei:app.example.com:nuclei -u https://app.example.com -silent -jsonl",
        },
    )
    return nuclei.to_graph(bundle)


@pytest.mark.parametrize(
    ("tool", "graph_fn", "narrative_fn", "scenario_key", "required_phrase"),
    [
        ("pius", _pius_graph, pius.to_narrative, "crt_linode_ndjson", "Organization"),
        ("subfinder", _subfinder_graph, subfinder.to_narrative, "corporate_k2am_passive_cs", "Domains"),
        ("httpx", _httpx_graph, httpx.to_narrative, "from_subfinder_k2am", "Systems"),
        ("katana", _katana_graph, katana.to_narrative, "from_httpx_k2am", "URLs"),
        ("nuclei", _nuclei_graph, nuclei.to_narrative, "cve_critical_sample", "Findings"),
    ],
)
def test_d1_d5_narrative_profiles_cover_all_node_values(
    tool: str,
    graph_fn,
    narrative_fn,
    scenario_key: str,
    required_phrase: str,
):
    graph = graph_fn()
    markdown = narrative_fn(graph, scenario_key=scenario_key)

    assert required_phrase in markdown
    assert "## Appendix" in markdown
    ok, missing = validate_narrative_coverage(graph, markdown, require_appendix=True)
    assert ok, f"{tool} narrative missing values: {missing[:8]}"
