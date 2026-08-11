"""Project / temporary context read (SPEC-010 / SPEC-016 / SPEC-017)."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException

from spiderfeet_v2.api.deps import get_crud_store, get_projection_store
from spiderfeet_v2.api.schemas import (
    TEMPORARY_CONTEXT_UPDATE_OPENAPI_EXAMPLES,
    ContextGraphOut,
    TemporaryContextListOut,
    TemporaryContextUpdate,
    TemporarySubgraphOut,
)
from spiderfeet_v2.db.crud import CrudError, CrudStore
from spiderfeet_v2.db.projections import ProjectionStore
from spiderfeet_v2.engine.persist import (
    list_project_temporary_subgraphs,
    project_context_id_for,
    temporary_subgraph_id_for,
)

router = APIRouter(tags=["v2-contexts"])
_LOG = logging.getLogger(__name__)


def _parse_graph_payload(row: Optional[Dict[str, Any]]) -> Dict[str, List[Any]]:
    if not row:
        return {"nodes": [], "edges": []}
    graph = row.get("graph")
    if isinstance(graph, dict):
        return {
            "nodes": list(graph.get("nodes") or []),
            "edges": list(graph.get("edges") or []),
        }
    js = row.get("json_string")
    if js:
        try:
            parsed = json.loads(js)
            if isinstance(parsed, dict):
                return {
                    "nodes": list(parsed.get("nodes") or []),
                    "edges": list(parsed.get("edges") or []),
                }
        except json.JSONDecodeError:
            pass
    if "nodes" in row or "edges" in row:
        return {
            "nodes": list(row.get("nodes") or []),
            "edges": list(row.get("edges") or []),
        }
    return {"nodes": [], "edges": []}


def _first_subgraph_id(
    projections: ProjectionStore,
    project_id: str,
    key: str,
) -> Optional[str]:
    proj = projections.get_project(project_id)
    if not proj:
        return None
    ids = proj.get(key) or []
    return ids[0] if ids else None


def _resolve_context_id(
    *,
    project_id: str,
    kind: str,
    projection_key: str,
    store: CrudStore,
    projections: ProjectionStore,
) -> str:
    """Canonical per-project id, with projection fallback only when that row exists."""
    if kind == "temporary_subgraph":
        canonical = temporary_subgraph_id_for(project_id)
    elif kind == "project_context":
        canonical = project_context_id_for(project_id)
    else:
        raise ValueError(f"unsupported context kind: {kind}")

    try:
        if store.get_subgraph(kind, canonical) is not None:
            return canonical
    except CrudError:
        pass

    projected = _first_subgraph_id(projections, project_id, projection_key)
    if projected and projected != canonical:
        try:
            if store.get_subgraph(kind, projected) is not None:
                _LOG.warning(
                    "project %s %s using legacy projection id %s "
                    "(canonical would be %s)",
                    project_id,
                    kind,
                    projected,
                    canonical,
                )
                return projected
        except CrudError:
            pass
    return canonical


def _load_context(
    *,
    project_id: str,
    kind: str,
    id_attr: str,
    projection_key: str,
    store: CrudStore,
    projections: ProjectionStore,
) -> Dict[str, Any]:
    if store.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    sg_id = _resolve_context_id(
        project_id=project_id,
        kind=kind,
        projection_key=projection_key,
        store=store,
        projections=projections,
    )
    try:
        dual = store.get_subgraph_dual(kind, sg_id)
    except CrudError:
        dual = {
            "kind": kind,
            id_attr: sg_id,
            "project_id": project_id,
            "graph": {"nodes": [], "edges": []},
            "json_string": None,
        }
    if dual is None:
        dual = {
            "kind": kind,
            id_attr: sg_id,
            "project_id": project_id,
            "graph": {"nodes": [], "edges": []},
            "json_string": None,
        }
    graph = _parse_graph_payload(dual)
    return ContextGraphOut(
        project_id=project_id,
        kind=kind,
        subgraph_id=dual.get(id_attr) or sg_id,
        nodes=graph["nodes"],
        edges=graph["edges"],
        json_string=dual.get("json_string"),
    ).model_dump()


@router.get(
    "/projects/{project_id}/contexts/temporary",
    response_model=TemporaryContextListOut,
    summary="List all temporary_subgraph rows for a project (SPEC-017 R17-04)",
)
def get_temporary_context(
    project_id: str,
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    if store.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    subgraphs: List[Dict[str, Any]] = []
    for row in list_project_temporary_subgraphs(store, project_id):
        graph = _parse_graph_payload(row)
        sg_id = row.get("temporary_subgraph_id")
        if not sg_id:
            continue
        subgraphs.append(
            TemporarySubgraphOut(
                temporary_subgraph_id=str(sg_id),
                scan_name=row.get("scan_name"),
                scan_description=row.get("scan_description"),
                nodes=graph["nodes"],
                edges=graph["edges"],
            ).model_dump()
        )
    # Stable order: target first, then scan_name, then id.
    subgraphs.sort(
        key=lambda s: (
            0 if s.get("scan_name") == "target" else 1,
            str(s.get("scan_name") or ""),
            str(s.get("temporary_subgraph_id") or ""),
        )
    )
    return TemporaryContextListOut(
        project_id=project_id,
        subgraphs=subgraphs,
    ).model_dump()


@router.get(
    "/projects/{project_id}/contexts/project",
    response_model=ContextGraphOut,
)
def get_project_context(
    project_id: str,
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    return _load_context(
        project_id=project_id,
        kind="project_context",
        id_attr="project_context_id",
        projection_key="project_context",
        store=store,
        projections=projections,
    )


@router.put(
    "/projects/{project_id}/contexts/temporary",
    response_model=TemporaryContextListOut,
    deprecated=True,
)
def update_temporary_context(
    project_id: str,
    body: TemporaryContextUpdate = Body(
        ...,
        openapi_examples=TEMPORARY_CONTEXT_UPDATE_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    """Deprecated — engine owns temporary writes (SPEC-017). Returns current list."""
    del body  # unused — client PUT is not a source of truth
    _LOG.info(
        "PUT temporary context ignored for project %s (SPEC-017 engine-owned writes)",
        project_id,
    )
    if store.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return get_temporary_context(project_id, store=store)
