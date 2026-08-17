"""SPEC-019 F4 — HTTPX website root owns HTTP status and homepage URL."""

from __future__ import annotations

from modules_v2._core.graph_builder import GraphBuilder, validate_graph
from modules_v2._core.rule_engine import RuleEngine, load_rule_pack
from modules_v2._core.paths import SHARED_RULES_DIR, mapping_path
from modules_v2.adapters.httpx.hooks import apply_httpx_records


def _graph(doc: dict) -> dict:
    rule_pack = load_rule_pack(mapping_path("httpx"), shared_dir=SHARED_RULES_DIR)
    engine = RuleEngine(rule_pack)
    builder = GraphBuilder()
    scan = engine._add_scan_head(builder, doc)
    apply_httpx_records(builder, scan["id"], doc)
    graph = builder.build()
    validate_graph(graph)
    return graph


def test_httpx_apex_and_subdomain_own_status_and_homepage() -> None:
    doc = {
        "target": "k2am.com.au",
        "records": [
            {
                "url": "https://k2am.com.au/",
                "input": "k2am.com.au",
                "status_code": 200,
                "title": "Home",
            },
            {
                "url": "https://www.k2am.com.au/",
                "input": "www.k2am.com.au",
                "status_code": 301,
                "title": "WWW",
            },
        ],
    }
    graph = _graph(doc)
    nodes = graph["nodes"]
    edges = graph["edges"]

    apex = next(n for n in nodes if n["nugget_id"] == "DOMAIN_NAME" and n["nugget_data"] == "k2am.com.au")
    www = next(n for n in nodes if n["nugget_id"] == "SUBDOMAIN" and n["nugget_data"] == "www.k2am.com.au")

    def had(parent_id: str, nugget_id: str, value: str) -> bool:
        for n in nodes:
            if n["nugget_id"] != nugget_id or str(n["nugget_data"]) != value:
                continue
            if any(e["source"] == parent_id and e["target"] == n["id"] and e["relation"] == "had" for e in edges):
                return True
        return False

    assert had(apex["id"], "HTTP_STATUS_CODE", "200")
    assert had(www["id"], "HTTP_STATUS_CODE", "301")
    home = next(n for n in nodes if n["nugget_id"] == "LINKED_URL_INTERNAL" and n["nugget_data"].endswith("k2am.com.au/"))
    assert any(e["source"] == apex["id"] and e["target"] == home["id"] and e["relation"] == "contains" for e in edges)
