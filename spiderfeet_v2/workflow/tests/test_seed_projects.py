"""R13-07 — seed_projects builds/materializes 5 SPEC-013 projects."""

from __future__ import annotations

from pathlib import Path

from spiderfeet_v2.api.tests.conftest import FakeCrudStore
from spiderfeet_v2.workflow.loader import load_workflow, validate_workflow_dict
from spiderfeet_v2.workflow.seed_projects import (
    SEED_SPECS,
    build_seed_workflow_doc,
    seed_all,
)

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A2 = ROOT / ".seed" / "12A2_Workflow_YAML_Example.yaml"


def test_12a2_validates():
    """R13-07: no-input netdiscover template validates under relaxed DSL schema."""
    doc = load_workflow(EXAMPLE_12A2, validate=True)
    assert not doc.get("inputs")
    assert len(doc["steps"]) == 1
    assert doc["steps"][0]["uses"] == "tool.netdiscover"


def test_build_seed_docs_are_distinct():
    docs = [build_seed_workflow_doc(s) for s in SEED_SPECS]
    assert len(docs) == 5
    assert len({d["id"] for d in docs}) == 5
    assert len({d["info"]["name"] for d in docs}) == 5
    assert not docs[0].get("inputs")
    for d in docs[1:]:
        validate_workflow_dict(d)
        vals = d["inputs"]["targets"]["values"]
        assert len(vals) == 1
        assert vals[0].startswith("https://")


def test_seed_all_materializes_on_fake_store():
    """R13-07: persist_workflow_yaml path for all 5 seeds (no scan results)."""
    store = FakeCrudStore()
    results = seed_all(store, replace=True)
    assert len(results) == 5
    assert all(not r["skipped"] for r in results)
    assert len(store.list_projects()) == 5

    simple = next(r for r in results if r["template"] == "12A2")
    assert simple["step_count"] == 1
    assert simple["has_target"] is False
    wf = store.get_workflow(simple["workflow_id"])
    assert wf is not None
    assert not wf.get("target_id")
    assert wf["first_step_id"]
    step = store.get_scan_step(wf["first_step_id"])
    assert step["step_module_id"] == "sfp_cli_netdiscover"
    assert not step.get("scan_ui_text_form")
    assert not step.get("scan_ui_graph_form")

    clone = next(r for r in results if r["input_host"] == "sbs.com.au")
    assert clone["step_count"] == 6
    assert clone["has_target"] is True
    cwf = store.get_workflow(clone["workflow_id"])
    target = store.get_target(cwf["target_id"])
    assert target["target_value"] == "https://sbs.com.au"

    again = seed_all(store, replace=True)
    assert len(store.list_projects()) == 5
    assert again[0]["project_id"] == results[0]["project_id"]
