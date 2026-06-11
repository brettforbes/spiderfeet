#!/usr/bin/env python3
"""Normalize service_origin values in osint_services.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.map.service_classification import (  # noqa: E402
    SERVICE_ORIGIN_EXTERNAL_API,
    service_origin_for_module_id,
)

OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
LEGACY_EXTERNAL = frozenset({"external", "custom"})


def main() -> int:
    services = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    changed = 0
    for svc in services:
        module_id = str(svc.get("module_id") or "")
        ds_model = (svc.get("data_source") or {}).get("model")
        external_api = ds_model != "LOCAL_NOAUTH"
        raw = str(svc.get("service_origin") or "")
        canonical = service_origin_for_module_id(module_id, external_api=external_api)
        if raw in LEGACY_EXTERNAL and external_api:
            canonical = SERVICE_ORIGIN_EXTERNAL_API
        if svc.get("service_origin") != canonical:
            svc["service_origin"] = canonical
            changed += 1
    OSINT_JSON.write_text(json.dumps(services, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"updated service_origin on {changed} services")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
