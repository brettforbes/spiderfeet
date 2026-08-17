"""Tests for the SPEC-004 Pius structured-native adapter (D1)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_CORPUS = REPO_ROOT / ".seed" / "scripts" / "cli_corpus"
RULES = CLI_CORPUS / "rules"
FIXTURE_NDJSON = CLI_CORPUS / "fixtures" / "pius_linode_crt_sample.jsonl"

if str(CLI_CORPUS) not in sys.path:
    sys.path.insert(0, str(CLI_CORPUS))

from adapters import pius
from adapters.pius.classify import classify_record, normalize_value
from core.graph_builder import validate_graph
from core.pius_lists import load_pius_lists
from core.rule_engine import load_rule_pack
from pius_structured import build_pius_bundle, parse_ndjson


def _linode_bundle() -> dict:
    records = parse_ndjson(FIXTURE_NDJSON.read_text(encoding="utf-8"))
    return build_pius_bundle(
        records,
        {
            "tool": "pius",
            "org": "Linode",
            "target": "linode.com",
            "command": "pius run --org Linode --domain linode.com --plugins crt-sh --output ndjson",
            "started_at": "2026-06-01T00:00:00+00:00",
            "duration_s": 1.0,
            "exit_code": 0,
            "scan_data": "pius:Linode:pius run --org Linode --domain linode.com --plugins crt-sh --output ndjson",
        },
    )


def test_pius_rule_pack_loads_as_structured_native():
    rule_pack = load_rule_pack(RULES / "pius" / "mapping.yaml", shared_dir=RULES / "_shared")

    assert rule_pack.tool == "pius"
    assert rule_pack.capture_family == "structured_native"


def test_pius_lists_load():
    data = load_pius_lists()
    assert data["schema"] == "pius_lists_v1"
    assert "CEO" in data["placeholders"]


def test_pius_r0_unwraps_markdown_links():
    normalized = normalize_value("[www.squarepeg.vc](https://www.squarepeg.vc)")
    assert normalized.candidate_value == "www.squarepeg.vc"


def test_pius_r2_preseed_becomes_candidate_entity():
    classification = classify_record(
        {"Type": "preseed", "Value": "Akamai Technologies, Inc.", "Source": "whois", "Data": {}}
    )
    assert classification is not None
    assert classification.nugget_id == "CANDIDATE_ENTITY"


def test_pius_adapter_builds_four_outputs():
    bundle = _linode_bundle()
    outputs = pius.build_outputs(bundle, scenario_key="crt_linode_ndjson", org="Linode")

    assert "status.linode.com" in outputs["text"]
    assert outputs["structured"]["schema"] == "pius_finding_v1"
    assert len(outputs["structured"]["records"]) >= 10
    validate_graph(outputs["graph"])
    assert "## Appendix" in outputs["markdown_report"]


def test_pius_adapter_emits_company_and_domains_for_linode():
    graph = pius.to_graph(_linode_bundle())
    nugget_ids = {n["nugget_id"] for n in graph["nodes"]}

    assert "COMPANY" in nugget_ids
    assert "DOMAIN_NAME" in nugget_ids
    assert "DOMAINS" in nugget_ids
    assert "CANDIDATE_ENTITY" in nugget_ids
    assert any(n["nugget_data"] == "Linode" and n["nugget_id"] == "COMPANY_NAME" for n in graph["nodes"])
    assert any(
        n["nugget_data"] == "status.linode.com" for n in graph["nodes"] if n["nugget_id"] == "DOMAIN_NAME"
    )


def test_pius_r10_wildcard_banner_tags_domains():
    bundle = _linode_bundle()
    bundle["stderr_banner"] = (
        "INFO wildcard detected base=news.example.com ips_count=1\n"
        "INFO wildcard detected, filtering subdomains parent=news.example.com\n"
    )
    bundle["records"] = list(bundle["records"]) + [
        {"Type": "domain", "Value": "news.example.com", "Source": "crt-sh", "Data": {"org": "Linode"}}
    ]
    graph = pius.to_graph(bundle)
    domain = next(
        n for n in graph["nodes"] if n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "news.example.com"
    )
    descriptors = {
        (n["nugget_id"], n["nugget_data"])
        for n in graph["nodes"]
        if any(e["target"] == n["id"] and e["source"] == domain["id"] for e in graph["edges"])
    }
    assert ("IS_WILDCARD_DNS", "true") in descriptors
    assert ("SUBDOMAIN_ENUMERATION_SUPPRESSED", "true") in descriptors


def test_cli_tool_to_graph_delegates_to_pius_adapter():
    from cli_tool_to_graph import pius_to_graph

    raw = FIXTURE_NDJSON.read_text(encoding="utf-8")
    graph = pius_to_graph(raw, "Linode", "pius run --org Linode --domain linode.com --output ndjson")
    assert any(n["nugget_id"] == "DOMAIN_NAME" for n in graph["nodes"])
    validate_graph(graph)


