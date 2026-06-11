#!/usr/bin/env python3
"""Audit quarantine route_seed_nugget vs module_test_seeds validation (Stage 5)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
QUARANTINE = REPO_ROOT / ".docs" / "analysis" / "quarantine_services.json"
SEEDS_JSON = REPO_ROOT / ".docs" / "analysis" / "module_test_seeds.json"


def route_status(mods: dict, mid: str, nugget: str | None) -> str:
    if not nugget:
        return "n/a"
    entry = mods.get(mid, {}).get(nugget, {})
    if entry.get("validated_produces"):
        return "VALID+"
    if entry.get("validated_negative"):
        return "VALID-"
    if nugget not in mods.get(mid, {}):
        return "missing"
    return str(entry.get("last_verdict", "?"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Emit machine-readable summary")
    args = parser.parse_args()

    services = json.loads(QUARANTINE.read_text(encoding="utf-8"))
    mods = json.loads(SEEDS_JSON.read_text(encoding="utf-8"))["seeds"]

    ok: list[str] = []
    fail: list[dict] = []
    for svc in services:
        mid = svc["module_id"]
        route = svc.get("route_seed_nugget")
        st = route_status(mods, mid, route)
        if st.startswith("VALID"):
            ok.append(mid)
        else:
            validated = [
                k
                for k, v in mods.get(mid, {}).items()
                if v.get("validated_produces") or v.get("validated_negative")
            ]
            fail.append(
                {
                    "module_id": mid,
                    "route_seed_nugget": route,
                    "status": st,
                    "validated_on": validated,
                    "seed_nuggets": list(mods.get(mid, {}).keys()),
                }
            )

    summary = {
        "ok_count": len(ok),
        "fail_count": len(fail),
        "ok_module_ids": sorted(ok),
        "failures": fail,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"ok={len(ok)} fail={len(fail)}")
    for row in fail:
        print(
            f"{row['module_id']}: route={row['route_seed_nugget']} st={row['status']} "
            f"validated_on={row['validated_on']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
