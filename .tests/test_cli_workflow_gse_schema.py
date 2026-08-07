"""P2 — gse_v1.schema.json validation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".seed" / "scripts"
EXAMPLE = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
GSE_SCHEMA = SCRIPTS / "cli_workflow" / "schema" / "gse_v1.schema.json"

sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.loader import WorkflowLoadError, validate_gse_binding, validate_workflow_dict  # noqa: E402


def test_gse_schema_file_exists():
    assert GSE_SCHEMA.is_file()


def test_all_12a_output_vars_validate_gse():
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    validate_workflow_dict(doc, validate_gse=True)


def test_informal_concat_binding_rejected():
    sketch = {
        "type": "string_list",
        "value": 'concat({{IP_ADDRESS}}, ":", {{PORT}})',
    }
    with pytest.raises(Exception):
        validate_gse_binding(sketch)


def test_invalid_gse_missing_select_shape():
    bad = {"type": "string_list", "foo": "bar"}
    with pytest.raises(Exception):
        validate_gse_binding(bad)


def test_valid_union_binding():
    validate_gse_binding(
        {
            "type": "string_list",
            "union": ["$step.vars.a", "$step.vars.b"],
            "distinct": True,
        }
    )


def test_12a_ip_port_for_each_fragment_validates():
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    nmap = next(s for s in doc["steps"] if s["id"] == "sfp_cli_nmap")
    binding = nmap["output"]["vars"]["ip_port_list"]
    validate_gse_binding(binding)


def test_workflow_with_bad_gse_var_rejected():
    doc = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    doc["steps"][0].setdefault("output", {}).setdefault("vars", {})["bad"] = {
        "type": "not_a_string_list",
        "select": {"source": "$step.scan_graph", "nodes": {"nugget_id": "HOST"}},
    }
    with pytest.raises(Exception):
        validate_workflow_dict(doc, validate_gse=True)
