"""Scan-step retrieval — four UI forms via AL3 projection (R10-24)."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from spiderfeet_v2.api.deps import get_crud_store, get_projection_store
from spiderfeet_v2.api.schemas import ScanStepOut
from spiderfeet_v2.db.crud import CrudStore
from spiderfeet_v2.db.projections import ProjectionStore

router = APIRouter(tags=["v2-scan-steps"])


@router.get("/scan-steps", response_model=List[Dict[str, Any]])
def list_scan_steps(store: CrudStore = Depends(get_crud_store)) -> List[Dict[str, Any]]:
    return store.list_scan_steps()


@router.get("/scan-steps/{scan_instance_id}", response_model=ScanStepOut)
def get_scan_step(
    scan_instance_id: str,
    projections: ProjectionStore = Depends(get_projection_store),
    store: CrudStore = Depends(get_crud_store),
) -> Dict[str, Any]:
    """Return four forms (text/structured/graph/narrative) + consumed/produced.

    Prefers AL3 ``scan_step_json`` projection; merges CRUD attrs when present.
    """
    proj = projections.get_scan_step(scan_instance_id)
    crud = store.get_scan_step(scan_instance_id)
    if proj is None and crud is None:
        raise HTTPException(status_code=404, detail="Scan step not found")

    out: Dict[str, Any] = {
        "scan_instance_id": scan_instance_id,
        "cli_command": None,
        "text_form": None,
        "structured_form": None,
        "graph_form": None,
        "markdown_narrative_form": None,
        "consumed": [],
        "produced": [],
        "scan_result_graph": [],
    }
    if proj:
        out.update(proj)
    if crud:
        # Fill gaps from CRUD attribute names when projection is empty.
        out.setdefault("step_module_id", crud.get("step_module_id"))
        out["step_module_id"] = crud.get("step_module_id")
        out["scan_status"] = crud.get("scan_status")
        out["scan_ui_structured_form_type"] = crud.get("scan_ui_structured_form_type")
        if not out.get("cli_command"):
            out["cli_command"] = crud.get("scan_ui_cli_command")
        if not out.get("text_form"):
            out["text_form"] = crud.get("scan_ui_text_form")
        if not out.get("structured_form"):
            out["structured_form"] = crud.get("scan_ui_structured_form")
        if not out.get("graph_form"):
            out["graph_form"] = crud.get("scan_ui_graph_form")
        if not out.get("markdown_narrative_form"):
            out["markdown_narrative_form"] = crud.get(
                "scan_ui_markdown_narrative_form"
            )
        if not out.get("consumed"):
            out["consumed"] = crud.get("consumed_ids") or []
        if not out.get("produced"):
            out["produced"] = crud.get("produced_ids") or []
    return out
