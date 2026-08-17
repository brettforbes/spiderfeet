"""AO1 / R10-27 — single-step orchestrator unit tests (in-memory store)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.engine.modules import clear_module_registry, register_module
from spiderfeet_v2.engine.step_runner import OrchestratorError, run_single_step
from spiderfeet_v2.workflow.typedb_convert import scan_instance_id_for

FIXTURE_JSON = (
    Path(__file__).resolve().parents[3]
    / "modules_v2"
    / "tests"
    / "fixtures"
    / "subfinder_vcof_sparse.json"
)

WORKFLOW_YAML = """apiVersion: spiderfeet.workflow/v1
kind: Workflow
id: workflow--ao1-unit
info:
  name: ao1-unit
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
"""


@pytest.fixture
def store() -> FakeCrudStore:
    clear_module_registry()
    s = FakeCrudStore()
    s.create_target(
        {
            "target_id": "target--ao1",
            "target_value": "venturecapitalopportunitiesfund.com.au",
        }
    )
    s.create_workflow(
        {
            "workflow_id": "workflow--ao1-unit",
            "name": "ao1-unit",
            "target_id": "target--ao1",
            "workflow_yaml": WORKFLOW_YAML,
        }
    )
    s.create_project(
        {
            "project_id": "project--ao1",
            "workflow_ids": ["workflow--ao1-unit"],
        }
    )
    yield s
    clear_module_registry()


def _fixture_module_result(_spec: Any = None) -> Dict[str, Any]:
    from modules_v2.sfp_cli_subfinder import sfp_cli_subfinder

    raw = FIXTURE_JSON.read_text(encoding="utf-8")
    return sfp_cli_subfinder().run(
        {
            "json_text": raw,
            "scenario_key": "ao1_unit",
            "domain": "venturecapitalopportunitiesfund.com.au",
        }
    )


def test_dry_run_resolves_module_and_inputs(store: FakeCrudStore) -> None:
    result = run_single_step(
        store,
        workflow_id="workflow--ao1-unit",
        step_id="sfp_cli_subfinder",
        dry_run=True,
    )
    assert result.status == "DRY_RUN"
    assert result.module_id == "sfp_cli_subfinder"
    assert result.input_values == ["venturecapitalopportunitiesfund.com.au"]
    assert result.scan_instance_id == scan_instance_id_for(
        "workflow--ao1-unit", "sfp_cli_subfinder"
    )
    # dry-run must not persist
    assert store.get_scan_step(result.scan_instance_id) is None


def test_run_persists_four_forms_vars_and_export(store: FakeCrudStore) -> None:
    register_module("sfp_cli_subfinder", _fixture_module_result)

    result = run_single_step(
        store,
        workflow_id="workflow--ao1-unit",
        step_id="sfp_cli_subfinder",
        project_id="project--ao1",
        dry_run=False,
    )

    assert result.status == "SUCCESS"
    assert result.scan_status == "FINISHED"
    assert result.module_id == "sfp_cli_subfinder"
    assert result.exported_to_temporary is True
    assert result.output_vars.get("all_domains")
    assert "venturecapitalopportunitiesfund.com.au" in result.output_vars["all_domains"]

    row = store.get_scan_step(result.scan_instance_id)
    assert row is not None
    assert row["scan_status"] == "FINISHED"
    assert row["scan_ui_text_form"]
    assert row["scan_ui_structured_form"]
    assert row["scan_ui_graph_form"]
    assert row["scan_ui_markdown_narrative_form"]
    assert row["scan_ui_cli_command"]
    assert row["scan_ui_structured_form_type"] == "json"

    results = json.loads(row["scan_results"])
    assert results["vars"]["all_domains"]

    rg = store.get_subgraph("scan_result_graph", result.scan_result_id)
    assert rg is not None
    assert rg["scan_instance_id"] == result.scan_instance_id

    # SPEC-018 R18-06: temp export is synchronous before FINISHED.
    temp = store.get_subgraph("temporary_subgraph", result.temporary_subgraph_id)
    assert temp is not None
    assert (temp.get("graph") or {}).get("nodes") or temp.get("nodes")


def test_unknown_step_raises(store: FakeCrudStore) -> None:
    with pytest.raises(OrchestratorError, match="step not found"):
        run_single_step(
            store,
            workflow_id="workflow--ao1-unit",
            step_id="missing_step",
            dry_run=True,
        )


def test_module_id_from_uses(store: FakeCrudStore) -> None:
    register_module("sfp_cli_subfinder", _fixture_module_result)
    result = run_single_step(
        store,
        workflow_id="workflow--ao1-unit",
        step_id="sfp_cli_subfinder",
        dry_run=False,
    )
    assert result.module_id == "sfp_cli_subfinder"
    assert isinstance(result.command, list)


def test_unexpected_module_exception_leaves_error_failed(store: FakeCrudStore) -> None:
    """R15-05 — generic exception after RUNNING must terminalise ERROR-FAILED."""

    def _boom(_spec: Any = None) -> Dict[str, Any]:
        raise RuntimeError("simulated module crash")

    register_module("sfp_cli_subfinder", _boom)
    with pytest.raises(OrchestratorError, match="simulated module crash"):
        run_single_step(
            store,
            workflow_id="workflow--ao1-unit",
            step_id="sfp_cli_subfinder",
            dry_run=False,
        )
    sid = scan_instance_id_for("workflow--ao1-unit", "sfp_cli_subfinder")
    step = store.get_scan_step(sid)
    assert step is not None
    assert step.get("scan_status") == "ERROR-FAILED"
    assert step.get("scan_status") != "RUNNING"

def test_build_scan_step_spec_argv_includes_all_urls_r19_07() -> None:
    """R19-07: argv steps must pass full input_values as urls for Nuclei batching."""
    from spiderfeet_v2.engine.step_runner import _build_scan_step_spec
    from spiderfeet_v2.workflow.tempfile_mgr import TempFileManager

    urls = [f"https://host{i}.example" for i in range(45)]
    step = {
        "config": {
            "argv": [
                "nuclei",
                "-u",
                "$step.input.values[0]",
                "-jsonl-export",
                "$step.temp.out",
            ],
        }
    }
    spec, _argv = _build_scan_step_spec(
        step,
        urls,
        TempFileManager(),
        workflow_inputs={"targets": urls},
    )
    assert spec["domain"] == urls[0]
    assert spec["target"] == urls[0]
    assert spec["urls"] == urls
    assert len(spec["urls"]) == 45
