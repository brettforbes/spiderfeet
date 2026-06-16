#!/usr/bin/env python3
"""Close per-route issues; create one stage-4 issue per OSINT module (177)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OSINT_JSON = ROOT / ".docs/analysis/osint_services.json"
MANIFEST = Path(__file__).resolve().parent / "github_issues_manifest.json"
REPO = "brettforbes/spiderFeet"
CLOSE_COMMENT = (
    "Closing: backlog consolidated to **one issue per module** (operator request). "
    "Route-level testing is tracked inside the replacement `[Module test]` issue for this module."
)
DELAY = 1.2
RATE_SLEEP = 90
PROGRESS = Path(__file__).resolve().parent / "consolidate_progress.json"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def rate_limited(text: str) -> bool:
    t = text.lower()
    return "rate limit" in t or "secondary rate" in t or "temporarily blocked" in t


def list_route_issues() -> list[int]:
    nums: list[int] = []
    page = 1
    while True:
        p = run([
            "gh", "api",
            f"repos/{REPO}/issues?state=open&labels=route-test&per_page=100&page={page}",
        ])
        if p.returncode != 0:
            raise RuntimeError(p.stderr or p.stdout)
        batch = json.loads(p.stdout)
        if not batch:
            break
        nums.extend(x["number"] for x in batch)
        if len(batch) < 100:
            break
        page += 1
    return nums


def close_issue(num: int, add_comment: bool = False) -> None:
    for attempt in range(12):
        p = run([
            "gh", "api", "-X", "PATCH", f"repos/{REPO}/issues/{num}",
            "-f", "state=closed",
        ])
        if p.returncode == 0:
            if add_comment:
                run([
                    "gh", "api", "-X", "POST", f"repos/{REPO}/issues/{num}/comments",
                    "-f", f"body={CLOSE_COMMENT}",
                ])
            return
        if rate_limited(p.stderr or p.stdout):
            time.sleep(RATE_SLEEP + attempt * 30)
            continue
        raise RuntimeError(f"close #{num}: {p.stderr or p.stdout}")
    raise RuntimeError(f"close #{num}: rate limit exhausted")


def create_module_issue(mid: str, name: str, consumed: list, produced: list, epic: int) -> int:
    c_n = len(consumed)
    p_n = len(produced)
    pairs = c_n * p_n if consumed and produced else 0
    body = f"""**Epic:** #{epic}

## Problem statement
Exercise and record all consumption→production **routes** for OSINT module `{mid}` (`{name}`) in `spiderFeet-map`.

## Scope (this issue)
- Consumed nugget types ({c_n}): {', '.join(f'`{x}`' for x in consumed) or 'none'}
- Produced nugget types ({p_n}): {', '.join(f'`{x}`' for x in produced) or 'none'}
- Route candidates to test (consumed × produced): **{pairs}**

## Acceptance criteria
- [ ] Module metadata reviewed against provider docs (API current)
- [ ] Realistic test nugget data used (AU / UK / US where applicable)
- [ ] Every viable route for this module tested via API (CLI parity where required)
- [ ] Each run creates `scan-record`; successful runs create `route` with `route-state=in-test`
- [ ] Failures annotated; if no route works, service marked `invalid` per seed doc §2.4.3
- [ ] Paid/API-only modules documented as untested with reason

## Spec binding
- SPEC-002: R2-04-03 (per module, not per route issue)

## Note
Per-route GitHub issues were closed in favour of this single module issue.
"""
    title = f"[Module test] {mid}: {name}"
    payload = json.dumps({"title": title, "body": body, "labels": ["stage-4", "module-test"]})
    for attempt in range(10):
        p = subprocess.run(
            ["gh", "api", "-X", "POST", f"repos/{REPO}/issues", "--input", "-"],
            input=payload,
            capture_output=True,
            text=True,
        )
        if p.returncode == 0:
            return int(json.loads(p.stdout)["number"])
        err = p.stderr or p.stdout
        if rate_limited(err):
            time.sleep(RATE_SLEEP + attempt * 30)
            continue
        raise RuntimeError(err)
    raise RuntimeError("create failed")


def ensure_label() -> None:
    run([
        "gh", "api", "-X", "POST", f"repos/{REPO}/labels",
        "-f", "name=module-test", "-f", "color=1D76DB",
        "-f", "description=Stage 4 — test all routes for one OSINT module",
    ])


def load_modules() -> list[dict]:
    return json.loads(OSINT_JSON.read_text(encoding="utf-8"))


def main() -> int:
    ensure_label()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"created": {}, "epics": {}, "project": None}
    epic = (
        manifest["epics"].get("spiderFeet:EPIC-SF-04-MODULES")
        or manifest["epics"].get("EPIC-SF-04-MODULES_NUM")
        or manifest["epics"].get("spiderFeet:EPIC-SF-04-ROUTES")
        or manifest["epics"].get("EPIC-SF-04-ROUTES_NUM")
        or 74
    )

    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("close", "all"):
        progress = json.loads(PROGRESS.read_text(encoding="utf-8")) if PROGRESS.exists() else {}
        closed_set = set(progress.get("closed_route_issues", []))
        nums = [n for n in list_route_issues() if n not in closed_set]
        print(f"Closing {len(nums)} route-test issues ({len(closed_set)} already done)...")
        for i, num in enumerate(nums, 1):
            close_issue(num, add_comment=False)
            closed_set.add(num)
            if i % 25 == 0:
                print(f"  closed {i}/{len(nums)}")
                PROGRESS.write_text(
                    json.dumps({"closed_route_issues": sorted(closed_set)}, indent=2),
                    encoding="utf-8",
                )
            time.sleep(DELAY)
        PROGRESS.write_text(
            json.dumps({"closed_route_issues": sorted(closed_set)}, indent=2),
            encoding="utf-8",
        )
        run([
            "gh", "api", "-X", "POST", f"repos/{REPO}/issues/74/comments",
            "-f",
            f"body={CLOSE_COMMENT} Per-route issues bulk-closed; use `[Module test]` issues instead.",
        ])
        manifest["created"] = {k: v for k, v in manifest["created"].items() if not k.startswith("RT-")}
        MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if mode in ("create", "all"):
        modules = load_modules()
        print(f"Creating {len(modules)} module-test issues...")
        for i, m in enumerate(modules, 1):
            key = f"MOD-{m['module_id']}"
            if key in manifest["created"]:
                continue
            num = create_module_issue(
                m["module_id"],
                m.get("name", m["module_id"]),
                m.get("consumed_nuggets") or [],
                m.get("produced_nuggets") or [],
                epic,
            )
            manifest["created"][key] = num
            if i % 10 == 0:
                print(f"  created {i}/{len(modules)} #{num}")
                MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            time.sleep(DELAY)
        MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Update epic title on GitHub
    run([
        "gh", "issue", "edit", str(epic), "--repo", REPO,
        "--title", "[Epic] Stage 4 — Module tests (177 OSINT modules)",
    ])
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
