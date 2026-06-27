"""AI agent API key registry (Settings)."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from spiderfeet import SpiderFeetHelpers
from spiderfeet.credentials.vault import decrypt_value, encrypt_value
from spiderfeet.map.subscriptions import mask_secret

ALLOWED_PROVIDERS = frozenset(
    {
        "openai",
        "anthropic",
        "google",
        "azure_openai",
        "ollama",
        "custom",
    }
)


def _store_path() -> Path:
    return Path(SpiderFeetHelpers.dataPath()) / "settings" / "ai_agents.json"


def _load_raw() -> List[Dict[str, Any]]:
    path = _store_path()
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return list(data) if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save_raw(rows: List[Dict[str, Any]]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def _public_row(row: Dict[str, Any]) -> Dict[str, Any]:
    enc = str(row.get("api_key_enc") or "")
    plain = decrypt_value(enc) if enc else ""
    return {
        "id": row.get("id"),
        "label": row.get("label") or "",
        "provider": row.get("provider") or "custom",
        "model": row.get("model") or "",
        "enabled": bool(row.get("enabled", True)),
        "has_api_key": bool(plain.strip()),
        "masked_api_key": mask_secret(plain),
    }


def list_ai_agents() -> List[Dict[str, Any]]:
    return [_public_row(r) for r in _load_raw()]


def create_ai_agent(body: Dict[str, Any]) -> Dict[str, Any]:
    provider = str(body.get("provider") or "custom").lower()
    if provider not in ALLOWED_PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")
    api_key = str(body.get("api_key") or "").strip()
    row = {
        "id": str(uuid.uuid4()),
        "label": str(body.get("label") or provider),
        "provider": provider,
        "model": str(body.get("model") or ""),
        "enabled": bool(body.get("enabled", True)),
        "api_key_enc": encrypt_value(api_key) if api_key else "",
    }
    rows = _load_raw()
    rows.append(row)
    _save_raw(rows)
    return _public_row(row)


def update_ai_agent(agent_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
    rows = _load_raw()
    for idx, row in enumerate(rows):
        if row.get("id") != agent_id:
            continue
        if "label" in body:
            row["label"] = str(body["label"])
        if "provider" in body:
            provider = str(body["provider"]).lower()
            if provider not in ALLOWED_PROVIDERS:
                raise ValueError(f"Unsupported provider: {provider}")
            row["provider"] = provider
        if "model" in body:
            row["model"] = str(body["model"])
        if "enabled" in body:
            row["enabled"] = bool(body["enabled"])
        if "api_key" in body:
            api_key = str(body.get("api_key") or "").strip()
            row["api_key_enc"] = encrypt_value(api_key) if api_key else ""
        rows[idx] = row
        _save_raw(rows)
        return _public_row(row)
    raise LookupError(f"Unknown agent id: {agent_id}")


def delete_ai_agent(agent_id: str) -> None:
    rows = _load_raw()
    new_rows = [r for r in rows if r.get("id") != agent_id]
    if len(new_rows) == len(rows):
        raise LookupError(f"Unknown agent id: {agent_id}")
    _save_raw(new_rows)
