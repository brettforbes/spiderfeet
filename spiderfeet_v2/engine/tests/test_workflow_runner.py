"""AO2 / R10-28 — full-workflow chaining unit tests (in-memory store)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.engine.modules import clear_module_registry, register_module
from spiderfeet_v2.engine.workflow_runner import run_workflow
from spiderfeet_v2.workflow.loader import schedule_waves
from spiderfeet_v2.workflow.typedb_convert import scan_instance_id_for

ROOT = Path(__file__).resolve().parents[3]
FIXTURE_SUBFINDER = (
    ROOT / "modules_v2" / "tests" / "fixtures" / "subfinder_vcof_sparse.json"
)
FIXTURE_HTTPX = (
    ROOT / "modules_v2" / "tests" / "fixtures" / "httpx_vcof_sparse.json"
)
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"

CHAIN_YAML = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--ao2-unit
info:
  name: ao2-unit
  author: test
inputs:
  targets:
    type: string_list
    values:
      - https://venturecapitalopportunitiesfund.com.au
steps:
  - id: sfp_cli_subfinder
    uses: tool.subfinder
    needs: []
    input:
      type: string_list
      from: $workflow.inputs.targets
      normalize: hostname_from_url
      empty: error
    config:
      argv:
        - "-d"
        - "$step.input.values[0]"
        - "-oJ"
        - "-cs"
        - "-silent"
    output:
      vars:
        apex_domains:
          type: string_list
          select:
            source: $step.scan_graph
            nodes:
              nugget_id: DOMAIN_NAME
              where:
                - not:
                    related:
                      direction: out
                      relation: had
                      nugget_id: DOMAIN_NAME_PARENT
            project: nugget_data
            distinct: true
        subdomains:
          type: string_list
          select:
            source: $step.scan_graph
            nodes:
              nugget_id: DOMAIN_NAME
              where:
                - related:
                    direction: out
                    relation: had
                    nugget_id: DOMAIN_NAME_PARENT
            project: nugget_data
            distinct: true
        all_domains:
          type: string_list
          union:
            - $step.vars.apex_domains
            - $step.vars.subdomains
          distinct: true
    context:
      export: scan_graph

  - id: sfp_cli_httpx
    uses: tool.httpx
    needs: [sfp_cli_subfinder]
    input:
      type: string_list
      from: $steps.sfp_cli_subfinder.vars.all_domains
      empty: error
    config:
      argv:
        - "-l"
        - "$step.files.input"
        - "-json"
        - "-silent"
      files:
        input:
          mode: auto
          format: line_text
        output:
          mode: auto
          format: jsonl
    output:
      vars:
        live_hosts:
          type: string_list
          select:
            source: $step.scan_graph
            nodes:
              nugget_id: DOMAIN_NAME
            project: nugget_data
            distinct: true
    context:
      export: scan_graph
"""

SKIP_YAML = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--ao2-skip
info:
  name: ao2-skip
  author: test
inputs:
  targets:
    type: string_list
    values:
      - https://example.com
steps:
  - id: sfp_cli_subfinder
    uses: tool.subfinder
    needs: []
    input:
      type: string_list
      from: $workflow.inputs.targets
      normalize: hostname_from_url
      empty: error
    config:
      argv:
        - "-d"
        - "$step.input.values[0]"
        - "-silent"
    output:
      vars:
        all_domains:
          type: string_list
          select:
            source: $step.scan_graph
            nodes:
              nugget_id: DOMAIN_NAME
            project: nugget_data
            distinct: true
    context:
      export: none

  - id: sfp_cli_nerva
    uses: tool.nerva
    needs: [sfp_cli_subfinder]
    input:
      type: string_list
      from: $steps.sfp_cli_subfinder.vars.all_domains
      empty: skip_step
    config:
      argv:
        - "--json"
        - "--list"
        - "$step.files.input"
    context:
      export: none
