#!/usr/bin/env python3
"""Sync service_state in osint_services.json and optionally TypeDB map records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.map.config import load_connection_config  # noqa: E402
from spiderfeet.map.connection import driver_session, ping  # noqa: E402
from spiderfeet.map.constants import OSINT_SERVICES_JSON  # noqa: E402
from spiderfeet.map.naming import relation_type_for_module_id  # noqa: E402
from spiderfeet.map.routes_catalog import load_osint_services  # noqa: E402
from spiderfeet.map.service_states import (  # noqa: E402
    DEFAULT_SERVICE_STATE,
    UPSTREAM_ERROR_MODULE_IDS,
    service_state_for_service,
)
from spiderfeet.map.typeql_util import literal_string, run_write  # noqa: E402


def sync_json(*, write: bool) -> int:
    with OSINT_SERVICES_JSON.open(encoding="utf-8") as handle:
        rows = json.load(handle)
    changed = 0
    for row in rows:
        module_id = str(row.get("module_id") or "")
        target = "error" if module_id in UPSTREAM_ERROR_MODULE_IDS else DEFAULT_SERVICE_STATE
        if row.get("service_state") != target:
            row["service_state"] = target
            changed += 1
    print(f"json modules={len(rows)} changed={changed}")
    if write and changed:
        with OSINT_SERVICES_JSON.open("w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        load_osint_services.cache_clear()
        print(f"wrote {OSINT_SERVICES_JSON}")
    return changed


def _typedb_update_query(module_id: str, state: str) -> str:
    rel = relation_type_for_module_id(module_id)
    mid = literal_string(module_id)
    return f"""
match
  $s isa {rel},
    has module_id {mid},
    has service_state $old;
delete
  $old of $s;
insert
  $s has service_state {literal_string(state)};
"""


def sync_typedb(*, write: bool) -> int:
    cfg = load_connection_config()
    if not ping(cfg):
        print("typedb: skipped (server not reachable)")
        return 0
    updated = 0
    with driver_session(cfg) as driver:
        for svc in load_osint_services():
            module_id = str(svc.get("module_id") or "")
            if not module_id:
                continue
            state = service_state_for_service(svc)
            if write:
                try:
                    run_write(driver, cfg.database, _typedb_update_query(module_id, state))
                    updated += 1
                except Exception as exc:
                    print(f"typedb {module_id}: {exc}")
            else:
                updated += 1
    print(f"typedb service_state updates={updated}")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--typedb", action="store_true", help="Push service_state to TypeDB")
    args = parser.parse_args()
    sync_json(write=args.write)
    if args.typedb:
        sync_typedb(write=args.write)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
