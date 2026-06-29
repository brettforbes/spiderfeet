"""Subscriptions API service — unified SpiderFeet + CLI credential providers."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from spiderfeet import SpiderFeetDb
from spiderfeet.api.schemas import (
    SecretOptMasked,
    SubscriptionModuleDetail,
    SubscriptionModuleSummary,
    SubscriptionModuleUpdate,
)
from spiderfeet.credentials.registry import (
    enrich_provider_from_catalog,
    list_providers,
    osint_modules_not_in_registry,
    provider_by_id,
    provider_group,
    secret_field_names,
    service_labels_for_provider,
)
from spiderfeet.credentials.store import (
    encrypt_and_store_module_secrets,
    has_cli_provider_secrets,
    masked_secret_opts,
    set_cli_provider_secrets,
)
from spiderfeet.credentials.sync import sync_cli_apps_for_provider
from spiderfeet.map.fixture_categories import fixture_category_for_service
from spiderfeet.map.signup_links import signup_metadata
from spiderfeet.map.subscriptions import (
    has_configured_api_key,
    requires_api_key,
    subscription_status,
    subscription_tier_for_service,
    writable_secret_opts,
)


def _configured_modules(runtime_config: Dict[str, Any]) -> Dict[str, Any]:
    return runtime_config.get("__modules__", {}) or {}


def _secret_opts_masked_list(provider_id: str, runtime_config: Dict[str, Any]) -> List[SecretOptMasked]:
    rows = masked_secret_opts(provider_id, runtime_config)
    return [SecretOptMasked(**row) for row in rows]


def _has_provider_key(provider: Dict[str, Any], runtime_config: Dict[str, Any]) -> bool:
    provider_id = str(provider.get("provider_id") or "")
    if provider.get("kind") == "cli_only":
        return has_cli_provider_secrets(provider_id, runtime_config)
    mod_id = str(provider.get("spiderfeet_module_id") or provider_id)
    svc = _service_for_module(mod_id)
    if svc is None:
        return False
    return has_configured_api_key(svc, _configured_modules(runtime_config))


def _service_for_module(module_id: str):
    from spiderfeet.map.routes_catalog import service_by_module_id

    return service_by_module_id(module_id)


def _summary_from_provider(provider: Dict[str, Any], runtime_config: Dict[str, Any]) -> SubscriptionModuleSummary:
    enriched = enrich_provider_from_catalog(provider)
    provider_id = str(enriched.get("provider_id") or "")
    tier = str(enriched.get("subscription_tier") or "free_auth")
    if enriched.get("spiderfeet_module_id"):
        svc = _service_for_module(str(enriched["spiderfeet_module_id"]))
        if svc is not None:
            tier = subscription_tier_for_service(svc)
    has_key = _has_provider_key(enriched, runtime_config)
    signup = {
        "signup_url": enriched.get("signup_url"),
        "signup_bucket": enriched.get("signup_bucket"),
        "signup_note": enriched.get("signup_note"),
    }
    if enriched.get("spiderfeet_module_id") and not signup.get("signup_url"):
        svc = _service_for_module(str(enriched["spiderfeet_module_id"]))
        if svc:
            signup = signup_metadata(svc)
    return SubscriptionModuleSummary(
        module_id=provider_id,
        name=str(enriched.get("name") or provider_id),
        subscription_tier=tier,
        requires_api_key=True,
        has_api_key=has_key,
        fixture_category=str(enriched.get("fixture_category") or "positive"),
        signup_url=signup.get("signup_url"),
        signup_bucket=signup.get("signup_bucket"),
        signup_note=signup.get("signup_note"),
        secret_opts=_secret_opts_masked_list(provider_id, runtime_config),
        provider_kind=str(enriched.get("kind") or "shared"),
        service_labels=service_labels_for_provider(enriched),
        cli_apps=[str(x) for x in (enriched.get("cli_apps") or [])],
        group=provider_group(enriched),
    )


def _summary_from_legacy_service(service: Dict[str, Any], runtime_config: Dict[str, Any]) -> SubscriptionModuleSummary:
    configured = _configured_modules(runtime_config)
    tier, needs_key, has_key, _skip = subscription_status(service, configured)
    signup = signup_metadata(service)
    module_id = str(service.get("module_id") or "")
    return SubscriptionModuleSummary(
        module_id=module_id,
        name=str(service.get("name") or ""),
        subscription_tier=tier,
        requires_api_key=needs_key,
        has_api_key=has_key,
        fixture_category=fixture_category_for_service(service),
        signup_url=signup.get("signup_url"),
        signup_bucket=signup.get("signup_bucket"),
        signup_note=signup.get("signup_note"),
        secret_opts=_secret_opts_masked_list(module_id, runtime_config),
        provider_kind="spiderfeet",
        service_labels=[f"SpiderFeet: {module_id}"],
        cli_apps=[],
        group="spiderfeet",
    )


def _matches_filters(
    row: SubscriptionModuleSummary,
    *,
    provider_kind: Optional[str],
    cli_app: Optional[str],
    group: Optional[str],
) -> bool:
    if provider_kind and provider_kind != "all":
        if row.provider_kind != provider_kind and not (
            provider_kind == "spiderfeet" and row.provider_kind == "shared"
        ):
            if provider_kind == "cli" and row.provider_kind not in ("cli_only", "shared"):
                return False
            elif provider_kind == "spiderfeet" and row.provider_kind not in ("spiderfeet", "shared"):
                return False
            elif provider_kind not in ("cli", "spiderfeet") and row.provider_kind != provider_kind:
                return False
    if cli_app and cli_app not in (row.cli_apps or []):
        return False
    if group and group != "all" and row.group != group:
        return False
    return True


def list_subscription_modules(
    *,
    search: Optional[str] = None,
    provider_kind: Optional[str] = None,
    cli_app: Optional[str] = None,
    group: Optional[str] = None,
    limit: int = 200,
    offset: int = 0,
    runtime_config: Optional[Dict[str, Any]] = None,
) -> List[SubscriptionModuleSummary]:
    runtime_config = runtime_config or {}
    query = (search or "").strip().lower()
    rows: List[SubscriptionModuleSummary] = []

    for provider in list_providers():
        enriched = enrich_provider_from_catalog(provider)
        provider_id = str(enriched.get("provider_id") or "")
        name = str(enriched.get("name") or "")
        if query and query not in provider_id.lower() and query not in name.lower():
            continue
        rows.append(_summary_from_provider(provider, runtime_config))

    for svc in osint_modules_not_in_registry():
        module_id = str(svc.get("module_id") or "")
        name = str(svc.get("name") or "")
        if query and query not in module_id.lower() and query not in name.lower():
            continue
        rows.append(_summary_from_legacy_service(svc, runtime_config))

    rows = [r for r in rows if _matches_filters(r, provider_kind=provider_kind, cli_app=cli_app, group=group)]
    rows.sort(key=lambda r: (r.group, r.module_id))
    return rows[offset : offset + limit]


def get_subscription_module(
    module_id: str,
    *,
    runtime_config: Optional[Dict[str, Any]] = None,
) -> Optional[SubscriptionModuleDetail]:
    runtime_config = runtime_config or {}
    provider = provider_by_id(module_id)
    if provider is not None:
        enriched = enrich_provider_from_catalog(provider)
        provider_id = str(enriched.get("provider_id") or module_id)
        instructions = [str(x) for x in (enriched.get("api_key_instructions") or [])]
        tier = str(enriched.get("subscription_tier") or "free_auth")
        signup = {}
        if enriched.get("spiderfeet_module_id"):
            svc = _service_for_module(str(enriched["spiderfeet_module_id"]))
            if svc is not None:
                tier = subscription_tier_for_service(svc)
                signup = signup_metadata(svc)
        return SubscriptionModuleDetail(
            module_id=provider_id,
            name=str(enriched.get("name") or provider_id),
            summary=str(enriched.get("summary") or enriched.get("signup_note") or ""),
            access_tier=str(enriched.get("access_tier") or ""),
            subscription_tier=tier,
            requires_api_key=True,
            has_api_key=_has_provider_key(enriched, runtime_config),
            website=enriched.get("website"),
            signup_url=enriched.get("signup_url") or signup.get("signup_url"),
            signup_bucket=enriched.get("signup_bucket") or signup.get("signup_bucket"),
            signup_note=enriched.get("signup_note") or signup.get("signup_note"),
            api_key_instructions=instructions,
            consumed_nuggets=[str(x) for x in (enriched.get("consumed_nuggets") or [])],
            produced_nuggets=[str(x) for x in (enriched.get("produced_nuggets") or [])],
            secret_opts=_secret_opts_masked_list(provider_id, runtime_config),
            provider_kind=str(enriched.get("kind") or "shared"),
            service_labels=service_labels_for_provider(enriched),
            cli_apps=[str(x) for x in (enriched.get("cli_apps") or [])],
            group=provider_group(enriched),
        )

    service = _service_for_module(module_id)
    if service is None or not requires_api_key(service):
        return None
    configured = _configured_modules(runtime_config)
    tier = subscription_tier_for_service(service)
    has_key = has_configured_api_key(service, configured)
    data_source = service.get("data_source") or {}
    instructions = data_source.get("api_key_instructions") or []
    if isinstance(instructions, str):
        instructions = [instructions]
    signup = signup_metadata(service)
    return SubscriptionModuleDetail(
        module_id=module_id,
        name=str(service.get("name") or ""),
        summary=str(service.get("summary") or ""),
        access_tier=str(service.get("access_tier") or ""),
        subscription_tier=tier,
        requires_api_key=True,
        has_api_key=has_key,
        website=data_source.get("website"),
        signup_url=signup.get("signup_url"),
        signup_bucket=signup.get("signup_bucket"),
        signup_note=signup.get("signup_note"),
        api_key_instructions=[str(x) for x in instructions],
        consumed_nuggets=[str(x) for x in (service.get("consumed_nuggets") or [])],
        produced_nuggets=[str(x) for x in (service.get("produced_nuggets") or [])],
        secret_opts=_secret_opts_masked_list(module_id, runtime_config),
        provider_kind="spiderfeet",
        service_labels=[f"SpiderFeet: {module_id}"],
        cli_apps=[],
        group="spiderfeet",
    )


def update_subscription_module(
    module_id: str,
    body: SubscriptionModuleUpdate,
    *,
    runtime_config: Dict[str, Any],
) -> SubscriptionModuleDetail:
    provider = provider_by_id(module_id)
    if provider is not None:
        if provider.get("kind") == "cli_only":
            allowed = set(secret_field_names(provider))
            unknown = [name for name in body.secrets if name not in allowed]
            if unknown:
                raise ValueError(f"Unsupported secret opt(s): {', '.join(sorted(unknown))}")
            if not body.secrets:
                raise ValueError("At least one secret opt is required")
            secrets = {k: "" if v is None else str(v) for k, v in body.secrets.items()}
            set_cli_provider_secrets(module_id, secrets, runtime_config)
            sync_cli_apps_for_provider(module_id, runtime_config)
            detail = get_subscription_module(module_id, runtime_config=runtime_config)
            if detail is None:
                raise RuntimeError(f"Failed to reload subscription detail for {module_id}")
            return detail

        mod_id = str(provider.get("spiderfeet_module_id") or module_id)
        allowed = set(secret_field_names(provider))
        unknown = [name for name in body.secrets if name not in allowed]
        if unknown:
            raise ValueError(f"Unsupported secret opt(s): {', '.join(sorted(unknown))}")
        if not body.secrets:
            raise ValueError("At least one secret opt is required")
        secrets = {k: "" if v is None else str(v) for k, v in body.secrets.items()}
        encrypt_and_store_module_secrets(mod_id, secrets, runtime_config)
        sync_cli_apps_for_provider(module_id, runtime_config)
        detail = get_subscription_module(module_id, runtime_config=runtime_config)
        if detail is None:
            raise RuntimeError(f"Failed to reload subscription detail for {module_id}")
        return detail

    service = _service_for_module(module_id)
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

    secrets = {k: "" if v is None else str(v) for k, v in body.secrets.items()}
    encrypt_and_store_module_secrets(module_id, secrets, runtime_config)
    detail = get_subscription_module(module_id, runtime_config=runtime_config)
    if detail is None:
        raise RuntimeError(f"Failed to reload subscription detail for {module_id}")
    return detail
