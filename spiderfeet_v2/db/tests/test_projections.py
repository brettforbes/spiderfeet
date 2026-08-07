"""AL3 / R10-19: fun-driven JSON projections + scan_step four-form round-trip."""

from __future__ import annotations

import json

import pytest

SMOKE_DB = "spiderfeet-al3-smoke"

PID = "project--al3"
WID = "workflow--al3"
TID = "target--al3"
SID = "scan_step--al3"
HOST_ID = "HOST--al3"
IP_ID = "IPV4_ADDRESS--al3"
PORT_ID = "TCP_PORT_OPEN--al3"
STATUS_ID = "HOST_STATUS--al3"
RG_ID = "scan-result--al3"
PC_ID = "project-context--al3"
TS_ID = "temporary-subgraph--al3"

CLI = "nmap -sn al3.example"
TEXT = "Nmap scan report for al3.example\nHost is up."
STRUCTURED = '{"hosts":[{"addr":"203.0.113.30","status":"up"}]}'
GRAPH = json.dumps(
    {
        "nodes": [
            {"id": HOST_ID, "nugget_id": "HOST", "nugget_data": "al3.example"},
            {"id": IP_ID, "nugget_id": "IPV4_ADDRESS", "nugget_data": "203.0.113.30"},
        ],
        "edges": [{"from": HOST_ID, "to": IP_ID, "type": "contains"}],
    },
    separators=(",", ":"),
)
NARRATIVE = "# AL3 scan\n\nHost al3.example produced IPV4_ADDRESS 203.0.113.30."


@pytest.fixture(scope="module")
def stores():
    pytest.importorskip("typedb.driver")
    from spiderfeet.map.typeql_util import run_write
    from spiderfeet_v2.db.bootstrap import bootstrap_actual
    from spiderfeet_v2.db.config import TypeDBConfigError, load_connection_config
    from spiderfeet_v2.db.connection import open_driver, ping
    from spiderfeet_v2.db.crud import CrudStore
    from spiderfeet_v2.db.projections import ProjectionStore

    try:
        cfg = load_connection_config()
    except TypeDBConfigError as exc:
        pytest.skip(f"TypeDB config missing: {exc}")
    if not ping(cfg):
        pytest.skip("TypeDB server not reachable")

    report = bootstrap_actual(cfg, database=SMOKE_DB, reset=True)
    assert report.ok, report.errors

    driver = open_driver(cfg)
    try:
        run_write(
            driver,
            SMOKE_DB,
            f"""
            insert
              $host isa host,
                has nugget_id "HOST",
                has nugget_instance_id "{HOST_ID}",
                has nugget_data "al3.example";
              $ip isa ipv4-address,
                has nugget_id "IPV4_ADDRESS",
                has nugget_instance_id "{IP_ID}",
                has nugget_data "203.0.113.30";
              $port isa tcp-port-open,
                has nugget_id "TCP_PORT_OPEN",
                has nugget_instance_id "{PORT_ID}",
                has nugget_data "443";
              $st isa host-status,
                has nugget_id "HOST_STATUS",
                has nugget_instance_id "{STATUS_ID}",
                has nugget_data "up";
            """,
        )
        run_write(
            driver,
            SMOKE_DB,
            f"""
            match
              $host isa host, has nugget_instance_id "{HOST_ID}";
              $ip isa ipv4-address, has nugget_instance_id "{IP_ID}";
              $port isa tcp-port-open, has nugget_instance_id "{PORT_ID}";
              $st isa host-status, has nugget_instance_id "{STATUS_ID}";
            insert
              $c isa contains_this, links (source: $host, target: $ip);
              $h isa has_this, links (source: $host, target: $st);
              $l isa listens_to_this, links (source: $host, target: $port);
            """,
        )
    finally:
        driver.close()

    crud = CrudStore.connect(cfg, database=SMOKE_DB)
    proj = ProjectionStore.connect(cfg, database=SMOKE_DB)

    crud.create_target(
        {
            "target_id": TID,
            "target_value": "al3.example",
            "target_description": "AL3 projection smoke",
        }
    )
    crud.create_scan_step(
        {
            "scan_instance_id": SID,
            "step_module_id": "sfp_cli_nmap",
            "scan_status": "FINISHED",
            "scan_nugget_count": 2,
            "scan_ui_cli_command": CLI,
            "scan_ui_text_form": TEXT,
            "scan_ui_structured_form": STRUCTURED,
            "scan_ui_structured_form_type": "json",
            "scan_ui_graph_form": GRAPH,
            "scan_ui_markdown_narrative_form": NARRATIVE,
            "consumed_ids": [HOST_ID],
            "produced_ids": [IP_ID],
            "service_module_id": "sfp_cli_nmap",
        }
    )
    crud.create_workflow(
        {
            "workflow_id": WID,
            "name": "al3-workflow",
            "workflow_yaml": "name: al3\nsteps: []",
            "target_id": TID,
            "first_step_id": SID,
            "prior_step_ids": [SID],
            "next_step_ids": [SID],
        }
    )
    crud.create_project(
        {
            "project_id": PID,
            "stix_incident_id": "incident--al3",
            "workflow_ids": [WID],
        }
    )
    crud.create_subgraph(
        {
            "kind": "scan_result_graph",
            "scan_result_id": RG_ID,
            "scan_instance_id": SID,
        }
    )
    crud.create_subgraph(
        {
            "kind": "project_context",
            "project_context_id": PC_ID,
            "project_id": PID,
        }
    )
    crud.create_subgraph(
        {
            "kind": "temporary_subgraph",
            "temporary_subgraph_id": TS_ID,
            "project_id": PID,
        }
    )

    yield crud, proj

    driver = open_driver(cfg)
    try:
        if driver.databases.contains(SMOKE_DB):
            driver.databases.get(SMOKE_DB).delete()
    finally:
        driver.close()


