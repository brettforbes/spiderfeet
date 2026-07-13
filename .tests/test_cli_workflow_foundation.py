"""SPEC-007 foundation tests: schema, GSE, context merge."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".seed" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.context_export import merge_graph  # noqa: E402
from cli_workflow.core.gse_eval import eval_binding, eval_select  # noqa: E402
from cli_workflow.core.loader import (  # noqa: E402
    load_workflow,
    topological_waves,
    validate_workflow_dict,
)
from cli_workflow.core.normalize import hostname_from_url  # noqa: E402

NUGGET = ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"
EXAMPLE = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"


def test_hostname_from_url():
    assert hostname_from_url("https://example.com/path") == "example.com"
    assert hostname_from_url("example.com") == "example.com"


def test_workflow_example_loads_and_waves():
    doc = load_workflow(EXAMPLE, validate=True)
    waves = topological_waves(doc["steps"])
    assert waves is not None
    assert waves[0] == ["subfinder_enum"]
    assert set(waves[1]) == {"nmap_ports", "httpx_live"}


def test_context_merge_unique():
    g1 = {
        "nodes": [{"id": "A", "nugget_id": "HOST", "nugget_data": "h1"}],
        "edges": [{"source": "A", "target": "B", "relation": "contains"}],
    }
    g2 = {
        "nodes": [
            {"id": "A", "nugget_id": "HOST", "nugget_data": "h1"},
            {"id": "C", "nugget_id": "IP_ADDRESS", "nugget_data": "1.2.3.4"},
        ],
        "edges": [
            {"source": "A", "target": "B", "relation": "contains"},
            {"source": "A", "target": "C", "relation": "contains"},
        ],
    }
    ctx: dict = {"nodes": [], "edges": []}
    merge_graph(ctx, g1)
    merge_graph(ctx, g2)
    assert len(ctx["nodes"]) == 2
    assert len(ctx["edges"]) == 2


def test_gse_subfinder_domains():
    path = NUGGET / "subfinder_corporate_upside_au_passive_cs_proposed_nuggets_edges.json"
    if not path.is_file():
        pytest.skip("subfinder fixture missing")
    graph = json.loads(path.read_text(encoding="utf-8"))
    apex = eval_select(
        {
            "source": "$step.scan_graph",
            "nodes": {
                "nugget_id": "DOMAIN_NAME",
                "where": [
                    {
                        "not": {
                            "related": {
                                "direction": "out",
                                "relation": "had",
                                "nugget_id": "DOMAIN_NAME_PARENT",
                            }
                        }
                    }
                ],
            },
            "project": "nugget_data",
            "distinct": True,
        },
        graph,
    )
    subs = eval_select(
        {
            "source": "$step.scan_graph",
            "nodes": {
                "nugget_id": "DOMAIN_NAME",
                "where": [
                    {
                        "related": {
                            "direction": "out",
                            "relation": "had",
                            "nugget_id": "DOMAIN_NAME_PARENT",
                        }
                    }
                ],
            },
            "project": "nugget_data",
            "distinct": True,
        },
        graph,
    )
    assert len(subs) > 0
    assert set(apex).isdisjoint(set(subs))
    merged = eval_binding(
        {
            "type": "string_list",
            "union": ["a", "b"],
            "distinct": True,
        },
        env_lists={"a": apex, "b": subs},
    )
    assert set(merged) == set(apex) | set(subs)


def test_gse_nmap_ip_port_product():
    path = NUGGET / "nmap_tcp_top_ports_permissive_proposed_nuggets_edges.json"
    if not path.is_file():
        pytest.skip("nmap fixture missing")
    graph = json.loads(path.read_text(encoding="utf-8"))
    values = eval_select(
        {
            "source": "$step.scan_graph",
            "for_each": {
                "as": "endpoint",
                "nodes": {"nugget_id_in": ["HOST", "SYSTEM", "DEVICE", "CDN", "SERVER"]},
                "collect": [
                    {
                        "as": "ip",
                        "reachable_from": "endpoint",
                        "along": {"relation": "contains", "transitive": True},
                        "nodes": {"nugget_id_in": ["IP_ADDRESS", "IPV6_ADDRESS"]},
                        "project": "nugget_data",
                    },
                    {
                        "as": "port",
                        "reachable_from": "endpoint",
                        "along": {"relation": "contains", "transitive": True},
                        "nodes": {"nugget_id": "PORT"},
                        "project": "nugget_data",
                    },
                ],
                "emit": {"product": ["ip", "port"], "join": ":"},
            },
            "distinct": True,
        },
        graph,
    )
    assert len(values) > 0
    assert any(":" in v for v in values)
    # spot-check shape
    assert all(v.count(":") == 1 for v in values)


def test_invalid_workflow_rejected():
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    doc["steps"][0]["uses"] = "tool.not_a_real_tool"
    with pytest.raises(Exception):
        validate_workflow_dict(doc)
