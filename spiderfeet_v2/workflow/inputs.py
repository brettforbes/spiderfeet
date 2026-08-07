"""Resolve step ``input.from`` with optional normalization."""

from __future__ import annotations

from typing import Any, List, Mapping

from spiderfeet_v2.workflow.normalize import normalize_list
from spiderfeet_v2.workflow.variables import resolve_step_input


def resolve_step_inputs(
    step: Mapping[str, Any],
    env: Mapping[str, Any],
) -> List[str]:
    """Resolve ``input.from`` and apply ``input.normalize`` when set."""
    inp = step.get("input") or {}
    values = resolve_step_input(inp["from"], env)
    return normalize_list(values, inp.get("normalize"))
