"""R3 — variable resolution tests."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".seed" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cli_workflow.core.variables import build_env, resolve_step_input  # noqa: E402


def test_resolve_workflow_inputs_and_step_vars():
    env = build_env(
        workflow_inputs={"targets": ["example.com"]},
        steps={"subfinder_enum": {"vars": {"all_domains": ["a.example.com"]}}},
    )
    assert resolve_step_input("$workflow.inputs.targets", env) == ["example.com"]
    assert resolve_step_input("$steps.subfinder_enum.vars.all_domains", env) == ["a.example.com"]
