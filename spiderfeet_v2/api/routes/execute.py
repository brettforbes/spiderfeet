"""Workflow / step execute stubs (R10-24; real orchestration in Epic AO)."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException

from spiderfeet_v2.api.deps import get_crud_store
from spiderfeet_v2.api.schemas import (
    EXECUTE_STEP_OPENAPI_EXAMPLES,
    EXECUTE_WORKFLOW_OPENAPI_EXAMPLES,
    ExecuteResponse,
    ExecuteStepRequest,
    ExecuteWorkflowRequest,
)
from spiderfeet_v2.db.crud import CrudStore

router = APIRouter(tags=["v2-execute"])

_STUB_MSG = (
    "Execute accepted as stub — Epic AO (AO1/AO2) wires the orchestrator "
    "(resolve inputs → module run → persist scan_step → GSE vars → context export)."
)


@router.post(
    "/workflows/{workflow_id}/execute",
    response_model=ExecuteResponse,
    status_code=202,
)
def execute_workflow(
    workflow_id: str,
    body: ExecuteWorkflowRequest = Body(
        ...,
        openapi_examples=EXECUTE_WORKFLOW_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
) -> ExecuteResponse:
    """Run a full workflow (stub until AO2)."""
    if store.get_workflow(workflow_id) is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if body.project_id and store.get_project(body.project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return ExecuteResponse(
        status="stub",
        message=_STUB_MSG,
        workflow_id=workflow_id,
        orchestrator="pending",
    )


@router.post(
    "/workflows/{workflow_id}/steps/{step_id}/execute",
    response_model=ExecuteResponse,
    status_code=202,
)
def execute_workflow_step(
    workflow_id: str,
    step_id: str,
    body: ExecuteStepRequest = Body(
        ...,
        openapi_examples=EXECUTE_STEP_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
) -> ExecuteResponse:
    """Run a single workflow step (stub until AO1).

    ``step_id`` may be a DSL step name or a ``scan_instance_id``.
    """
    if store.get_workflow(workflow_id) is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if body.project_id and store.get_project(body.project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return ExecuteResponse(
        status="stub",
        message=_STUB_MSG,
        workflow_id=workflow_id,
        step_id=body.step_id or step_id,
        orchestrator="pending",
    )
