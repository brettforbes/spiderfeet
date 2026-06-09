"""Positive vs negative fixture classification for OSINT modules (Stage 4c)."""

from __future__ import annotations

from typing import Any, Dict

from spiderfeet.map.test_targets import fixture_kind_for_entry, load_module_test_seeds

NEGATIVE_CATEGORIES = frozenset({
    "Reputation Systems",
    "Leaks, Dumps and Breaches",
    "Secondary Networks",
})

NEGATIVE_MODULE_IDS = frozenset({
    "sfp_psbdmp",
})


def fixture_category_for_service(service: Dict[str, Any]) -> str:
    """Return ``positive`` or ``negative`` for an osint_services.json row."""
    explicit = str(service.get("fixture_category") or "").strip().lower()
    if explicit in ("positive", "negative"):
        return explicit

    module_id = str(service.get("module_id") or "")
    seeds = load_module_test_seeds().get(module_id) or {}
    for entry in seeds.values():
        if isinstance(entry, dict) and fixture_kind_for_entry(entry) == "negative":
            return "negative"

    categories = set(service.get("categories") or [])
    if categories.intersection(NEGATIVE_CATEGORIES) or module_id in NEGATIVE_MODULE_IDS:
        return "negative"
    return "positive"
