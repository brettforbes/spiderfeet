"""T3/S4 — dry E2E of 12A with fixture graphs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".seed" / "scripts"
EXAMPLE = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
FIXTURES = SCRIPTS / "cli_workflow" / "fixtures"

sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.loader import load_workflow  # noqa: E402
from cli_workflow.runtime.executor import execute_workflow  # noqa: E402


def test_dry_e2e_12a_context_export_policy():
    doc = load_workflow(EXAMPLE, validate=True)
    fixture_map = yaml.safe_load((FIXTURES / "dry_run_12a_graphs.yaml").read_text(encoding="utf-8"))

    class _Runner:
        def run_step(self, step, input_values):  # noqa: ANN001
            graph = json.loads((ROOT / fixture_map[step["id"]]).read_text(encoding="utf-8"))
            return {"scan_graph": graph}

    result = execute_workflow(doc, _Runner())
    export_ids = {
        s["id"]
        for s in doc["steps"]
        if (s.get("context") or {}).get("export") == "scan_graph"
    }
    assert export_ids == {"sfp_cli_subfinder", "sfp_cli_nmap", "sfp_cli_nerva", "sfp_cli_nuclei"}
    assert result.steps["sfp_cli_subfinder"].vars["all_domains"]
    assert result.steps["sfp_cli_nmap"].vars["ip_port_list"]
    assert len(result.context["nodes"]) > 0
