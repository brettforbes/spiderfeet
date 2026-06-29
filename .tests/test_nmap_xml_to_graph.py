"""Tests for Nmap XML to CLI profiling nugget graph generation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = REPO_ROOT / ".seed/scripts/cli_corpus/nmap_xml_to_graph.py"
NMAP_XML = REPO_ROOT / ".docs/docs-for-cli-tools/app_examination_docs/nmap/17_output_structured.xml"


def _load_generator():
    import sys

    spec = importlib.util.spec_from_file_location("nmap_xml_to_graph", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["nmap_xml_to_graph"] = module
    spec.loader.exec_module(module)
    return module


def test_nmap_xml_graph_parses_ssh_keys_and_http_title():
    generator = _load_generator()
    graph = generator.nmap_xml_to_graph(NMAP_XML)
    nodes = graph["nodes"]
    nugget_ids = {node["nugget_id"] for node in nodes}

    assert {"DSA", "RSA", "ECDSA", "EDDSA"}.issubset(nugget_ids)
    assert "HTTP_TITLE" in nugget_ids

    by_id = {node["id"]: node for node in nodes}
    ssh_key_node_ids = {
        node["id"]
        for node in nodes
        if node["nugget_id"] in {"DSA", "RSA", "ECDSA", "EDDSA"}
    }
    assert ssh_key_node_ids
    assert all(
        by_id[edge["source"]]["nugget_id"] == "SERVICE"
        and edge["relation"] == "contains"
        for edge in graph["edges"]
        if edge["target"] in ssh_key_node_ids
    )


def test_nmap_xml_graph_uses_template_fields_and_normalized_values():
    generator = _load_generator()
    graph = generator.nmap_xml_to_graph(NMAP_XML)
    required = {
        "id",
        "nugget_instance_id",
        "nugget_id",
        "nugget_description",
        "nugget_type",
        "nugget_event_type",
        "nugget_icon",
        "nugget_colour",
        "nugget_data",
        "nugget_source_data",
        "nugget_module",
        "nugget_confidence",
        "data",
    }

    for node in graph["nodes"]:
        assert required.issubset(node)
        assert node["id"] == node["nugget_instance_id"]
        assert node["nugget_instance_id"].startswith(f"{node['nugget_id']}--")

    port_values = {node["nugget_data"] for node in graph["nodes"] if node["nugget_id"] == "PORT"}
    service_values = {
        node["nugget_data"] for node in graph["nodes"] if node["nugget_id"] == "SERVICE"
    }
    assert "22" in port_values
    assert "80" in port_values
    assert "ssh" in service_values
    assert "http" in service_values


def test_nmap_xml_graph_and_description_are_deterministic():
    generator = _load_generator()
    first = generator.nmap_xml_to_graph(NMAP_XML)
    second = generator.nmap_xml_to_graph(NMAP_XML)

    assert first == second
    assert generator.describe_graph(first, "nse_default_permissive") == generator.describe_graph(
        second,
        "nse_default_permissive",
    )
