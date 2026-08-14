"""SPEC-017 A3/A6 — ensure_project_target_temps on Run/Scan Now; Reset wipes only."""

from __future__ import annotations

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.engine.persist import (
    ensure_project_target_temps,
    list_project_temporary_subgraphs,
    reset_workflow_execution,
)


YAML = """
id: wf-ensure
name: ensure
author: test
inputs:
  targets:
    values: [https://ensure.example]
steps:
  - id: sfp_cli_subfinder
    uses: tool.subfinder
    input:
      domain:
        from: $workflow.inputs.targets
    output:
      vars: {}
"""


def test_ensure_dedupes_duplicate_target_temps() -> None:
    """Race leftovers: two scan_name=target rows → keep one on ensure."""
    store = FakeCrudStore()
    store.create_target(
        {
            "target_id": "target--dup",
            "target_value": "dup.example",
            "target_nugget_type": "DOMAIN_NAME",
        }
    )
    store.create_workflow(
        {
            "workflow_id": "workflow--dup",
            "target_id": "target--dup",
            "project_id": "project--dup",
            "workflow_yaml": YAML,
        }
    )
    store.create_project(
        {
            "project_id": "project--dup",
            "workflow_ids": ["workflow--dup"],
        }
    )
    from spiderfeet_v2.engine.persist import seed_targets_into_temporary_context

    # Bypass ensure re-check by writing two rows with different ids directly.
    seed_targets_into_temporary_context(
        store, project_id="project--dup", hostnames=["dup.example"]
    )
    # Force a second row as if a race won twice.
    store.create_subgraph(
        {
            "kind": "temporary_subgraph",
            "temporary_subgraph_id": "temporary-subgraph--dup-extra",
            "project_id": "project--dup",
            "scan_name": "target",
            "scan_description": "Workflow target",
            "graph": {
                "produced_at": "2099-01-01T00:00:00Z",
                "nodes": [],
                "edges": [],
            },
        }
    )
    assert len(list_project_temporary_subgraphs(store, "project--dup")) == 2
    ensure_project_target_temps(store, project_id="project--dup")
    rows = list_project_temporary_subgraphs(store, "project--dup")
    assert len(rows) == 1
    assert rows[0]["scan_name"] == "target"


def test_ensure_creates_target_temp_once() -> None:
    store = FakeCrudStore()
    store.create_target(
        {
            "target_id": "target--ensure",
            "target_value": "ensure.example",
            "target_nugget_type": "DOMAIN_NAME",
        }
    )
    store.create_workflow(
        {
            "workflow_id": "workflow--ensure",
            "target_id": "target--ensure",
            "project_id": "project--ensure",
            "workflow_yaml": YAML,
        }
    )
    store.create_project(
        {
            "project_id": "project--ensure",
            "workflow_ids": ["workflow--ensure"],
        }
    )

    first = ensure_project_target_temps(store, project_id="project--ensure")
    assert first["ensured"] is True
    assert first["temporary"]["exported"] is True
    rows = list_project_temporary_subgraphs(store, "project--ensure")
    assert len(rows) == 1
    assert rows[0]["scan_name"] == "target"

    second = ensure_project_target_temps(store, project_id="project--ensure")
    assert second["temporary"].get("already_present") is True
    assert len(list_project_temporary_subgraphs(store, "project--ensure")) == 1


def test_reset_returns_run_ready_and_wipes_without_reseed() -> None:
    store = FakeCrudStore()
    store.create_target(
        {
            "target_id": "target--rst",
            "target_value": "rst.example",
        }
    )
    store.create_workflow(
        {
            "workflow_id": "workflow--rst",
            "target_id": "target--rst",
            "project_id": "project--rst",
            "workflow_yaml": YAML,
            "first_step_id": "scan_step--x",
        }
    )
    store.create_project(
        {"project_id": "project--rst", "workflow_ids": ["workflow--rst"]}
    )
    store.create_scan_step(
        {
            "scan_instance_id": "scan_step--x",
            "step_module_id": "sfp_cli_subfinder",
            "scan_status": "FINISHED",
        }
    )
    ensure_project_target_temps(store, project_id="project--rst")
    assert len(list_project_temporary_subgraphs(store, "project--rst")) == 1

    report = reset_workflow_execution(
        store, workflow_id="workflow--rst", project_id="project--rst"
    )
    assert report["status"] == "RESET"
    assert report["run_ready"] is True
    assert report["temporary_subgraph_id"] is None
    assert report["target_seed"] is None
    temps = list_project_temporary_subgraphs(store, "project--rst")
    assert temps == []
