"""Persist and read credentials (module opts + CLI-only providers)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from spiderfeet import SpiderFeetDb, SpiderFeetHelpers
from spiderfeet.credentials.registry import enrich_provider_from_catalog, provider_by_id, secret_field_names
from spiderfeet.credentials.vault import decrypt_value, encrypt_value, is_encrypted
from spiderfeet.map.subscriptions import mask_secret


def _cli_credentials_path() -> Path:
    return Path(SpiderFeetHelpers.dataPath()) / "settings" / "cli_credentials.json"


def _load_cli_credentials() -> Dict[str, Dict[str, str]]:
    path = _cli_credentials_path()
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cli_credentials(data: Dict[str, Dict[str, str]]) -> None:
    path = _cli_credentials_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _serialize_module_opt(module_id: str, opt_name: str, value: Any) -> Dict[str, Any]:
    if isinstance(value, bool):
        return {f"{module_id}:{opt_name}": 1 if value else 0}
    if isinstance(value, list):
        return {f"{module_id}:{opt_name}": ",".join(str(x) for x in value)}
    return {f"{module_id}:{opt_name}": value}


def get_cli_provider_secrets(
    provider_id: str,
    runtime_config: Dict[str, Any],
) -> Dict[str, str]:
    provider = provider_by_id(provider_id)
    if provider is None or provider.get("kind") != "cli_only":
        return {}
    blob = _load_cli_credentials().get(provider_id) or {}
    out: Dict[str, str] = {}
    for opt in secret_field_names(provider):
        raw = blob.get(opt, "")
        out[opt] = decrypt_value(str(raw or ""))
    return out


def has_cli_provider_secrets(provider_id: str, runtime_config: Dict[str, Any]) -> bool:
    secrets = get_cli_provider_secrets(provider_id, runtime_config)
    return any(str(v).strip() for v in secrets.values())


def set_cli_provider_secrets(
    provider_id: str,
    secrets: Dict[str, str],
    runtime_config: Dict[str, Any],
) -> None:
    provider = provider_by_id(provider_id)
    if provider is None or provider.get("kind") != "cli_only":
        raise LookupError(f"Unknown CLI provider: {provider_id}")
    allowed = set(secret_field_names(provider))
    unknown = [k for k in secrets if k not in allowed]
    if unknown:
        raise ValueError(f"Unsupported secret opt(s): {', '.join(sorted(unknown))}")

    data = _load_cli_credentials()
    row = data.setdefault(provider_id, {})
    for opt_name in allowed:
        value = str(secrets.get(opt_name) or "")
        row[opt_name] = encrypt_value(value) if value else ""
    _save_cli_credentials(data)


def masked_secret_opts(provider_id: str, runtime_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    provider = enrich_provider_from_catalog(provider_by_id(provider_id) or {})
    if not provider or not provider.get("provider_id"):
        from spiderfeet.map.routes_catalog import service_by_module_id
        from spiderfeet.map.subscriptions import writable_secret_opts

        svc = service_by_module_id(provider_id)
        if svc is None:
            return []
        modules = runtime_config.get("__modules__") or {}
        runtime_opts = (modules.get(provider_id) or {}).get("opts") or {}
        names = writable_secret_opts(svc, modules)
        return [
            {
                "name": name,
                "label": name,
                "masked_value": mask_secret(str(runtime_opts.get(name) or "")),
                "configured": bool(str(runtime_opts.get(name) or "").strip()),
            }
            for name in names
        ]
    if provider.get("kind") == "cli_only":
        secrets = get_cli_provider_secrets(provider_id, runtime_config)
    else:
        mod_id = str(provider.get("spiderfeet_module_id") or provider_id)
        modules = runtime_config.get("__modules__") or {}
        runtime_opts = (modules.get(mod_id) or {}).get("opts") or {}
        secrets = {opt: str(runtime_opts.get(opt) or "") for opt in secret_field_names(provider)}

    items = []
    for field in provider.get("secret_fields") or []:
        opt = str(field.get("opt") or "api_key")
        raw = secrets.get(opt, "")
        items.append(
            {
                "name": opt,
                "label": str(field.get("label") or opt),
                "masked_value": mask_secret(raw),
                "configured": bool(str(raw or "").strip()),
            }
        )
    return items


def encrypt_and_store_module_secrets(
    module_id: str,
    secrets: Dict[str, str],
    runtime_config: Dict[str, Any],
) -> None:
    modules = runtime_config.get("__modules__") or {}
    if module_id not in modules:
        raise LookupError(f"Module not loaded in runtime: {module_id}")

    store: Dict[str, Any] = {}
    module_opts = modules[module_id].setdefault("opts", {})
    for opt_name, value in secrets.items():
        stored_value = "" if value is None else str(value)
        if stored_value:
            enc = encrypt_value(stored_value)
            module_opts[opt_name] = stored_value
            store.update(_serialize_module_opt(module_id, opt_name, enc))
        else:
            module_opts[opt_name] = ""
            store.update(_serialize_module_opt(module_id, opt_name, ""))

    SpiderFeetDb(runtime_config).configSet(store)


def read_module_secret_plaintext(
    module_id: str,
    opt_name: str,
    runtime_config: Dict[str, Any],
    dbh: Optional[SpiderFeetDb] = None,
) -> str:
    modules = runtime_config.get("__modules__") or {}
    runtime_opts = (modules.get(module_id) or {}).get("opts") or {}
    if str(runtime_opts.get(opt_name) or "").strip():
        return str(runtime_opts.get(opt_name))

    db = dbh or SpiderFeetDb(runtime_config)
    raw = str(db.configGet().get(f"{module_id}:{opt_name}", "") or "")
    return decrypt_value(raw) if is_encrypted(raw) else raw


def resolve_env_value(provider: Dict[str, Any], from_opt: str, runtime_config: Dict[str, Any]) -> str:
    kind = provider.get("kind")
    provider_id = str(provider.get("provider_id") or "")
    if kind == "cli_only":
        return get_cli_provider_secrets(provider_id, runtime_config).get(from_opt, "")
    mod_id = str(provider.get("spiderfeet_module_id") or provider_id)
    return read_module_secret_plaintext(mod_id, from_opt, runtime_config)
