"""SPEC-010 AM1 / R10-20 — parse, validate, schedule, argv/files, GSE (12A)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from spiderfeet_v2.workflow.argv import build_step_command
from spiderfeet_v2.workflow.gse_eval import evaluate_output_vars
from spiderfeet_v2.workflow.inputs import resolve_step_inputs
from spiderfeet_v2.workflow.loader import (
    WorkflowLoadError,
    load_workflow,
    schedule_waves,
    topological_waves,
    validate_workflow_dict,
    workflow_input_values,
)
from spiderfeet_v2.workflow.tempfile_mgr import TempFileManager
from spiderfeet_v2.workflow.variables import build_env

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"


@pytest.fixture(scope="module")
def doc_12a():
    return load_workflow(EXAMPLE_12A, validate=True)


def test_12a_loads_and_validates(doc_12a):
    assert doc_12a["apiVersion"] == "spiderfeet.workflow/v1"
    assert doc_12a["kind"] == "Workflow"
    assert len(doc_12a["steps"]) == 6
    assert workflow_input_values(doc_12a)["targets"] == ["https://example.com"]


def test_12a_schedule_waves(doc_12a):
    waves = schedule_waves(doc_12a["steps"])
    assert waves[0] == ["sfp_cli_subfinder"]
    assert set(waves[1]) == {"sfp_cli_nmap", "sfp_cli_httpx"}
    # full DAG shape
    flat = [sid for wave in waves for sid in wave]
    assert flat[:1] == ["sfp_cli_subfinder"]
    assert "sfp_cli_nerva" in flat
    assert "sfp_cli_nuclei" in flat
    assert topological_waves(doc_12a["steps"]) == waves


def test_cycle_rejected():
    raw = yaml.safe_load(EXAMPLE_12A.read_text(encoding="utf-8"))
    raw["steps"][0]["needs"] = ["sfp_cli_nuclei"]
    with pytest.raises(WorkflowLoadError, match="cycle"):
        validate_workflow_dict(raw)


def test_resolve_input_from_with_normalize(doc_12a):
    inputs = workflow_input_values(doc_12a)
    env = build_env(workflow_inputs=inputs, steps={})
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_subfinder")
    values = resolve_step_inputs(step, env)
    assert values == ["example.com"]


def test_resolve_input_from_prior_step_vars(doc_12a):
    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_subfinder": {"vars": {"all_domains": ["a.example.com", "b.example.com"]}}},
    )
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nmap")
    values = resolve_step_inputs(step, env)
    assert values == ["a.example.com", "b.example.com"]


def test_build_argv_and_files_subfinder(doc_12a):
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_subfinder")
    temps = TempFileManager()
    try:
        cmd = build_step_command(
            step,
            ["example.com", "other.example.com"],
            temps,
            workflow_inputs={"targets": ["https://example.com"]},
        )
        assert cmd.input_path is not None
        assert cmd.output_path is not None
        lines = cmd.input_path.read_text(encoding="utf-8").strip().splitlines()
        assert lines == ["example.com", "other.example.com"]
        assert cmd.argv[0] == "-dL"
        assert cmd.argv[1] == str(cmd.input_path)
        assert cmd.argv[2] == "-oJ"
        assert cmd.argv[-2] == str(cmd.output_path) or cmd.argv[5] == str(cmd.output_path)
        assert "-silent" in cmd.argv
        # argv is a list of strings — never a shell-joined command
        assert all(isinstance(t, str) for t in cmd.argv)
        assert " " not in cmd.argv[0]
    finally:
        temps.cleanup()


def test_evaluate_output_vars_subfinder_gse(doc_12a):
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_subfinder")
    graph = {
        "nodes": [
            {"id": "d1", "nugget_id": "DOMAIN_NAME", "nugget_data": "example.com"},
            {"id": "d2", "nugget_id": "DOMAIN_NAME", "nugget_data": "www.example.com"},
            {"id": "p1", "nugget_id": "DOMAIN_NAME_PARENT", "nugget_data": "example.com"},
        ],
        "edges": [
            {"source": "d2", "target": "p1", "relation": "had"},
        ],
    }
    vars_out = evaluate_output_vars(step, graph)
    assert vars_out["apex_domains"] == ["example.com"]
    assert vars_out["subdomains"] == ["www.example.com"]
    assert vars_out["all_domains"] == ["example.com", "www.example.com"]


def test_evaluate_output_vars_nmap_product(doc_12a):
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nmap")
    # 12A GSE matches SPEC-005 IP classification (IPV4_ADDRESS / IPV6_ADDRESS).
    graph = {
        "nodes": [
            {"id": "h1", "nugget_id": "HOST", "nugget_data": "www.example.com"},
            {"id": "ip1", "nugget_id": "IPV4_ADDRESS", "nugget_data": "1.2.3.4"},
            {"id": "p443", "nugget_id": "PORT", "nugget_data": "443"},
            {"id": "p80", "nugget_id": "PORT", "nugget_data": "80"},
        ],
        "edges": [
            {"source": "h1", "target": "ip1", "relation": "contains"},
            {"source": "h1", "target": "p443", "relation": "contains"},
            {"source": "h1", "target": "p80", "relation": "contains"},
        ],
    }
    vars_out = evaluate_output_vars(step, graph)
    assert "1.2.3.4:80" in vars_out["ip_port_list"]
    assert "1.2.3.4:443" in vars_out["ip_port_list"]


def test_duplicate_step_ids_rejected(doc_12a):
    raw = yaml.safe_load(EXAMPLE_12A.read_text(encoding="utf-8"))
    raw["steps"].append(dict(raw["steps"][0]))
    with pytest.raises(WorkflowLoadError, match="duplicate"):
        validate_workflow_dict(raw, validate_gse=False)