def test_project_projection_json(stores) -> None:
    _, proj = stores
    assert PID in proj.list_project_ids()
    got = proj.get_project(PID)
    assert got is not None
    assert got == {
        "project_id": PID,
        "workflows": [WID],
        "targets": [TID],
        "project_context": [PC_ID],
        "temporary_subgraph": [TS_ID],
    }
    assert json.loads(json.dumps(got)) == got
    assert proj.get_project("project--missing") is None


def test_workflow_projection_json(stores) -> None:
    _, proj = stores
    got = proj.get_workflow(WID)
    assert got is not None
    assert got == {
        "workflow_id": WID,
        "target": TID,
        "first_step": SID,
        "prior_step": [SID],
        "next_step": [SID],
        "workflow_yaml": "name: al3\nsteps: []",
    }
    assert proj.get_workflow("workflow--missing") is None


def test_scan_step_four_forms_and_roles_round_trip(stores) -> None:
    """Four UI forms + consumed/produced round-trip losslessly via fun wrappers."""
    crud, proj = stores
    stored = crud.get_scan_step(SID)
    assert stored is not None

    projected = proj.get_scan_step(SID)
    assert projected is not None

    # Fun projection field names (SPEC010_FUN_PROJECTIONS §4)
    assert projected["scan_instance_id"] == SID
    assert projected["cli_command"] == CLI
    assert projected["text_form"] == TEXT
    assert projected["structured_form"] == STRUCTURED
    assert projected["graph_form"] == GRAPH
    assert projected["markdown_narrative_form"] == NARRATIVE
    assert projected["consumed"] == [HOST_ID]
    assert projected["produced"] == [IP_ID]
    assert projected["scan_result_graph"] == [RG_ID]

    # Lossless vs CRUD attribute storage (same values, different key names)
    assert projected["cli_command"] == stored["scan_ui_cli_command"]
    assert projected["text_form"] == stored["scan_ui_text_form"]
    assert projected["structured_form"] == stored["scan_ui_structured_form"]
    assert projected["graph_form"] == stored["scan_ui_graph_form"]
    assert (
        projected["markdown_narrative_form"]
        == stored["scan_ui_markdown_narrative_form"]
    )
    assert projected["consumed"] == stored["consumed_ids"]
    assert projected["produced"] == stored["produced_ids"]

    # JSON-serializable and round-trips through dumps/loads
    assert json.loads(json.dumps(projected)) == projected

    # Graph form parses and keeps IPv4 id (no IP_ADDRESS)
    graph_obj = json.loads(projected["graph_form"])
    assert "IP_ADDRESS" not in json.dumps(graph_obj)
    assert any(n.get("nugget_id") == "IPV4_ADDRESS" for n in graph_obj["nodes"])

    assert proj.get_scan_step("scan_step--missing") is None


