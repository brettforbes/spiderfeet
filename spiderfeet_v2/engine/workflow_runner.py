"""AO2 full-workflow chaining orchestrator (SPEC-010 R10-28)."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Callable, Dict, List, Mapping, Optional, Set

from spiderfeet_v2.engine.persist import (
    ensure_project_target_temps,
    ensure_scan_step,
    persist_module_result,
)
from spiderfeet_v2.engine.status import (
    OUTCOME_DRY_RUN,
    OUTCOME_ERROR,
    OUTCOME_SKIPPED,
    OUTCOME_SUCCESS,
    STATUS_FINISHED,
)
from spiderfeet_v2.engine.modules import resolve_module_id
from spiderfeet_v2.engine.step_runner import (
    OrchestratorError,
    StepRunResult,
    _load_workflow_doc,
    run_single_step,
)
from spiderfeet_v2.workflow.loader import WorkflowLoadError, schedule_waves, workflow_input_values
from spiderfeet_v2.workflow.normalize import hostname_from_url
from spiderfeet_v2.workflow.typedb_convert import scan_instance_id_for

OUTCOME_CANCELLED = "CANCELLED"


@dataclass
class WorkflowRunResult:
    """Outcome of a full chained workflow run."""

    workflow_id: str
    status: str
    message: str
    waves: List[List[str]] = field(default_factory=list)
    steps: List[StepRunResult] = field(default_factory=list)
    temporary_subgraph_id: Optional[str] = None
    exported_to_temporary: bool = False
    dry_run: bool = False
    error: Optional[str] = None
    stopped_early: bool = False

    def to_api_dict(self) -> Dict[str, Any]:
        step_dicts = [s.to_api_dict() for s in self.steps]
        for sd in step_dicts:
            sd["orchestrator"] = "ao2"
        return {
            "status": self.status,
            "message": self.message,
            "workflow_id": self.workflow_id,
            "orchestrator": "ao2",
            "waves": [list(w) for w in self.waves],
            "steps": step_dicts,
            "step_count": len(self.steps),
            "succeeded": sum(1 for s in self.steps if s.status == OUTCOME_SUCCESS),
            "failed": sum(1 for s in self.steps if s.status == OUTCOME_ERROR),
            "skipped": sum(1 for s in self.steps if s.status == OUTCOME_SKIPPED),
            "temporary_subgraph_id": self.temporary_subgraph_id,
            "exported_to_temporary": self.exported_to_temporary,
            "dry_run": self.dry_run,
            "error": self.error,
            "stopped_early": self.stopped_early,
        }


def _step_by_id(steps: List[Mapping[str, Any]], step_id: str) -> Mapping[str, Any]:
    for step in steps:
        if str(step.get("id")) == step_id:
            return step
    return {}


def _declared_output_vars(step: Mapping[str, Any]) -> Dict[str, List[str]]:
    declared = (step.get("output") or {}).get("vars") or {}
    return {name: [] for name in declared}


def _seed_hostnames(doc: Mapping[str, Any]) -> List[str]:
    """Apex/hostname seeds from workflow inputs (URL → hostname)."""
    values = workflow_input_values(dict(doc)).get("targets") or []
    hosts: List[str] = []
    seen: Set[str] = set()
    for raw in values:
        host = hostname_from_url(str(raw))
        if host and host not in seen:
            seen.add(host)
            hosts.append(host)
    return hosts


def _skip_failed_dependency(
    store: Any,
    *,
    workflow_id: str,
    step: Mapping[str, Any],
    dry_run: bool,
    reason: str,
    existing_temporary_subgraph_id: Optional[str],
) -> StepRunResult:
    """Persist a SKIPPED shell when an upstream need failed/was skipped."""
    dsl_step_id = str(step.get("id") or "")
    try:
        module_id = resolve_module_id(step)
    except Exception:  # noqa: BLE001
        uses = str(step.get("uses") or "")
        module_id = (
            f"sfp_cli_{uses.split('.', 1)[1]}" if uses.startswith("tool.") else uses
        )
    scan_id = scan_instance_id_for(workflow_id, dsl_step_id)

    if dry_run:
        return StepRunResult(
            workflow_id=workflow_id,
            step_id=dsl_step_id,
            scan_instance_id=scan_id,
            module_id=module_id,
            status=OUTCOME_DRY_RUN,
            scan_status=OUTCOME_DRY_RUN,
            message=f"Dry-run: would skip {dsl_step_id} ({reason})",
            dry_run=True,
            input_values=[],
            output_vars=_declared_output_vars(step),
            temporary_subgraph_id=existing_temporary_subgraph_id,
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
        "text": f"SKIPPED: step {dsl_step_id} ({reason})\n",
        "structured": {"skipped": True, "reason": reason},
        "structured_type": "json",
        "graph": {"nodes": [], "edges": []},
        "narrative": f"# Skipped\n\nStep `{dsl_step_id}` skipped ({reason}).\n",
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
        message=f"Step {dsl_step_id} skipped ({reason})",
        output_vars={},
        counts={"nodes": 0, "edges": 0},
        scan_result_id=persisted.get("scan_result_id"),
        temporary_subgraph_id=existing_temporary_subgraph_id,
        input_values=[],
    )


def _record_prior_vars(
    prior_vars: Dict[str, Dict[str, List[str]]],
    result: StepRunResult,
    step: Mapping[str, Any],
    *,
    dry_run: bool,
) -> None:
    if dry_run:
        prior_vars[result.step_id] = _declared_output_vars(step)
    else:
        prior_vars[result.step_id] = {
            k: list(v) for k, v in (result.output_vars or {}).items()
        }


def run_workflow(
    store: Any,
    *,
    workflow_id: str,
    project_id: Optional[str] = None,
    dry_run: bool = False,
    timeout: Optional[float] = None,
    existing_temporary_subgraph_id: Optional[str] = None,
    stop_on_error: bool = False,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> WorkflowRunResult:
    """Chain workflow steps by ``needs``, thread vars, accumulate temp context.

    Steps are scheduled into parallel waves via ``schedule_waves``. Within a
    wave, ready steps run concurrently. A failed step does not abort sibling
    branches; dependents of failed/skipped steps are skipped. Set
    ``stop_on_error=True`` to restore hard abort after the current wave.

    ``should_cancel`` (SPEC-015 R15-04): checked between waves; when true the
    run stops with status ``CANCELLED``.
    """
    doc = _load_workflow_doc(store, workflow_id)
    steps = list(doc.get("steps") or [])
    if not steps:
        raise OrchestratorError(f"workflow has no steps: {workflow_id}")

    try:
        waves = schedule_waves(steps)
    except WorkflowLoadError as exc:
        raise OrchestratorError(str(exc)) from exc

    needs_map: Dict[str, Set[str]] = {
        str(s.get("id")): set(s.get("needs") or []) for s in steps
    }

    prior_vars: Dict[str, Dict[str, List[str]]] = {}
    temp_id = existing_temporary_subgraph_id
    temp_lock = Lock()
    exported_any = False

    if project_id and not dry_run:
        # SPEC-017: do not wipe on Run — Reset owns wipe+reseed. Ensure target
        # temp exists (e.g. first run before Composer called /complete).
        ensure = ensure_project_target_temps(store, project_id=project_id)
        seed = ensure.get("temporary") or {}
        temp_id = seed.get("temporary_subgraph_id") or temp_id
        if seed.get("exported"):
            exported_any = True

    results: List[StepRunResult] = []
    stopped_early = False
    hard_error: Optional[str] = None
    cancelled = False
    unusable: Set[str] = set()  # failed or skipped-due-to-dep

    def _run_one(step_id: str, prior_snapshot: Dict[str, Dict[str, List[str]]]) -> StepRunResult:
        with temp_lock:
            current_temp = temp_id
        try:
            return run_single_step(
                store,
                workflow_id=workflow_id,
                step_id=step_id,
                project_id=project_id,
                dry_run=dry_run,
                prior_vars=prior_snapshot,
                timeout=timeout,
                existing_temporary_subgraph_id=current_temp,
            )
        except OrchestratorError as exc:
            return StepRunResult(
                workflow_id=workflow_id,
                step_id=step_id,
                scan_instance_id=scan_instance_id_for(workflow_id, step_id),
                module_id="",
                status=OUTCOME_ERROR,
                scan_status=OUTCOME_ERROR,
                message=str(exc),
                error=str(exc),
                dry_run=dry_run,
                temporary_subgraph_id=current_temp,
            )

    for wave in waves:
        if should_cancel and should_cancel():
            cancelled = True
            stopped_early = True
            break

        runnable: List[str] = []
        for step_id in wave:
            blocked = needs_map.get(step_id, set()) & unusable
            if blocked:
                step = _step_by_id(steps, step_id)
                reason = f"upstream failed/skipped: {', '.join(sorted(blocked))}"
                skip = _skip_failed_dependency(
                    store,
                    workflow_id=workflow_id,
                    step=step,
                    dry_run=dry_run,
                    reason=reason,
                    existing_temporary_subgraph_id=temp_id,
                )
                results.append(skip)
                _record_prior_vars(prior_vars, skip, step, dry_run=dry_run)
                unusable.add(step_id)
                continue
            runnable.append(step_id)

        if not runnable:
            continue

        prior_snapshot = {
            sid: {k: list(v) for k, v in vars_map.items()}
            for sid, vars_map in prior_vars.items()
        }

        wave_results: List[StepRunResult] = []
        workers = min(len(runnable), 8)
        if workers == 1:
            wave_results.append(_run_one(runnable[0], prior_snapshot))
        else:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {
                    pool.submit(_run_one, step_id, prior_snapshot): step_id
                    for step_id in runnable
                }
                for fut in as_completed(futures):
                    wave_results.append(fut.result())

        # Deterministic order within the wave for result listing.
        order = {sid: i for i, sid in enumerate(runnable)}
        wave_results.sort(key=lambda r: order.get(r.step_id, 0))

        for result in wave_results:
            step = _step_by_id(steps, result.step_id)
            results.append(result)
            _record_prior_vars(prior_vars, result, step, dry_run=dry_run)
            if result.temporary_subgraph_id:
                temp_id = result.temporary_subgraph_id
            if result.exported_to_temporary:
                exported_any = True
            if result.status == OUTCOME_ERROR:
                unusable.add(result.step_id)
                hard_error = result.error or result.message or hard_error

        if stop_on_error and any(r.status == OUTCOME_ERROR for r in wave_results):
            stopped_early = True
            break

        if should_cancel and should_cancel():
            cancelled = True
            stopped_early = True
            break

    if cancelled:
        status = OUTCOME_CANCELLED
        message = (
            f"Workflow {workflow_id} cancelled after {len(results)} step(s)"
        )
        hard_error = hard_error or "cancelled"
    elif dry_run and all(s.status == OUTCOME_DRY_RUN for s in results) and not hard_error:
        status = OUTCOME_DRY_RUN
        message = (
            f"Dry-run: scheduled {len(results)} step(s) across "
            f"{len(waves)} wave(s)"
        )
    elif hard_error or any(s.status == OUTCOME_ERROR for s in results):
        status = OUTCOME_ERROR
        message = (
            f"Workflow {workflow_id} failed after {len(results)} step(s)"
            + ("; stopped early" if stopped_early else "")
        )
    else:
        status = OUTCOME_SUCCESS
        message = (
            f"Workflow {workflow_id} completed: {len(results)} step(s) across "
            f"{len(waves)} wave(s)"
        )

    return WorkflowRunResult(
        workflow_id=workflow_id,
        status=status,
        message=message,
        waves=waves,
        steps=results,
        temporary_subgraph_id=temp_id,
        exported_to_temporary=exported_any,
        dry_run=dry_run,
        error=hard_error,
        stopped_early=stopped_early,
    )
