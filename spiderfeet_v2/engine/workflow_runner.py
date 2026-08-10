"""AO2 full-workflow chaining orchestrator (SPEC-010 R10-28)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional

from spiderfeet_v2.engine.persist import reset_temporary_context
from spiderfeet_v2.engine.status import (
    OUTCOME_DRY_RUN,
    OUTCOME_ERROR,
    OUTCOME_SKIPPED,
    OUTCOME_SUCCESS,
)
from spiderfeet_v2.engine.step_runner import (
    OrchestratorError,
    StepRunResult,
    _load_workflow_doc,
    run_single_step,
)
from spiderfeet_v2.workflow.loader import WorkflowLoadError, schedule_waves

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


def run_workflow(
    store: Any,
    *,
    workflow_id: str,
    project_id: Optional[str] = None,
    dry_run: bool = False,
    timeout: Optional[float] = None,
    existing_temporary_subgraph_id: Optional[str] = None,
    stop_on_error: bool = True,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> WorkflowRunResult:
    """Chain workflow steps by ``needs``, thread vars, accumulate temp context.

    Steps are scheduled into parallel waves via ``schedule_waves``. Within a
    wave, steps run sequentially (deterministic). Prior steps' ``output.vars``
    are threaded into later ``input.from`` resolution. When a step marks
    ``context.export: scan_graph``, its graph merges into the project temporary
    subgraph (same id accumulated across the run).

    ``should_cancel`` (SPEC-015 R15-04): checked between steps; when true the
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

    prior_vars: Dict[str, Dict[str, List[str]]] = {}
    temp_id = existing_temporary_subgraph_id
    if project_id and not dry_run:
        temp_id = reset_temporary_context(
            store,
            project_id=project_id,
            existing_subgraph_id=existing_temporary_subgraph_id,
        )
    results: List[StepRunResult] = []
    exported_any = False
    stopped_early = False
    hard_error: Optional[str] = None
    cancelled = False

    for wave in waves:
        for step_id in wave:
            if should_cancel and should_cancel():
                cancelled = True
                stopped_early = True
                break
            try:
                result = run_single_step(
                    store,
                    workflow_id=workflow_id,
                    step_id=step_id,
                    project_id=project_id,
                    dry_run=dry_run,
                    prior_vars=prior_vars,
                    timeout=timeout,
                    existing_temporary_subgraph_id=temp_id,
                )
            except OrchestratorError as exc:
                hard_error = str(exc)
                results.append(
                    StepRunResult(
                        workflow_id=workflow_id,
                        step_id=step_id,
                        scan_instance_id="",
                        module_id="",
                        status=OUTCOME_ERROR,
                        scan_status=OUTCOME_ERROR,
                        message=str(exc),
                        error=str(exc),
                        dry_run=dry_run,
                    )
                )
                if stop_on_error:
                    stopped_early = True
                    break
                continue

            results.append(result)
            # Thread vars for later input.from (including empty SKIPPED vars).
            # On dry-run, seed declared output.vars keys so downstream
            # $steps.<id>.vars.<name> refs resolve (values stay empty).
            if dry_run:
                step_doc = next(
                    (s for s in steps if str(s.get("id")) == result.step_id),
                    {},
                )
                declared = (step_doc.get("output") or {}).get("vars") or {}
                prior_vars[result.step_id] = {name: [] for name in declared}
            else:
                prior_vars[result.step_id] = {
                    k: list(v) for k, v in (result.output_vars or {}).items()
                }
            if result.temporary_subgraph_id:
                temp_id = result.temporary_subgraph_id
            if result.exported_to_temporary:
                exported_any = True

            if result.status == OUTCOME_ERROR and stop_on_error:
                hard_error = result.error or result.message
                stopped_early = True
                break
        if stopped_early:
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