def test_scan_step_update_round_trip_via_projections(stores) -> None:
    """Updating four forms + roles through CRUD is visible via fun projections."""
    crud, proj = stores
    new_text = "updated-text-body"
    new_structured = '{"hosts":[]}'
    new_graph = '{"nodes":[],"edges":[]}'
    new_md = "# updated"

    crud.update_scan_step(
        SID,
        {
            "scan_ui_text_form": new_text,
            "scan_ui_structured_form": new_structured,
            "scan_ui_graph_form": new_graph,
            "scan_ui_markdown_narrative_form": new_md,
            "consumed_ids": [HOST_ID, STATUS_ID],
            "produced_ids": [IP_ID, PORT_ID],
            "service_module_id": "sfp_cli_nmap",
        },
    )
    projected = proj.get_scan_step(SID)
    assert projected is not None
    assert projected["text_form"] == new_text
    assert projected["structured_form"] == new_structured
    assert projected["graph_form"] == new_graph
    assert projected["markdown_narrative_form"] == new_md
    assert projected["consumed"] == sorted([HOST_ID, STATUS_ID])
    assert projected["produced"] == sorted([IP_ID, PORT_ID])

    # restore original for other tests / teardown cleanliness
    crud.update_scan_step(
        SID,
        {
            "scan_ui_text_form": TEXT,
            "scan_ui_structured_form": STRUCTURED,
            "scan_ui_graph_form": GRAPH,
            "scan_ui_markdown_narrative_form": NARRATIVE,
            "consumed_ids": [HOST_ID],
            "produced_ids": [IP_ID],
            "service_module_id": "sfp_cli_nmap",
        },
    )


def test_meta_subgraph_edge_projections(stores) -> None:
    _, proj = stores
    meta = proj.get_meta_subgraph(HOST_ID)
    assert meta is not None
    assert meta["root"] == HOST_ID
    edge_set = {(e["from"], e["to"], e["type"]) for e in meta["edges"]}
    assert (HOST_ID, IP_ID, "contains") in edge_set
    assert (HOST_ID, STATUS_ID, "had") in edge_set
    assert (HOST_ID, PORT_ID, "listens-to") in edge_set
    assert HOST_ID in meta["nodes"]
    assert IP_ID in meta["nodes"]
    assert proj.get_meta_subgraph("HOST--missing") is None


def test_module_level_wrappers(stores) -> None:
    from spiderfeet_v2.db.config import load_connection_config
    from spiderfeet_v2.db.projections import (
        meta_subgraph_json,
        project_json,
        scan_step_json,
        workflow_json,
    )

    cfg = load_connection_config()
    assert project_json(PID, cfg=cfg, database=SMOKE_DB)["project_id"] == PID
    assert workflow_json(WID, cfg=cfg, database=SMOKE_DB)["workflow_id"] == WID
    assert scan_step_json(SID, cfg=cfg, database=SMOKE_DB)["text_form"] == TEXT
    assert meta_subgraph_json(HOST_ID, cfg=cfg, database=SMOKE_DB)["root"] == HOST_ID
