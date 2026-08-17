"""SPEC-019 F3 — Subfinder COMPANY / SUBDOMAIN hierarchy."""

from __future__ import annotations

from modules_v2._core.graph_builder import GraphBuilder, validate_graph
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2._core.graph_builder import nugget_node
from modules_v2.adapters.subfinder.hooks import apply_subfinder_records


def _graph(doc: dict) -> dict:
    rule_pack = load_rule_pack(mapping_path("subfinder"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)
    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    apply_subfinder_records(builder, scan["id"], doc)
    graph = builder.build()
    validate_graph(graph)
    return graph


def test_subfinder_company_domain_subdomain_tree() -> None:
    doc = {
        "target": "k2am.com.au",
        "enumeration_mode": "passive",
        "records": [
            {"host": "www.k2am.com.au", "sources": ["crtsh"], "mode": "passive"},
            {"host": "owa.k2am.com.au", "sources": ["crtsh"], "mode": "passive"},
        ],
    }
    graph = _graph(doc)
    nodes = graph["nodes"]
    edges = graph["edges"]

    company = next(n for n in nodes if n["nugget_id"] == "COMPANY")
    apex = next(n for n in nodes if n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "k2am.com.au")
    subs = [n for n in nodes if n["nugget_id"] == "SUBDOMAIN"]
    assert company["nugget_data"] == "company:k2am.com.au"
    assert any(e["source"] == company["id"] and e["target"] == apex["id"] and e["relation"] == "contains" for e in edges)
    assert {n["nugget_data"] for n in subs} == {"www.k2am.com.au", "owa.k2am.com.au"}
    assert all(
        any(e["source"] == apex["id"] and e["target"] == s["id"] and e["relation"] == "contains" for e in edges)
        for s in subs
    )
    assert not any(
        e["relation"] == "contains" and e["target"] in {s["id"] for s in subs} and e["source"] != apex["id"]
        for e in edges
    )
