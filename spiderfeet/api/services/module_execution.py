"""Infer per-module execution summary from scan results and logs (Stage 4c)."""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from spiderfeet.api.schemas import ModuleExecutionSummary, ScanResultItem

_ERROR_LEVELS = frozenset({"ERROR", "CRITICAL"})


def _module_error_in_logs(log_rows: Sequence[Sequence], module_id: str) -> bool:
    for row in log_rows:
        if len(row) < 4:
            continue
        component = str(row[1] or "")
        level = str(row[2] or "").upper()
        if component == module_id and level in _ERROR_LEVELS:
            return True
    return False


def count_module_produced(
    raw: Iterable[ScanResultItem],
    module_id: str,
    *,
    storage_modules: frozenset[str],
) -> int:
    count = 0
    for item in raw:
        if item.module in storage_modules or item.module == "SpiderFeet UI":
            continue
        if item.module == module_id:
            count += 1
    return count


def infer_module_execution(
    *,
    module_id: str,
    status: str,
    events_emitted: int,
    log_rows: Optional[Sequence[Sequence]] = None,
    expected_absent_types: Optional[List[str]] = None,
    scan_results_by_type: Optional[dict[str, int]] = None,
) -> ModuleExecutionSummary:
    """Derive verdict from scan lifecycle, produced events, and optional logs."""
    terminal_error = status == "ERROR-FAILED"
    module_error = bool(log_rows) and _module_error_in_logs(log_rows, module_id)

    if terminal_error or module_error:
        return ModuleExecutionSummary(
            module_id=module_id,
            status=status,
            events_emitted=events_emitted,
            verdict="error_failed",
        )

    if status != "FINISHED":
        return ModuleExecutionSummary(
            module_id=module_id,
            status=status,
            events_emitted=events_emitted,
            verdict="incomplete",
        )

    if events_emitted > 0:
        return ModuleExecutionSummary(
            module_id=module_id,
            status=status,
            events_emitted=events_emitted,
            verdict="hit",
        )

    absent_violations: List[str] = []
    if expected_absent_types and scan_results_by_type:
        for event_type in expected_absent_types:
            if scan_results_by_type.get(event_type, 0) > 0:
                absent_violations.append(event_type)

    if absent_violations:
        return ModuleExecutionSummary(
            module_id=module_id,
            status=status,
            events_emitted=events_emitted,
            verdict="absent_violation",
            absent_violations=absent_violations,
        )

    return ModuleExecutionSummary(
        module_id=module_id,
        status=status,
        events_emitted=events_emitted,
        verdict="clean_miss",
    )
