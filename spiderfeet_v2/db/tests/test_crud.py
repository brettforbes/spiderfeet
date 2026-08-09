"""AL1 / R10-17: entity CRUD round-trips against scratch DB spiderfeet-al1-smoke."""

from __future__ import annotations

import json

import pytest

SMOKE_DB = "spiderfeet-al1-smoke"

PID = "project--al1"
WID = "workflow--al1"
TID = "target--al1"
SID = "scan_step--al1"
HOST_ID = "HOST--al1"
IP_ID = "IPV4_ADDRESS--al1"
RG_ID = "scan-result--al1"
PC_ID = "project-context--al1"
TS_ID = "temporary-subgraph--al1"


@pytest.fixture(scope="module")
def store():
    pytest.importorskip("typedb.driver")
    from spiderfeet_v2.db.bootstrap import bootstrap_actual
    from spiderfeet_v2.db.config import TypeDBConfigError, load_connection_config
    from spiderfeet_v2.db.connection import open_driver, ping
    from spiderfeet_v2.db.crud import CrudStore
    from spiderfeet.map.typeql_util import run_write

    try:
        cfg = load_connection_config()
    except TypeDBConfigError as exc:
        pytest.skip(f"TypeDB config missing: {exc}")
    if not ping(cfg):
        pytest.skip("TypeDB server not reachable")

    # Scratch only — never reset spiderfeet-actual here
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
                has nugget_data "al1.example";
              $ip isa ipv4-address,
                has nugget_id "IPV4_ADDRESS",
                has nugget_instance_id "{IP_ID}",
                has nugget_data "203.0.113.70";
            """,
        )
    finally:
        driver.close()

    crud = CrudStore.connect(cfg, database=SMOKE_DB)
    yield crud

    driver = open_driver(cfg)
    try:
        if driver.databases.contains(SMOKE_DB):
            driver.databases.get(SMOKE_DB).delete()
    finally:
        driver.close()


def test_target_crud_round_trip(store) -> None:
    created = store.create_target(
        {
            "target_id": TID,
            "target_value": "al1.example",
            "target_description": "AL1 smoke target",
            "target_yaml": "value: al1.example",
            "target_created": "2026-08-07T10:00:00Z",
        }
    )
    assert created["target_id"] == TID
    assert created["target_value"] == "al1.example"
    assert created["target_description"] == "AL1 smoke target"
    assert created["target_yaml"] == "value: al1.example"
    assert created["target_created"] is not None

    got = store.get_target(TID)
    assert got == created
    assert json.loads(json.dumps(got))["target_value"] == "al1.example"

    updated = store.update_target(TID, {"target_value": "al1-updated.example"})
    assert updated["target_value"] == "al1-updated.example"
    assert updated["target_description"] == "AL1 smoke target"

    assert any(t["target_id"] == TID for t in store.list_targets())
    assert store.delete_target(TID) is True
    assert store.get_target(TID) is None
    # recreate for later tests that need a target
    store.create_target(
        {
            "target_id": TID,
            "target_value": "al1.example",
            "target_description": "AL1 smoke target",
        }
    )


def test_scan_step_crud_round_trip(store) -> None:
    created = store.create_scan_step(
        {
            "scan_instance_id": SID,
            "step_module_id": "sfp_cli_nmap",
            "scan_status": "FINISHED",
            "scan_nugget_count": 2,
            "scan_results_by_type": '{"IPV4_ADDRESS":1,"HOST":1}',
            "scan_results": '{"status":"FINISHED","nugget_count":2}',
            "scan_duration": 1.5,
            "scan_timestamp": "2026-08-07T10:05:00Z",
            "scan_notes": "al1",
            "scan_ui_cli_command": "nmap -sn al1.example",
            "scan_ui_text_form": "text-body",
            "scan_ui_structured_form": "{}",
            "scan_ui_structured_form_type": "json",
            "scan_ui_graph_form": '{"nodes":[],"edges":[]}',
            "scan_ui_markdown_narrative_form": "# narrative",
            "scan_yaml": "id: nmap_ping",
            "consumed_ids": [HOST_ID],
            "produced_ids": [IP_ID],
            "service_module_id": "sfp_cli_nmap",
        }
    )
    assert created["scan_instance_id"] == SID
    assert created["scan_status"] == "FINISHED"
    assert created["scan_nugget_count"] == 2
    assert created["scan_duration"] == pytest.approx(1.5)
    assert created["scan_ui_text_form"] == "text-body"
    assert created["scan_ui_graph_form"] == '{"nodes":[],"edges":[]}'
    assert created["consumed_ids"] == [HOST_ID]
    assert created["produced_ids"] == [IP_ID]
    assert created["service_module_id"] == "sfp_cli_nmap"

    got = store.get_scan_step(SID)
    assert got["scan_ui_markdown_narrative_form"] == "# narrative"

    updated = store.update_scan_step(
        SID,
        {
            "scan_status": "ERROR-FAILED",
            "scan_ui_text_form": "updated-text",
            "consumed_ids": [HOST_ID],
            "produced_ids": [],
            "service_module_id": "sfp_cli_nmap",
        },
    )
    assert updated["scan_status"] == "ERROR-FAILED"
    assert updated["scan_ui_text_form"] == "updated-text"
    assert updated["produced_ids"] == []
    assert updated["consumed_ids"] == [HOST_ID]

    # restore for workflow/subgraph tests
    store.update_scan_step(
        SID,
        {
            "scan_status": "FINISHED",
            "consumed_ids": [HOST_ID],
            "produced_ids": [IP_ID],
            "service_module_id": "sfp_cli_nmap",
        },
    )


def test_workflow_crud_round_trip(store) -> None:
    # ensure target + step exist
    if store.get_target(TID) is None:
        store.create_target({"target_id": TID, "target_value": "al1.example"})
    if store.get_scan_step(SID) is None:
        store.create_scan_step(
            {
                "scan_instance_id": SID,
                "step_module_id": "sfp_cli_nmap",
                "scan_status": "FINISHED",
                "service_module_id": "sfp_cli_nmap",
            }
        )

    created = store.create_workflow(
        {
            "workflow_id": WID,
            "name": "al1-workflow",
            "description": "AL1 CRUD workflow",
            "author": "tester",
            "created": "2026-08-07T10:10:00Z",
            "workflow_yaml": "name: al1\nsteps: []",
            "target_id": TID,
            "first_step_id": SID,
            "prior_step_ids": [SID],
            "next_step_ids": [SID],
        }
    )
    assert created["workflow_id"] == WID
    assert created["name"] == "al1-workflow"
    assert created["target_id"] == TID
    assert created["first_step_id"] == SID
    assert created["prior_step_ids"] == [SID]
    assert created["next_step_ids"] == [SID]

    updated = store.update_workflow(
        WID,
        {
            "name": "al1-workflow-v2",
            "target_id": TID,
            "first_step_id": SID,
            "prior_step_ids": [],
            "next_step_ids": [SID],
        },
    )
    assert updated["name"] == "al1-workflow-v2"
    assert updated["prior_step_ids"] == []
    assert updated["next_step_ids"] == [SID]


def test_project_crud_round_trip(store) -> None:
    """R13-02: project is an entity; workflows link via workflow→project."""
    # Standalone project (zero workflows) must persist.
    empty_pid = "project--al1-empty"
    if store.get_project(empty_pid) is not None:
        store.delete_project(empty_pid)
    empty = store.create_project(
        {
            "project_id": empty_pid,
            "project_name": "Empty Project",
            "project_description": "No workflows yet",
            "project_created": "2026-08-07T10:14:00Z",
        }
    )
    assert empty["project_id"] == empty_pid
    assert empty["project_name"] == "Empty Project"
    assert empty["workflow_ids"] == []
    store.delete_project(empty_pid)

    if store.get_workflow(WID) is None:
        if store.get_target(TID) is None:
            store.create_target({"target_id": TID, "target_value": "al1.example"})
        store.create_workflow(
            {
                "workflow_id": WID,
                "name": "al1-workflow",
                "target_id": TID,
            }
        )

    if store.get_project(PID) is not None:
        store.delete_project(PID)

    created = store.create_project(
        {
            "project_id": PID,
            "stix_incident_id": "incident--al1",
            "project_name": "AL1 Project",
            "project_description": "CRUD round-trip",
            "project_created": "2026-08-07T10:15:00Z",
            "workflow_ids": [WID],
        }
    )
    assert created["project_id"] == PID
    assert created["stix_incident_id"] == "incident--al1"
    assert created["project_name"] == "AL1 Project"
    assert created["project_description"] == "CRUD round-trip"
    assert created["workflow_ids"] == [WID]
    # Workflow side must see the project link.
    wf = store.get_workflow(WID)
    assert wf is not None
    assert wf["project_id"] == PID

    updated = store.update_project(
        PID,
        {
            "stix_incident_id": "incident--al1-b",
            "project_name": "AL1 Project v2",
            "workflow_ids": [WID],
        },
    )
    assert updated["stix_incident_id"] == "incident--al1-b"
    assert updated["project_name"] == "AL1 Project v2"
    assert store.list_projects()


def test_subgraph_crud_round_trip(store) -> None:
    if store.get_scan_step(SID) is None:
        store.create_scan_step(
            {
                "scan_instance_id": SID,
                "step_module_id": "sfp_cli_nmap",
                "service_module_id": "sfp_cli_nmap",
            }
        )
    if store.get_project(PID) is None:
        if store.get_workflow(WID) is None:
            if store.get_target(TID) is None:
                store.create_target({"target_id": TID, "target_value": "al1.example"})
            store.create_workflow(
                {"workflow_id": WID, "name": "al1", "target_id": TID}
            )
        store.create_project({"project_id": PID, "workflow_ids": [WID]})

    rg = store.create_subgraph(
        {
            "kind": "scan_result_graph",
            "scan_result_id": RG_ID,
            "scan_instance_id": SID,
        }
    )
    assert rg["kind"] == "scan_result_graph"
    assert rg["scan_result_id"] == RG_ID
    assert rg["scan_instance_id"] == SID
    assert rg.get("json_string") is None

    pc = store.create_subgraph(
        {
            "kind": "project_context",
            "project_context_id": PC_ID,
            "project_id": PID,
        }
    )
    assert pc["project_context_id"] == PC_ID
    assert pc["project_id"] == PID

    ts = store.create_subgraph(
        {
            "kind": "temporary_subgraph",
            "temporary_subgraph_id": TS_ID,
            "project_id": PID,
        }
    )
    assert ts["temporary_subgraph_id"] == TS_ID

    # create a second project to re-point temporary subgraph owner
    pid2 = "project--al1-b"
    wid2 = "workflow--al1-b"
    store.create_workflow(
        {"workflow_id": wid2, "name": "al1-b", "target_id": TID}
    )
    store.create_project({"project_id": pid2, "workflow_ids": [wid2]})
    moved = store.update_subgraph(
        "temporary_subgraph", TS_ID, {"project_id": pid2}
    )
    assert moved["project_id"] == pid2

    assert store.delete_subgraph("scan_result_graph", RG_ID) is True
    assert store.get_subgraph("scan_result_graph", RG_ID) is None
    assert store.delete_subgraph("project_context", PC_ID) is True
    assert store.delete_subgraph("temporary_subgraph", TS_ID) is True
    store.delete_project(pid2)
    store.delete_workflow(wid2)


def test_delete_cascade_order(store) -> None:
    """Delete remaining linked objects without leaving the scratch dirty for teardown."""
    # recreate minimal chain if earlier tests cleaned pieces
    if store.get_target(TID) is None:
        store.create_target({"target_id": TID, "target_value": "al1.example"})
    if store.get_scan_step(SID) is None:
        store.create_scan_step(
            {
                "scan_instance_id": SID,
                "step_module_id": "sfp_cli_nmap",
                "service_module_id": "sfp_cli_nmap",
            }
        )
    if store.get_workflow(WID) is None:
        store.create_workflow(
            {
                "workflow_id": WID,
                "name": "al1",
                "target_id": TID,
                "first_step_id": SID,
            }
        )
    if store.get_project(PID) is None:
        store.create_project({"project_id": PID, "workflow_ids": [WID]})

    assert store.delete_project(PID) is True
    assert store.delete_workflow(WID) is True
    assert store.delete_scan_step(SID) is True
    assert store.delete_target(TID) is True
