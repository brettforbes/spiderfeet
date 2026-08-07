"""AL2 / R10-18: dual-form subgraph serializer round-trip on scratch DB."""

from __future__ import annotations

import json

import pytest

from spiderfeet_v2.db.subgraph_codec import (
    JSON_TO_TYPEQL,
    TYPEQL_TO_JSON,
    graphs_equal,
    normalize_graph,
)

SMOKE_DB = "spiderfeet-al2-smoke"

PID = "project--al2"
WID = "workflow--al2"
TID = "target--al2"
SID = "scan_step--al2"
RG_ID = "scan-result--al2"

SAMPLE_GRAPH = {
    "nodes": [
        {
            "id": "HOST--al2-host",
            "nugget_instance_id": "HOST--al2-host",
            "nugget_id": "HOST",
            "nugget_type": "ENTITY",
            "nugget_description": "Host",
            "nugget_data": "al2.example",
            "nugget_colour": "#10B981",
        },
        {
            "id": "IPV4_ADDRESS--al2-ip",
            "nugget_instance_id": "IPV4_ADDRESS--al2-ip",
            "nugget_id": "IPV4_ADDRESS",
            "nugget_type": "ENTITY",
            "nugget_description": "IPv4 Address",
            "nugget_data": "203.0.113.42",
            "nugget_colour": "#3B82F6",
        },
        {
            "id": "TCP_PORT_OPEN--al2-port",
            "nugget_instance_id": "TCP_PORT_OPEN--al2-port",
            "nugget_id": "TCP_PORT_OPEN",
            "nugget_type": "ENTITY",
            "nugget_description": "Open TCP Port",
            "nugget_data": "80",
            "nugget_colour": "#8B5CF6",
        },
        {
            "id": "HOST_STATUS--al2-status",
            "nugget_instance_id": "HOST_STATUS--al2-status",
            "nugget_id": "HOST_STATUS",
            "nugget_type": "DESCRIPTOR",
            "nugget_description": "Host Status",
            "nugget_data": "up",
            "nugget_colour": "#F59E0B",
        },
    ],
    "edges": [
        {
            "source": "HOST--al2-host",
            "target": "IPV4_ADDRESS--al2-ip",
            "relation": "contains",
        },
        {
            "source": "HOST--al2-host",
            "target": "HOST_STATUS--al2-status",
            "relation": "had",
        },
        {
            "source": "HOST--al2-host",
            "target": "TCP_PORT_OPEN--al2-port",
            "relation": "listens-to",
        },
    ],
}


def test_edge_naming_mapping_complete() -> None:
    assert JSON_TO_TYPEQL == {
        "had": "has_this",
        "contains": "contains_this",
        "listens-to": "listens_to_this",
    }
    assert TYPEQL_TO_JSON == {
        "has_this": "had",
        "contains_this": "contains",
        "listens_to_this": "listens-to",
    }


@pytest.fixture(scope="module")
def store():
    pytest.importorskip("typedb.driver")
    from spiderfeet_v2.db.bootstrap import bootstrap_actual
    from spiderfeet_v2.db.config import TypeDBConfigError, load_connection_config
    from spiderfeet_v2.db.connection import open_driver, ping
    from spiderfeet_v2.db.crud import CrudStore

    try:
        cfg = load_connection_config()
    except TypeDBConfigError as exc:
        pytest.skip(f"TypeDB config missing: {exc}")
    if not ping(cfg):
        pytest.skip("TypeDB server not reachable")

    # Scratch only — never reset spiderfeet-actual here
    report = bootstrap_actual(cfg, database=SMOKE_DB, reset=True)
    assert report.ok, report.errors

    crud = CrudStore.connect(cfg, database=SMOKE_DB)
    # Minimal ownership chain for a scan_result_graph
    crud.create_target({"target_id": TID, "target_value": "al2.example"})
    crud.create_scan_step(
        {
            "scan_instance_id": SID,
            "step_module_id": "sfp_cli_nmap",
            "service_module_id": "sfp_cli_nmap",
            "scan_status": "FINISHED",
        }
    )
    crud.create_workflow(
        {
            "workflow_id": WID,
            "name": "al2-workflow",
            "target_id": TID,
            "first_step_id": SID,
        }
    )
    crud.create_project({"project_id": PID, "workflow_ids": [WID]})
    yield crud

    driver = open_driver(cfg)
    try:
        if driver.databases.contains(SMOKE_DB):
            driver.databases.get(SMOKE_DB).delete()
    finally:
        driver.close()


def test_dual_form_round_trip(store) -> None:
    """JSON graph → store (json_string + in-graph) → read back → equal."""
    created = store.create_subgraph(
        {
            "kind": "scan_result_graph",
            "scan_result_id": RG_ID,
            "scan_instance_id": SID,
            "graph": SAMPLE_GRAPH,
        }
    )
    assert created["kind"] == "scan_result_graph"
    assert created["scan_result_id"] == RG_ID
    assert created["json_string"] is not None

    expected = normalize_graph(SAMPLE_GRAPH)
    assert graphs_equal(created["graph"], expected)
    assert graphs_equal(created["graph_from_json_string"], expected)
    assert graphs_equal(
        json.loads(created["json_string"]), expected
    )

    # Fresh read via dual API
    dual = store.get_subgraph_dual("scan_result_graph", RG_ID)
    assert graphs_equal(dual["graph"], expected)
    assert graphs_equal(dual["graph_from_json_string"], expected)
    assert dual["graph"] == dual["graph_from_json_string"]

    # In-graph-only reconstruction
    from_typedb = store.get_subgraph_graph("scan_result_graph", RG_ID)
    assert from_typedb is not None
    assert graphs_equal(from_typedb, expected)

    # Replace payload (all three edge types still present after update)
    updated_graph = {
        "nodes": SAMPLE_GRAPH["nodes"][:3],  # drop HOST_STATUS
        "edges": [
            e
            for e in SAMPLE_GRAPH["edges"]
            if e["relation"] != "had"
        ],
    }
    replaced = store.put_subgraph_dual(
        "scan_result_graph", RG_ID, updated_graph
    )
    assert graphs_equal(replaced["graph"], updated_graph)
    assert graphs_equal(replaced["graph_from_json_string"], updated_graph)
    assert len(replaced["graph"]["edges"]) == 2
    relations = {e["relation"] for e in replaced["graph"]["edges"]}
    assert relations == {"contains", "listens-to"}

    assert store.delete_subgraph("scan_result_graph", RG_ID) is True
