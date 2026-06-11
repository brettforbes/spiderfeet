#!/usr/bin/env python3
"""Copy validated seed metadata onto route_seed_nugget when missing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SEEDS_JSON = REPO_ROOT / ".docs" / "analysis" / "module_test_seeds.json"
CATALOGUE = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"

_COPY_KEYS = (
    "input_value",
    "region",
    "validation",
    "validated_produces",
    "validated_negative",
    "fixture_kind",
    "last_verdict",
    "last_produced_count",
    "notes",
    "upstream_blocked",
)


def _best_source(mod_seeds: dict, route: str) -> dict | None:
    route_entry = mod_seeds.get(route) or {}
    if route_entry.get("validated_produces") or route_entry.get("validated_negative"):
        return None
    for entry in mod_seeds.values():
        if entry.get("validated_produces") or entry.get("validated_negative"):
            return entry
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    payload = json.loads(SEEDS_JSON.read_text(encoding="utf-8"))
    seeds = payload.setdefault("seeds", {})
    osint = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    mirrored: list[str] = []

    for svc in osint:
        mid = str(svc.get("module_id") or "")
        route = svc.get("route_seed_nugget")
        if not mid or not route:
            continue
        mod_seeds = seeds.setdefault(mid, {})
        source = _best_source(mod_seeds, route)
        if not source:
            continue
        target = dict(mod_seeds.get(route) or {})
        for key in _COPY_KEYS:
            if key in source and key not in target:
                target[key] = source[key]
        mod_seeds[route] = target
        mirrored.append(f"{mid}:{route}")

    print(f"mirrored={len(mirrored)}")
    for line in mirrored:
        print(line)

    if args.write:
        SEEDS_JSON.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
