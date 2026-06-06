"""Module test catalog endpoints (Stage 4 — R2-04-04)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from spiderfeet.api.bootstrap import get_runtime
from spiderfeet.api.schemas import (
    TestsModuleDetail,
    TestsModuleSummary,
    TestsNuggetSamplesResponse,
    TestsPlanResponse,
    TestsSummaryResponse,
)
from spiderfeet.api.services import tests as tests_service
from spiderfeet.map.test_targets import all_nugget_samples

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
    runtime = get_runtime()
    return tests_service.list_modules(
        search=search,
        consumption_group=consumption_group,
        limit=limit,
        offset=offset,
        runtime_config=runtime.config,
    )


@router.get("/nugget-samples", response_model=TestsNuggetSamplesResponse)
def nugget_samples() -> TestsNuggetSamplesResponse:
    """Default scan targets per consumed nugget_id (Stage 4c pilot)."""
    return TestsNuggetSamplesResponse(samples=all_nugget_samples())


@router.get("/plan", response_model=TestsPlanResponse)
def tests_plan(
    search: Optional[str] = Query(None, description="Filter by module_id or display name"),
    consumption_group: Optional[str] = Query(None, description="Filter by consumption_group"),
    limit: int = Query(200, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> TestsPlanResponse:
    """Pre-expanded batch run queue for the Tests tab (matches /tests/modules filters)."""
    runtime = get_runtime()
    return tests_service.test_plan(
        search=search,
        consumption_group=consumption_group,
        limit=limit,
        offset=offset,
        runtime_config=runtime.config,
    )


@router.get("/modules/{module_id}", response_model=TestsModuleDetail)
def get_module(module_id: str) -> TestsModuleDetail:
    """Module detail with full route matrix (consumed × produced)."""
    detail = tests_service.get_module(module_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Unknown module_id: {module_id}")
    return detail
