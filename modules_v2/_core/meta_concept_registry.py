"""SPEC-014 shared meta-concept registry loader (modules_v2 mirror of cli_corpus)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from .paths import SHARED_RULES_DIR

_REGISTRY_PATH = SHARED_RULES_DIR / "narrative_v2.yaml"

REQUIRED_CONCEPT_KEYS = (
    "scan",
    "host",
    "system",
    "cdn",
    "org",
    "domain",
    "url",
    "service_port",
    "environment",
    "security",
    "trace",
)


class MetaConceptRegistryError(ValueError):
    """Raised when the shared narrative registry is missing or invalid."""


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise MetaConceptRegistryError(f"missing narrative registry: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise MetaConceptRegistryError(f"narrative registry must be a mapping: {path}")
    return data


@lru_cache(maxsize=1)
def load_narrative_v2(path: str | None = None) -> dict[str, Any]:
    """Load and validate the shared narrative_v2 registry."""
    registry_path = Path(path) if path else _REGISTRY_PATH
    data = _load_yaml(registry_path)
    concepts = data.get("meta_concepts")
    if not isinstance(concepts, dict) or not concepts:
        raise MetaConceptRegistryError("meta_concepts must be a non-empty mapping")

    missing = [key for key in REQUIRED_CONCEPT_KEYS if key not in concepts]
    if missing:
        raise MetaConceptRegistryError(f"meta_concepts missing required keys: {missing}")

    default_cap = int((data.get("mermaid") or {}).get("example_cap_default") or 3)
    for key, concept in concepts.items():
        if not isinstance(concept, dict):
            raise MetaConceptRegistryError(f"meta_concepts.{key} must be a mapping")
        roots = concept.get("root_nugget_ids") or []
        if not isinstance(roots, list) or not roots:
            raise MetaConceptRegistryError(f"meta_concepts.{key}.root_nugget_ids must be non-empty")
        cats = concept.get("category_nugget_ids")
        if cats is None:
            concept["category_nugget_ids"] = []
        elif not isinstance(cats, list):
            raise MetaConceptRegistryError(f"meta_concepts.{key}.category_nugget_ids must be a list")
        if "example_cap" not in concept:
            concept["example_cap"] = default_cap
        if "order" not in concept:
            concept["order"] = 100
        if "heading" not in concept:
            concept["heading"] = str(key).replace("_", " ").title()
    return data


def clear_registry_cache() -> None:
    load_narrative_v2.cache_clear()


def list_meta_concepts(*, path: str | None = None) -> list[dict[str, Any]]:
    data = load_narrative_v2(path)
    rows: list[dict[str, Any]] = []
    for concept_id, concept in (data.get("meta_concepts") or {}).items():
        row = dict(concept)
        row["id"] = concept_id
        rows.append(row)
    rows.sort(key=lambda c: (int(c.get("order", 100)), str(c.get("id", ""))))
    return rows


def get_meta_concept(concept_id: str, *, path: str | None = None) -> dict[str, Any]:
    data = load_narrative_v2(path)
    concept = (data.get("meta_concepts") or {}).get(concept_id)
    if not isinstance(concept, dict):
        raise KeyError(concept_id)
    row = dict(concept)
    row["id"] = concept_id
    return row


def mermaid_settings(*, path: str | None = None) -> dict[str, Any]:
    data = load_narrative_v2(path)
    mermaid = dict(data.get("mermaid") or {})
    mermaid.setdefault("shape_cap", 12)
    mermaid.setdefault("example_cap_default", 3)
    mermaid.setdefault("mode", "type_relation")
    return mermaid


def registry_path() -> Path:
    return _REGISTRY_PATH
