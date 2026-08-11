"""SPEC-017 R17-02 — stamp + per-export temporary_subgraph rows."""

from __future__ import annotations

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.engine.persist import (
    list_project_temporary_subgraphs,
    persist_temporary_export,
    reset_temporary_context,
    seed_targets_into_temporary_context,
)
from spiderfeet_v2.engine.temporary_viewer_graph import stamp_viewer_graph


def test_stamp_viewer_graph_remaps_and_labels() -> None:
    graph = {
        "nodes": [
            {
                "id": "DOMAIN_NAME--aaa",
                "nugget_instance_id": "DOMAIN_NAME--aaa",
                "nugget_id": "DOMAIN_NAME",
                "nugget_data": "example.com",
            }
        ],
        "edges": [],
    }
    stamped = stamp_viewer_graph(graph, scan_name="subfinder_enum")
    assert len(stamped["nodes"]) == 1
    node = stamped["nodes"][0]
    assert node["temporary_id"].startswith("temporary--")
    assert node["id"] == node["temporary_id"]
    assert node["nugget_instance_id"] == "DOMAIN_NAME--aaa"
    assert node["source"] == "subfinder_enum"


def test_persist_creates_separate_rows_per_export() -> None:
    store = FakeCrudStore()
    store.create_project({"project_id": "project--t", "workflow_ids": []})
    step_a = {"id": "step_a", "description": "A", "context": {"export": "scan_graph"}}
    step_b = {"id": "step_b", "context": {"export": "scan_graph"}}
    g1 = {
        "nodes": [
            {
                "id": "DOMAIN_NAME--1",
                "nugget_instance_id": "DOMAIN_NAME--1",
                "nugget_id": "DOMAIN_NAME",
                "nugget_data": "a.com",
            }
        ],
        "edges": [],
    }
    g2 = {
        "nodes": [
            {
                "id": "DOMAIN_NAME--1",
                "nugget_instance_id": "DOMAIN_NAME--1",
                "nugget_id": "DOMAIN_NAME",
                "nugget_data": "a.com",
            }
        ],
        "edges": [],
    }
    r1 = persist_temporary_export(
        store, project_id="project--t", step=step_a, scan_graph=g1
    )
    r2 = persist_temporary_export(
        store, project_id="project--t", step=step_b, scan_graph=g2
    )
    assert r1["persisted"] and r2["persisted"]
    assert r1["temporary_subgraph_id"] != r2["temporary_subgraph_id"]
    rows = list_project_temporary_subgraphs(store, "project--t")
    assert len(rows) == 2
    names = {r.get("scan_name") for r in rows}
    assert names == {"step_a", "step_b"}
    # Overlapping nugget_instance_id, distinct temporary ids
    tids = []
    for r in rows:
        nodes = (r.get("graph") or {}).get("nodes") or []
        tids.append(nodes[0]["temporary_id"])
    assert tids[0] != tids[1]


def test_reset_deletes_all_then_seed_target() -> None:
    store = FakeCrudStore()
    store.create_project({"project_id": "project--r", "workflow_ids": []})
    persist_temporary_export(
        store,
        project_id="project--r",
        step={"id": "x", "context": {"export": "scan_graph"}},
        scan_graph={
            "nodes": [
                {
                    "id": "DOMAIN_NAME--1",
                    "nugget_instance_id": "DOMAIN_NAME--1",
                    "nugget_id": "DOMAIN_NAME",
                    "nugget_data": "x.com",
                }
            ],
            "edges": [],
        },
    )
    reset_temporary_context(store, project_id="project--r")
    assert list_project_temporary_subgraphs(store, "project--r") == []
    seed = seed_targets_into_temporary_context(
        store, project_id="project--r", hostnames=["seed.example"]
    )
    assert seed["exported"] is True
    assert seed["scan_name"] == "target"
    rows = list_project_temporary_subgraphs(store, "project--r")
    assert len(rows) == 1
    assert rows[0]["scan_name"] == "target"
