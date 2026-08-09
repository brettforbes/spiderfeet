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
    """Update workflow attrs, or re-parse ``workflow_yaml`` (R13-05).

    When ``workflow_yaml`` is present, the body is treated as a full YAML
    replace: validate → ``persist_workflow_yaml(replace=True)`` → return the
    updated CRUD row. Invalid YAML yields 400 with the stored bundle unchanged.
    """
    payload = body.model_dump(exclude_none=True)
    yaml_text = payload.pop("workflow_yaml", None)
    if yaml_text is not None:
        from spiderfeet_v2.workflow.typedb_convert import (
            WorkflowConvertError,
            parse_yaml_string,
            persist_workflow_yaml,
        )

        existing = store.get_workflow(workflow_id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Workflow not found")
        try:
            doc = parse_yaml_string(yaml_text)
            if not isinstance(doc, dict):
                raise WorkflowConvertError("workflow_yaml must be a YAML mapping")
            # Path id is authoritative for replace.
            doc["id"] = workflow_id
            persist_workflow_yaml(
                store,
                doc,
                validate=True,
                replace=True,
                project_id=existing.get("project_id"),
            )
        except WorkflowConvertError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # yaml parse / unexpected
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        row = store.get_workflow(workflow_id)
        if row is None:
            raise HTTPException(status_code=500, detail="Workflow missing after re-parse")
        return row
    try:
        return store.update_workflow(workflow_id, payload)
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
