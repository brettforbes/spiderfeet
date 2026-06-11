#!/usr/bin/env python3
"""One-off scan_ui probe for a single module (development)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.map.seed_probe import post_scan_ui  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module-id", required=True)
    parser.add_argument("--nugget-id", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--fixture-kind", default="positive")
    parser.add_argument("--local", action="store_true")
    args = parser.parse_args()

    if args.local:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "run_quarantine_battery",
            REPO_ROOT / ".seed" / "scripts" / "run_quarantine_battery.py",
        )
        battery = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(battery)
        result = battery.post_scan_ui_local(
            module_id=args.module_id,
            consumed_nugget_id=args.nugget_id,
            input_value=args.input,
            timeout_seconds=args.timeout,
            fixture_kind=args.fixture_kind,
        )
    else:
        result = post_scan_ui(
            args.api_base,
            module_id=args.module_id,
            consumed_nugget_id=args.nugget_id,
            input_value=args.input,
            timeout_seconds=args.timeout,
            fixture_kind=args.fixture_kind,
        )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
