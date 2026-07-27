"""Content platform bundle loader for SPEC-008 (/api/v1/content/*)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from spiderfeet.api.bootstrap import REPO_ROOT

_CONTENT_ROOT = REPO_ROOT / "modules_v2" / "content"
_TOOL_ID_RE = re.compile(r"^[a-zA-Z0-9_-]+$")

_registry_cache: dict[str, Any] | None = None
_registry_mtime: float = 0.0


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _safe_tool_id(tool_id: str) -> str:
    if not _TOOL_ID_RE.match(tool_id):
        raise ValueError(f"Invalid tool_id: {tool_id}")
    return tool_id


def _bundle_dir(tool_id: str) -> Path:
    _safe_tool_id(tool_id)
    bundle = (_CONTENT_ROOT / tool_id).resolve()
    root = _CONTENT_ROOT.resolve()
    if not str(bundle).startswith(str(root)):
        raise ValueError(f"Invalid tool path: {tool_id}")
    return bundle


def _content_root_mtime() -> float:
    if not _CONTENT_ROOT.is_dir():
        return 0.0
    mtimes = [_CONTENT_ROOT.stat().st_mtime]
    for child in _CONTENT_ROOT.iterdir():
        if child.is_dir():
            mtimes.append(child.stat().st_mtime)
            manifest = child / "manifest.json"
            if manifest.is_file():
                mtimes.append(manifest.stat().st_mtime)
    return max(mtimes)


def _load_registry() -> dict[str, dict[str, Any]]:
    global _registry_cache, _registry_mtime
    mtime = _content_root_mtime()
    if _registry_cache is not None and mtime <= _registry_mtime:
        return _registry_cache

    registry: dict[str, dict[str, Any]] = {}
    if _CONTENT_ROOT.is_dir():
        for child in sorted(_CONTENT_ROOT.iterdir()):
            if not child.is_dir():
                continue
            manifest_path = child / "manifest.json"
            if not manifest_path.is_file():
                continue
            manifest = _read_json(manifest_path)
            tool_id = manifest.get("tool_id") or child.name
            registry[tool_id] = {
                "tool_id": tool_id,
                "display_name": manifest.get("display_name", tool_id),
                "kind": manifest.get("kind", "cli"),
                "category": manifest.get("category"),
                "manifest": manifest,
                "bundle_dir": child,
            }

    _registry_cache = registry
    _registry_mtime = mtime
    return registry


def invalidate_cache() -> None:
    global _registry_cache, _registry_mtime
    _registry_cache = None
    _registry_mtime = 0.0


def list_tools(limit: int = 100, offset: int = 0) -> dict[str, Any]:
    registry = _load_registry()
    rows = [
        {
            "tool_id": entry["tool_id"],
            "display_name": entry["display_name"],
            "kind": entry["kind"],
            "category": entry.get("category"),
        }
        for entry in sorted(registry.values(), key=lambda r: r["tool_id"])
    ]
    total = len(rows)
    return {
        "tools": rows[offset : offset + limit],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_manifest(tool_id: str) -> dict[str, Any] | None:
    entry = _load_registry().get(_safe_tool_id(tool_id))
    if not entry:
        return None
    return entry["manifest"]


def get_options_markdown(tool_id: str) -> str | None:
    bundle = _bundle_dir(tool_id)
    path = bundle / "options.md"
    if not path.is_file():
        return None
    return _read_text(path)


def get_options_schema(tool_id: str) -> dict[str, Any] | None:
    bundle = _bundle_dir(tool_id)
    path = bundle / "options_schema.json"
    if not path.is_file():
        return None
    return _read_json(path)


def get_zero_to_hero_markdown(tool_id: str) -> str | None:
    bundle = _bundle_dir(tool_id)
    path = bundle / "zero_to_hero.md"
    if not path.is_file():
        return None
    return _read_text(path)


def get_graph_structure_markdown(tool_id: str) -> str | None:
    bundle = _bundle_dir(tool_id)
    path = bundle / "graph_structure.md"
    if not path.is_file():
        return None
    return _read_text(path)


def content_links_for_tool(tool_id: str) -> dict[str, str] | None:
    if tool_id not in _load_registry():
        return None
    base = f"/api/v1/content/tools/{tool_id}"
    return {
        "manifest": base,
        "options": f"{base}/options",
        "options_schema": f"{base}/options-schema",
        "zero_to_hero": f"{base}/zero-to-hero",
        "graph_structure": f"{base}/graph-structure",
    }
