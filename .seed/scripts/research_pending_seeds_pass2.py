#!/usr/bin/env python3
"""Pass 2: negative-fixture validation + targeted probes + upstream blocker notes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime  # noqa: E402
from spiderfeet.map.constants import MODULE_TEST_SEEDS_JSON  # noqa: E402
from spiderfeet.map.routes_catalog import service_by_module_id  # noqa: E402
from spiderfeet.map.seed_probe import (  # noqa: E402
    fetch_scan_log_summary,
    post_scan_ui,
    probe_negative_clean,
    probe_positive_candidates,
)
from spiderfeet.map.test_corpus import (  # noqa: E402
    merge_validation_results_into_registry,
    plan_validation_items,
    rows_from_seed_registry,
    summarize_registry_validation,
    write_test_corpus_csv,
)
from spiderfeet.map.test_targets import load_module_test_seeds, seed_coverage_complete  # noqa: E402

# Benign clean inputs for negative-fixture validation (expect clean_miss)
NEGATIVE_CLEAN: Dict[str, List[str]] = {
    "sfp_ahmia": ["sbs.com.au", "example.com"],
    "sfp_onionsearchengine": ["sbs.com.au", "example.com"],
    "sfp_torch": ["sbs.com.au", "example.com"],
    "sfp_reversewhois": ["example.com", "sbs.com.au"],
    "sfp_emailformat": ["example.com", "sbs.com.au"],
    "sfp_skymem": ["example.com", "sbs.com.au"],
    "sfp_grep_app": ["example.com"],
    "sfp_opennic": ["example.com"],
    "sfp_flickr": ["example.com"],
    "sfp_slideshare": ["example.com"],
    "sfp_twitter": ["example.com"],
    "sfp_callername": ["+18005551212", "+12125551234"],
}

# Expanded positive probes (pass 2)
POSITIVE_PROBE: Dict[str, List[str]] = {
    "sfp_gleif": ["Google LLC", "Microsoft Corporation", "Apple Inc."],
    "sfp_openstreetmap": [
        "1600 Amphitheatre Parkway, Mountain View, CA 94043",
        "10 Downing Street, London",
    ],
    "sfp_keybase": ["keybase", "github", "google"],
    "sfp_venmo": ["paypal", "venmo"],
    "sfp_google_tag_manager": ["google.com", "GTM-5K8Q5L"],
    "sfp_crobat_api": ["slack.com", "dropbox.com", "stripe.com"],
    "sfp_crt": ["github.com", "stackoverflow.com", "wikipedia.org"],
    "sfp_bgpview": ["91.198.174.192", "15169"],
    "sfp_mnemonic": ["google.com"],
    "sfp_threatminer": ["google.com"],
    "sfp_commoncrawl": ["example.com"],
    "sfp_digitaloceanspace": ["digitalocean.com"],
    "sfp_gravatar": ["test@example.com"],
}

# Upstream API dead — document in registry, do not expect seed validation
UPSTREAM_BLOCKED = {
    "sfp_dnsdumpster": "dnsdumpster.com removed CSRF form (2026); module needs rewrite",
    "sfp_sublist3r": "api.sublist3r.com returns empty/non-JSON body",
    "sfp_searchcode": "searchcode.com API returns HTTP 404",
    "sfp_myspace": "myspace.com search endpoint connection failures",
}


def annotate_upstream_blocked(*, write: bool) -> int:
    if not write:
        return len(UPSTREAM_BLOCKED)
    with MODULE_TEST_SEEDS_JSON.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.setdefault("seeds", {})
    for module_id, note in UPSTREAM_BLOCKED.items():
        svc = service_by_module_id(module_id) or {}
        consumed = (svc.get("consumed_nuggets") or ["DOMAIN_NAME"])[0]
        entry = seeds.setdefault(module_id, {}).setdefault(consumed, {})
        entry["upstream_blocked"] = True
        entry["notes"] = f"SPEC_GAP upstream: {note}"
        entry["validation"] = "blocked-upstream"
    with MODULE_TEST_SEEDS_JSON.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    load_module_test_seeds.cache_clear()
    return len(UPSTREAM_BLOCKED)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / ".docs/analysis/pending_seed_research_pass2.json"),
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
    pending_ids = {i["module_id"] for i in pending}

    wins: List[Dict[str, Any]] = []
    negative_wins: List[Dict[str, Any]] = []
    findings: List[Dict[str, Any]] = []

    # 1) Negative fixture validation
    for mid, candidates in NEGATIVE_CLEAN.items():
        if mid not in pending_ids:
            continue
        item = next(i for i in pending if i["module_id"] == mid)
        consumed = item["consumed_nugget_id"]
        print(f"[neg] {mid} …", flush=True)
        result = probe_negative_clean(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            candidates=candidates,
            timeout_seconds=args.timeout,
        )
        if result:
            svc = service_by_module_id(mid) or {}
            produced_types = list(svc.get("produced_nuggets") or [])
            result["fixture_kind"] = "negative"
            result["validated_negative"] = True
            result["region"] = "US"
            result["notes"] = "Benign input; expect clean_miss (negative fixture)"
            if produced_types:
                result["expected_absent_types"] = produced_types
            negative_wins.append(result)
            print(f"  NEG OK {result['input_value']!r} verdict={result.get('verdict')}", flush=True)
        else:
            last = post_scan_ui(
                args.api_base,
                module_id=mid,
                consumed_nugget_id=consumed,
                input_value=candidates[0],
                timeout_seconds=args.timeout,
                fixture_kind="negative",
            )
            findings.append({**item, **last, "phase": "negative", "outcome": "fail"})
            print(f"  NEG FAIL verdict={last.get('verdict')}", flush=True)

    # 2) Positive probes
    for mid, candidates in POSITIVE_PROBE.items():
        if mid not in pending_ids:
            continue
        item = next(i for i in pending if i["module_id"] == mid)
        consumed = item["consumed_nugget_id"]
        print(f"[pos] {mid} …", flush=True)
        result = probe_positive_candidates(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            candidates=candidates,
            timeout_seconds=args.timeout,
        )
        if result:
            result["region"] = "US"
            result["notes"] = "Pass 2 targeted probe; status=FINISHED"
            wins.append(result)
            print(f"  WIN {result['input_value']!r} produced={result['produced_count']}", flush=True)
        else:
            last = post_scan_ui(
                args.api_base,
                module_id=mid,
                consumed_nugget_id=consumed,
                input_value=candidates[0],
                timeout_seconds=args.timeout,
                fixture_kind="positive",
            )
            logs = fetch_scan_log_summary(args.api_base, last.get("scan_id"), limit=12)
            findings.append({**item, **last, "phase": "positive", "log_snippet": logs})
            print(f"  miss verdict={last.get('verdict')}", flush=True)

    blocked_count = annotate_upstream_blocked(write=args.write)

    report = {
        "positive_wins": wins,
        "negative_wins": negative_wins,
        "findings": findings,
        "upstream_blocked": UPSTREAM_BLOCKED,
    }
    out = Path(args.report)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.write:
        if wins:
            merge_validation_results_into_registry(wins)
        if negative_wins:
            merge_validation_results_into_registry(negative_wins)
        if wins or negative_wins:
            write_test_corpus_csv(rows_from_seed_registry())
            print("Updated registry")

    cumulative = summarize_registry_validation(
        configured_modules=get_runtime().config.get("__modules__", {}),
        subscription_tier="none",
    )
    summary = {
        "positive_wins": len(wins),
        "negative_wins": len(negative_wins),
        "upstream_annotated": blocked_count,
        "cumulative": cumulative,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
