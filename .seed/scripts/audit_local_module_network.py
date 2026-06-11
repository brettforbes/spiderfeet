#!/usr/bin/env python3
"""Audit local-origin modules for outbound network patterns (Stage 5 catalogue)."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO_ROOT / "modules"
OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
OUT_JSON = REPO_ROOT / ".docs" / "analysis" / "local_module_network_audit.json"


def _module_path(module_id: str) -> Path:
    return MODULES_DIR / f"{module_id}.py"


def audit_file(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    patterns = {
        "fetchUrl": "fetchUrl(" in text,
        "requests": "requests." in text or "import requests" in text,
        "dns": "dns." in text or "resolveHost" in text,
        "whois": "whois" in text.lower(),
        "subprocess": "Popen(" in text or "subprocess" in text,
        "has_dataSource_in_meta": '"dataSource"' in text or "'dataSource'" in text,
    }
    literal_urls: List[str] = []
    try:
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "fetchUrl" and node.args:
                    arg0 = node.args[0]
                    if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                        if arg0.value.startswith("http"):
                            literal_urls.append(arg0.value[:120])
    except SyntaxError:
        pass
    return {**patterns, "literal_http_urls": literal_urls[:5]}


def main() -> int:
    services = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    local_ids = [
        str(s["module_id"])
        for s in services
        if str(s.get("service_origin") or "") == "local"
    ]
    rows: List[Dict[str, Any]] = []
    for module_id in sorted(local_ids):
        path = _module_path(module_id)
        if not path.is_file():
            continue
        row = {"module_id": module_id, **audit_file(path)}
        row["recommendation"] = (
            "keep-local"
            if not row["has_dataSource_in_meta"]
            else "review-external-api"
        )
        rows.append(row)
    OUT_JSON.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    review = [r["module_id"] for r in rows if r["recommendation"] == "review-external-api"]
    print(f"audited {len(rows)} local modules; review-external-api={len(review)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
