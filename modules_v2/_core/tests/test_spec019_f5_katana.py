"""SPEC-019 F5 — Katana URLs owned by website roots."""

from __future__ import annotations

from modules_v2._core.graph_builder import GraphBuilder, validate_graph
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2.adapters.katana.hooks import apply_katana_records


def _graph(doc: dict) -> dict:
    rule_pack = load_rule_pack(mapping_path("katana"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)
    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    apply_katana_records(builder, scan["id"], doc)
    graph = builder.build()
    validate_graph(graph)
    return graph


def test_katana_internal_urls_under_subdomain_external_off_apex() -> None:
    doc = {
        "target": "k2am.com.au",
        "records": [
            {"url": "https://www.k2am.com.au/about", "request": {"endpoint": "https://www.k2am.com.au/about"}},
            {"url": "https://evil.example.com/x", "request": {"endpoint": "https://evil.example.com/x"}},
        ],
    }
    graph = _graph(doc)
    nodes = graph["nodes"]
    edges = graph["edges"]
    www = next(n for n in nodes if n["nugget_id"] == "SUBDOMAIN" and n["nugget_data"] == "www.k2am.com.au")
    internal = next(n for n in nodes if n["nugget_id"] == "LINKED_URL_INTERNAL")
    external = next(n for n in nodes if n["nugget_id"] == "LINKED_URL_EXTERNAL")
    assert any(e["source"] == www["id"] and e["target"] == internal["id"] for e in edges)
    assert not any(e["target"] == external["id"] and e["relation"] == "contains" and e["source"] == www["id"] for e in edges)
