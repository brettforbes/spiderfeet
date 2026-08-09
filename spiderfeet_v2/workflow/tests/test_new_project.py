"""R13-04 / B2-1 — info-only workflow document builder (unit)."""

from __future__ import annotations

from spiderfeet_v2.workflow.new_project import (
    build_info_only_workflow_doc,
    build_info_only_workflow_yaml,
)
from spiderfeet_v2.workflow.typedb_convert import parse_yaml_string


def test_build_info_only_workflow_has_no_steps_or_inputs() -> None:
    doc = build_info_only_workflow_doc(
        workflow_id="workflow--test",
        name="Demo",
        description="Desc",
        author="User",
        created="2026-08-09T10:00:00Z",
    )
    assert doc["apiVersion"] == "spiderfeet.workflow/v1"
    assert doc["kind"] == "Workflow"
    assert doc["id"] == "workflow--test"
    assert doc["info"]["name"] == "Demo"
    assert "steps" not in doc
    assert "inputs" not in doc
    yaml_text = build_info_only_workflow_yaml(
        workflow_id="workflow--test",
        name="Demo",
        description="Desc",
        created="2026-08-09T10:00:00Z",
    )
    parsed = parse_yaml_string(yaml_text)
    assert parsed["info"]["author"] == "User"
    assert "steps" not in parsed
