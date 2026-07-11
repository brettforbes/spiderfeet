"""Tests for CLI tool graph generators."""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
GRAPH_SCRIPT = REPO_ROOT / ".seed" / "scripts" / "cli_corpus" / "cli_tool_to_graph.py"
GRAPH_BUILDER_SCRIPT = REPO_ROOT / ".seed" / "scripts" / "cli_corpus" / "graph_builder.py"


@pytest.fixture(scope="module")
def graph_mod():
    import importlib.util

    spec = importlib.util.spec_from_file_location("cli_tool_to_graph", GRAPH_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def graph_builder_mod():
    import importlib.util

    spec = importlib.util.spec_from_file_location("graph_builder", GRAPH_BUILDER_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_netdiscover_rejects_raw_text(graph_mod):
    raw = "172.18.0.1\t00:15:5d:c1:a8:4a\t1\t42\tMicrosoft Corporation\n"
    with pytest.raises(ValueError, match="netdiscover_scan JSON"):
        graph_mod.netdiscover_to_graph(raw, "local", "netdiscover -P")


def test_cli_tool_graph_uses_shared_identity_helper(graph_mod, graph_builder_mod):
    node = graph_mod._node("IP_ADDRESS", "ENTITY", "172.18.0.1", "IP Address")
    expected_id = graph_builder_mod.nugget_instance_id("IP_ADDRESS", "172.18.0.1")
    assert node["id"] == expected_id
    assert node["nugget_instance_id"] == expected_id


def test_cli_tool_graph_has_no_divergent_uuid_helper():
    source = GRAPH_SCRIPT.read_text(encoding="utf-8")
    assert "def _uid" not in source
    assert "uuid.NAMESPACE_DNS" not in source
    assert "nugget_id}:{data" not in source


def test_core_graph_builder_import_and_legacy_shim_match(graph_builder_mod):
    import importlib
    import sys

    cli_corpus = str(GRAPH_BUILDER_SCRIPT.parent)
    if cli_corpus not in sys.path:
        sys.path.insert(0, cli_corpus)

    core_graph_builder = importlib.import_module("core.graph_builder")

    assert graph_builder_mod.GraphBuilder is core_graph_builder.GraphBuilder
    assert graph_builder_mod.nugget_instance_id("IP_ADDRESS", "172.18.0.1") == (
        core_graph_builder.nugget_instance_id("IP_ADDRESS", "172.18.0.1")
    )


def test_nerva_graph_from_jsonl(graph_mod):
    raw = json.dumps(
        {
            "schema": "nerva_fingerprint_v1",
            "records": [
                {
                    "host": "scanme.nmap.org",
                    "ip": "45.33.32.156",
                    "port": 80,
                    "protocol": "http",
                    "transport": "tcp",
                    "version": "Apache/2.4.7",
                }
            ],
        }
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
    assert "DOMAIN_NAME" in types
    assert any(n["nugget_id"] == "CANDIDATE_ENTITY" and n["nugget_data"] == "Acme" for n in g["nodes"])
    assert all(n["nugget_data"] != "Acme" or n["nugget_id"] != "DOMAIN_NAME" for n in g["nodes"])


def test_capstone_graph_artifacts_exist():
    for path in (
        "nugget_structure/netdiscover_local_subnet_active_parsable_proposed_nuggets_edges.json",
        "nugget_structure/nerva_tcp_http_rich_json_proposed_nuggets_edges.json",
        "nugget_structure/pius_corporate_bbc_gleif_ndjson_proposed_nuggets_edges.json",
    ):
        full = REPO_ROOT / ".docs" / "docs-for-cli-tools" / path
        assert full.is_file(), path
        data = json.loads(full.read_text(encoding="utf-8"))
        assert data["nodes"] and data["edges"]
