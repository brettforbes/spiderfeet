"""Module test catalog endpoints (Stage 4 — R2-04-04)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from spiderfeet.api.schemas import TestsModuleDetail, TestsModuleSummary, TestsSummaryResponse
from spiderfeet.api.services import tests as tests_service

router = APIRouter(prefix="/tests", tags=["tests"])


@router.get("/summary", response_model=TestsSummaryResponse)
def tests_summary() -> TestsSummaryResponse:
    """Aggregate module/route counts for the Tests tab summary table."""
    return tests_service.tests_summary()


@router.get("/modules", response_model=List[TestsModuleSummary])
def list_modules(
    search: Optional[str] = Query(None, description="Filter by module_id or display name"),
    consumption_group: Optional[str] = Query(None, description="Filter by consumption_group"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> List[TestsModuleSummary]:
    """Paged module list for Tests tab accordions."""
    return tests_service.list_modules(
        search=search,
        consumption_group=consumption_group,
        limit=limit,
        offset=offset,
    )


@router.get("/modules/{module_id}", response_model=TestsModuleDetail)
def get_module(module_id: str) -> TestsModuleDetail:
    """Module detail with full route matrix (consumed × produced)."""
    detail = tests_service.get_module(module_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Unknown module_id: {module_id}")
    return detail
