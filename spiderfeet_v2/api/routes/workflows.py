"""Workflows CRUD + AL3 projection read (R10-24)."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from spiderfeet_v2.api.deps import get_crud_store, get_projection_store
from spiderfeet_v2.api.schemas import (
    WORKFLOW_CREATE_OPENAPI_EXAMPLES,
    WorkflowCreate,
    WorkflowOut,
    WorkflowProjectionOut,
    WorkflowUpdate,
)
from spiderfeet_v2.db.crud import CrudError, CrudStore
from spiderfeet_v2.db.projections import ProjectionStore

router = APIRouter(tags=["v2-workflows"])


@router.get("/workflows", response_model=List[WorkflowOut])
def list_workflows(store: CrudStore = Depends(get_crud_store)) -> List[Dict[str, Any]]:
    return store.list_workflows()


@router.post("/workflows", response_model=WorkflowOut, status_code=201)
def create_workflow(
    body: WorkflowCreate = Body(
        ...,
        openapi_examples=WORKFLOW_CREATE_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    try:
        return store.create_workflow(body.model_dump(exclude_none=True))
    except CrudError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/workflows/{workflow_id}",
    response_model=None,
    responses={200: {"description": "Workflow CRUD or AL3 projection"}},
)
def get_workflow(
    workflow_id: str,
    projection: bool = Query(
        False,
        description="When true, return AL3 fun projection (target/steps/yaml).",
    ),
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    if projection:
        row = projections.get_workflow(workflow_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return WorkflowProjectionOut(**row).model_dump()
    row = store.get_workflow(workflow_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return row


@router.patch("/workflows/{workflow_id}", response_model=WorkflowOut)
@router.put("/workflows/{workflow_id}", response_model=WorkflowOut)
def update_workflow(
    workflow_id: str,
    body: WorkflowUpdate,
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    try:
        return store.update_workflow(workflow_id, body.model_dump(exclude_none=True))
    except CrudError as exc:
        msg = str(exc)
        code = 404 if "not found" in msg else 400
        raise HTTPException(status_code=code, detail=msg) from exc


@router.delete("/workflows/{workflow_id}", status_code=204)
def delete_workflow(
    workflow_id: str,
    store: CrudStore = Depends(get_crud_store),
) -> None:
    if not store.delete_workflow(workflow_id):
        raise HTTPException(status_code=404, detail="Workflow not found")
