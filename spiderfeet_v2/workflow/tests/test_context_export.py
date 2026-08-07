"""SPEC-010 AM3 / R10-22 — context.export mark + append-unique merge."""

from __future__ import annotations

from pathlib import Path

import pytest

from spiderfeet_v2.workflow.context_export import (
    EXPORT_NONE,
    EXPORT_SCAN_GRAPH,
    apply_context_export,
    empty_context,
    export_steps,
    is_marked_for_export,
    mark_scan_result_for_export,
    merge_graph,
    merge_graphs,
    step_context_export,
    step_exports_scan_graph,
)
from spiderfeet_v2.workflow.loader import load_workflow

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"


@pytest.fixture(scope="module")
def doc_12a():
    return load_workflow(EXAMPLE_12A, validate=True)


def _node(nid: str, nugget_id: str = "DOMAIN_NAME", data: str | None = None) -> dict:
    return {
        "id": nid,
        "nugget_instance_id": nid,
        "nugget_id": nugget_id,
        "nugget_data": data or nid,
    }


def _edge(src: str, tgt: str, rel: str = "had") -> dict:
    return {"source": src, "target": tgt, "relation": rel}


def test_12a_export_marks(doc_12a):
    by_id = {s["id"]: s for s in doc_12a["steps"]}
    assert step_exports_scan_graph(by_id["sfp_cli_subfinder"]) is True
    assert step_exports_scan_graph(by_id["sfp_cli_nmap"]) is True
    assert step_exports_scan_graph(by_id["sfp_cli_nerva"]) is True
    assert step_exports_scan_graph(by_id["sfp_cli_nuclei"]) is True
    assert step_exports_scan_graph(by_id["sfp_cli_httpx"]) is False
    assert step_exports_scan_graph(by_id["sfp_cli_katana"]) is False
    assert step_context_export(by_id["sfp_cli_httpx"]) == EXPORT_NONE
    assert export_steps(doc_12a["steps"]) == [
        "sfp_cli_subfinder",
        "sfp_cli_nmap",
        "sfp_cli_nerva",
        "sfp_cli_nuclei",
    ]


def test_mark_scan_result_for_export():
    graph = {"nodes": [_node("a")], "edges": []}
    export_step = {"id": "s1", "context": {"export": EXPORT_SCAN_GRAPH}}
    none_step = {"id": "s2", "context": {"export": EXPORT_NONE}}
    omitted = {"id": "s3"}

    marked = mark_scan_result_for_export(graph, export_step)
    assert marked["context_export"] == EXPORT_SCAN_GRAPH
    assert marked["export_to_temporary_context"] is True
    assert is_marked_for_export(marked) is True
    # original unchanged
    assert "context_export" not in graph

    marked_none = mark_scan_result_for_export(graph, none_step)
    assert marked_none["context_export"] == EXPORT_NONE
    assert marked_none["export_to_temporary_context"] is False
    assert is_marked_for_export(marked_none) is False

    assert mark_scan_result_for_export(graph, omitted)["export_to_temporary_context"] is False


def test_merge_overlapping_graphs_dedupes_nodes_and_edges():
    """Verification gate: two overlapping scan graphs → deduped nodes/edges."""
    g1 = {
        "nodes": [
            _node("n1", data="shared.example.com"),
            _node("n2", data="only-g1.example.com"),
        ],
        "edges": [
            _edge("n2", "n1", "had"),
            _edge("n1", "n1", "contains"),  # self-edge kept once
        ],
    }
    g2 = {
        "nodes": [
            _node("n1", data="shared.example.com"),  # overlap by id
            _node("n3", data="only-g2.example.com"),
            # alternate id key only
            {
                "nugget_instance_id": "n2",
                "nugget_id": "DOMAIN_NAME",
                "nugget_data": "only-g1.example.com",
            },
        ],
        "edges": [
            _edge("n2", "n1", "had"),  # duplicate edge
            {"from": "n3", "to": "n1", "type": "had"},  # alt keys
            _edge("n3", "n1", "had"),  # same as above after normalize
        ],
    }

    merged = merge_graphs(g1, g2)
    node_ids = [n["id"] for n in merged["nodes"]]
    assert node_ids == ["n1", "n2", "n3"]
    edge_keys = {(e["source"], e["target"], e["relation"]) for e in merged["edges"]}
    assert edge_keys == {
        ("n2", "n1", "had"),
        ("n1", "n1", "contains"),
        ("n3", "n1", "had"),
    }
    assert len(merged["edges"]) == 3


def test_merge_graph_mutates_context_in_place():
    ctx = empty_context()
    merge_graph(ctx, {"nodes": [_node("a")], "edges": []})
    merge_graph(ctx, {"nodes": [_node("a"), _node("b")], "edges": [_edge("b", "a")]})
    assert [n["id"] for n in ctx["nodes"]] == ["a", "b"]
    assert len(ctx["edges"]) == 1


def test_apply_context_export_only_merges_when_scan_graph():
    ctx = empty_context()
    graph = {
        "nodes": [_node("x"), _node("y")],
        "edges": [_edge("y", "x")],
    }
    envelope: dict = {"kind": "scan_result_graph", "scan_result_id": "rg-1"}

    none_step = {"id": "httpx", "context": {"export": "none"}}
    result = apply_context_export(ctx, none_step, graph, scan_result_graph=envelope)
    assert result["exported"] is False
    assert ctx["nodes"] == []
    assert envelope["export_to_temporary_context"] is False

    export_step = {"id": "nuclei", "context": {"export": "scan_graph"}}
    result2 = apply_context_export(ctx, export_step, graph, scan_result_graph=envelope)
    assert result2["exported"] is True
    assert envelope["export_to_temporary_context"] is True
    assert [n["id"] for n in ctx["nodes"]] == ["x", "y"]
    assert len(ctx["edges"]) == 1

    # second identical export stays deduped
    apply_context_export(ctx, export_step, graph)
    assert len(ctx["nodes"]) == 2
    assert len(ctx["edges"]) == 1


def test_apply_context_export_accumulates_across_steps(doc_12a):
    """Temporary context accumulates only export: scan_graph steps (12A shape)."""
    by_id = {s["id"]: s for s in doc_12a["steps"]}
    ctx = empty_context()

    subfinder_g = {
        "nodes": [_node("d1", data="example.com"), _node("d2", data="www.example.com")],
        "edges": [_edge("d2", "d1")],
    }
    httpx_g = {
        "nodes": [_node("u1", nugget_id="URL", data="https://www.example.com")],
        "edges": [],
    }
    nuclei_g = {
        "nodes": [
            _node("d2", data="www.example.com"),  # overlap with subfinder
            _node("v1", nugget_id="VULNERABILITY_GENERAL", data="cve-demo"),
        ],
        "edges": [_edge("v1", "d2", "had")],
    }

    apply_context_export(ctx, by_id["sfp_cli_subfinder"], subfinder_g)
    apply_context_export(ctx, by_id["sfp_cli_httpx"], httpx_g)  # none — skip
    apply_context_export(ctx, by_id["sfp_cli_nuclei"], nuclei_g)

    ids = {n["id"] for n in ctx["nodes"]}
    assert ids == {"d1", "d2", "v1"}
    assert "u1" not in ids
    assert len(ctx["edges"]) == 2
