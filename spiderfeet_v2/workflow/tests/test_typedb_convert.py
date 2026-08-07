"""SPEC-010 AM2 / R10-21 — YAML ↔ TypeDB conversion (pure + TypeDB round-trip)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from spiderfeet_v2.workflow.loader import load_workflow
from spiderfeet_v2.workflow.typedb_convert import (
    API_WORKFLOW_KEYS,
    WorkflowConvertError,
    canonical_workflow_dict,
    dump_canonical_yaml,
    load_workflow_api_json,
    load_workflow_yaml,
    module_id_for_step,
    persist_workflow_yaml,
    scan_instance_id_for,
    typedb_forms_to_yaml,
    typedb_to_api_json,
    workflows_equal,
    yaml_to_typedb_forms,
)

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
SMOKE_DB = "spiderfeet-am2-smoke"


@pytest.fixture(scope="module")
def doc_12a():
    return load_workflow(EXAMPLE_12A, validate=True)


def test_yaml_to_typedb_forms_12a(doc_12a):
    forms = yaml_to_typedb_forms(doc_12a)
    assert forms.workflow_id == doc_12a["id"]
    assert forms.workflow["name"] == doc_12a["info"]["name"]
    assert forms.target["target_value"] == "https://example.com"
    assert forms.target["target_yaml"]
    assert len(forms.steps) == 6
    assert {s["step_module_id"] for s in forms.steps} == {
        "sfp_cli_subfinder",
        "sfp_cli_nmap",
        "sfp_cli_nerva",
        "sfp_cli_httpx",
        "sfp_cli_katana",
        "sfp_cli_nuclei",
    }
    # DAG roles
    first = forms.workflow["first_step_id"]
    assert first == scan_instance_id_for(doc_12a["id"], "sfp_cli_subfinder")
    prior = set(forms.workflow["prior_step_ids"])
    nxt = set(forms.workflow["next_step_ids"])
    assert first in prior
    assert scan_instance_id_for(doc_12a["id"], "sfp_cli_nerva") in nxt
    assert scan_instance_id_for(doc_12a["id"], "sfp_cli_nuclei") in nxt
    # yaml shadows parse
    assert yaml.safe_load(forms.workflow_yaml)["id"] == doc_12a["id"]
    for step in forms.steps:
        frag = yaml.safe_load(step["scan_yaml"])
        assert frag["id"] in forms.step_id_by_scan_instance.values()


def test_pure_round_trip_equals_canonical(doc_12a):
    forms = yaml_to_typedb_forms(doc_12a)
    rebuilt = typedb_forms_to_yaml(
        forms.workflow, steps=forms.steps, target=forms.target
    )
    assert workflows_equal(doc_12a, rebuilt)
    # Also via workflow_yaml-only path
    rebuilt2 = typedb_forms_to_yaml({"workflow_id": forms.workflow_id, "workflow_yaml": forms.workflow_yaml})
    assert workflows_equal(doc_12a, rebuilt2)


def test_fragment_rebuild_without_workflow_yaml(doc_12a):
    forms = yaml_to_typedb_forms(doc_12a)
    workflow_no_yaml = {
        k: v for k, v in forms.workflow.items() if k != "workflow_yaml"
    }
    rebuilt = typedb_forms_to_yaml(
        workflow_no_yaml, steps=forms.steps, target=forms.target
    )
    assert rebuilt["id"] == doc_12a["id"]
    assert rebuilt["apiVersion"] == "spiderfeet.workflow/v1"
    assert len(rebuilt["steps"]) == 6
    assert set(s["id"] for s in rebuilt["steps"]) == set(
        s["id"] for s in doc_12a["steps"]
    )


def test_typedb_to_api_json_shape(doc_12a):
    forms = yaml_to_typedb_forms(doc_12a)
    api = typedb_to_api_json(forms.workflow, prefer_projection_keys=False)
    assert tuple(api.keys()) == API_WORKFLOW_KEYS
    assert api["workflow_id"] == doc_12a["id"]
    assert api["target"] == forms.target["target_id"]
    assert api["first_step"] == forms.workflow["first_step_id"]
    assert api["prior_step"] == forms.workflow["prior_step_ids"]
    assert api["next_step"] == forms.workflow["next_step_ids"]
    assert api["workflow_yaml"] == forms.workflow_yaml
    # projection-shaped input
    projected = {
        "workflow_id": api["workflow_id"],
        "target": api["target"],
        "first_step": api["first_step"],
        "prior_step": api["prior_step"],
        "next_step": api["next_step"],
        "workflow_yaml": api["workflow_yaml"],
    }
    assert typedb_to_api_json(projected) == api


def test_module_id_for_step_from_uses():
    assert module_id_for_step({"id": "enum", "uses": "tool.subfinder"}) == "sfp_cli_subfinder"
    assert module_id_for_step({"id": "sfp_cli_nmap", "uses": "tool.nmap"}) == "sfp_cli_nmap"


def test_canonical_dump_stable(doc_12a):
    a = dump_canonical_yaml(doc_12a)
    b = dump_canonical_yaml(yaml.safe_load(a))
    assert a == b
    assert canonical_workflow_dict(doc_12a) == yaml.safe_load(a)


# ---------------------------------------------------------------------------
# TypeDB integration (AL1 CRUD + AL3 projection)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def stores():
    pytest.importorskip("typedb.driver")
    from spiderfeet_v2.db.bootstrap import bootstrap_actual
    from spiderfeet_v2.db.config import TypeDBConfigError, load_connection_config
    from spiderfeet_v2.db.connection import open_driver, ping
    from spiderfeet_v2.db.crud import CrudStore
    from spiderfeet_v2.db.projections import ProjectionStore

    try:
        cfg = load_connection_config()
    except TypeDBConfigError as exc:
        pytest.skip(f"TypeDB config missing: {exc}")
    if not ping(cfg):
        pytest.skip("TypeDB server not reachable")

    report = bootstrap_actual(cfg, database=SMOKE_DB, reset=True)
    assert report.ok, report.errors

    crud = CrudStore.connect(cfg, database=SMOKE_DB)
    proj = ProjectionStore.connect(cfg, database=SMOKE_DB)
    yield crud, proj

    driver = open_driver(cfg)
    try:
        if driver.databases.contains(SMOKE_DB):
            driver.databases.get(SMOKE_DB).delete()
    finally:
        driver.close()


def test_typedb_round_trip_yaml_equals_canonical(stores, doc_12a):
    crud, proj = stores
    forms = persist_workflow_yaml(crud, doc_12a, replace=True)
    assert forms.workflow_id == doc_12a["id"]

    loaded = load_workflow_yaml(crud, doc_12a["id"])
    assert workflows_equal(doc_12a, loaded)

    # CRUD row → API shape
    api_from_crud = load_workflow_api_json(crud, doc_12a["id"])
    assert api_from_crud["workflow_id"] == doc_12a["id"]
    assert api_from_crud["target"] == forms.target["target_id"]
    assert api_from_crud["first_step"] == forms.workflow["first_step_id"]
    assert set(api_from_crud["prior_step"]) == set(forms.workflow["prior_step_ids"])
    assert set(api_from_crud["next_step"]) == set(forms.workflow["next_step_ids"])
    assert workflows_equal(
        doc_12a, yaml.safe_load(api_from_crud["workflow_yaml"])
    )

    # ProjectionStore (AL3) → API shape matches
    api_from_proj = load_workflow_api_json(
        crud, doc_12a["id"], projection_store=proj
    )
    assert api_from_proj["workflow_id"] == api_from_crud["workflow_id"]
    assert api_from_proj["target"] == api_from_crud["target"]
    assert api_from_proj["first_step"] == api_from_crud["first_step"]
    assert set(api_from_proj["prior_step"]) == set(api_from_crud["prior_step"])
    assert set(api_from_proj["next_step"]) == set(api_from_crud["next_step"])
    assert api_from_proj["workflow_yaml"] == api_from_crud["workflow_yaml"]


def test_persist_replace_idempotent(stores, doc_12a):
    crud, _ = stores
    persist_workflow_yaml(crud, doc_12a, replace=True)
    persist_workflow_yaml(crud, doc_12a, replace=True)
    loaded = load_workflow_yaml(crud, doc_12a["id"])
    assert workflows_equal(doc_12a, loaded)

    with pytest.raises(WorkflowConvertError, match="already exists"):
        persist_workflow_yaml(crud, doc_12a, replace=False)
