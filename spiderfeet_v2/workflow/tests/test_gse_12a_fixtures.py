"""SPEC-018 A5 — 12A output.vars on corpus fixtures (post-A2)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from spiderfeet_v2.workflow.gse_eval import evaluate_output_vars
from spiderfeet_v2.workflow.loader import load_workflow

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
NS = ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"

CASES = [
    (
        "sfp_cli_subfinder",
        NS / "subfinder_corporate_upside_au_passive_cs_proposed_nuggets_edges.json",
        {"targets": ["theupside.com.au"]},
        {
            "subdomains": (1, None),
            "all_domains": (1, None),
        },
    ),
    (
        "sfp_cli_nmap",
        NS / "nmap_tcp_top_ports_permissive_proposed_nuggets_edges.json",
        {},
        {"ip_port_list": (1, None)},
    ),
    (
        "sfp_cli_httpx",
        NS / "httpx_from_subfinder_upside_au_proposed_nuggets_edges.json",
        {},
        {"live_hosts": (1, None)},
    ),
    (
        "sfp_cli_katana",
        NS / "katana_from_httpx_upside_com_proposed_nuggets_edges.json",
        {},
        {"crawl_urls": (100, None)},
    ),
]


@pytest.fixture(scope="module")
def doc_12a():
    return load_workflow(EXAMPLE_12A, validate=True)


def _graph(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {"nodes": raw.get("nodes", []), "edges": raw.get("edges", [])}


@pytest.mark.parametrize("step_id,fixture,workflow_inputs,expectations", CASES)
def test_12a_output_vars_on_corpus(
    doc_12a, step_id, fixture, workflow_inputs, expectations
):
    step = next(s for s in doc_12a["steps"] if s["id"] == step_id)
    vars_out = evaluate_output_vars(
        step,
        _graph(fixture),
        workflow_inputs=workflow_inputs or None,
    )
    for var_name, (min_count, max_count) in expectations.items():
        values = vars_out[var_name]
        assert len(values) >= min_count, f"{step_id}.{var_name} empty on {fixture.name}"
        if max_count is not None:
            assert len(values) <= max_count


def test_subfinder_apex_may_be_empty_on_corpus(doc_12a):
    """Documented A1 gap: apex GSE empty when all domains carry DOMAIN_NAME_PARENT."""
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_subfinder")
    fixture = NS / "subfinder_corporate_upside_au_passive_cs_proposed_nuggets_edges.json"
    vars_out = evaluate_output_vars(
        step,
        _graph(fixture),
        workflow_inputs={"targets": ["theupside.com.au"]},
    )
    assert vars_out["apex_domains"] == []
    assert "theupside.com.au" in vars_out["all_domains"] or len(vars_out["all_domains"]) >= 1
