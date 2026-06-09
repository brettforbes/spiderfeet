#!/usr/bin/env python3
"""Per-module seed research probes for pending none-tier modules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.seed_probe import (  # noqa: E402
    fetch_scan_log_summary,
    fixture_kind_for_module,
    post_scan_ui,
    probe_positive_candidates,
)
from spiderfeet.map.test_corpus import (  # noqa: E402
    merge_validation_results_into_registry,
    plan_validation_items,
    rows_from_seed_registry,
    write_test_corpus_csv,
)
from spiderfeet.map.test_targets import seed_coverage_complete  # noqa: E402

# Module-specific candidate inputs (research pass 1)
MODULE_CANDIDATES: Dict[str, List[str]] = {
    "sfp_ahmia": ["facebookcorewwwi.onion", "google.com", "bbc.co.uk"],
    "sfp_bgpview": ["8.8.8.8", "1.1.1.1", "8.8.8.0/24", "15169"],
    "sfp_callername": ["+12125551234", "+18005551212", "+14155552671"],
    "sfp_commoncrawl": ["google.com", "bbc.co.uk", "github.com"],
    "sfp_crobat_api": ["google.com", "microsoft.com", "github.com"],
    "sfp_crt": ["google.com", "github.com", "microsoft.com", "sbs.com.au"],
    "sfp_crxcavator": ["google.com", "github.com"],
    "sfp_digitaloceanspace": ["digitalocean.com", "github.com"],
    "sfp_dnsdumpster": ["google.com", "microsoft.com", "github.com"],
    "sfp_emailformat": ["google.com", "bbc.co.uk", "microsoft.com"],
    "sfp_flickr": ["flickr.com", "yahoo.com"],
    "sfp_gleif": ["Google LLC", "Microsoft Corporation", "Apple Inc."],
    "sfp_google_tag_manager": ["GTM-5K8Q5L", "GTM-WQZ7T5", "google.com"],
    "sfp_googleobjectstorage": ["google.com", "youtube.com"],
    "sfp_gravatar": ["noreply@google.com", "test@gmail.com", "admin@bbc.co.uk"],
    "sfp_grep_app": ["google.com", "github.com"],
    "sfp_keybase": ["google", "github", "spiderfoot"],
    "sfp_mnemonic": ["8.8.8.8", "google.com", "1.1.1.1"],
    "sfp_myspace": ["test@gmail.com", "admin@yahoo.com"],
    "sfp_onionsearchengine": ["facebookcorewwwi.onion", "google.com"],
    "sfp_opennic": ["opennic.org", "wiki.opennic.org"],
    "sfp_openstreetmap": ["1600 Amphitheatre Parkway, Mountain View, CA", "London, UK"],
    "sfp_reversewhois": ["google.com", "microsoft.com"],
    "sfp_s3bucket": ["amazon.com", "github.com", "sbs.com.au"],
    "sfp_searchcode": ["google.com", "github.com"],
    "sfp_skymem": ["google.com", "bbc.co.uk"],
    "sfp_slideshare": ["slideshare.net", "linkedin.com"],
    "sfp_sublist3r": ["google.com", "microsoft.com", "github.com"],
    "sfp_threatminer": ["8.8.8.8", "google.com"],
    "sfp_torch": ["facebookcorewwwi.onion", "google.com"],
    "sfp_twitter": ["twitter.com", "x.com"],
    "sfp_venmo": ["venmo", "paypal", "google"],
}

BLOCKED_PATTERNS = (
    "CSRF",
    "error_failed",
    "JSON",
    "Bad response",
    "404",
    "403",
    "timeout",
    "504",
)


def classify_blocker(notes: str, verdict: str | None) -> str:
    text = (notes or "").lower()
    if verdict == "error_failed":
        return "module-error"
    for pat in BLOCKED_PATTERNS:
        if pat.lower() in text:
            return f"api-{pat.lower()}"
    if verdict == "clean_miss":
        return "no-output-clean-input"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / ".docs/analysis/pending_seed_research.json"),
    )
    args = parser.parse_args()

    items = plan_validation_items(
        configured_modules=get_runtime().config.get("__modules__", {}),
        subscription_tier="none",
    )
    pending = [
        i
        for i in items
        if not seed_coverage_complete(i["module_id"], i["consumed_nugget_id"])
    ]

    findings: List[Dict[str, Any]] = []
    wins: List[Dict[str, Any]] = []

    for index, item in enumerate(pending, start=1):
        mid = item["module_id"]
        consumed = item["consumed_nugget_id"]
        candidates = MODULE_CANDIDATES.get(mid, [item["input_value"]])
        ordered = list(dict.fromkeys(candidates + [item["input_value"]]))
        print(f"[{index}/{len(pending)}] {mid} …", flush=True)

        result = probe_positive_candidates(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            candidates=ordered,
            timeout_seconds=args.timeout,
        )
        if result:
            result["region"] = "US"
            result["notes"] = "Per-module research probe; status=FINISHED"
            result["validation"] = "smoke"
            wins.append(result)
            print(f"  WIN {result['input_value']!r} produced={result['produced_count']}", flush=True)
            findings.append({**item, **result, "outcome": "validated"})
            continue

        # capture best failure for research notes
        last = post_scan_ui(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            input_value=ordered[0],
            timeout_seconds=args.timeout,
            fixture_kind="positive",
        )
        logs = fetch_scan_log_summary(args.api_base, last.get("scan_id"))
        blocker = classify_blocker(logs, last.get("verdict"))
        findings.append(
            {
                **item,
                **last,
                "outcome": "blocked",
                "blocker_class": blocker,
                "log_snippet": logs[:500],
                "candidates_tried": ordered,
            }
        )
        print(f"  blocked ({blocker}) verdict={last.get('verdict')} logs={logs[:80]!r}", flush=True)

    report = {"wins": wins, "findings": findings}
    out = Path(args.report)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wins": len(wins), "blocked": len(findings) - len(wins)}, indent=2))

    md_path = REPO_ROOT / ".docs/analysis/pending_seed_research.md"
    lines = [
        "# Pending seed research (none-tier)",
        "",
        f"Generated by `research_pending_seeds.py`. Wins: **{len(wins)}** / {len(pending)}.",
        "",
        "## Validated this pass",
        "",
    ]
    if wins:
        for w in wins:
            lines.append(
                f"- `{w['module_id']}` — `{w['input_value']}` ({w['produced_count']} produced)"
            )
    else:
        lines.append("- _(none)_")
    lines.extend(["", "## Blocked / needs follow-up", ""])
    for f in findings:
        if f.get("outcome") != "blocked":
            continue
        lines.append(
            f"### {f['module_id']}\n"
            f"- **Blocker:** `{f.get('blocker_class')}`\n"
            f"- **Last:** status={f.get('status')} verdict={f.get('verdict')} "
            f"produced={f.get('produced_count')}\n"
            f"- **Tried:** {', '.join(f.get('candidates_tried') or [])}\n"
            f"- **Logs:** `{f.get('log_snippet', '')[:200]}`\n"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {md_path}")

    if args.write and wins:
        merge_validation_results_into_registry(wins)
        write_test_corpus_csv(rows_from_seed_registry())
        print("Updated registry from research wins")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
