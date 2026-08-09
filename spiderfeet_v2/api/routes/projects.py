"""Projects CRUD + AL3 projection read (R10-24)."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from spiderfeet_v2.api.deps import get_crud_store, get_projection_store
from spiderfeet_v2.api.schemas import (
    PROJECT_CREATE_OPENAPI_EXAMPLES,
    ProjectCreate,
    ProjectOut,
    ProjectProjectionOut,
    ProjectUpdate,
)
from spiderfeet_v2.db.crud import CrudError, CrudStore
from spiderfeet_v2.db.projections import ProjectionStore

router = APIRouter(tags=["v2-projects"])


@router.get("/projects", response_model=List[ProjectOut])
def list_projects(store: CrudStore = Depends(get_crud_store)) -> List[Dict[str, Any]]:
    """List projects for the Projects page (SPEC-011 R11-03)."""
    return store.list_projects()


@router.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(
    body: ProjectCreate = Body(
        ...,
        openapi_examples=PROJECT_CREATE_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    try:
        return store.create_project(body.model_dump(exclude_none=True))
    except CrudError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/projects/{project_id}")
def get_project(
    project_id: str,
    projection: bool = Query(
        True,
        description="Default true: AL3 projection (workflows/targets/contexts) "
        "merged with CRUD attributes for Composer load.",
    ),
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    crud_row = store.get_project(project_id)
    if crud_row is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if not projection:
        return crud_row
    proj = projections.get_project(project_id) or {
        "project_id": project_id,
        "workflows": crud_row.get("workflow_ids") or [],
        "targets": [],
        "project_context": [],
        "temporary_subgraph": [],
    }
    merged = ProjectProjectionOut(
        **{
            **proj,
            "stix_incident_id": crud_row.get("stix_incident_id"),
            "project_name": crud_row.get("project_name"),
            "project_description": crud_row.get("project_description"),
            "project_created": crud_row.get("project_created"),
        }
    ).model_dump()
    merged["workflow_ids"] = crud_row.get("workflow_ids") or []
    return merged


@router.patch("/projects/{project_id}", response_model=ProjectOut)
@router.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: str,
    body: ProjectUpdate,
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    try:
        return store.update_project(project_id, body.model_dump(exclude_none=True))
    except CrudError as exc:
        msg = str(exc)
        code = 404 if "not found" in msg else 400
        raise HTTPException(status_code=code, detail=msg) from exc


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(
    project_id: str,
    store: CrudStore = Depends(get_crud_store),
) -> None:
    if not store.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
