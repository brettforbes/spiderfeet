"""Load credential registry and resolve provider metadata."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from spiderfeet.map.routes_catalog import load_osint_services, service_by_module_id
from spiderfeet.map.signup_links import signup_metadata
from spiderfeet.map.subscriptions import subscription_tier_for_service

ProviderKind = Literal["spiderfeet", "cli_only", "shared"]

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / ".docs" / "analysis" / "credential_registry.json"


@lru_cache(maxsize=1)
def load_registry() -> Dict[str, Any]:
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return data


def cli_app_defaults() -> Dict[str, Any]:
    return load_registry().get("cli_apps") or {}


def list_providers() -> List[Dict[str, Any]]:
    return list(load_registry().get("providers") or [])


def provider_by_id(provider_id: str) -> Optional[Dict[str, Any]]:
    for row in list_providers():
        if row.get("provider_id") == provider_id:
            return row
    return None


def service_labels_for_provider(provider: Dict[str, Any]) -> List[str]:
    labels: List[str] = []
    mod_id = provider.get("spiderfeet_module_id")
    if mod_id:
        labels.append(f"SpiderFeet: {mod_id}")
    for app in provider.get("cli_apps") or []:
        labels.append(f"CLI: {app}")
    return labels


def provider_group(provider: Dict[str, Any]) -> str:
    kind = provider.get("kind") or "shared"
    if kind == "cli_only":
        return "cli"
    if kind == "shared":
        return "shared"
    if kind == "spiderfeet":
        return "spiderfeet"
    mod_id = provider.get("spiderfeet_module_id")
    cli_apps_list = provider.get("cli_apps") or []
    if mod_id and cli_apps_list:
        return "shared"
    if cli_apps_list:
        return "cli"
    return "spiderfeet"


def enrich_provider_from_catalog(provider: Dict[str, Any]) -> Dict[str, Any]:
    """Merge OSINT catalogue fields when provider maps to a SpiderFeet module."""
    mod_id = provider.get("spiderfeet_module_id")
    if not mod_id:
        return dict(provider)
    svc = service_by_module_id(mod_id)
    if svc is None:
        return dict(provider)
    signup = signup_metadata(svc)
    data_source = svc.get("data_source") or {}
    instructions = data_source.get("api_key_instructions") or []
    if isinstance(instructions, str):
        instructions = [instructions]
    merged = dict(provider)
    merged.setdefault("name", str(svc.get("name") or mod_id))
    merged.setdefault("subscription_tier", subscription_tier_for_service(svc))
    merged.setdefault("signup_url", signup.get("signup_url"))
    merged.setdefault("signup_bucket", signup.get("signup_bucket"))
    merged.setdefault("signup_note", signup.get("signup_note"))
    merged.setdefault("website", data_source.get("website"))
    merged.setdefault("api_key_instructions", [str(x) for x in instructions])
    merged.setdefault("summary", str(svc.get("summary") or ""))
    merged.setdefault("access_tier", str(svc.get("access_tier") or ""))
    merged.setdefault("consumed_nuggets", [str(x) for x in (svc.get("consumed_nuggets") or [])])
    merged.setdefault("produced_nuggets", [str(x) for x in (svc.get("produced_nuggets") or [])])
    merged.setdefault("fixture_category", str(svc.get("fixture_category") or "positive"))
    return merged


def secret_field_names(provider: Dict[str, Any]) -> List[str]:
    return [str(f.get("opt") or "api_key") for f in (provider.get("secret_fields") or [])]


def spiderfeet_module_ids_in_registry() -> set[str]:
    ids: set[str] = set()
    for p in list_providers():
        mid = p.get("spiderfeet_module_id")
        if mid:
            ids.add(str(mid))
    return ids


def osint_modules_not_in_registry() -> List[Dict[str, Any]]:
    """Key-required OSINT modules without explicit registry row (legacy path)."""
    reg_ids = spiderfeet_module_ids_in_registry()
    from spiderfeet.map.subscriptions import requires_api_key
    from spiderfeet.map.service_states import include_in_operator_ui

    out = []
    for svc in load_osint_services():
        if not include_in_operator_ui(svc):
            continue
        if not requires_api_key(svc):
            continue
        mid = str(svc.get("module_id") or "")
        if mid not in reg_ids:
            out.append(svc)
    return out
