"""service_origin and legacy catalogue normalization (Stage 5 map filters)."""

from __future__ import annotations

SERVICE_ORIGIN_EXTERNAL_API = "external-api"
SERVICE_ORIGIN_CLI = "cli"
SERVICE_ORIGIN_LOCAL = "local"

VALID_SERVICE_ORIGINS = frozenset(
    {
        SERVICE_ORIGIN_EXTERNAL_API,
        SERVICE_ORIGIN_CLI,
        SERVICE_ORIGIN_LOCAL,
    }
)

_LEGACY_ORIGIN_TO_CLASSIFICATION = {
    "external": SERVICE_ORIGIN_EXTERNAL_API,
    "quarantine": None,  # resolved from module_id
    "custom": SERVICE_ORIGIN_EXTERNAL_API,
}


def service_origin_for_module_id(module_id: str, *, external_api: bool) -> str:
    """Classify how the service runs: remote API, CLI wrapper, or local logic."""
    if external_api:
        return SERVICE_ORIGIN_EXTERNAL_API
    if str(module_id).startswith("sfp_tool_"):
        return SERVICE_ORIGIN_CLI
    return SERVICE_ORIGIN_LOCAL


def normalize_service_origin(
    raw: str | None,
    *,
    module_id: str,
    external_api: bool,
) -> str:
    """Map legacy catalogue / TypeDB values to external-api | cli | local."""
    value = str(raw or "").strip().lower()
    if value in VALID_SERVICE_ORIGINS:
        return value
    if value in _LEGACY_ORIGIN_TO_CLASSIFICATION:
        mapped = _LEGACY_ORIGIN_TO_CLASSIFICATION[value]
        if mapped:
            return mapped
        return service_origin_for_module_id(module_id, external_api=external_api)
    return service_origin_for_module_id(module_id, external_api=external_api)
