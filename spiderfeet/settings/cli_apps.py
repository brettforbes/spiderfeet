"""CLI application path registry (Settings)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from spiderfeet import SpiderFeetHelpers

REPO_ROOT = Path(__file__).resolve().parents[2]
from spiderfeet.credentials.registry import cli_app_defaults


def _settings_path() -> Path:
    return Path(SpiderFeetHelpers.dataPath()) / "settings" / "cli_apps.json"


def _default_registry() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for app_id, row in cli_app_defaults().items():
        out[app_id] = {
            "tool_id": app_id,
            "display_name": row.get("display_name") or app_id,
            "binary_path": row.get("default_binary_path") or "",
            "runtime": row.get("runtime") or "windows",
            "env_file": row.get("default_env_file"),
            "enabled": bool(row.get("enabled", True)),
        }
    return out


def get_cli_app_registry(runtime_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    path = _settings_path()
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data:
                merged = _default_registry()
                merged.update(data)
                return merged
        except (json.JSONDecodeError, OSError):
            pass
    return _default_registry()


def save_cli_app_registry(registry: Dict[str, Any]) -> None:
    path = _settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def validate_binary_path(binary_path: str) -> str:
    text = (binary_path or "").strip()
    if not text:
        raise ValueError("binary_path is required")
    if ".." in text.replace("\\", "/"):
        raise ValueError("binary_path must not contain ..")
    if len(text) > 512:
        raise ValueError("binary_path too long")
    return text


def validate_env_file_path(env_file: Optional[str]) -> Optional[str]:
    if not env_file:
        return None
    text = env_file.strip().replace("\\", "/")
    if ".." in text:
        raise ValueError("env_file must not contain ..")
    if not text.startswith(".tools/"):
        raise ValueError("env_file must be under .tools/")
    return text


def resolve_env_file_path(app_row: Dict[str, Any]) -> Optional[Path]:
    rel = app_row.get("env_file")
    if not rel:
        return None
    return (REPO_ROOT / str(rel).replace("\\", "/")).resolve()


def list_cli_apps(runtime_config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    reg = get_cli_app_registry(runtime_config)
    return [dict(v, tool_id=k) for k, v in sorted(reg.items())]


def update_cli_apps(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    reg = _default_registry()
    for item in items:
        tool_id = str(item.get("tool_id") or "").strip()
        if not tool_id:
            raise ValueError("tool_id is required")
        reg[tool_id] = {
            "tool_id": tool_id,
            "display_name": str(item.get("display_name") or tool_id),
            "binary_path": validate_binary_path(str(item.get("binary_path") or "")),
            "runtime": str(item.get("runtime") or "windows"),
            "env_file": validate_env_file_path(item.get("env_file")),
            "enabled": bool(item.get("enabled", True)),
        }
    save_cli_app_registry(reg)
    return list_cli_apps()
