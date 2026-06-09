#!/usr/bin/env python3
"""Close out remaining pending seed research: negatives, upstream blocks, long-timeout probes."""

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
from spiderfeet.map.test_targets import (  # noqa: E402
    load_module_test_seeds,
    seed_coverage_complete,
    seed_research_complete,
)

# Promote to negative fixture (benign input → clean_miss)
NEGATIVE_PROBE: Dict[str, List[str]] = {
    "sfp_keybase": ["spiderfeet", "nonexistent_keybase_user_999"],
    "sfp_crobat_api": ["example.com", "sbs.com.au"],
    "sfp_s3bucket": ["example.com", "sbs.com.au"],
}

# One-shot positive retry before marking upstream-blocked
POSITIVE_RETRY: Dict[str, List[str]] = {
    "sfp_crt": ["github.com", "wikipedia.org", "stackoverflow.com"],
}

# Annotate when probes fail or module is known broken (does not count as smoke coverage)
UPSTREAM_BLOCKED: Dict[str, str] = {
    "sfp_flickr": "Flickr API key scrape fails (Failed to obtain API key); needs API key config",
    "sfp_commoncrawl": "CommonCrawl index list HTML changed; module cannot parse latest indexes",
    "sfp_crt": "crt.sh returns errors/unavailable JSON for automated queries (rate-limit or outage)",
    "sfp_dnsdumpster": "dnsdumpster.com removed CSRF form (2026); module needs rewrite",
    "sfp_sublist3r": "api.sublist3r.com returns empty/non-JSON body",
    "sfp_searchcode": "searchcode.com API returns HTTP 404",
    "sfp_myspace": "myspace.com search endpoint connection failures",
    "sfp_s3bucket": "S3 bucket brute-force exceeds practical scan_ui timeout; defer to module-tuning issue",
}

SLOW_MODULES_TIMEOUT = 180


def annotate_upstream(*, modules: Dict[str, str], write: bool) -> List[str]:
    if not write:
        return list(modules)
    with MODULE_TEST_SEEDS_JSON.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    seeds = payload.setdefault("seeds", {})
    applied: List[str] = []
    for module_id, note in modules.items():
        svc = service_by_module_id(module_id) or {}
        consumed = (svc.get("consumed_nuggets") or ["DOMAIN_NAME"])[0]
        entry = seeds.setdefault(module_id, {}).setdefault(consumed, {})
        if entry.get("validated_produces") or entry.get("validated_negative"):
            continue
        entry["upstream_blocked"] = True
        entry["validation"] = "blocked-upstream"
        entry["notes"] = f"SPEC_GAP upstream: {note}"
        applied.append(module_id)
    with MODULE_TEST_SEEDS_JSON.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    load_module_test_seeds.cache_clear()
    return applied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--report",
        default=str(REPO_ROOT / ".docs/analysis/pending_seed_research_finalize.json"),
    )
    args = parser.parse_args()

    items = plan_validation_items(
        configured_modules=get_runtime().config.get("__modules__", {}),
        subscription_tier="none",
    )
    pending = [
        i
        for i in items
        if not seed_research_complete(i["module_id"], i["consumed_nugget_id"])
    ]
    pending_ids = {i["module_id"] for i in pending}

    negative_wins: List[Dict[str, Any]] = []
    positive_wins: List[Dict[str, Any]] = []
    findings: List[Dict[str, Any]] = []

    for mid, candidates in NEGATIVE_PROBE.items():
        if mid not in pending_ids:
            continue
        item = next(i for i in pending if i["module_id"] == mid)
        consumed = item["consumed_nugget_id"]
        timeout = SLOW_MODULES_TIMEOUT if mid == "sfp_s3bucket" else args.timeout
        print(f"[neg] {mid} (timeout={timeout}) …", flush=True)
        result = probe_negative_clean(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            candidates=candidates,
            timeout_seconds=timeout,
        )
        if result:
            svc = service_by_module_id(mid) or {}
            produced_types = list(svc.get("produced_nuggets") or [])
            result["fixture_kind"] = "negative"
            result["validated_negative"] = True
            result["region"] = "US"
            result["notes"] = "Finalize pass: benign input; expect clean_miss (negative fixture)"
            if produced_types:
                result["expected_absent_types"] = produced_types
            negative_wins.append(result)
            print(f"  NEG OK {result['input_value']!r}", flush=True)
        else:
            last = post_scan_ui(
                args.api_base,
                module_id=mid,
                consumed_nugget_id=consumed,
                input_value=candidates[0],
                timeout_seconds=timeout,
                fixture_kind="negative",
            )
            findings.append({**item, **last, "phase": "negative"})
            print(f"  NEG FAIL status={last.get('status')} verdict={last.get('verdict')}", flush=True)

    still_open = {i["module_id"] for i in pending if i["module_id"] in pending_ids}
    for mid, candidates in POSITIVE_RETRY.items():
        if mid not in still_open:
            continue
        if mid in {w["module_id"] for w in negative_wins}:
            continue
        item = next(i for i in pending if i["module_id"] == mid)
        consumed = item["consumed_nugget_id"]
        print(f"[pos-retry] {mid} …", flush=True)
        result = probe_positive_candidates(
            args.api_base,
            module_id=mid,
            consumed_nugget_id=consumed,
            candidates=candidates,
            timeout_seconds=args.timeout,
        )
        if result:
            result["region"] = "US"
            result["notes"] = "Finalize pass positive retry"
            positive_wins.append(result)
            print(f"  WIN {result['input_value']!r}", flush=True)
        else:
            last = post_scan_ui(
                args.api_base,
                module_id=mid,
                consumed_nugget_id=consumed,
                input_value=candidates[0],
                timeout_seconds=args.timeout,
            )
            logs = fetch_scan_log_summary(args.api_base, last.get("scan_id"), limit=8)
            findings.append({**item, **last, "phase": "positive_retry", "log_snippet": logs})
            print(f"  miss verdict={last.get('verdict')}", flush=True)

    to_block = {
        mid: note
        for mid, note in UPSTREAM_BLOCKED.items()
        if mid in pending_ids and mid not in {w["module_id"] for w in positive_wins + negative_wins}
    }
    blocked = annotate_upstream(modules=to_block, write=args.write)

    report = {
        "negative_wins": negative_wins,
        "positive_wins": positive_wins,
        "findings": findings,
        "upstream_blocked_applied": blocked,
    }
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.write:
        if positive_wins:
            merge_validation_results_into_registry(positive_wins)
        if negative_wins:
            merge_validation_results_into_registry(negative_wins)
        if positive_wins or negative_wins:
            write_test_corpus_csv(rows_from_seed_registry())
            print("Updated registry")

    summary = summarize_registry_validation(
        configured_modules=get_runtime().config.get("__modules__", {}),
        subscription_tier="none",
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
