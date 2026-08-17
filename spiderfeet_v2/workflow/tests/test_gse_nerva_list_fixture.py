"""SPEC-019 R19-06 / B2 — Nerva `--list` ip:port file contract on 12A (no live CLI)."""

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
NERVA_FIXTURE = ROOT / "modules_v2" / "tests" / "fixtures" / "nerva_scanme_80.json"


@pytest.fixture(scope="module")
def doc_12a():
    return load_workflow(EXAMPLE_12A, validate=True)


@pytest.fixture(scope="module")
def nerva_step(doc_12a):
    return next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nerva")


def _graph_from_fixture(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {"nodes": raw.get("nodes", []), "edges": raw.get("edges", [])}


def _ip_ports_from_nmap_corpus(doc_12a) -> list[str]:
    nmap_step = next(s for s in doc_12a["steps"] if s["id"] == "sfp_cli_nmap")
    graph = _graph_from_fixture(NMAP_FIXTURE)
    ip_ports = evaluate_output_vars(nmap_step, graph)["ip_port_list"]
    assert ip_ports
    assert all(":" in line for line in ip_ports)
    return ip_ports


def test_12a_nerva_step_uses_list_file_argv(nerva_step) -> None:
    argv = (nerva_step.get("config") or {}).get("argv") or []
    assert "--list" in argv
    assert "$step.files.input" in argv
    assert "-iL" not in argv
    assert (nerva_step.get("input") or {}).get("empty") == "skip_step"


def test_nerva_list_file_ip_port_lines(doc_12a, nerva_step) -> None:
    ip_ports = _ip_ports_from_nmap_corpus(doc_12a)
    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_nmap": {"vars": {"ip_port_list": ip_ports}}},
    )
    resolved = resolve_step_inputs(nerva_step, env)
    assert resolved == ip_ports

    temps = TempFileManager()
    try:
        cmd = build_step_command(nerva_step, resolved, temps)
        assert "-t" not in cmd.argv
        assert "--list" in cmd.argv
        list_idx = cmd.argv.index("--list")
        list_path = cmd.argv[list_idx + 1]
        assert list_path == str(cmd.input_path)
        lines = cmd.input_path.read_text(encoding="utf-8").strip().splitlines()
        assert lines == ip_ports
    finally:
        temps.cleanup()


def test_nerva_empty_ip_port_list_skip_step(doc_12a, nerva_step) -> None:
    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_nmap": {"vars": {"ip_port_list": []}}},
    )
    resolved = resolve_step_inputs(nerva_step, env)
    assert resolved == []
    assert (nerva_step.get("input") or {}).get("empty") == "skip_step"


def test_nerva_dry_run_argv_list_file_path(doc_12a, nerva_step) -> None:
    """Argv resolution dry-run: non-empty list materializes `--list` file path in argv."""
    ip_ports = _ip_ports_from_nmap_corpus(doc_12a)
    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"sfp_cli_nmap": {"vars": {"ip_port_list": ip_ports}}},
    )
    resolved = resolve_step_inputs(nerva_step, env)

    temps = TempFileManager()
    try:
        cmd = build_step_command(nerva_step, resolved, temps)
        dry_run_argv = list(cmd.argv)
        list_path = Path(dry_run_argv[dry_run_argv.index("--list") + 1])
        assert list_path.is_file()
        assert list_path.read_text(encoding="utf-8").strip().splitlines() == ip_ports
    finally:
        temps.cleanup()

    assert "--output" in dry_run_argv
    out_idx = dry_run_argv.index("--output")
    assert out_idx + 1 < len(dry_run_argv)


def test_nerva_fixture_jsonl_fingerprint_records() -> None:
    doc = json.loads(NERVA_FIXTURE.read_text(encoding="utf-8"))
    records = doc.get("records") or []
    assert doc.get("schema") == "nerva_fingerprint_v1"
    assert len(records) >= 1
    for row in records:
        assert row.get("host")
        assert row.get("port")
        assert row.get("protocol")