"""


@pytest.fixture
def store() -> FakeCrudStore:
    clear_module_registry()
    s = FakeCrudStore()
    s.create_target(
        {
            "target_id": "target--ao2",
            "target_value": "venturecapitalopportunitiesfund.com.au",
        }
    )
    s.create_workflow(
        {
            "workflow_id": "workflow--ao2-unit",
            "name": "ao2-unit",
            "target_id": "target--ao2",
            "workflow_yaml": CHAIN_YAML,
        }
    )
    s.create_project(
        {
            "project_id": "project--ao2",
            "workflow_ids": ["workflow--ao2-unit"],
        }
    )
    yield s
    clear_module_registry()


def _subfinder_fixture(_spec: Any = None) -> Dict[str, Any]:
    from modules_v2.sfp_cli_subfinder import sfp_cli_subfinder

    return sfp_cli_subfinder().run(
        {
            "json_text": FIXTURE_SUBFINDER.read_text(encoding="utf-8"),
            "scenario_key": "ao2_unit",
            "domain": "venturecapitalopportunitiesfund.com.au",
        }
    )


def _httpx_fixture(spec: Any = None) -> Dict[str, Any]:
    from modules_v2.sfp_cli_httpx import sfp_cli_httpx

    assert spec is not None
    # Chaining must have resolved prior all_domains into this step's primary.
    assert spec.get("domain") == "venturecapitalopportunitiesfund.com.au" or (
        isinstance(spec.get("argv"), list) and spec["argv"]
    )
    return sfp_cli_httpx().run(
        {
            "json_text": FIXTURE_HTTPX.read_text(encoding="utf-8"),
            "scenario_key": "ao2_unit_httpx",
            "domain": "venturecapitalopportunitiesfund.com.au",
        }
    )


def _empty_subfinder(_spec: Any = None) -> Dict[str, Any]:
    """Subfinder that emits no DOMAIN_NAME nodes → empty all_domains."""
    return {
        "status": "SUCCESS",
        "text": "empty\n",
        "structured": {"records": []},
        "structured_type": "json",
        "graph": {"nodes": [], "edges": []},
        "narrative": "# Empty\n",
        "command": ["subfinder"],
        "counts": {"nodes": 0, "edges": 0},
        "duration": 0.0,
    }


def test_dry_run_schedules_waves(store: FakeCrudStore) -> None:
    result = run_workflow(
        store,
        workflow_id="workflow--ao2-unit",
        project_id="project--ao2",
        dry_run=True,
    )
    assert result.status == "DRY_RUN"
    assert result.waves == [["sfp_cli_subfinder"], ["sfp_cli_httpx"]]
    assert len(result.steps) == 2
    assert all(s.status == "DRY_RUN" for s in result.steps)
    assert result.steps[0].input_values == [
        "venturecapitalopportunitiesfund.com.au"
    ]
    assert store.scan_steps == {}


def test_chain_threads_vars_and_accumulates_temp(store: FakeCrudStore) -> None:
    register_module("sfp_cli_subfinder", _subfinder_fixture)
    register_module("sfp_cli_httpx", _httpx_fixture)

    result = run_workflow(
        store,
        workflow_id="workflow--ao2-unit",
        project_id="project--ao2",
        dry_run=False,
    )

    assert result.status == "SUCCESS"
    assert result.exported_to_temporary is True
    assert result.temporary_subgraph_id
    assert sum(1 for s in result.steps if s.status == "SUCCESS") == 2

    sub_id = scan_instance_id_for("workflow--ao2-unit", "sfp_cli_subfinder")
    httpx_id = scan_instance_id_for("workflow--ao2-unit", "sfp_cli_httpx")

    assert store.get_scan_step(sub_id)["scan_status"] == "FINISHED"
    assert store.get_scan_step(httpx_id)["scan_status"] == "FINISHED"

    sub_vars = json.loads(store.get_scan_step(sub_id)["scan_results"])["vars"]
    assert sub_vars.get("all_domains")

    httpx_step = next(s for s in result.steps if s.step_id == "sfp_cli_httpx")
    assert httpx_step.input_values == sub_vars["all_domains"]

    temp = store.get_subgraph("temporary_subgraph", result.temporary_subgraph_id)
    assert temp is not None
    nodes: List[Any] = (temp.get("graph") or {}).get("nodes") or temp.get("nodes") or []
    # Both exporting steps merge into one temporary context.
    assert len(nodes) >= 1

    api = result.to_api_dict()
    assert api["orchestrator"] == "ao2"
    assert api["step_count"] == 2
    assert api["succeeded"] == 2


def test_empty_skip_step_does_not_fail_workflow(store: FakeCrudStore) -> None:
    store.create_workflow(
        {
            "workflow_id": "workflow--ao2-skip",
            "name": "ao2-skip",
            "target_id": "target--ao2",
            "workflow_yaml": SKIP_YAML,
        }
    )
    store.create_project(
        {
            "project_id": "project--ao2-skip",
            "workflow_ids": ["workflow--ao2-skip"],
        }
    )
    register_module("sfp_cli_subfinder", _empty_subfinder)

    result = run_workflow(
        store,
        workflow_id="workflow--ao2-skip",
        project_id="project--ao2-skip",
        dry_run=False,
    )
    assert result.status == "SUCCESS"
    assert [s.status for s in result.steps] == ["SUCCESS", "SKIPPED"]
    nerva = result.steps[1]
    assert nerva.step_id == "sfp_cli_nerva"
    assert nerva.input_values == []


def test_failed_sibling_does_not_block_other_branch(store: FakeCrudStore) -> None:
    """nmap failure must not prevent httpx→katana (branch-aware orchestration)."""
    branch_yaml = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--ao2-branch
info:
  name: ao2-branch
  author: test
inputs:
  targets:
    type: string_list
    values:
      - https://example.com
steps:
  - id: sfp_cli_subfinder
    uses: tool.subfinder
    needs: []
    input:
      type: string_list
      from: $workflow.inputs.targets
      normalize: hostname_from_url
      empty: error
    config:
      argv: ["-d", "$step.input.values[0]", "-silent"]
    output:
      vars:
        all_domains:
          type: string_list
          select:
            source: $step.scan_graph
            nodes:
              nugget_id: DOMAIN_NAME
            project: nugget_data
            distinct: true
    context:
      export: none
  - id: sfp_cli_nmap
    uses: tool.nmap
    needs: [sfp_cli_subfinder]
    input:
      type: string_list
      from: $steps.sfp_cli_subfinder.vars.all_domains
      empty: error
    config:
      args: ["-Pn"]
    context:
      export: none
  - id: sfp_cli_httpx
    uses: tool.httpx
    needs: [sfp_cli_subfinder]
    input:
      type: string_list
      from: $steps.sfp_cli_subfinder.vars.all_domains
      empty: error
    config:
      args: ["-json"]
    output:
      vars:
        live_hosts:
          type: string_list
          select:
            source: $step.scan_graph
            nodes:
              nugget_id: DOMAIN_NAME
            project: nugget_data
            distinct: true
    context:
      export: none
  - id: sfp_cli_katana
    uses: tool.katana
    needs: [sfp_cli_httpx]
    input:
      type: string_list
      from: $steps.sfp_cli_httpx.vars.live_hosts
      empty: skip_step
    config:
      args: ["-j"]
    context:
      export: none
  - id: sfp_cli_nerva
    uses: tool.nerva
    needs: [sfp_cli_nmap]
    input:
      type: string_list
      from: $steps.sfp_cli_nmap.vars.missing
      empty: skip_step
    config:
      args: ["--json"]
    context:
      export: none
"""
    store.create_workflow(
        {
            "workflow_id": "workflow--ao2-branch",
            "name": "ao2-branch",
            "target_id": "target--ao2",
            "workflow_yaml": branch_yaml,
        }
    )
    store.create_project(
        {
            "project_id": "project--ao2-branch",
            "workflow_ids": ["workflow--ao2-branch"],
        }
    )

    def _ok_sub(_spec: Any = None) -> Dict[str, Any]:
        return {
            "status": "SUCCESS",
            "text": "example.com\n",
            "structured": {"records": [{"host": "example.com"}]},
            "structured_type": "json",
            "graph": {
                "nodes": [
                    {
                        "id": "DOMAIN_NAME--ex",
                        "nugget_instance_id": "DOMAIN_NAME--ex",
                        "nugget_id": "DOMAIN_NAME",
                        "nugget_data": "example.com",
                    }
                ],
                "edges": [],
            },
            "narrative": "# Ok\n",
            "command": ["subfinder"],
            "counts": {"nodes": 1, "edges": 0},
            "duration": 0.0,
        }

    def _fail_nmap(_spec: Any = None) -> Dict[str, Any]:
        return {
            "status": "TIMEOUT",
            "text": "",
            "structured": {"error": "timeout after 120.0s"},
            "structured_type": "xml",
            "graph": {"nodes": [], "edges": []},
            "narrative": "",
            "command": ["nmap"],
            "counts": {"nodes": 0, "edges": 0},
            "duration": 120.0,
            "error": "timeout after 120.0s",
        }

    def _ok_httpx(_spec: Any = None) -> Dict[str, Any]:
        return {
            "status": "SUCCESS",
            "text": "https://example.com\n",
            "structured": {"records": [{"url": "https://example.com"}]},
            "structured_type": "json",
            "graph": {
                "nodes": [
                    {
                        "id": "DOMAIN_NAME--ex",
                        "nugget_instance_id": "DOMAIN_NAME--ex",
                        "nugget_id": "DOMAIN_NAME",
                        "nugget_data": "example.com",
                    }
                ],
                "edges": [],
            },
            "narrative": "# Ok\n",
            "command": ["httpx"],
            "counts": {"nodes": 1, "edges": 0},
            "duration": 0.1,
        }

    def _ok_katana(spec: Any = None) -> Dict[str, Any]:
        assert spec is not None
        return {
            "status": "SUCCESS",
            "text": "https://example.com/\n",
            "structured": {"records": []},
            "structured_type": "json",
            "graph": {"nodes": [], "edges": []},
            "narrative": "# Ok\n",
            "command": ["katana"],
            "counts": {"nodes": 0, "edges": 0},
            "duration": 0.1,
        }

    register_module("sfp_cli_subfinder", _ok_sub)
    register_module("sfp_cli_nmap", _fail_nmap)
    register_module("sfp_cli_httpx", _ok_httpx)
    register_module("sfp_cli_katana", _ok_katana)
    register_module("sfp_cli_nerva", _ok_katana)

    result = run_workflow(
        store,
        workflow_id="workflow--ao2-branch",
        project_id="project--ao2-branch",
        dry_run=False,
        stop_on_error=False,
    )
    by_id = {s.step_id: s for s in result.steps}
    assert by_id["sfp_cli_subfinder"].status == "SUCCESS"
    assert by_id["sfp_cli_nmap"].status == "ERROR"
    assert by_id["sfp_cli_httpx"].status == "SUCCESS"
    assert by_id["sfp_cli_katana"].status == "SUCCESS"
    assert by_id["sfp_cli_nerva"].status == "SKIPPED"
    assert result.stopped_early is False
    # Seed target DOMAIN_NAME lands in temporary context at run start.
    temp = store.get_subgraph("temporary_subgraph", result.temporary_subgraph_id)
    nodes = (temp.get("graph") or {}).get("nodes") or temp.get("nodes") or []
    assert any(
        n.get("nugget_id") == "DOMAIN_NAME" and n.get("nugget_data") == "example.com"
        for n in nodes
    )


