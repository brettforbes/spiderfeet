"""Resolve scan_ui consumed nuggets into SpiderFeet scan target value + type."""

from __future__ import annotations

from spiderfeet import SpiderFeetHelpers

# Catalogue nugget types used as explicit scan seeds (not CLI-regex inferrable).
CATALOGUE_SCAN_TARGET_TYPES = frozenset(
    {
        "COMPANY_NAME",
        "PHYSICAL_ADDRESS",
        "WEB_ANALYTICS_ID",
        "LEI",
    }
)


def normalize_scan_target(target: str, target_type: str) -> str:
    if target_type in ("HUMAN_NAME", "USERNAME", "BITCOIN_ADDRESS"):
        return target.replace('"', "")
    if target_type in CATALOGUE_SCAN_TARGET_TYPES:
        return target
    return target.lower()


def resolve_scan_ui_target(nugget_id: str, nugget_data: str) -> tuple[str, str]:
    """Map consumed nugget input to (target_value, target_type) for scan start."""
    data = (nugget_data or "").strip()
    if not data:
        raise ValueError("blank nugget_data")

    inferred = SpiderFeetHelpers.targetTypeFromString(data)

    if nugget_id == "USERNAME" and inferred is None:
        quoted = data if (data.startswith('"') and data.endswith('"')) else f'"{data}"'
        if SpiderFeetHelpers.targetTypeFromString(quoted) == "USERNAME":
            return normalize_scan_target(quoted, "USERNAME"), "USERNAME"

    if inferred == nugget_id:
        return normalize_scan_target(data, inferred), inferred

    if inferred == "INTERNET_NAME" and nugget_id == "DOMAIN_NAME":
        return normalize_scan_target(data, "INTERNET_NAME"), "INTERNET_NAME"

    if nugget_id in CATALOGUE_SCAN_TARGET_TYPES:
        return normalize_scan_target(data, nugget_id), nugget_id

    if inferred is not None:
        return normalize_scan_target(data, inferred), inferred

    raise ValueError("nugget_data is not a valid SpiderFeet target")
