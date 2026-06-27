#!/usr/bin/env python3
"""Sync SpiderFeet credentials into CLI app env files (delegates to credential sync engine)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.api.bootstrap import init_runtime
from spiderfeet.credentials.sync import sync_all_registered_cli_apps


def main() -> int:
    runtime = init_runtime()
    results = sync_all_registered_cli_apps(runtime.config)
    for app_id, path in results.items():
        print(f"Synced {app_id} -> {path}")
    if not results:
        print("No CLI apps with env files registered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
