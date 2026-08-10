"""SPEC-015 R15-01 — async execute + run registry unit tests."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.engine.modules import clear_module_registry, register_module
from spiderfeet_v2.engine.run_registry import (
    STATE_ERROR,
    STATE_SUCCESS,
    RunRegistry,
)


CHAIN_YAML = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--async-unit
info:
  name: async-unit
  description: R15-01 registry test
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
      empty: error
    config:
      argv:
        - "-d"
        - "$step.input.values[0]"
        - "-silent"
    context:
      export: none
"""


@pytest.fixture
def store() -> FakeCrudStore:
    clear_module_registry()
    s = FakeCrudStore()
    s.create_target(
        {"target_id": "target--async", "target_value": "example.com"}
    )
    s.create_workflow(
        {
            "workflow_id": "workflow--async-unit",
            "name": "async-unit",
            "target_id": "target--async",
            "workflow_yaml": CHAIN_YAML,
        }
    )
    s.create_project(
        {
            "project_id": "project--async",
            "workflow_ids": ["workflow--async-unit"],
        }
    )
    yield s
    clear_module_registry()


def _ok_module(_spec: Any = None) -> Dict[str, Any]:
    return {
        "status": "SUCCESS",
        "text": "ok\n",
        "structured": {"records": []},
        "structured_type": "json",
        "graph": {"nodes": [], "edges": []},
        "narrative": "# Ok\n",
        "command": ["subfinder"],
        "counts": {"nodes": 0, "edges": 0},
        "duration": 0.0,
    }


def _fail_module(_spec: Any = None) -> Dict[str, Any]:
    return {
        "status": "ERROR",
        "text": "boom\n",
        "structured": {"error": "boom"},
        "structured_type": "json",
        "graph": {"nodes": [], "edges": []},
        "narrative": "# Fail\n",
        "command": ["subfinder"],
        "counts": {"nodes": 0, "edges": 0},
        "duration": 0.0,
        "error": "boom",
    }


def test_registry_workflow_success(store: FakeCrudStore) -> None:
    register_module("sfp_cli_subfinder", _ok_module)
    registry = RunRegistry(max_workers=1, store_factory=lambda: store)
    rec = registry.submit_workflow(
        workflow_id="workflow--async-unit",
        project_id="project--async",
        dry_run=False,
    )
    assert rec.state == "queued"
    assert rec.run_id.startswith("run--")

    finished = registry.wait(rec.run_id, timeout=30)
    assert finished is not None
    assert finished.state == STATE_SUCCESS
    assert finished.result is not None
    assert finished.result.get("status") in ("SUCCESS", "DRY_RUN")
    assert finished.started_at
    assert finished.finished_at


def test_registry_workflow_error_state(store: FakeCrudStore) -> None:
    register_module("sfp_cli_subfinder", _fail_module)
    registry = RunRegistry(max_workers=1, store_factory=lambda: store)
    rec = registry.submit_workflow(
        workflow_id="workflow--async-unit",
        project_id="project--async",
        dry_run=False,
    )
    finished = registry.wait(rec.run_id, timeout=30)
    assert finished is not None
    assert finished.state == STATE_ERROR
    assert finished.error


def test_registry_dry_run_success(store: FakeCrudStore) -> None:
    registry = RunRegistry(max_workers=1, store_factory=lambda: store)
    rec = registry.submit_workflow(
        workflow_id="workflow--async-unit",
        project_id="project--async",
        dry_run=True,
    )
    finished = registry.wait(rec.run_id, timeout=30)
    assert finished is not None
    assert finished.state == STATE_SUCCESS
    assert finished.result and finished.result.get("status") == "DRY_RUN"
