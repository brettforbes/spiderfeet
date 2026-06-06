"""Subscriptions endpoints — per-module API key management (Stage 4 — R2-04-05)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from spiderfeet.api.bootstrap import Runtime, get_runtime
from spiderfeet.api.schemas import (
    SubscriptionModuleDetail,
    SubscriptionModuleSummary,
    SubscriptionModuleUpdate,
)
from spiderfeet.api.services import subscriptions as subscriptions_service

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


def runtime_dep() -> Runtime:
    return get_runtime()


@router.get("/modules", response_model=List[SubscriptionModuleSummary])
def list_subscription_modules(
    search: Optional[str] = Query(None, description="Filter by module_id or display name"),
    limit: int = Query(200, ge=1, le=200),
    offset: int = Query(0, ge=0),
    runtime: Runtime = Depends(runtime_dep),
) -> List[SubscriptionModuleSummary]:
    """List OSINT modules that require API credentials, with masked key status."""
    return subscriptions_service.list_subscription_modules(
        search=search,
        limit=limit,
        offset=offset,
        runtime_config=runtime.config,
    )


@router.get("/modules/{module_id}", response_model=SubscriptionModuleDetail)
def get_subscription_module(
    module_id: str,
    runtime: Runtime = Depends(runtime_dep),
) -> SubscriptionModuleDetail:
    """Module subscription detail (metadata + masked secret opts)."""
    detail = subscriptions_service.get_subscription_module(
        module_id,
        runtime_config=runtime.config,
    )
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Unknown module_id: {module_id}")
    return detail


@router.put("/modules/{module_id}", response_model=SubscriptionModuleDetail)
def update_subscription_module(
    module_id: str,
    body: SubscriptionModuleUpdate,
    runtime: Runtime = Depends(runtime_dep),
) -> SubscriptionModuleDetail:
    """Set or clear secret module opts; persists to SpiderFeet DB config."""
    try:
        return subscriptions_service.update_subscription_module(
            module_id,
            body,
            runtime_config=runtime.config,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
