"""Test nugget corpus I/O and validation helpers (Stage 4b — R2-04-02 / R2-04-07)."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from spiderfeet.map.constants import MODULE_TEST_SEEDS_JSON, REPO_ROOT
from spiderfeet.map.routes_catalog import (
    ModuleTestDefinition,
    expand_module_tests_for_service,
    load_osint_services,
    module_test_id,
    route_name,
)
from spiderfeet.map.service_states import include_in_operator_ui
from spiderfeet.map.subscriptions import subscription_status
from spiderfeet.map.test_targets import (
    load_module_test_seeds,
    sample_target_for_module,
    seed_coverage_complete,
    seed_research_complete,
    seed_upstream_blocked,
)

TEST_NUGGET_DATA_CSV = REPO_ROOT / ".docs" / "analysis" / "test_nugget_data.csv"

CSV_COLUMNS = (
    "module_id",
    "consumed_nugget_id",
    "region",
    "input_value",
    "validated_produces",
    "notes",
)


@dataclass(frozen=True)
class CorpusRow:
    module_id: str
    consumed_nugget_id: str
    region: str
    input_value: str
    validated_produces: bool
    notes: str = ""

    def as_csv_row(self) -> Dict[str, str]:
        return {
            "module_id": self.module_id,
            "consumed_nugget_id": self.consumed_nugget_id,
            "region": self.region,
            "input_value": self.input_value,
            "validated_produces": "true" if self.validated_produces else "false",
            "notes": self.notes,
        }


def _bool_from_csv(value: str) -> bool:
    return str(value or "").strip().lower() in ("1", "true", "yes", "y")


def load_test_corpus_csv(path: Path | None = None) -> List[CorpusRow]:
    """Load module test corpus rows from CSV."""
    csv_path = path or TEST_NUGGET_DATA_CSV
    if not csv_path.is_file():
        return []
    rows: List[CorpusRow] = []
    with csv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            module_id = str(raw.get("module_id") or "").strip()
            consumed = str(raw.get("consumed_nugget_id") or "").strip()
            value = str(raw.get("input_value") or "").strip()
            if not module_id or not consumed or not value:
                continue
            rows.append(
                CorpusRow(
                    module_id=module_id,
                    consumed_nugget_id=consumed,
                    region=str(raw.get("region") or "").strip(),
                    input_value=value,
                    validated_produces=_bool_from_csv(raw.get("validated_produces", "")),
                    notes=str(raw.get("notes") or "").strip(),
                )
            )
    return rows


def write_test_corpus_csv(rows: Iterable[CorpusRow], path: Path | None = None) -> Path:
    """Write corpus rows to CSV (sorted for stable diffs)."""
    csv_path = path or TEST_NUGGET_DATA_CSV
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    sorted_rows = sorted(
        rows,
        key=lambda row: (row.module_id, row.consumed_nugget_id, row.region),
    )
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row.as_csv_row())
    return csv_path


def rows_from_seed_registry() -> List[CorpusRow]:
    """Flatten module_test_seeds.json into corpus rows."""
    rows: List[CorpusRow] = []
    for module_id, consumed_map in load_module_test_seeds().items():
        for consumed_id, entry in consumed_map.items():
            value = str(entry.get("input_value") or "").strip()
            if not value:
                continue
            validation = str(entry.get("validation") or "").strip().lower()
            kind = str(entry.get("fixture_kind") or "positive").strip().lower()
            validated = (
                validation == "smoke"
                or bool(entry.get("validated_produces"))
                or (kind == "negative" and bool(entry.get("validated_negative")))
            )
            notes = str(entry.get("notes") or "").strip()
            if validation and not notes:
                notes = f"validation={validation}"
            rows.append(
                CorpusRow(
                    module_id=module_id,
                    consumed_nugget_id=consumed_id,
                    region=str(entry.get("region") or "").strip(),
                    input_value=value,
                    validated_produces=validated,
                    notes=notes,
                )
            )
    return rows


def plan_validation_items(
    *,
    configured_modules: Optional[Dict[str, Any]] = None,
    subscription_tier: Optional[str] = None,
    module_limit: Optional[int] = None,
    module_offset: int = 0,
) -> List[Dict[str, Any]]:
    """Build one validation item per module test (primary consumed nugget)."""
    configured = configured_modules or {}
    seen_modules: set[str] = set()
    items: List[Dict[str, Any]] = []

    for svc in load_osint_services():
        module_id = str(svc.get("module_id") or "")
        if not module_id:
            continue
        if not include_in_operator_ui(svc):
            continue
        tier, _needs_key, has_key, skip = subscription_status(svc, configured)
        if skip == "missing-api-key":
            continue
        if subscription_tier and tier != subscription_tier:
            continue
        if module_id in seen_modules:
            continue
        tests = expand_module_tests_for_service(svc)
        if not tests:
            continue
        route_seed = svc.get("route_seed_nugget")
        primary = tests[0]
        if route_seed:
            matched = next(
                (t for t in tests if t.consumed_nugget_id == route_seed),
                None,
            )
            if matched:
                primary = matched
            else:
                produced = tuple(svc.get("produced_nuggets") or [])
                primary = ModuleTestDefinition(
                    test_id=module_test_id(module_id, route_seed),
                    module_id=module_id,
                    consumed_nugget_id=route_seed,
                    expected_produced_nugget_ids=produced,
                    route_names=tuple(
                        route_name(route_seed, pid, module_id) for pid in produced
                    ),
                )
        input_value = sample_target_for_module(
            module_id,
            primary.consumed_nugget_id,
            route_seed,
        )
        if not input_value:
            continue
        seen_modules.add(module_id)
        if module_offset and len(seen_modules) <= module_offset:
            continue
        items.append(
            {
                "module_id": module_id,
                "consumed_nugget_id": primary.consumed_nugget_id,
                "input_value": input_value,
                "subscription_tier": tier,
            }
        )
        if module_limit and len(items) >= module_limit:
            break
    return items


def summarize_registry_validation(
    *,
    configured_modules: Optional[Dict[str, Any]] = None,
    subscription_tier: Optional[str] = None,
) -> Dict[str, Any]:
    """Cumulative pass rate from registry vs modules eligible for validation."""
    items = plan_validation_items(
        configured_modules=configured_modules,
        subscription_tier=subscription_tier,
    )
    seeds = load_module_test_seeds()
    validated_ids: List[str] = []
    positive_ids: List[str] = []
    negative_ids: List[str] = []
    blocked_ids: List[str] = []
    pending_ids: List[str] = []
    for item in items:
        module_id = item["module_id"]
        consumed_id = item["consumed_nugget_id"]
        if seed_coverage_complete(module_id, consumed_id):
            validated_ids.append(module_id)
            entry = seeds.get(module_id, {}).get(consumed_id, {})
            if str(entry.get("fixture_kind") or "").lower() == "negative":
                negative_ids.append(module_id)
            elif entry.get("validated_produces"):
                positive_ids.append(module_id)
        elif seed_upstream_blocked(module_id, consumed_id):
            blocked_ids.append(module_id)
        else:
            pending_ids.append(module_id)
    total = len(items)
    validated = len(validated_ids)
    blocked = len(blocked_ids)
    research_closed = validated + blocked
    return {
        "total_modules": total,
        "validated_produces_count": len(positive_ids),
        "validated_negative_count": len(negative_ids),
        "coverage_count": validated,
        "rate_pct": round(100 * validated / total, 1) if total else 0.0,
        "blocked_upstream_count": blocked,
        "research_complete_count": research_closed,
        "research_complete_pct": round(100 * research_closed / total, 1) if total else 0.0,
        "actionable_pending_count": len(pending_ids),
        "validated_module_ids": sorted(set(validated_ids)),
        "positive_module_ids": sorted(set(positive_ids)),
        "negative_module_ids": sorted(set(negative_ids)),
        "blocked_upstream_module_ids": sorted(set(blocked_ids)),
        "pending_module_ids": sorted(set(pending_ids)),
    }


def merge_validation_results_into_registry(
    results: Iterable[Dict[str, Any]],
    *,
    registry_path: Path | None = None,
) -> Dict[str, Any]:
    """Update module_test_seeds.json with positive or negative smoke validation."""
    path = registry_path or MODULE_TEST_SEEDS_JSON
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.setdefault("seeds", {})

    for row in results:
        module_id = row.get("module_id")
        consumed_id = row.get("consumed_nugget_id")
        if not module_id or not consumed_id:
            continue
        target = row.get("merge_target") or "primary"
        module_seeds = seeds.setdefault(module_id, {})
        entry = module_seeds.setdefault(consumed_id, {})
        if target == "positive_hit":
            hit = entry.setdefault("positive_hit", {})
            if row.get("input_value"):
                hit["input_value"] = row["input_value"]
            hit["validated_produces"] = bool(row.get("validated_produces"))
            if row.get("produced_count") is not None:
                hit["last_produced_count"] = int(row["produced_count"])
            if row.get("notes"):
                hit["notes"] = str(row["notes"])
            continue

        if row.get("input_value"):
            entry["input_value"] = row["input_value"]
        if row.get("region"):
            entry["region"] = row["region"]
        elif not entry.get("region"):
            entry["region"] = "US"
        if row.get("fixture_kind"):
            entry["fixture_kind"] = row["fixture_kind"]

        if row.get("expected_absent_types"):
            entry["expected_absent_types"] = list(row["expected_absent_types"])
        if row.get("validated_negative"):
            entry["fixture_kind"] = "negative"
            entry["validated_negative"] = True
            entry.pop("validated_produces", None)
        elif row.get("validated_produces"):
            entry["validated_produces"] = True
            entry.pop("validated_negative", None)

        if row.get("produced_count") is not None:
            entry["last_produced_count"] = int(row["produced_count"])
        if row.get("verdict"):
            entry["last_verdict"] = str(row["verdict"])

        status = row.get("status")
        note_bits = []
        if status:
            note_bits.append(f"status={status}")
        if row.get("verdict"):
            note_bits.append(f"verdict={row['verdict']}")
        if row.get("notes"):
            note_bits.append(str(row["notes"]))
        if row.get("upstream_blocked"):
            entry["upstream_blocked"] = True
        if note_bits:
            entry["notes"] = "; ".join(note_bits)

        if entry.get("validated_produces") or entry.get("validated_negative"):
            entry["validation"] = "smoke"
        elif entry.get("validation") == "smoke":
            entry["validation"] = "pilot"

    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    load_module_test_seeds.cache_clear()
    return payload
