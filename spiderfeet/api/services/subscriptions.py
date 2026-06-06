"""Subscriptions API service — persist module API keys (Stage 4 — R2-04-05)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from spiderfeet import SpiderFeetDb
from spiderfeet.api.schemas import (
    SecretOptMasked,
    SubscriptionModuleDetail,
    SubscriptionModuleSummary,
    SubscriptionModuleUpdate,
)
from spiderfeet.map.routes_catalog import load_osint_services, service_by_module_id
from spiderfeet.map.subscriptions import (
    has_configured_api_key,
    mask_secret,
    requires_api_key,
    subscription_status,
    subscription_tier_for_service,
    writable_secret_opts,
)


def _configured_modules(runtime_config: Dict[str, Any]) -> Dict[str, Any]:
    return runtime_config.get("__modules__", {}) or {}


def _secret_opts_masked(
    service: Dict[str, Any],
    configured: Dict[str, Any],
) -> List[SecretOptMasked]:
    module_id = str(service.get("module_id") or "")
    runtime_opts = (configured.get(module_id) or {}).get("opts") or {}
    items: List[SecretOptMasked] = []
    for name in writable_secret_opts(service, configured):
        raw = runtime_opts.get(name, "")
        masked = mask_secret(raw)
        items.append(
            SecretOptMasked(
                name=name,
                masked_value=masked,
                configured=bool(str(raw or "").strip()),
            )
        )
    return items


def _summary_row(service: Dict[str, Any], configured: Dict[str, Any]) -> SubscriptionModuleSummary:
    tier, needs_key, has_key, _skip = subscription_status(service, configured)
    return SubscriptionModuleSummary(
        module_id=str(service.get("module_id") or ""),
        name=str(service.get("name") or ""),
        subscription_tier=tier,
        requires_api_key=needs_key,
        has_api_key=has_key,
        secret_opts=_secret_opts_masked(service, configured),
    )


def list_subscription_modules(
    *,
    search: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
    runtime_config: Optional[Dict[str, Any]] = None,
) -> List[SubscriptionModuleSummary]:
    configured = _configured_modules(runtime_config or {})
    query = (search or "").strip().lower()
    rows: List[SubscriptionModuleSummary] = []
    for svc in load_osint_services():
        if not requires_api_key(svc):
            continue
        module_id = str(svc.get("module_id") or "")
        name = str(svc.get("name") or "")
        if query and query not in module_id.lower() and query not in name.lower():
            continue
        rows.append(_summary_row(svc, configured))
    return rows[offset : offset + limit]


def get_subscription_module(
    module_id: str,
    *,
    runtime_config: Optional[Dict[str, Any]] = None,
) -> Optional[SubscriptionModuleDetail]:
    service = service_by_module_id(module_id)
    if service is None:
        return None
    configured = _configured_modules(runtime_config or {})
    tier = subscription_tier_for_service(service)
    needs_key = requires_api_key(service)
    has_key = has_configured_api_key(service, configured)
    data_source = service.get("data_source") or {}
    instructions = data_source.get("api_key_instructions") or []
    if isinstance(instructions, str):
        instructions = [instructions]
    return SubscriptionModuleDetail(
        module_id=module_id,
        name=str(service.get("name") or ""),
        summary=str(service.get("summary") or ""),
        access_tier=str(service.get("access_tier") or ""),
        subscription_tier=tier,
        requires_api_key=needs_key,
        has_api_key=has_key,
        website=data_source.get("website"),
        api_key_instructions=[str(x) for x in instructions],
        consumed_nuggets=[str(x) for x in (service.get("consumed_nuggets") or [])],
        produced_nuggets=[str(x) for x in (service.get("produced_nuggets") or [])],
        secret_opts=_secret_opts_masked(service, configured),
    )


def _serialize_module_opt(module_id: str, opt_name: str, value: Any) -> Dict[str, Any]:
    if isinstance(value, bool):
        return {f"{module_id}:{opt_name}": 1 if value else 0}
    if isinstance(value, list):
        return {f"{module_id}:{opt_name}": ",".join(str(x) for x in value)}
    return {f"{module_id}:{opt_name}": value}


def update_subscription_module(
    module_id: str,
    body: SubscriptionModuleUpdate,
    *,
    runtime_config: Dict[str, Any],
) -> SubscriptionModuleDetail:
    service = service_by_module_id(module_id)
    if service is None:
        raise LookupError(f"Unknown module_id: {module_id}")
    if not requires_api_key(service):
        raise ValueError(f"Module {module_id} does not require API credentials")

    configured = _configured_modules(runtime_config)
    allowed = set(writable_secret_opts(service, configured))
    if not body.secrets:
        raise ValueError("At least one secret opt is required")

    unknown = [name for name in body.secrets if name not in allowed]
    if unknown:
        raise ValueError(f"Unsupported secret opt(s): {', '.join(sorted(unknown))}")

    modules = runtime_config.get("__modules__") or {}
    if module_id not in modules:
        raise LookupError(f"Module not loaded in runtime: {module_id}")

    store: Dict[str, Any] = {}
    module_opts = modules[module_id].setdefault("opts", {})
    for opt_name, value in body.secrets.items():
        stored_value = "" if value is None else str(value)
        module_opts[opt_name] = stored_value
        store.update(_serialize_module_opt(module_id, opt_name, stored_value))

    SpiderFeetDb(runtime_config).configSet(store)
    detail = get_subscription_module(module_id, runtime_config=runtime_config)
    if detail is None:
        raise RuntimeError(f"Failed to reload subscription detail for {module_id}")
    return detail
