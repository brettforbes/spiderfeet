"""Shared scan result fetching and status polling."""

from __future__ import annotations

import time
from typing import List, Optional, Tuple

from spiderfeet import SpiderFeetDb

from spiderfeet.api.schemas import ScanLogEntry, ScanResultItem

_STORAGE_MODULES = {"sfp__stor_db", "sfp__stor_stdout"}


def parse_scan_result_row(row: tuple) -> ScanResultItem:
    return ScanResultItem(
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


def fetch_scan_results(
    config: dict, scan_id: str, filter_fp: bool = False
) -> List[ScanResultItem]:
    dbh = SpiderFeetDb(config)
    rows = dbh.scanResultEvent(scan_id, "ALL", filterFp=filter_fp)
    return [parse_scan_result_row(row) for row in rows]


def fetch_scan_logs(
    config: dict,
    scan_id: str,
    *,
    limit: Optional[int] = None,
    from_row_id: int = 0,
    reverse: bool = False,
) -> List[ScanLogEntry]:
    dbh = SpiderFeetDb(config)
    rows = dbh.scanLogs(scan_id, limit, from_row_id or None, reverse)
    items: List[ScanLogEntry] = []
    for row in rows:
        generated = int(row[0]) if row[0] is not None else 0
        items.append(
            ScanLogEntry(
                generated_ms=generated,
                component=row[1],
                type=str(row[2] or ""),
                message=str(row[3] or ""),
                row_id=int(row[4]) if len(row) > 4 and row[4] is not None else None,
            )
        )
    return items


def wait_for_scan(
    config: dict,
    scan_id: str,
    timeout_seconds: int = 120,
    poll_interval: float = 1.0,
) -> Tuple[str, Optional[int], Optional[int]]:
    """Poll until scan reaches a terminal status. Returns (status, started, ended)."""
    dbh = SpiderFeetDb(config)
    deadline = time.time() + timeout_seconds
    terminal = {
        "FINISHED",
        "ERROR-FAILED",
        "ABORTED",
        "ABORT-REQUESTED",
    }
    while time.time() < deadline:
        row = dbh.scanInstanceGet(scan_id)
        if row and row[5] in terminal:
            return row[5], _as_int(row[3]), _as_int(row[4])
        time.sleep(poll_interval)
    raise TimeoutError(f"Scan {scan_id} did not finish within {timeout_seconds}s")


def _as_int(value) -> Optional[int]:
    if value is None or value == 0 or value == "0":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
