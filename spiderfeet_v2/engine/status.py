"""Scan-step status lifecycle (R10-27).

TypeDB ``scan_status`` is constrained to the v1 scan lifecycle values
(``STARTING`` … ``FINISHED`` / ``ERROR-FAILED``). The orchestrator API still
surfaces a compact ``SUCCESS`` / ``ERROR`` outcome alongside ``scan_status``.
"""

from __future__ import annotations

# Persisted scan_status values (schema @values constraint).
STATUS_STARTING = "STARTING"
STATUS_RUNNING = "RUNNING"
STATUS_FINISHED = "FINISHED"
STATUS_ERROR_FAILED = "ERROR-FAILED"
STATUS_UNKNOWN = "UNKNOWN"
STATUS_DRY_RUN = "DRY_RUN"  # API-only; never persisted as scan_status

# Compact orchestrator outcome (ExecuteResponse.status).
OUTCOME_SUCCESS = "SUCCESS"
OUTCOME_ERROR = "ERROR"
OUTCOME_DRY_RUN = "DRY_RUN"

# Module statuses that count as a successful terminal outcome.
MODULE_OK = frozenset({"SUCCESS"})


def scan_status_for_module(module_status: str | None) -> str:
    """Map modules_v2 result status → TypeDB scan_status."""
    if module_status in MODULE_OK:
        return STATUS_FINISHED
    return STATUS_ERROR_FAILED


def outcome_for_scan_status(scan_status: str) -> str:
    """Map persisted scan_status → compact API outcome."""
    if scan_status == STATUS_FINISHED:
        return OUTCOME_SUCCESS
    if scan_status == STATUS_DRY_RUN:
        return OUTCOME_DRY_RUN
    return OUTCOME_ERROR
