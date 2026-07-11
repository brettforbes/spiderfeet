"""SPEC-004 Phase 4 structural golden signatures (not byte-locked graphs)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
FIXTURES = CLI_CORPUS / "fixtures"
GOLDENS_PATH = REPO_ROOT / ".tests" / "spec004_structural_goldens.json"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import httpx, katana, nuclei, pius, subfinder
from nuclei_structured import build_nuclei_bundle, parse_ndjson
from pius_structured import build_pius_bundle, parse_ndjson as parse_pius_ndjson
from subfinder_structured import build_subfinder_bundle


def graph_signature(graph: dict) -> dict:
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}
    node_sig = sorted(f"{n['nugget_id']}|{n['nugget_data']}" for n in nodes)
    edge_sig = sorted(
        f"{by_id[e['source']]['nugget_id']}|{e['relation']}|{by_id[e['target']]['nugget_id']}"
        for e in edges
        if e.get("source") in by_id and e.get("target") in by_id
    )
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": node_sig,
        "edges": edge_sig,
    }


def _pius_graph() -> dict:
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


def _subfinder_graph() -> dict:
    bundle = build_subfinder_bundle(
        [{"host": "owa.k2am.com.au", "input": "k2am.com.au", "mode": "passive", "sources": ["crtsh"]}],
        {
            "tool": "subfinder",
            "target": "k2am.com.au",
            "enumeration_mode": "passive",
            "command": "subfinder -d k2am.com.au -oJ -cs",
            "scan_data": "subfinder:k2am.com.au:subfinder -d k2am.com.au -oJ -cs",
        },
    )
    return subfinder.to_graph(bundle)


def _httpx_graph() -> dict:
    from httpx_structured import build_httpx_bundle

    bundle = build_httpx_bundle(
        [{"url": "https://www.k2am.com.au", "host": "www.k2am.com.au", "scheme": "https", "port": "443", "status_code": 200}],
        {"tool": "httpx", "target": "k2am.com.au", "command": "httpx -l hosts.txt -json", "scan_data": "httpx:k2am.com.au:httpx"},
    )
    return httpx.to_graph(bundle)


def _katana_graph() -> dict:
    from katana_structured import build_katana_bundle

    bundle = build_katana_bundle(
        [{"url": "https://www.k2am.com.au/about", "request": {"method": "GET"}, "response": {"status_code": 200}}],
        {"tool": "katana", "target": "k2am.com.au", "command": "katana -list urls.txt -j", "scan_data": "katana:k2am.com.au:katana"},
    )
    return katana.to_graph(bundle)


def _nuclei_graph() -> dict:
    records = parse_ndjson((FIXTURES / "nuclei_cve_critical_sample.jsonl").read_text(encoding="utf-8"))
    bundle = build_nuclei_bundle(
        records,
        {"tool": "nuclei", "target": "app.example.com", "command": "nuclei -jsonl", "scan_data": "nuclei:app.example.com:nuclei"},
    )
    return nuclei.to_graph(bundle)


SCENARIOS = {
    "pius_linode": _pius_graph,
    "subfinder_k2am": _subfinder_graph,
    "httpx_k2am": _httpx_graph,
    "katana_k2am": _katana_graph,
    "nuclei_cve_critical": _nuclei_graph,
}


@pytest.mark.parametrize("scenario_key", sorted(SCENARIOS))
def test_structural_golden_signature_matches(scenario_key: str):
    goldens = json.loads(GOLDENS_PATH.read_text(encoding="utf-8"))
    assert scenario_key in goldens, f"missing structural golden for {scenario_key}"
    current = graph_signature(SCENARIOS[scenario_key]())
    expected = goldens[scenario_key]
    assert current == expected, scenario_key
