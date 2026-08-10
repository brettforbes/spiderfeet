"""Workflow / step execute routes (R10-24 / R10-27 / R10-28).

AO1 wires single-step orchestration. AO2 wires full-workflow chaining.
SPEC-015 adds async execute (R15-01) via the in-memory run registry.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, Depends, HTTPException

from spiderfeet_v2.api.deps import get_crud_store, get_projection_store
import yaml

from spiderfeet_v2.api.schemas import (
    EXECUTE_STEP_OPENAPI_EXAMPLES,
    EXECUTE_WORKFLOW_OPENAPI_EXAMPLES,
    ExecuteAsyncAccepted,
    ExecuteResponse,
    ExecuteStepRequest,
    ExecuteWorkflowRequest,
    WorkflowStatusOut,
)
from spiderfeet_v2.db.crud import CrudStore
from spiderfeet_v2.db.projections import ProjectionStore
from spiderfeet_v2.engine import OrchestratorError, run_single_step, run_workflow
from spiderfeet_v2.engine.run_registry import get_run_registry
from spiderfeet_v2.workflow.typedb_convert import scan_instance_id_for

router = APIRouter(tags=["v2-execute"])


def _first_temporary_id(
    projections: ProjectionStore,
    project_id: Optional[str],
) -> Optional[str]:
    if not project_id:
        return None
    proj = projections.get_project(project_id)
    if not proj:
        return None
    ids = proj.get("temporary_subgraph") or []
    return ids[0] if ids else None


@router.get(
    "/workflows/{workflow_id}/status",
    response_model=WorkflowStatusOut,
    status_code=200,
)
def get_workflow_status(
    workflow_id: str,
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    """Return per-step ``scan_status`` for live DAG progress (R15-02).

    Enumerates DSL step ids from stored ``workflow_yaml`` and reads only
    ``scan_status`` (no four-form blobs). Missing shells → ``UNKNOWN``.
    """
    workflow = store.get_workflow(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    yaml_text = workflow.get("workflow_yaml") or ""
    step_ids: list[str] = []
    if str(yaml_text).strip():
        try:
            doc = yaml.safe_load(yaml_text)
        except yaml.YAMLError:
            doc = None
        if isinstance(doc, dict):
            for step in doc.get("steps") or []:
                if isinstance(step, dict) and step.get("id"):
                    step_ids.append(str(step["id"]))

    steps_out: list[Dict[str, Any]] = []
    for step_id in step_ids:
        sid = scan_instance_id_for(workflow_id, step_id)
        status = store.get_scan_status(sid)
        steps_out.append(
            {
                "step_id": step_id,
                "scan_instance_id": sid,
                "scan_status": status or "UNKNOWN",
            }
        )

    registry = get_run_registry()
    active = registry.active_for_workflow(workflow_id)
    latest = active or registry.latest_for_workflow(workflow_id)
    return {
        "workflow_id": workflow_id,
        "run_id": latest.run_id if latest else None,
        "run_state": latest.state if latest else None,
        "steps": steps_out,
    }


@router.post(
    "/workflows/{workflow_id}/execute-async",
    response_model=ExecuteAsyncAccepted,
    status_code=202,
)
def execute_workflow_async(
    workflow_id: str,
    body: ExecuteWorkflowRequest = Body(
        default=ExecuteWorkflowRequest(),
        openapi_examples=EXECUTE_WORKFLOW_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    """Accept a full-workflow run and execute it in the background (R15-01).

    Returns ``202`` with ``run_id``. Poll ``GET /workflows/{id}/status`` (R15-02)
    for per-step ``scan_status`` while the run is active.
    """
    if store.get_workflow(workflow_id) is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if body.project_id and store.get_project(body.project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    registry = get_run_registry()
    rec = registry.submit_workflow(
        workflow_id=workflow_id,
        project_id=body.project_id,
        dry_run=body.dry_run,
        temporary_subgraph_id=_first_temporary_id(projections, body.project_id),
    )
    return {
        "run_id": rec.run_id,
        "workflow_id": workflow_id,
        "state": rec.state,
        "kind": "workflow",
        "message": "Workflow execute accepted; poll GET /workflows/{id}/status",
    }


@router.post(
    "/workflows/{workflow_id}/execute",
    response_model=ExecuteResponse,
    status_code=200,
)
def execute_workflow(
    workflow_id: str,
    body: ExecuteWorkflowRequest = Body(
        ...,
        openapi_examples=EXECUTE_WORKFLOW_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    """Run a full workflow: chain by needs, thread vars, accumulate context (R10-28)."""
    if store.get_workflow(workflow_id) is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if body.project_id and store.get_project(body.project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        result = run_workflow(
            store,
            workflow_id=workflow_id,
            project_id=body.project_id,
            dry_run=body.dry_run,
            existing_temporary_subgraph_id=_first_temporary_id(
                projections, body.project_id
            ),
        )
    except OrchestratorError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return result.to_api_dict()


@router.post(
    "/workflows/{workflow_id}/steps/{step_id}/execute",
    response_model=ExecuteResponse,
    status_code=200,
)
def execute_workflow_step(
    workflow_id: str,
    step_id: str,
    body: ExecuteStepRequest = Body(
        ...,
        openapi_examples=EXECUTE_STEP_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    """Run a single workflow step via the AO1 orchestrator (R10-27).

    ``step_id`` may be a DSL step name or a ``scan_instance_id``.
    """
    if store.get_workflow(workflow_id) is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if body.project_id and store.get_project(body.project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    dsl_key = body.step_id or step_id
    try:
        result = run_single_step(
            store,
            workflow_id=workflow_id,
            step_id=dsl_key,
            project_id=body.project_id,
            dry_run=body.dry_run,
            existing_temporary_subgraph_id=_first_temporary_id(
                projections, body.project_id
            ),
        )
    except OrchestratorError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return result.to_api_dict()
