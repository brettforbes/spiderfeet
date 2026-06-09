"""Live scan_ui probe helpers for seed validation and tuning (Stage 4c)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from spiderfeet.map.fixture_categories import fixture_category_for_service
from spiderfeet.map.routes_catalog import service_by_module_id
from spiderfeet.map.test_targets import (
    fixture_kind_for_entry,
    positive_hit_entry,
    seed_entry,
)

CLEAN_INPUT_CANDIDATES: Dict[str, List[str]] = {
    "DOMAIN_NAME": ["sbs.com.au", "bbc.co.uk", "example.com"],
    "INTERNET_NAME": ["sbs.com.au", "bbc.co.uk", "example.com"],
    "IP_ADDRESS": ["8.8.8.8", "1.1.1.1"],
    "IPV6_ADDRESS": ["2001:4860:4860::8888"],
    "EMAILADDR": ["noreply@spiderfoot.net", "admin@bbc.co.uk"],
}

DIRTY_INPUT_CANDIDATES: Dict[str, List[str]] = {
    "DOMAIN_NAME": ["google.com", "github.com", "microsoft.com"],
    "INTERNET_NAME": ["google.com", "github.com", "zone-h.org"],
    "IP_ADDRESS": ["185.220.101.1", "91.198.174.192"],
    "EMAILADDR": ["admin@bbc.co.uk", "test@gmail.com"],
}


def fixture_kind_for_module(module_id: str, consumed_nugget_id: str) -> str:
    entry = seed_entry(module_id, consumed_nugget_id)
    if entry:
        return fixture_kind_for_entry(entry)
    svc = service_by_module_id(module_id) or {}
    return fixture_category_for_service(svc)


def evaluate_scan_ui_payload(
    payload: Dict[str, Any],
    *,
    fixture_kind: str,
) -> Dict[str, Any]:
    """Classify scan_ui response for positive or negative fixture semantics."""
    produced = payload.get("produced") or []
    record = payload.get("scan_record") or {}
    module_execution = payload.get("module_execution") or {}
    status = str(record.get("status") or "UNKNOWN")
    verdict = module_execution.get("verdict")
    count = len(produced)
    if fixture_kind == "negative":
        if verdict:
            passed = status == "FINISHED" and verdict == "clean_miss"
        else:
            # API without module_execution (pre-4c); approximate clean_miss
            passed = status == "FINISHED" and count == 0
        return {
            "status": status,
            "verdict": verdict,
            "produced_count": count,
            "validated_produces": False,
            "validated_negative": passed,
            "scan_id": record.get("scan_instance_id"),
        }

    passed = status == "FINISHED" and count > 0
    return {
        "status": status,
        "verdict": verdict,
        "produced_count": count,
        "validated_produces": passed,
        "validated_negative": False,
        "scan_id": record.get("scan_instance_id"),
    }


def post_scan_ui(
    api_base: str,
    *,
    module_id: str,
    consumed_nugget_id: str,
    input_value: str,
    timeout_seconds: int,
    fixture_kind: Optional[str] = None,
) -> Dict[str, Any]:
    """POST scan_ui and return normalized probe result (or error row)."""
    url = f"{api_base.rstrip('/')}/scan_ui"
    body = {
        "module_id": module_id,
        "consumed": {"nugget_id": consumed_nugget_id, "nugget_data": input_value},
        "wait": True,
        "timeout_seconds": timeout_seconds,
    }
    base = {
        "module_id": module_id,
        "consumed_nugget_id": consumed_nugget_id,
        "input_value": input_value,
    }
    try:
        response = requests.post(url, json=body, timeout=timeout_seconds + 45)
    except requests.RequestException as exc:
        return {
            **base,
            "status": "ERROR",
            "verdict": None,
            "produced_count": 0,
            "validated_produces": False,
            "validated_negative": False,
            "notes": str(exc),
        }
    if not response.ok:
        return {
            **base,
            "status": f"HTTP_{response.status_code}",
            "verdict": None,
            "produced_count": 0,
            "validated_produces": False,
            "validated_negative": False,
            "notes": response.text[:300],
        }
    payload = response.json()
    kind = fixture_kind or fixture_kind_for_module(module_id, consumed_nugget_id)
    result = evaluate_scan_ui_payload(payload, fixture_kind=kind)
    return {**base, **result}


def fetch_scan_log_summary(
    api_base: str,
    scan_id: Optional[str],
    *,
    limit: int = 8,
) -> str:
    """Short diagnostic snippet from GET /scans/{id}/logs."""
    if not scan_id:
        return ""
    url = f"{api_base.rstrip('/')}/scans/{scan_id}/logs"
    try:
        response = requests.get(url, params={"limit": limit}, timeout=15)
    except requests.RequestException:
        return ""
    if not response.ok:
        return ""
    lines: List[str] = []
    for row in response.json():
        component = row.get("component") or "?"
        level = row.get("type") or "?"
        message = str(row.get("message") or "")[:120]
        lines.append(f"{component}:{level}:{message}")
    return "; ".join(lines)


def probe_positive_candidates(
    api_base: str,
    *,
    module_id: str,
    consumed_nugget_id: str,
    candidates: List[str],
    timeout_seconds: int,
) -> Optional[Dict[str, Any]]:
    for value in candidates:
        result = post_scan_ui(
            api_base,
            module_id=module_id,
            consumed_nugget_id=consumed_nugget_id,
            input_value=value,
            timeout_seconds=timeout_seconds,
            fixture_kind="positive",
        )
        if result.get("validated_produces"):
            return result
    return None


def probe_negative_clean(
    api_base: str,
    *,
    module_id: str,
    consumed_nugget_id: str,
    candidates: List[str],
    timeout_seconds: int,
) -> Optional[Dict[str, Any]]:
    for value in candidates:
        result = post_scan_ui(
            api_base,
            module_id=module_id,
            consumed_nugget_id=consumed_nugget_id,
            input_value=value,
            timeout_seconds=timeout_seconds,
            fixture_kind="negative",
        )
        if result.get("validated_negative"):
            result["fixture_kind"] = "negative"
            return result
    return None
