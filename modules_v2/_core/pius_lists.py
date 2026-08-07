"""Load shared Pius classification lists (08 R2)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

SHARED_RULES_DIR = Path(__file__).resolve().parents[1] / "rules" / "_shared"
PIUS_LISTS_PATH = SHARED_RULES_DIR / "pius_lists.yaml"


class PiusListError(ValueError):
    """Raised when pius_lists.yaml fails validation."""


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PiusListError(f"{path} must contain a YAML mapping")
    return data


def load_pius_lists(path: Path | None = None) -> dict[str, Any]:
    """Load and validate `pius_lists.yaml`."""
    path = path or PIUS_LISTS_PATH
    data = _load_yaml(path)
    if data.get("schema") != "pius_lists_v1":
        raise PiusListError(f"{path} requires schema pius_lists_v1")
    for key in ("registrars", "placeholders", "legal_suffix_denylist"):
        values = data.get(key)
        if not isinstance(values, list):
            raise PiusListError(f"{path} requires list `{key}`")
    return data


def is_known_registrar(value: str, lists: dict[str, Any] | None = None) -> bool:
    """08 R2 — match registrar/registry-operator names."""
    lists = lists or load_pius_lists()
    normalized = value.strip().casefold()
    for entry in lists["registrars"]:
        if normalized == str(entry).strip().casefold():
            return True
    return False


def is_placeholder_value(value: str, lists: dict[str, Any] | None = None) -> bool:
    """08 R2 — generic role/title/redaction placeholders."""
    lists = lists or load_pius_lists()
    normalized = value.strip().casefold()
    for entry in lists["placeholders"]:
        if normalized == str(entry).strip().casefold():
            return True
    return False
