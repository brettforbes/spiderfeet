"""Test nugget corpus I/O and validation helpers (Stage 4b — R2-04-02 / R2-04-07)."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from spiderfeet.map.constants import MODULE_TEST_SEEDS_JSON, REPO_ROOT
from spiderfeet.map.routes_catalog import expand_module_tests_for_service, load_osint_services
from spiderfeet.map.subscriptions import subscription_status
from spiderfeet.map.test_targets import load_module_test_seeds, sample_target_for_module

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
            validated = validation == "smoke" or bool(entry.get("validated_produces"))
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
) -> List[Dict[str, Any]]:
    """Build one validation item per module test (primary consumed nugget)."""
    configured = configured_modules or {}
    seen_modules: set[str] = set()
    items: List[Dict[str, Any]] = []

    for svc in load_osint_services():
        module_id = str(svc.get("module_id") or "")
        if not module_id:
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
        primary = tests[0]
        input_value = sample_target_for_module(
            module_id,
            primary.consumed_nugget_id,
            svc.get("route_seed_nugget"),
        )
        if not input_value:
            continue
        seen_modules.add(module_id)
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


def merge_validation_results_into_registry(
    results: Iterable[Dict[str, Any]],
    *,
    registry_path: Path | None = None,
) -> Dict[str, Any]:
    """Update module_test_seeds.json entries with validated_produces + notes."""
    path = registry_path or MODULE_TEST_SEEDS_JSON
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.setdefault("seeds", {})

    for row in results:
        module_id = row.get("module_id")
        consumed_id = row.get("consumed_nugget_id")
        if not module_id or not consumed_id:
            continue
        module_seeds = seeds.setdefault(module_id, {})
        entry = module_seeds.setdefault(consumed_id, {})
        if row.get("input_value"):
            entry["input_value"] = row["input_value"]
        if row.get("region"):
            entry["region"] = row["region"]
        elif not entry.get("region"):
            entry["region"] = "US"
        entry["validated_produces"] = bool(row.get("validated_produces"))
        if row.get("produced_count") is not None:
            entry["last_produced_count"] = int(row["produced_count"])
        status = row.get("status")
        note_bits = []
        if status:
            note_bits.append(f"status={status}")
        if row.get("notes"):
            note_bits.append(str(row["notes"]))
        if note_bits:
            entry["notes"] = "; ".join(note_bits)
        if entry.get("validated_produces"):
            entry["validation"] = "smoke"
        elif entry.get("validation") == "smoke":
            entry["validation"] = "pilot"

    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    load_module_test_seeds.cache_clear()
    return payload
