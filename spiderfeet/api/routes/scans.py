"""Scan lifecycle and results endpoints."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from spiderfeet import SpiderFeetDb
from spiderfeet.api.bootstrap import Runtime, get_runtime
from spiderfeet.api.schemas import (
    SCAN_CREATE_OPENAPI_EXAMPLES,
    ScanCreateRequest,
    ScanCreateResponse,
    ScanDetail,
    ScanResultItem,
    ScanSummary,
)
from spiderfeet.api.services.scans import ScanStartError, start_scan

router = APIRouter(tags=["scans"])


def runtime_dep() -> Runtime:
    return get_runtime()


@router.post("/scans", response_model=ScanCreateResponse, status_code=201)
def create_scan(
    body: ScanCreateRequest = Body(
        ...,
        example={
            "target": "sbs.com.au",
            "use_case": "passive",
        },
        openapi_examples=SCAN_CREATE_OPENAPI_EXAMPLES,
    ),
    runtime: Runtime = Depends(runtime_dep),
) -> ScanCreateResponse:
    """Start a scan (CLI ``-s`` / CherryPy ``/startscan`` parity)."""
    try:
        scan_id = start_scan(runtime, body)
    except ScanStartError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    row = SpiderFeetDb(runtime.config).scanInstanceGet(scan_id)
    status = row[5] if row else "STARTING"
    return ScanCreateResponse(scan_id=scan_id, status=status)


@router.get("/scans", response_model=List[ScanSummary])
def list_scans(runtime: Runtime = Depends(runtime_dep)) -> List[ScanSummary]:
    """List scans (CherryPy ``/scanlist`` parity)."""
    dbh = SpiderFeetDb(runtime.config)
    rows = dbh.scanInstanceList()
    result = []
    for row in rows:
        result.append(
            ScanSummary(
                scan_id=row[0],
                name=row[1],
                target=row[2],
                created=_int_or_none(row[3]),
                started=_int_or_none(row[4]),
                ended=_int_or_none(row[5]),
                status=row[6] or "UNKNOWN",
                result_count=int(row[7]) if row[7] else 0,
            )
        )
    return result


@router.get("/scans/{scan_id}", response_model=ScanDetail)
def get_scan(
    scan_id: str,
    runtime: Runtime = Depends(runtime_dep),
) -> ScanDetail:
    """Scan status (CherryPy ``/scanstatus`` parity)."""
    dbh = SpiderFeetDb(runtime.config)
    row = dbh.scanInstanceGet(scan_id)
    if not row:
        raise HTTPException(status_code=404, detail="Scan not found")
    return ScanDetail(
        scan_id=scan_id,
        name=row[0],
        target=row[1],
        created=_int_or_none(row[2]),
        started=_int_or_none(row[3]),
        ended=_int_or_none(row[4]),
        status=row[5] or "UNKNOWN",
    )


@router.get("/scans/{scan_id}/results", response_model=List[ScanResultItem])
def get_scan_results(
    scan_id: str,
    event_type: str = Query("ALL", alias="event_type"),
    filter_false_positives: bool = Query(False, alias="filter_fp"),
    runtime: Runtime = Depends(runtime_dep),
) -> List[ScanResultItem]:
    """Scan result events (CherryPy ``/scaneventresults`` parity)."""
    dbh = SpiderFeetDb(runtime.config)
    if not dbh.scanInstanceGet(scan_id):
        raise HTTPException(status_code=404, detail="Scan not found")

    try:
        rows = dbh.scanResultEvent(
            scan_id,
            event_type,
            filterFp=filter_false_positives,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    items = []
    for row in rows:
        items.append(
            ScanResultItem(
                generated=int(row[0]) if row[0] is not None else 0,
                data=row[1] or "",
                source_data=row[2],
                module=row[3] or "",
                type=row[4] or "",
                confidence=int(row[5] or 0),
                visibility=int(row[6] or 0),
                risk=int(row[7] or 0),
                event_description=row[10] if len(row) > 10 else None,
                false_positive=bool(row[12]) if len(row) > 12 else False,
            )
        )
    return items


def _int_or_none(value) -> Optional[int]:
    if value is None or value == 0 or value == "0":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
