"""P1 — workflow_v1.schema.json validation."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".seed" / "scripts"
FIXTURES = SCRIPTS / "cli_workflow" / "fixtures"
EXAMPLE = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
SCHEMA = SCRIPTS / "cli_workflow" / "schema" / "workflow_v1.schema.json"

sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.loader import (  # noqa: E402
    WorkflowLoadError,
    load_workflow,
    validate_workflow_dict,
)


def test_workflow_schema_file_exists():
    assert SCHEMA.is_file()


def test_12a_example_validates():
    doc = load_workflow(EXAMPLE, validate=True)
    assert doc["apiVersion"] == "spiderfeet.workflow/v1"
    assert len(doc["steps"]) == 6


def test_cli_validate_12a():
    import subprocess

    env = {"PYTHONPATH": str(SCRIPTS)}
    r = subprocess.run(
        ["poetry", "run", "python", "-m", "cli_workflow.cli", "validate", str(EXAMPLE)],
        cwd=ROOT,
        env={**__import__("os").environ, **env},
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_invalid_fixture_bad_api_version_rejected():
    path = FIXTURES / "invalid_workflow_bad_api_version.yaml"
    with pytest.raises(Exception):
        load_workflow(path, validate=True)


def test_jsonschema_rejects_extra_top_level_property():
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    doc["unexpected_field"] = True
    with pytest.raises(Exception):
        validate_workflow_dict(doc, validate_gse=False)


def test_duplicate_step_ids_rejected():
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    doc["steps"].append(copy.deepcopy(doc["steps"][0]))
    with pytest.raises(WorkflowLoadError, match="duplicate"):
        validate_workflow_dict(doc, validate_gse=False)
