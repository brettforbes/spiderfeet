"""R2 — DAG validation tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".seed" / "scripts"
EXAMPLE = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.loader import WorkflowLoadError, load_workflow, topological_waves, validate_workflow_dict  # noqa: E402


def test_12a_topological_waves():
    doc = load_workflow(EXAMPLE, validate=True)
    waves = topological_waves(doc["steps"])
    assert waves[0] == ["subfinder_enum"]
    assert set(waves[1]) == {"nmap_ports", "httpx_live"}


def test_cycle_rejected():
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    doc["steps"][0]["needs"] = ["nuclei_vulns"]
    with pytest.raises(WorkflowLoadError, match="cycle"):
        validate_workflow_dict(doc)
