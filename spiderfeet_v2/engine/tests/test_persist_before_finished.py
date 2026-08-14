"""SPEC-018 R18-06 — persist temp subgraph before scan_status=FINISHED."""

from __future__ import annotations

from typing import Any, Dict, List

import pytest

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.engine.modules import clear_module_registry, register_module
from spiderfeet_v2.engine.persist import list_project_temporary_subgraphs
from spiderfeet_v2.engine.step_runner import run_single_step

WORKFLOW_EXPORT = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--r18-06-export
info:
  name: r18-06-export
inputs:
  targets:
    type: string_list
    values:
      - export.example
steps:
  - id: sfp_cli_subfinder
    uses: tool.subfinder
    needs: []
    input:
      type: string_list
      from: $workflow.inputs.targets
    config:
      argv:
        - "-d"
        - "$step.input.values[0]"
    context:
      export: scan_graph
"""

WORKFLOW_NONE = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--r18-06-none
info:
  name: r18-06-none
inputs:
  targets:
    type: string_list
    values:
      - none.example
steps:
  - id: sfp_cli_httpx
    uses: tool.httpx
    needs: []
    input:
      type: string_list
      from: $workflow.inputs.targets
    config:
      argv:
        - "-u"
        - "$step.input.values[0]"
    context:
      export: none
"""


def _ok_module(_spec: Any = None) -> Dict[str, Any]:
    return {
        "status": "SUCCESS",
        "text": "ok\n",
        "structured": {"records": []},
        "structured_type": "json",
        "graph": {
            "nodes": [
                {
                    "nugget_id": "DOMAIN_NAME",
                    "nugget_data": "export.example",
                    "nugget_instance_id": "DOMAIN_NAME--export.example",
                }
            ],
            "edges": [],
        },
        "narrative": "# ok\n",
        "command": ["subfinder", "-d", "export.example"],
        "counts": {"nodes": 1, "edges": 0},
        "duration": 0.1,
    }


class _OrderTrackingStore(FakeCrudStore):
    """Record temp subgraph create vs scan_step FINISHED write order."""

    def __init__(self) -> None:
        super().__init__()
        self.events: List[str] = []

    def create_subgraph(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if data.get("kind") == "temporary_subgraph":
            self.events.append("temp_create")
        return super().create_subgraph(data)

    def update_scan_step(self, scan_instance_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        status = data.get("scan_status")
        if status == "FINISHED":
            self.events.append("scan_finished")
        return super().update_scan_step(scan_instance_id, data)


def _seed(store: FakeCrudStore, *, workflow_id: str, yaml: str, step_module: str) -> str:
    project_id = f"project--{workflow_id}"
    store.create_target(
        {
            "target_id": f"target--{workflow_id}",
            "target_value": "seed.example",
        }
    )
    store.create_workflow(
        {
            "workflow_id": workflow_id,
            "target_id": f"target--{workflow_id}",
            "workflow_yaml": yaml,
        }
    )
    store.create_project({"project_id": project_id, "workflow_ids": [workflow_id]})
    return project_id


@pytest.fixture(autouse=True)
def _clear_modules() -> None:
    clear_module_registry()
    yield
    clear_module_registry()


def test_export_scan_graph_temp_persisted_before_finished() -> None:
    """R18-06: temporary_subgraph row exists before scan_status reaches FINISHED."""
    store = _OrderTrackingStore()
    project_id = _seed(store, workflow_id="workflow--r18-06-export", yaml=WORKFLOW_EXPORT, step_module="subfinder")
    register_module("sfp_cli_subfinder", _ok_module)

    result = run_single_step(
        store,
        workflow_id="workflow--r18-06-export",
        step_id="sfp_cli_subfinder",
        project_id=project_id,
        dry_run=False,
    )

    assert result.scan_status == "FINISHED"
    assert result.exported_to_temporary is True
    assert result.temporary_subgraph_id

    temp = store.get_subgraph("temporary_subgraph", result.temporary_subgraph_id)
    assert temp is not None
    graph = temp.get("graph") or {}
    assert len(graph.get("nodes") or []) >= 1

    export_temps = [
        r for r in list_project_temporary_subgraphs(store, project_id)
        if r.get("scan_name") == "sfp_cli_subfinder"
    ]
    assert len(export_temps) == 1

    assert "temp_create" in store.events
    assert "scan_finished" in store.events
    assert store.events.index("temp_create") < store.events.index("scan_finished")


def test_export_none_does_not_create_step_temp_subgraph() -> None:
    """R18-06: export:none steps do not add a step export temp (target seed may exist)."""
    store = FakeCrudStore()
    project_id = _seed(store, workflow_id="workflow--r18-06-none", yaml=WORKFLOW_NONE, step_module="httpx")
    register_module("sfp_cli_httpx", _ok_module)

    result = run_single_step(
        store,
        workflow_id="workflow--r18-06-none",
        step_id="sfp_cli_httpx",
        project_id=project_id,
        dry_run=False,
    )

    assert result.scan_status == "FINISHED"
    assert result.exported_to_temporary is False

    temps = list_project_temporary_subgraphs(store, project_id)
    assert len(temps) == 1
    assert temps[0]["scan_name"] == "target"
    assert all(r.get("scan_name") != "sfp_cli_httpx" for r in temps)
