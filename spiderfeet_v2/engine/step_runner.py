"""AO1 single-step orchestrator (SPEC-010 R10-27)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

import yaml

from spiderfeet_v2.engine.modules import (
    ModuleResolveError,
    load_module_runner,
    resolve_module_id,
)
from spiderfeet_v2.engine.persist import (
    ensure_scan_step,
    persist_module_result,
    persist_temporary_export,
)
from spiderfeet_v2.engine.status import (
    MODULE_OK,
    OUTCOME_DRY_RUN,
    OUTCOME_ERROR,
    OUTCOME_SKIPPED,
    OUTCOME_SUCCESS,
    STATUS_ERROR_FAILED,
    STATUS_FINISHED,
    STATUS_RUNNING,
    STATUS_STARTING,
    outcome_for_scan_status,
)
from spiderfeet_v2.workflow.argv import build_step_command
from spiderfeet_v2.workflow.context_export import step_exports_scan_graph
from spiderfeet_v2.workflow.gse_eval import GseError, evaluate_output_vars
from spiderfeet_v2.workflow.inputs import resolve_step_inputs
from spiderfeet_v2.workflow.loader import workflow_input_values
from spiderfeet_v2.workflow.tempfile_mgr import TempFileManager
from spiderfeet_v2.workflow.typedb_convert import (
    WorkflowConvertError,
    load_workflow_yaml,
    scan_instance_id_for,
)
from spiderfeet_v2.workflow.variables import VariableError, build_env


class OrchestratorError(ValueError):
    """Single-step orchestration failure (bad inputs / missing workflow)."""


@dataclass
class StepRunResult:
    """Outcome of one orchestrated workflow step."""

    workflow_id: str
    step_id: str
    scan_instance_id: str
    module_id: str
    status: str
    scan_status: str
    message: str
    command: List[str] = field(default_factory=list)
    output_vars: Dict[str, List[str]] = field(default_factory=dict)
    counts: Dict[str, Any] = field(default_factory=dict)
    exported_to_temporary: bool = False
    temporary_subgraph_id: Optional[str] = None
    scan_result_id: Optional[str] = None
    error: Optional[str] = None
    dry_run: bool = False
    input_values: List[str] = field(default_factory=list)

    def to_api_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "message": self.message,
            "workflow_id": self.workflow_id,
            "step_id": self.step_id,
            "scan_instance_id": self.scan_instance_id,
            "orchestrator": "ao1",
            "module_id": self.module_id,
            "skipped": self.status == OUTCOME_SKIPPED,
            "scan_status": self.scan_status,
            "output_vars": self.output_vars,
            "exported_to_temporary": self.exported_to_temporary,
            "temporary_subgraph_id": self.temporary_subgraph_id,
            "scan_result_id": self.scan_result_id,
            "counts": self.counts,
            "error": self.error,
            "dry_run": self.dry_run,
            "command": self.command,
            "input_values": self.input_values,
        }


def _load_workflow_doc(store: Any, workflow_id: str) -> Dict[str, Any]:
    wf = store.get_workflow(workflow_id)
    if wf is None:
        raise OrchestratorError(f"workflow not found: {workflow_id}")
    yaml_text = wf.get("workflow_yaml")
    if yaml_text:
        doc = yaml.safe_load(yaml_text)
        if isinstance(doc, dict) and doc.get("steps"):
            return doc
    try:
        return load_workflow_yaml(store, workflow_id)
    except WorkflowConvertError as exc:
        raise OrchestratorError(str(exc)) from exc


def _find_step(doc: Mapping[str, Any], step_key: str) -> Dict[str, Any]:
    steps = list(doc.get("steps") or [])
    by_id = {str(s.get("id")): s for s in steps if s.get("id")}
    if step_key in by_id:
        return dict(by_id[step_key])

    # Allow scan_instance_id as the path key.
    workflow_id = str(doc.get("id") or "")
    for sid, step in by_id.items():
        if workflow_id and scan_instance_id_for(workflow_id, sid) == step_key:
            return dict(step)
        scan_yaml = step.get("scan_yaml")
        if isinstance(scan_yaml, str) and step_key in scan_yaml:
            return dict(step)
    raise OrchestratorError(f"step not found in workflow: {step_key}")


def _prior_vars_from_store(
    store: Any,
    workflow_id: str,
    step: Mapping[str, Any],
) -> Dict[str, Dict[str, List[str]]]:
    """Load output vars from previously persisted dependency scan_steps."""
    out: Dict[str, Dict[str, List[str]]] = {}
    for dep in step.get("needs") or []:
        sid = scan_instance_id_for(workflow_id, str(dep))
        row = store.get_scan_step(sid)
        if not row:
            continue
        raw = row.get("scan_results") or "{}"
        try:
            payload = json.loads(raw) if isinstance(raw, str) else dict(raw)
        except json.JSONDecodeError:
            continue
        vars_map = payload.get("vars") or {}
        if isinstance(vars_map, dict):
            out[str(dep)] = {
                k: list(v) if isinstance(v, list) else [str(v)]
                for k, v in vars_map.items()
            }
    return out


def _build_scan_step_spec(
    step: Mapping[str, Any],
    input_values: List[str],
    temps: TempFileManager,
    *,
    workflow_inputs: Mapping[str, List[str]],
) -> tuple[Dict[str, Any], List[str]]:
    """Materialize argv/files and build a modules_v2 scan_step_spec."""
    config = step.get("config") or {}
    primary = input_values[0] if input_values else None

    if config.get("argv"):
        cmd = build_step_command(
            step,
            input_values,
            temps,
            workflow_inputs=workflow_inputs,
        )
        # Do not pass structured_path here — modules short-circuit on that key
        # and would read the empty pre-allocated -o file instead of running CLI.
        # After argv execution, modules hydrate stdout from the -o path themselves.
        spec = {
            "argv": list(cmd.argv),
            "domain": primary,
            "target": primary,
        }
        return spec, list(cmd.argv)

    # Domain/target style (modules build their own structured flags).
    spec = {
        "domain": primary,
        "target": primary,
    }
    if config.get("args") is not None:
        spec["args"] = list(config["args"])
    if config.get("active") is not None:
        spec["active"] = config["active"]
    if config.get("timeout") is not None:
        spec["timeout"] = config["timeout"]
    preview = list(config.get("args") or [])
    if primary:
        preview = preview + ["-d", str(primary)]
    return spec, preview


def run_single_step(
    store: Any,
    *,
    workflow_id: str,
    step_id: str,
    project_id: Optional[str] = None,
    dry_run: bool = False,
    prior_vars: Optional[Mapping[str, Mapping[str, List[str]]]] = None,
    timeout: Optional[float] = None,
    existing_temporary_subgraph_id: Optional[str] = None,
) -> StepRunResult:
    """Run one workflow step end-to-end (or dry-run resolve without invoking CLI)."""
    doc = _load_workflow_doc(store, workflow_id)
    step = _find_step(doc, step_id)
    dsl_step_id = str(step["id"])
    try:
        module_id = resolve_module_id(step)
    except ModuleResolveError as exc:
        raise OrchestratorError(str(exc)) from exc

    scan_id = scan_instance_id_for(workflow_id, dsl_step_id)
    workflow_inputs = workflow_input_values(doc)

    stored_prior = _prior_vars_from_store(store, workflow_id, step)
    if prior_vars:
        for k, v in prior_vars.items():
            # Accept flat {var: [vals]} or nested {vars: {var: [vals]}}.
            if isinstance(v, Mapping) and "vars" in v and isinstance(
                v.get("vars"), Mapping
            ):
                stored_prior[k] = {
                    vk: list(vv) for vk, vv in v["vars"].items()
                }
            else:
                stored_prior[k] = {vk: list(vv) for vk, vv in v.items()}

    # build_env expects steps[id] = {"vars": {...}}.
    env = build_env(
        workflow_inputs=workflow_inputs,
        steps={sid: {"vars": vars_map} for sid, vars_map in stored_prior.items()},
    )
    try:
        input_values = resolve_step_inputs(step, env)
    except (VariableError, KeyError, ValueError) as exc:
        raise OrchestratorError(
            f"failed to resolve inputs for step {dsl_step_id}: {exc}"
        ) from exc

    empty_mode = (step.get("input") or {}).get("empty") or "continue"
    # Dry-run may carry empty seeded prior vars; only enforce empty:error live.
    if not input_values and empty_mode == "error" and not dry_run:
        raise OrchestratorError(
            f"step {dsl_step_id} input is empty (empty: error)"
        )

    # DSL empty: skip_step — do not invoke the module; persist empty vars so
    # downstream steps can resolve $steps.<id>.vars.* as empty lists.
    if not input_values and empty_mode == "skip_step":
        if dry_run:
            return StepRunResult(
                workflow_id=workflow_id,
                step_id=dsl_step_id,
                scan_instance_id=scan_id,
                module_id=module_id,
                status=OUTCOME_DRY_RUN,
                scan_status=OUTCOME_DRY_RUN,
                message=f"Dry-run: would skip {dsl_step_id} (empty input)",
                dry_run=True,
                input_values=[],
            )
        ensure_scan_step(
            store,
            scan_instance_id=scan_id,
            module_id=module_id,
            step=step,
            scan_status=STATUS_FINISHED,
        )
        empty_result = {
            "status": "SUCCESS",
            "text": f"SKIPPED: step {dsl_step_id} (empty input)\n",
            "structured": {"skipped": True, "reason": "empty_input"},
            "structured_type": "json",
            "graph": {"nodes": [], "edges": []},
            "narrative": f"# Skipped\n\nStep `{dsl_step_id}` skipped (empty input).\n",
            "command": [],
            "counts": {"nodes": 0, "edges": 0},
            "duration": 0.0,
        }
        persisted = persist_module_result(
            store,
            scan_instance_id=scan_id,
            module_id=module_id,
            step=step,
            module_result=empty_result,
            output_vars={},
        )
        return StepRunResult(
            workflow_id=workflow_id,
            step_id=dsl_step_id,
            scan_instance_id=scan_id,
            module_id=module_id,
            status=OUTCOME_SKIPPED,
            scan_status=STATUS_FINISHED,
            message=f"Step {dsl_step_id} skipped (empty input)",
            output_vars={},
            counts={"nodes": 0, "edges": 0},
            scan_result_id=persisted.get("scan_result_id"),
            temporary_subgraph_id=existing_temporary_subgraph_id,
            input_values=[],
        )

    temps = TempFileManager(prefix=f"sf_ao1_{dsl_step_id}_")
    try:
        spec, argv_preview = _build_scan_step_spec(
            step,
            input_values,
            temps,
            workflow_inputs=workflow_inputs,
        )
        if timeout is not None:
            spec["timeout"] = timeout

        if dry_run:
            return StepRunResult(
                workflow_id=workflow_id,
                step_id=dsl_step_id,
                scan_instance_id=scan_id,
                module_id=module_id,
                status=OUTCOME_DRY_RUN,
                scan_status=OUTCOME_DRY_RUN,
                message=(
                    f"Dry-run: would invoke {module_id} with "
                    f"{len(input_values)} input value(s)"
                ),
                command=list(argv_preview),
                dry_run=True,
                input_values=list(input_values),
            )

        ensure_scan_step(
            store,
            scan_instance_id=scan_id,
            module_id=module_id,
            step=step,
            scan_status=STATUS_STARTING,
        )
        store.update_scan_step(scan_id, {"scan_status": STATUS_RUNNING})

        try:
            runner = load_module_runner(module_id)
        except ModuleResolveError as exc:
            ensure_scan_step(
                store,
                scan_instance_id=scan_id,
                module_id=module_id,
                step=step,
                scan_status=STATUS_ERROR_FAILED,
            )
            raise OrchestratorError(str(exc)) from exc

        module_result = runner(spec)
        if not isinstance(module_result, Mapping):
            raise OrchestratorError(
                f"{module_id}.run() returned non-mapping result"
            )

        graph = module_result.get("graph") or {"nodes": [], "edges": []}
        try:
            output_vars = evaluate_output_vars(step, graph)
        except GseError as exc:
            output_vars = {}
            module_result = dict(module_result)
            module_result["error"] = (
                f"{module_result.get('error') or ''}; GSE: {exc}".strip("; ")
            )
            if module_result.get("status") in MODULE_OK:
                module_result["status"] = "ERROR"

        persisted = persist_module_result(
            store,
            scan_instance_id=scan_id,
            module_id=module_id,
            step=step,
            module_result=module_result,
            output_vars=output_vars,
        )

        exported = False
        temp_id = existing_temporary_subgraph_id
        if project_id and step_exports_scan_graph(step):
            export_info = persist_temporary_export(
                store,
                project_id=project_id,
                step=step,
                scan_graph=graph,
                existing_subgraph_id=existing_temporary_subgraph_id,
            )
            exported = bool(export_info.get("exported"))
            temp_id = export_info.get("temporary_subgraph_id")

        terminal = persisted["scan_status"]
        outcome = outcome_for_scan_status(terminal)
        ok = terminal == STATUS_FINISHED
        return StepRunResult(
            workflow_id=workflow_id,
            step_id=dsl_step_id,
            scan_instance_id=scan_id,
            module_id=module_id,
            status=OUTCOME_SUCCESS if ok else OUTCOME_ERROR,
            scan_status=terminal,
            message=(
                f"Step {dsl_step_id} completed via {module_id}"
                if ok
                else f"Step {dsl_step_id} failed via {module_id}"
            ),
            command=[str(p) for p in (module_result.get("command") or argv_preview)],
            output_vars=output_vars,
            counts=dict(module_result.get("counts") or {}),
            exported_to_temporary=exported,
            temporary_subgraph_id=temp_id,
            scan_result_id=persisted.get("scan_result_id"),
            error=module_result.get("error"),
            input_values=list(input_values),
        )
    finally:
        temps.cleanup()
