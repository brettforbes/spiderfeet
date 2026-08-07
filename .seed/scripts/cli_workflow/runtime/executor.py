"""Workflow DAG executor skeleton (S3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Protocol

from cli_workflow.core.context_export import merge_graph
from cli_workflow.core.gse_eval import eval_binding
from cli_workflow.core.loader import topological_waves
from cli_workflow.core.variables import resolve_step_input


class StepRunner(Protocol):
  def run_step(
      self,
      step: Mapping[str, Any],
      input_values: List[str],
  ) -> Dict[str, Any]:
      """Return {scan_graph, structured_path?, exit_code}."""


@dataclass
class StepResult:
    step_id: str
    input_values: List[str]
    scan_graph: Dict[str, Any]
    vars: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class WorkflowResult:
    steps: Dict[str, StepResult] = field(default_factory=dict)
    context: Dict[str, List[Any]] = field(default_factory=lambda: {"nodes": [], "edges": []})


def _eval_step_vars(step: Mapping[str, Any], scan_graph: Mapping[str, Any]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    vars_map = (step.get("output") or {}).get("vars") or {}
    for name, binding in vars_map.items():
        if "select" in binding or "from_var" in binding or "literal" in binding:
            out[name] = eval_binding(binding, graph=scan_graph)
    for name, binding in vars_map.items():
        if "union" not in binding:
            continue
        env_lists: Dict[str, List[str]] = {}
        for ref in binding["union"]:
            key = ref.split(".")[-1]
            if key not in out:
                raise KeyError(f"union ref {ref} not ready for step {step.get('id')}")
            env_lists[ref] = out[key]
        out[name] = eval_binding(binding, env_lists=env_lists)
    return out


def execute_workflow(
    doc: Mapping[str, Any],
    runner: StepRunner,
    *,
    workflow_inputs: Optional[Mapping[str, List[str]]] = None,
) -> WorkflowResult:
    waves = topological_waves(doc["steps"])
    if waves is None:
        raise ValueError("workflow has cycle")

    inputs = workflow_inputs or {
        k: list(v.get("default") or [])
        for k, v in (doc.get("inputs") or {}).items()
    }
    result = WorkflowResult()
    step_by_id = {s["id"]: s for s in doc["steps"]}

    for wave in waves:
        for step_id in wave:
            step = step_by_id[step_id]
            env = {
                "workflow": {"inputs": inputs},
                "steps": {sid: {"vars": result.steps[sid].vars} for sid in result.steps},
                "step": {"vars": {}},
            }
            input_values = resolve_step_input(step["input"]["from"], env)
            run_out = runner.run_step(step, input_values)
            scan_graph = run_out["scan_graph"]
            vars_out = _eval_step_vars(step, scan_graph)
            sr = StepResult(step_id=step_id, input_values=input_values, scan_graph=scan_graph, vars=vars_out)
            result.steps[step_id] = sr
            export = (step.get("context") or {}).get("export")
            if export == "scan_graph":
                merge_graph(result.context, scan_graph)
    return result
