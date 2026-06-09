"""OSINT service_state helpers (catalogue + TypeDB map model)."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple

VALID_SERVICE_STATES = frozenset(
    {"in-test", "favourite", "unique", "error", "dominated"}
)
DEFAULT_SERVICE_STATE = "in-test"

# Upstream-broken none-tier modules (seed research finalize pass).
UPSTREAM_ERROR_MODULE_IDS = frozenset(
    {
        "sfp_commoncrawl",
        "sfp_crt",
        "sfp_dnsdumpster",
        "sfp_flickr",
        "sfp_myspace",
        "sfp_s3bucket",
        "sfp_searchcode",
        "sfp_sublist3r",
    }
)


def service_state_for_service(svc: Dict[str, Any]) -> str:
    raw = str(svc.get("service_state") or DEFAULT_SERVICE_STATE).strip()
    return raw if raw in VALID_SERVICE_STATES else DEFAULT_SERVICE_STATE


def include_in_operator_ui(svc: Dict[str, Any]) -> bool:
    """Tests and Subscriptions tabs hide error-state services."""
    return service_state_for_service(svc) != "error"


def filter_operator_services(
    services: Iterable[Dict[str, Any]],
) -> Tuple[Dict[str, Any], ...]:
    return tuple(svc for svc in services if include_in_operator_ui(svc))
