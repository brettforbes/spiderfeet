"""UI scan endpoint: consumed nugget + module -> scan-record + produced nuggets."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException

from spiderfeet.api.bootstrap import Runtime, get_runtime
from spiderfeet.api.schemas import (
    SCAN_UI_OPENAPI_EXAMPLES,
    SCAN_UI_SWAGGER_EXAMPLE,
    ScanUiRequest,
    ScanUiResponse,
)
from spiderfeet.api.services.scan_ui import ScanUiError, run_scan_ui

router = APIRouter(tags=["scan_ui"])


def runtime_dep() -> Runtime:
    return get_runtime()


@router.post("/scan_ui", response_model=ScanUiResponse)
def scan_ui(
    body: ScanUiRequest = Body(
        ...,
        example=SCAN_UI_SWAGGER_EXAMPLE,
        openapi_examples=SCAN_UI_OPENAPI_EXAMPLES,
    ),
    runtime: Runtime = Depends(runtime_dep),
) -> ScanUiResponse:
    """Run a single module from a consumed nugget and return UI-shaped results.

    Designed for the spiderfeet-widget iframe: one seed nugget in, produced
    nuggets plus ``scan-record`` metadata out. Waits for scan completion by
    default (``wait: true``).
    """
    try:
        return run_scan_ui(runtime, body)
    except ScanUiError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
