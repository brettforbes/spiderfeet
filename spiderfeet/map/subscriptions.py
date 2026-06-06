"""OSINT service subscription tier and API-key readiness (Stage 4 — R2-04-06)."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Tuple

SubscriptionTier = Literal["none", "free_auth", "paid_auth"]

# Module opts that look like endpoints/hosts, not secrets.
_NON_SECRET_OPT_NAMES = frozenset(
    {
        "api_hostname",
        "api_host",
        "api_url",
        "api_base",
        "api_endpoint",
        "api_version",
    }
)

_SECRET_OPT_MARKERS = ("api_key", "apikey", "token", "secret", "password", "client_secret")


def is_secret_module_opt(name: str) -> bool:
    """True when a module opt name represents a credential, not infrastructure config."""
    lowered = name.lower().strip()
    if not lowered or lowered in _NON_SECRET_OPT_NAMES:
        return False
    if lowered.endswith("_hostname") or lowered.endswith("_host") or lowered.endswith("_url"):
        return False
    return any(marker in lowered for marker in _SECRET_OPT_MARKERS)


def secret_opt_names(service: Dict[str, Any]) -> List[str]:
    names: List[str] = []
    for opt in service.get("module_opts") or []:
        name = str(opt.get("name") or "").strip()
        if is_secret_module_opt(name):
            names.append(name)
    return names


def subscription_tier_for_service(service: Dict[str, Any]) -> SubscriptionTier:
    """Classify service subscription: none, free_auth, or paid_auth."""
    tier = str(service.get("access_tier") or "").lower()
    if tier == "paid":
        return "paid_auth"
    if tier == "free_auth":
        return "free_auth"
    if requires_api_key(service):
        return "free_auth"
    return "none"


def requires_api_key(service: Dict[str, Any]) -> bool:
    flags = [str(f).lower() for f in (service.get("flags") or [])]
    if "apikey" in flags:
        return True
    tier = str(service.get("access_tier") or "").lower()
    if tier in ("free_auth", "paid", "paid_auth"):
        return True
    data_source = service.get("data_source") or {}
    if data_source.get("api_key_instructions"):
        return True
    return bool(secret_opt_names(service))


def has_configured_api_key(
    service: Dict[str, Any],
    configured_modules: Dict[str, Any],
) -> bool:
    """True when required secret opts are populated in runtime module config."""
    if not requires_api_key(service):
        return True

    module_id = str(service.get("module_id") or "")
    runtime_opts = (configured_modules.get(module_id) or {}).get("opts") or {}
    secret_names = secret_opt_names(service)
    if secret_names:
        return any(str(runtime_opts.get(name, "")).strip() for name in secret_names)

    # Auth tier / docs require a key but catalog omits opt name — scan runtime opts.
    return any(
        is_secret_module_opt(str(name))
        and str(value).strip()
        for name, value in runtime_opts.items()
    )


def subscription_status(
    service: Dict[str, Any],
    configured_modules: Dict[str, Any],
) -> Tuple[SubscriptionTier, bool, bool, str | None]:
    """Return tier, requires_api_key, has_api_key, skip_reason for tests plan."""
    tier = subscription_tier_for_service(service)
    needs_key = requires_api_key(service)
    has_key = has_configured_api_key(service, configured_modules)
    skip = "missing-api-key" if needs_key and not has_key else None
    return tier, needs_key, has_key, skip


def mask_secret(value: Any) -> str | None:
    """Mask a secret for API responses (never return full value on GET)."""
    text = str(value or "").strip()
    if not text:
        return None
    if len(text) <= 4:
        return "••••"
    return "••••••" + text[-4:]


def writable_secret_opts(
    service: Dict[str, Any],
    configured_modules: Dict[str, Any],
) -> List[str]:
    """Secret opt names that may be written via the Subscriptions API."""
    module_id = str(service.get("module_id") or "")
    names: set[str] = set(secret_opt_names(service))
    runtime_opts = (configured_modules.get(module_id) or {}).get("opts") or {}
    for name in runtime_opts:
        if is_secret_module_opt(str(name)):
            names.add(str(name))
    if requires_api_key(service) and not names:
        names.add("api_key")
    return sorted(names)
