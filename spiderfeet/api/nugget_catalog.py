"""Archetype nugget catalogue from `.docs/analysis/nuggets.json`."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
NUGGETS_JSON = REPO_ROOT / ".docs" / "analysis" / "nuggets.json"


@lru_cache(maxsize=1)
def load_nugget_archetypes() -> Dict[str, Dict[str, Any]]:
    if not NUGGETS_JSON.is_file():
        return {}
    with NUGGETS_JSON.open(encoding="utf-8") as handle:
        rows = json.load(handle)
    return {row["nugget_id"]: row for row in rows}


def archetype_for_event_type(event_type: str) -> Dict[str, Any]:
    return load_nugget_archetypes().get(event_type, {})


def entity_type_for_nugget_id(nugget_id: str) -> str:
    """TypeDB entity label (kebab-case), e.g. INTERNET_NAME -> internet-name."""
    return nugget_id.lower().replace("_", "-")


def validate_catalogue_nugget_id(nugget_id: str) -> Optional[Dict[str, Any]]:
    row = load_nugget_archetypes().get(nugget_id)
    return row
