"""Workflow / step execute routes (R10-24 / R10-27 / R10-28).

AO1 wires single-step orchestration. AO2 wires full-workflow chaining.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Body, Depends, HTTPException

from spiderfeet_v2.api.deps import get_crud_store, get_projection_store
from spiderfeet_v2.api.schemas import (
    EXECUTE_STEP_OPENAPI_EXAMPLES,
    EXECUTE_WORKFLOW_OPENAPI_EXAMPLES,
    ExecuteResponse,
    ExecuteStepRequest,
    ExecuteWorkflowRequest,
)
from spiderfeet_v2.db.crud import CrudStore
from spiderfeet_v2.db.projections import ProjectionStore
from spiderfeet_v2.engine import OrchestratorError, run_single_step, run_workflow

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
