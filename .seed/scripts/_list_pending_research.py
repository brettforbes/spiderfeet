#!/usr/bin/env python3
"""List pending seed modules with last validation outcome."""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import get_runtime
from spiderfeet.map.routes_catalog import service_by_module_id
from spiderfeet.map.test_corpus import plan_validation_items
from spiderfeet.map.test_targets import seed_coverage_complete

r = json.load(open(REPO_ROOT / ".docs/analysis/test_seed_validation_report.json"))
by_result = {x["module_id"]: x for x in r["results"]}
items = plan_validation_items(
    configured_modules=get_runtime().config.get("__modules__", {}),
    subscription_tier="none",
)
pending = [
    i
    for i in items
    if not seed_coverage_complete(i["module_id"], i["consumed_nugget_id"])
]
for p in pending:
    mid = p["module_id"]
    svc = service_by_module_id(mid) or {}
    res = by_result.get(mid, {})
    cats = ",".join(svc.get("categories") or [])
    print(
        "\t".join(
            [
                mid,
                p["consumed_nugget_id"],
                p["input_value"],
                str(res.get("status", "")),
                str(res.get("verdict", "")),
                str(res.get("produced_count", "")),
                cats,
                (svc.get("summary") or "")[:80],
            ]
        )
    )