def test_12a_dry_run_via_store(store: FakeCrudStore) -> None:
    """Load canonical 12A YAML and dry-run the full schedule (no live CLI)."""
    doc = yaml.safe_load(EXAMPLE_12A.read_text(encoding="utf-8"))
    wid = doc["id"]
    store.create_target(
        {"target_id": "target--12a", "target_value": "example.com"}
    )
    store.create_workflow(
        {
            "workflow_id": wid,
            "name": "12a",
            "target_id": "target--12a",
            "workflow_yaml": EXAMPLE_12A.read_text(encoding="utf-8"),
        }
    )
    store.create_project(
        {"project_id": "project--12a", "workflow_ids": [wid]}
    )

    expected = schedule_waves(doc["steps"])
    result = run_workflow(
        store,
        workflow_id=wid,
        project_id="project--12a",
        dry_run=True,
    )
    assert result.status == "DRY_RUN"
    assert result.waves == expected
    assert len(result.steps) == 6
    assert result.steps[0].step_id == "sfp_cli_subfinder"
    assert result.steps[0].input_values == ["example.com"]
    # Fan-out wave: nmap + httpx both resolve from subfinder vars (empty in dry-run
    # after first step — dry-run does not populate prior_vars from GSE).
    wave2_ids = {s.step_id for s in result.steps if s.step_id in ("sfp_cli_nmap", "sfp_cli_httpx")}
    assert wave2_ids == {"sfp_cli_nmap", "sfp_cli_httpx"}
