"""SPEC-019 F8 — apex DOMAIN_NAME / COMPANY validator + synthetic hierarchy."""

from __future__ import annotations

import pytest

from modules_v2._core.domain_hierarchy_validator import validate_apex_domain_company_parent
from modules_v2._core.graph_builder import GraphBuilder, nugget_node, validate_graph
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2.adapters.subfinder.hooks import apply_subfinder_records
from modules_v2.adapters.httpx.hooks import apply_httpx_records
from modules_v2.adapters.katana.hooks import apply_katana_records


def _subfinder_graph() -> dict:
    rule_pack = load_rule_pack(mapping_path("subfinder"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)
    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, {"target": "k2am.com.au"})
    apply_subfinder_records(
        builder,
        scan["id"],
        {
            "target": "k2am.com.au",
            "records": [{"host": "www.k2am.com.au", "sources": ["crtsh"], "mode": "passive"}],
        },
    )
    graph = builder.build()
    validate_graph(graph)
    validate_apex_domain_company_parent(graph, apex="k2am.com.au")
    return graph


def test_validator_rejects_apex_without_company() -> None:
    builder = GraphBuilder()
    scan = builder.add_node(nugget_node("SCAN_RECORD", "scan:test", description="Scan Record"))
    apex = builder.add_node(
        nugget_node("DOMAIN_NAME", "example.com", description="Domain Name"),
        parent_id=scan["id"],
    )
    builder.add_edge(scan["id"], apex["id"], "contains")
    graph = builder.build(validate=False)
    validate_graph(graph)
    with pytest.raises(ValueError, match="COMPANY"):
        validate_apex_domain_company_parent(graph, apex="example.com")


def test_validator_allows_incidental_domain_without_company() -> None:
    builder = GraphBuilder()
    scan = builder.add_node(nugget_node("SCAN_RECORD", "scan:test", description="Scan Record"))
    company = builder.add_node(
        nugget_node("COMPANY", "company:example.com", description="Company"),
        parent_id=scan["id"],
    )
    apex = builder.add_node(
        nugget_node("DOMAIN_NAME", "example.com", description="Domain Name"),
        parent_id=company["id"],
    )
    builder.add_edge(scan["id"], company["id"], "contains")
    builder.add_edge(company["id"], apex["id"], "contains")
    incidental = builder.add_node(nugget_node("DOMAIN_NAME", "cdn.other.net", description="Domain Name"))
    builder.add_edge(scan["id"], incidental["id"], "contains")
    graph = builder.build(validate=False)
    validate_graph(graph)
    validate_apex_domain_company_parent(graph, apex="example.com")


def test_subfinder_synthetic_hierarchy_passes_validator() -> None:
    _subfinder_graph()


def test_httpx_status_on_website_root() -> None:
    doc = {
        "target": "k2am.com.au",
        "records": [
            {
                "url": "https://k2am.com.au/",
                "input": "k2am.com.au",
                "status_code": 200,
                "title": "Home",
            },
        ],
    }
    rule_pack = load_rule_pack(mapping_path("httpx"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)
    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    apply_httpx_records(builder, scan["id"], doc)
    graph = builder.build()
    validate_apex_domain_company_parent(graph, apex="k2am.com.au")
    nodes = graph["nodes"]
    apex = next(n for n in nodes if n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "k2am.com.au")
    home = next(
        n
        for n in nodes
        if n["nugget_id"] == "LINKED_URL_INTERNAL" and str(n["nugget_data"]).endswith("k2am.com.au/")
    )
    assert any(
        e["source"] == apex["id"] and e["target"] == home["id"] and e["relation"] == "contains"
        for e in graph["edges"]
    )


def test_katana_pages_under_matching_host() -> None:
    rule_pack = load_rule_pack(mapping_path("katana"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)
    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, {"target": "k2am.com.au"})
    apply_katana_records(
        builder,
        scan["id"],
        {
            "target": "k2am.com.au",
            "records": [
                {
                    "url": "https://www.k2am.com.au/about",
                    "host": "www.k2am.com.au",
                }
            ],
        },
    )
    graph = builder.build()
    validate_apex_domain_company_parent(graph, apex="k2am.com.au")
    subs = [n for n in graph["nodes"] if n["nugget_id"] == "SUBDOMAIN"]
    assert any(n["nugget_data"] == "www.k2am.com.au" for n in subs)
