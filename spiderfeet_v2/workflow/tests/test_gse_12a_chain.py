"""SPEC-018 A3 — Nerva chain proof on corpus fixtures (no live CLI)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from spiderfeet_v2.workflow.argv import build_step_command
from spiderfeet_v2.workflow.gse_eval import evaluate_output_vars
from spiderfeet_v2.workflow.inputs import resolve_step_inputs
from spiderfeet_v2.workflow.loader import load_workflow
from spiderfeet_v2.workflow.tempfile_mgr import TempFileManager
from spiderfeet_v2.workflow.variables import build_env

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_12A = ROOT / ".seed" / "12A_Workflow_YAML_Example.yaml"
NS = ROOT / ".docs" / "docs-for-cli-tools" / "nugget_structure"

NMAP_FIXTURE = NS / "nmap_tcp_top_ports_permissive_proposed_nuggets_edges.json"
KATANA_FIXTURE = NS / "katana_from_httpx_upside_com_proposed_nuggets_edges.json"


@pytest.fixture(scope="module")
def doc_12a():
    return load_workflow(EXAMPLE_12A, validate=True)


def _graph_from_fixture(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {"nodes": raw.get("nodes", []), "edges": raw.get("edges", [])}


def test_nmap_ip_port_list_non_empty_on_corpus(doc_12a):
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nmap")
    graph = _graph_from_fixture(NMAP_FIXTURE)
    vars_out = evaluate_output_vars(step, graph)
    ip_ports = vars_out["ip_port_list"]
    assert len(ip_ports) >= 1
    assert all(":" in line for line in ip_ports)


def test_nerva_argv_receives_ip_port_list(doc_12a):
    nmap_step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nmap")
    nerva_step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nerva")
    graph = _graph_from_fixture(NMAP_FIXTURE)
    ip_ports = evaluate_output_vars(nmap_step, graph)["ip_port_list"]
    assert ip_ports

    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_nmap": {"vars": {"ip_port_list": ip_ports}}},
    )
    resolved = resolve_step_inputs(nerva_step, env)
    assert resolved == ip_ports

    temps = TempFileManager()
    try:
        cmd = build_step_command(nerva_step, resolved, temps)
        assert "--list" in cmd.argv
        list_idx = cmd.argv.index("--list")
        assert cmd.argv[list_idx + 1] == str(cmd.input_path)
        lines = cmd.input_path.read_text(encoding="utf-8").strip().splitlines()
        assert lines == ip_ports
    finally:
        temps.cleanup()


def test_nerva_empty_ip_port_list_is_empty_input(doc_12a):
    nerva_step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nerva")
    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_nmap": {"vars": {"ip_port_list": []}}},
    )
    resolved = resolve_step_inputs(nerva_step, env)
    assert resolved == []
    assert (nerva_step.get("input") or {}).get("empty") == "skip_step"


def test_katana_crawl_urls_non_empty_on_corpus(doc_12a):
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_katana")
    graph = _graph_from_fixture(KATANA_FIXTURE)
    urls = evaluate_output_vars(step, graph)["crawl_urls"]
    assert len(urls) >= 100


def test_nuclei_input_from_katana_vars(doc_12a):
    katana_step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_katana")
    nuclei_step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nuclei")
    graph = _graph_from_fixture(KATANA_FIXTURE)
    crawl_urls = evaluate_output_vars(katana_step, graph)["crawl_urls"]
    assert crawl_urls

    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_katana": {"vars": {"crawl_urls": crawl_urls[:3]}}},
    )
    resolved = resolve_step_inputs(nuclei_step, env)
    assert resolved == crawl_urls[:3]

    temps = TempFileManager()
    try:
        cmd = build_step_command(nuclei_step, resolved, temps)
        assert "-l" in cmd.argv
        list_idx = cmd.argv.index("-l")
        assert cmd.argv[list_idx + 1] == str(cmd.input_path)
        lines = cmd.input_path.read_text(encoding="utf-8").strip().splitlines()
        assert lines == crawl_urls[:3]
    finally:
        temps.cleanup()


def test_nuclei_empty_crawl_urls_is_skip_step(doc_12a):
    nuclei_step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nuclei")
    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_katana": {"vars": {"crawl_urls": []}}},
    )
    resolved = resolve_step_inputs(nuclei_step, env)
    assert resolved == []
    assert (nuclei_step.get("input") or {}).get("empty") == "skip_step"

def test_katana_crawl_urls_excludes_domain_name_r19_09(doc_12a):
    step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_katana")
    graph = _graph_from_fixture(KATANA_FIXTURE)
    urls = evaluate_output_vars(step, graph)["crawl_urls"]
    domain_values = {
        str(n.get("nugget_data", ""))
        for n in graph["nodes"]
        if n.get("nugget_id") == "DOMAIN_NAME"
    }
    assert domain_values
    overlap = [u for u in urls if u in domain_values]
    assert not overlap
    assert all("://" in u for u in urls[:100])


def test_nuclei_45_urls_three_batches_r19_09():
    from modules_v2.sfp_cli_nuclei import progress_totals

    urls = [f"https://host{i}.example" for i in range(45)]
    assert progress_totals(urls)["batches_total"] == 3
