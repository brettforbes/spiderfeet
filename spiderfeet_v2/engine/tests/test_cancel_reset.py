"""SPEC-015 R15-04 — cancel between steps + reset cancels in-flight runs."""

from __future__ import annotations

import time
from typing import Any, Dict

import pytest

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.engine.modules import clear_module_registry, register_module
from spiderfeet_v2.engine.persist import reset_workflow_execution
from spiderfeet_v2.engine.run_registry import (
    STATE_CANCELLED,
    RunRegistry,
    set_run_registry,
)
from spiderfeet_v2.engine.workflow_runner import OUTCOME_CANCELLED, run_workflow
from spiderfeet_v2.workflow.typedb_convert import scan_instance_id_for

CHAIN_YAML = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--cancel-unit
info:
  name: cancel-unit
  description: R15-04
  author: test
inputs:
  targets:
    type: string_list
    values:
      - example.com
steps:
  - id: sfp_cli_subfinder
    uses: tool.subfinder
    needs: []
    input:
      type: string_list
      from: $workflow.inputs.targets
    config:
      argv: ["-d", "$step.input.values[0]"]
    context:
      export: none
  - id: sfp_cli_httpx
    uses: tool.httpx
    needs: [sfp_cli_subfinder]
    input:
      type: string_list
      from: $workflow.inputs.targets
      empty: skip_step
    config:
      argv: ["-u", "$step.input.values[0]"]
    context:
      export: none
"""


@pytest.fixture
def store() -> FakeCrudStore:
    clear_module_registry()
    s = FakeCrudStore()
    s.create_target({"target_id": "target--cancel", "target_value": "example.com"})
    s.create_workflow(
        {
            "workflow_id": "workflow--cancel-unit",
            "name": "cancel-unit",
            "target_id": "target--cancel",
            "workflow_yaml": CHAIN_YAML,
        }
    )
    s.create_project(
        {
            "project_id": "project--cancel",
            "workflow_ids": ["workflow--cancel-unit"],
        }
    )
    yield s
    clear_module_registry()
    set_run_registry(None)


def _slow_ok(_spec: Any = None) -> Dict[str, Any]:
    time.sleep(0.35)
    return {
        "status": "SUCCESS",
        "text": "ok\n",
        "structured": {"records": []},
        "structured_type": "json",
        "graph": {"nodes": [], "edges": []},
        "narrative": "# Ok\n",
        "command": ["tool"],
        "counts": {"nodes": 0, "edges": 0},
        "duration": 0.35,
    }


def _ok(_spec: Any = None) -> Dict[str, Any]:
    return {
        "status": "SUCCESS",
        "text": "ok\n",
        "structured": {"records": []},
        "structured_type": "json",
        "graph": {"nodes": [], "edges": []},
        "narrative": "# Ok\n",
        "command": ["tool"],
        "counts": {"nodes": 0, "edges": 0},
        "duration": 0.0,
    }


def test_run_workflow_should_cancel_before_steps(store: FakeCrudStore) -> None:
    register_module("sfp_cli_subfinder", _ok)
    register_module("sfp_cli_httpx", _ok)
    result = run_workflow(
        store,
        workflow_id="workflow--cancel-unit",
        project_id="project--cancel",
        dry_run=False,
        should_cancel=lambda: True,
    )
    assert result.status == OUTCOME_CANCELLED
    assert result.stopped_early
    assert result.steps == []


def test_registry_cancel_then_reset(store: FakeCrudStore) -> None:
    register_module("sfp_cli_subfinder", _slow_ok)
    register_module("sfp_cli_httpx", _slow_ok)

    registry = RunRegistry(max_workers=1, store_factory=lambda: store)
    set_run_registry(registry)

    rec = registry.submit_workflow(
        workflow_id="workflow--cancel-unit",
        project_id="project--cancel",
        dry_run=False,
    )
    time.sleep(0.1)
    assert registry.cancel_workflow("workflow--cancel-unit") == rec.run_id
    finished = registry.wait(rec.run_id, timeout=30)
    assert finished is not None
    assert finished.state == STATE_CANCELLED

    sid = scan_instance_id_for("workflow--cancel-unit", "sfp_cli_subfinder")
    if store.get_scan_step(sid) is None:
        store.create_scan_step(
            {
                "scan_instance_id": sid,
                "step_module_id": "sfp_cli_subfinder",
                "scan_status": "FINISHED",
                "scan_ui_text_form": "leftover",
            }
        )
    else:
        store.update_scan_step(
            sid, {"scan_status": "FINISHED", "scan_ui_text_form": "leftover"}
        )

    report = reset_workflow_execution(
        store,
        workflow_id="workflow--cancel-unit",
        project_id="project--cancel",
    )
    assert report["status"] == "RESET"
    step = store.get_scan_step(sid)
    assert step is not None
    assert step.get("scan_status") == "UNKNOWN"
    assert not step.get("scan_ui_text_form")
