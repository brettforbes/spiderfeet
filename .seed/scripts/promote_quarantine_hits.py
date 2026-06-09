#!/usr/bin/env python3
"""Promote battery-validated quarantine modules to external in-test services."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BATTERY_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_battery_results.json"
QUARANTINE_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_services.json"
OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
SEEDS_JSON = REPO_ROOT / ".docs" / "analysis" / "module_test_seeds.json"
QUARANTINE_MD = REPO_ROOT / ".docs" / "quarantine_modules.md"


def load_battery_hits() -> list[dict]:
    payload = json.loads(BATTERY_JSON.read_text(encoding="utf-8"))
    return [
        row
        for row in payload.get("results") or []
        if row.get("classification") == "validated_hit"
    ]


def patch_quarantine_markdown(promoted_ids: set[str], remaining_count: int) -> bool:
    if not QUARANTINE_MD.is_file():
        return False
    text = QUARANTINE_MD.read_text(encoding="utf-8")
    text = re.sub(
        r"\*\*Total: \d+ modules\*\* pending review\.",
        f"**Total: {remaining_count} modules** pending review.",
        text,
        count=1,
    )
    promoted_note = (
        "\n\n## Promoted to external (`in-test`)\n\n"
        "The following modules passed quarantine smoke validation and were removed "
        "from the quarantine catalogue:\n\n"
        + "\n".join(f"- `{mid}`" for mid in sorted(promoted_ids))
        + "\n"
    )
    marker = "## Promoted to external"
    if marker not in text:
        text = text.replace("---\n\n## Module Categories", promoted_note + "---\n\n## Module Categories", 1)
    lines = []
    for line in text.splitlines():
        if any(f"`{mid}`" in line for mid in promoted_ids) and line.strip().startswith("| `sfp_"):
            continue
        lines.append(line)
    QUARANTINE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def merge_seed(hits: list[dict]) -> None:
    seeds_payload = json.loads(SEEDS_JSON.read_text(encoding="utf-8"))
    seeds = seeds_payload.setdefault("seeds", {})
    for row in hits:
        module_id = row["module_id"]
        nugget = row["consumed_nugget_id"]
        mod_seeds = seeds.setdefault(module_id, {})
        entry = mod_seeds.setdefault(nugget, {})
        entry.update(
            {
                "input_value": row["input_value"],
                "region": entry.get("region") or "global",
                "validation": "smoke",
                "validated_produces": True,
                "last_verdict": row.get("verdict") or "hit",
                "last_produced_count": row.get("produced_count", 0),
                "fixture_kind": "positive",
                "notes": (row.get("notes") or "")[:500],
            }
        )
    SEEDS_JSON.write_text(
        json.dumps(seeds_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    hits = load_battery_hits()
    promoted_ids = {row["module_id"] for row in hits}
    if not promoted_ids:
        print("no validated_hit rows in battery results")
        return 1

    quarantine = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    remaining = [row for row in quarantine if row.get("module_id") not in promoted_ids]
    osint = json.loads(OSINT_JSON.read_text(encoding="utf-8"))

    for row in osint:
        mid = row.get("module_id")
        if mid not in promoted_ids:
            continue
        row["service_origin"] = "external"
        row["service_state"] = "in-test"
        row.pop("fixture_category", None)
        ds = row.setdefault("data_source", {})
        ds["description"] = re.sub(
            r"\*\*Origin:\*\* quarantine.*",
            "**Origin:** external (promoted from quarantine validation)",
            ds.get("description", ""),
            count=1,
        )

    print(f"promote {len(promoted_ids)} modules; quarantine {len(quarantine)} -> {len(remaining)}")

    if args.write:
        QUARANTINE_JSON.write_text(
            json.dumps(remaining, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        OSINT_JSON.write_text(
            json.dumps(osint, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        merge_seed(hits)
        patch_quarantine_markdown(promoted_ids, len(remaining))
        print("wrote catalogue, seeds, and quarantine_modules.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
