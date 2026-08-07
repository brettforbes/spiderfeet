"""Resolve workflow variable references (SPEC-007 R3)."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Mapping

_REF = re.compile(
    r"^\$(workflow\.inputs\.(?P<inp>[a-zA-Z_][a-zA-Z0-9_]*)"
    r"|steps\.(?P<step>[a-z][a-z0-9_]*)\.vars\.(?P<var>[a-zA-Z_][a-zA-Z0-9_]*)"
    r"|step\.vars\.(?P<stepvar>[a-zA-Z_][a-zA-Z0-9_]*))$"
)


class VariableError(KeyError):
    pass


def resolve_string_list(ref: str, env: Mapping[str, Any]) -> List[str]:
    """Resolve a reference string to a string list."""
    m = _REF.match(ref.strip())
    if not m:
        raise VariableError(f"unsupported reference: {ref}")

    if m.group("inp"):
        inputs = env.get("workflow", {}).get("inputs", {})
        val = inputs.get(m.group("inp"))
        if val is None:
            raise VariableError(ref)
        return list(val)

    if m.group("step"):
        step_id = m.group("step")
        var = m.group("var")
        steps = env.get("steps", {})
        step_env = steps.get(step_id, {})
        vars_map = step_env.get("vars", {})
        if var not in vars_map:
            raise VariableError(ref)
        return list(vars_map[var])

    if m.group("stepvar"):
        var = m.group("stepvar")
        cur = env.get("step", {}).get("vars", {})
        if var not in cur:
            raise VariableError(ref)
        return list(cur[var])

    raise VariableError(ref)


def resolve_step_input(from_ref: str, env: Mapping[str, Any]) -> List[str]:
    return resolve_string_list(from_ref, env)


def build_env(
    *,
    workflow_inputs: Mapping[str, List[str]],
    steps: Mapping[str, Mapping[str, Any]],
    step_vars: Mapping[str, List[str]] | None = None,
) -> Dict[str, Any]:
    return {
        "workflow": {"inputs": dict(workflow_inputs)},
        "steps": {k: {"vars": dict(v.get("vars", {}))} for k, v in steps.items()},
        "step": {"vars": dict(step_vars or {})},
    }
