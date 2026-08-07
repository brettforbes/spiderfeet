"""Targets CRUD (R10-24 / AL1)."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException

from spiderfeet_v2.api.deps import get_crud_store
from spiderfeet_v2.api.schemas import (
    TARGET_CREATE_OPENAPI_EXAMPLES,
    TargetCreate,
    TargetOut,
    TargetUpdate,
)
from spiderfeet_v2.db.crud import CrudError, CrudStore

router = APIRouter(tags=["v2-targets"])


@router.get("/targets", response_model=List[TargetOut])
def list_targets(store: CrudStore = Depends(get_crud_store)) -> List[Dict[str, Any]]:
    return store.list_targets()


@router.post("/targets", response_model=TargetOut, status_code=201)
def create_target(
    body: TargetCreate = Body(
        ...,
        openapi_examples=TARGET_CREATE_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    try:
        return store.create_target(body.model_dump(exclude_none=True))
    except CrudError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/targets/{target_id}", response_model=TargetOut)
def get_target(
    target_id: str,
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    row = store.get_target(target_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Target not found")
    return row


@router.patch("/targets/{target_id}", response_model=TargetOut)
@router.put("/targets/{target_id}", response_model=TargetOut)
def update_target(
    target_id: str,
    body: TargetUpdate,
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    try:
        return store.update_target(target_id, body.model_dump(exclude_none=True))
    except CrudError as exc:
        msg = str(exc)
        code = 404 if "not found" in msg else 400
        raise HTTPException(status_code=code, detail=msg) from exc


@router.delete("/targets/{target_id}", status_code=204)
def delete_target(
    target_id: str,
    store: CrudStore = Depends(get_crud_store),
) -> None:
    if not store.delete_target(target_id):
        raise HTTPException(status_code=404, detail="Target not found")
