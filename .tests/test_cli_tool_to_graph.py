"""Tests for CLI tool graph generators."""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
GRAPH_SCRIPT = REPO_ROOT / ".seed" / "scripts" / "cli_corpus" / "cli_tool_to_graph.py"


@pytest.fixture(scope="module")
def graph_mod():
    import importlib.util

    spec = importlib.util.spec_from_file_location("cli_tool_to_graph", GRAPH_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_netdiscover_parse_sample(graph_mod):
    raw = "172.18.0.1\t00:15:5d:c1:a8:4a\t1\t42\tMicrosoft Corporation\n"
    rows = graph_mod.parse_netdiscover_p(raw)
    assert len(rows) == 1
    assert rows[0]["IP"] == "172.18.0.1"


def test_nerva_graph_from_jsonl(graph_mod):
    raw = (
        '{"host":"scanme.nmap.org","ip":"45.33.32.156","port":80,'
        '"protocol":"http","transport":"tcp","version":"Apache/2.4.7"}\n'
    )
    g = graph_mod.nerva_to_graph(raw, "scanme.nmap.org:80", "nerva -t scanme.nmap.org:80 --json")
    assert len(g["nodes"]) >= 5
    assert any(n["nugget_id"] == "SERVICE" for n in g["nodes"])


def test_pius_graph_filters_preseed(graph_mod):
    raw = (
        '{"Type":"preseed","Value":"Acme","Source":"whois"}\n'
        '{"Type":"domain","Value":"api.example.com","Source":"crt-sh"}\n'
    )
    g = graph_mod.pius_to_graph(raw, "Acme Corp", "pius run --org Acme")
    types = {n["nugget_id"] for n in g["nodes"]}
    assert "INTERNET_NAME" in types
    assert all(n["nugget_data"] != "Acme" or n["nugget_id"] != "INTERNET_NAME" for n in g["nodes"])


def test_capstone_graph_artifacts_exist():
    for path in (
        "nugget_structure/netdiscover_local_subnet_active_parsable_proposed_nuggets_edges.json",
        "nugget_structure/nerva_tcp_scanme_http_json_proposed_nuggets_edges.json",
        "nugget_structure/pius_passive_bbc_corporate_ndjson_proposed_nuggets_edges.json",
    ):
        full = REPO_ROOT / ".docs" / "docs-for-cli-tools" / path
        assert full.is_file(), path
        data = json.loads(full.read_text(encoding="utf-8"))
        assert data["nodes"] and data["edges"]
