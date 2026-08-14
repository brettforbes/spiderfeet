"""SPEC-018 R18-07 — input_total / input_done on workflow status."""

from __future__ import annotations

import json
import threading
import time
from typing import Any, Dict

from spiderfeet_v2.engine.modules import clear_module_registry, register_module
from spiderfeet_v2.engine.run_registry import STATE_RUNNING, get_run_registry
from spiderfeet_v2.workflow.typedb_convert import scan_instance_id_for

YAML_TWO_INPUTS = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--input-progress
info:
  name: input-progress
  description: R18-07
inputs:
  targets:
    type: string_list
    values:
      - alpha.example
      - beta.example
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
        - "-silent"
    context:
      export: none
  - id: sfp_cli_httpx
    uses: tool.httpx
    needs: [sfp_cli_subfinder]
    input:
      type: string_list
      from: $workflow.inputs.targets
    context:
      export: none
"""


def _slow_ok_module(_spec: Any = None) -> Dict[str, Any]:
    time.sleep(1.5)
    return {
        "status": "SUCCESS",
        "text": "ok\n",
        "structured": {"records": []},
        "structured_type": "json",
        "graph": {"nodes": [], "edges": []},
        "narrative": "# ok\n",
        "command": ["subfinder", "-d", "alpha.example"],
        "counts": {"nodes": 0, "edges": 0},
        "duration": 1.0,
    }


def _seed_workflow(client) -> None:
    client.post(
        "/api/v1/targets",
        json={"target_id": "target--input-progress", "target_value": "ip.example"},
    )
    client.post(
        "/api/v1/workflows",
        json={
            "workflow_id": "workflow--input-progress",
            "target_id": "target--input-progress",
            "workflow_yaml": YAML_TWO_INPUTS,
        },
    )
    client.post(
        "/api/v1/projects",
        json={
            "project_id": "project--input-progress",
            "workflow_ids": ["workflow--input-progress"],
        },
    )


def test_workflow_status_running_input_progress(client, fake_stores):
    """RUNNING step exposes input_done=0 and input_total=len(inputs)."""
    clear_module_registry()
    register_module("sfp_cli_subfinder", _slow_ok_module)
    _seed_workflow(client)

    started = threading.Event()
    original = get_run_registry()._mark_running

    def _mark_and_signal(run_id: str):
        rec = original(run_id)
        if rec is not None:
            started.set()
        return rec

    registry = get_run_registry()
    registry._mark_running = _mark_and_signal  # type: ignore[method-assign]

    try:
        r = client.post(
            "/api/v1/workflows/workflow--input-progress/steps/sfp_cli_subfinder/execute-async",
            json={"project_id": "project--input-progress", "dry_run": False},
        )
        assert r.status_code == 202, r.text
        run_id = r.json()["run_id"]

        assert started.wait(timeout=10), "background run did not start"

        deadline = time.time() + 10
        running_seen = False
        while time.time() < deadline:
            active = registry.get(run_id)
            if active and active.state == STATE_RUNNING:
                status = client.get(
                    "/api/v1/workflows/workflow--input-progress/status"
                ).json()
                step = next(
                    s
                    for s in status["steps"]
                    if s["step_id"] == "sfp_cli_subfinder"
                )
                if step["scan_status"] in ("RUNNING", "STARTING"):
                    assert step["input_total"] == 2
                    assert step["input_done"] == 0
                    running_seen = True
                    break
            time.sleep(0.05)

        assert running_seen, "expected RUNNING status with input progress"

        finished = registry.wait(run_id, timeout=30)
        assert finished is not None
        assert finished.state == "success"
    finally:
        registry._mark_running = original  # type: ignore[method-assign]
        clear_module_registry()


def test_workflow_status_finished_input_progress(client, fake_stores):
    """FINISHED step reads input_done=input_total=n from persisted scan_results."""
    clear_module_registry()
    register_module("sfp_cli_subfinder", _slow_ok_module)
    crud, _proj = fake_stores
    _seed_workflow(client)

    r = client.post(
        "/api/v1/workflows/workflow--input-progress/steps/sfp_cli_subfinder/execute-async",
        json={"project_id": "project--input-progress", "dry_run": False},
    )
    assert r.status_code == 202, r.text
    finished = get_run_registry().wait(r.json()["run_id"], timeout=30)
    assert finished is not None
    assert finished.state == "success"

    sid = scan_instance_id_for("workflow--input-progress", "sfp_cli_subfinder")
    row = crud.get_scan_step(sid)
    assert row is not None
    results = json.loads(row["scan_results"])
    assert results["input_total"] == 2
    assert results["input_done"] == 2

    status = client.get("/api/v1/workflows/workflow--input-progress/status").json()
    step = next(s for s in status["steps"] if s["step_id"] == "sfp_cli_subfinder")
    assert step["scan_status"] == "FINISHED"
    assert step["input_total"] == 2
    assert step["input_done"] == 2

    unknown = next(s for s in status["steps"] if s["step_id"] == "sfp_cli_httpx")
    assert unknown["scan_status"] == "UNKNOWN"
    assert "input_total" not in unknown
    assert "input_done" not in unknown

    clear_module_registry()
