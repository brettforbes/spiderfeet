"""Project / temporary context read + temporary-context update (R10-24 / R10-25 / R16-03)."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException

from spiderfeet_v2.api.deps import get_crud_store, get_projection_store
from spiderfeet_v2.api.schemas import (
    TEMPORARY_CONTEXT_UPDATE_OPENAPI_EXAMPLES,
    ContextGraphOut,
    TemporaryContextUpdate,
)
from spiderfeet_v2.api.temporary_ids import assert_no_temporary_ids, strip_temporary_ids
from spiderfeet_v2.db.crud import CrudError, CrudStore
from spiderfeet_v2.db.projections import ProjectionStore
from spiderfeet_v2.engine.persist import (
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
        meta = store.get_subgraph(kind, sg_id)
        dual = meta or {}
    if not dual:
        return ContextGraphOut(
            project_id=project_id,
            kind=kind,
            subgraph_id=sg_id,
            nodes=[],
            edges=[],
        ).model_dump()
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
    response_model=ContextGraphOut,
)
def get_temporary_context(
    project_id: str,
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    return _load_context(
        project_id=project_id,
        kind="temporary_subgraph",
        id_attr="temporary_subgraph_id",
        projection_key="temporary_subgraph",
        store=store,
        projections=projections,
    )


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
    response_model=ContextGraphOut,
)
def update_temporary_context(
    project_id: str,
    body: TemporaryContextUpdate = Body(
        ...,
        openapi_examples=TEMPORARY_CONTEXT_UPDATE_OPENAPI_EXAMPLES,
    ),
    store: CrudStore = Depends(get_crud_store),
    projections: ProjectionStore = Depends(get_projection_store),
) -> Dict[str, Any]:
    """Persist temporary context after stripping widget ``temporary_id`` tags.

    Edges keyed by temporary ids are remapped to ``nugget_instance_id`` (R10-25).
    Always writes to the project's canonical temporary_subgraph id (R16-03).
    """
    if store.get_project(project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found")

    cleaned = strip_temporary_ids({"nodes": body.nodes, "edges": body.edges})
    try:
        assert_no_temporary_ids(cleaned)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    sg_id = temporary_subgraph_id_for(project_id)
    if body.temporary_subgraph_id and body.temporary_subgraph_id != sg_id:
        _LOG.warning(
            "ignoring foreign temporary_subgraph_id %s for project %s; "
            "using canonical %s",
            body.temporary_subgraph_id,
            project_id,
            sg_id,
        )

    existing = store.get_subgraph("temporary_subgraph", sg_id)
    try:
        if existing is None:
            dual = store.create_subgraph(
                {
                    "kind": "temporary_subgraph",
                    "temporary_subgraph_id": sg_id,
                    "project_id": project_id,
                    "graph": cleaned,
                }
            )
        else:
            dual = store.update_subgraph(
                "temporary_subgraph",
                sg_id,
                {"graph": cleaned},
            )
    except CrudError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    graph = _parse_graph_payload(dual)
    # Prefer the cleaned payload we just wrote (dual may echo json_string).
    nodes = graph["nodes"] or cleaned["nodes"]
    edges = graph["edges"] or cleaned["edges"]
    for n in nodes:
        if isinstance(n, dict) and "temporary_id" in n:
            n.pop("temporary_id", None)

    return ContextGraphOut(
        project_id=project_id,
        kind="temporary_subgraph",
        subgraph_id=sg_id,
        nodes=nodes,
        edges=edges,
        json_string=dual.get("json_string"),
    ).model_dump()
