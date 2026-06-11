#!/usr/bin/env python3
"""Generate .docs/osint-services module reference markdown from catalogue JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.map.fixture_categories import fixture_category_for_service  # noqa: E402
from spiderfeet.map.subscriptions import subscription_tier_for_service  # noqa: E402
from spiderfeet.map.test_targets import (  # noqa: E402
    load_module_test_seeds,
    seed_coverage_complete,
    seed_upstream_blocked,
)

OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"
OUT_ROOT = REPO_ROOT / ".docs" / "osint-services"
MODULES_DIR = OUT_ROOT / "modules"
OVERVIEW = OUT_ROOT / "OVERVIEW.md"


def _test_status(module_id: str, route_seed: Optional[str]) -> str:
    if not route_seed:
        return "no-route-seed"
    if seed_coverage_complete(module_id, route_seed):
        seeds = load_module_test_seeds().get(module_id, {}).get(route_seed, {})
        if seeds.get("validated_produces"):
            return "validated-positive"
        if seeds.get("validated_negative"):
            return "validated-negative"
        return "validated"
    if seed_upstream_blocked(module_id, route_seed):
        return "upstream-blocked"
    return "not-validated"


def _tier_label(svc: Dict[str, Any]) -> str:
    tier = subscription_tier_for_service(svc)
    access = str(svc.get("access_tier") or "")
    if access:
        return f"{tier} ({access})"
    return tier


def _collection_key(svc: Dict[str, Any]) -> str:
    origin = str(svc.get("service_origin") or "")
    state = str(svc.get("service_state") or "")
    fixture = fixture_category_for_service(svc)
    if state == "error":
        return "other"
    if origin in ("external", "external-api"):
        return "positive-api" if fixture == "positive" else "negative-api"
    if origin == "cli":
        return "cli"
    if origin == "local":
        return "local"
    return "other"


def _md_list(items: List[str]) -> str:
    if not items:
        return "- (none)"
    return "\n".join(f"- `{item}`" for item in items)


def render_module(svc: Dict[str, Any]) -> str:
    module_id = str(svc["module_id"])
    route_seed = svc.get("route_seed_nugget")
    ds = svc.get("data_source") or {}
    tool = svc.get("tool_details") or {}
    lines = [
        f"# {svc.get('name') or module_id}",
        "",
        f"**Module ID:** `{module_id}`",
        "",
        "## Summary",
        "",
        str(svc.get("summary") or "").strip() or "(no summary)",
        "",
        "## Classification",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| service_origin | `{svc.get('service_origin')}` |",
        f"| service_state | `{svc.get('service_state')}` |",
        f"| fixture_category | `{fixture_category_for_service(svc)}` |",
        f"| subscription_tier | `{_tier_label(svc)}` |",
        f"| test_status (route seed) | `{_test_status(module_id, route_seed)}` |",
        "",
        "## Data source",
        "",
        f"- **Website:** {ds.get('website') or '—'}",
        f"- **Model:** `{ds.get('model') or '—'}`",
    ]
    refs = ds.get("references") or []
    if refs:
        lines.append(f"- **References:** {', '.join(str(r) for r in refs)}")
    if tool:
        lines.extend(
            [
                "",
                "## CLI / tool",
                "",
                f"- **Tool:** {tool.get('name') or '—'}",
                f"- **Website:** {tool.get('website') or '—'}",
                f"- **Repository:** {tool.get('repository') or '—'}",
            ]
        )
    lines.extend(
        [
            "",
            "## Routes",
            "",
            f"- **Route seed nugget:** `{route_seed or '—'}`",
            f"- **Consumed:**",
            _md_list(list(svc.get("consumed_nuggets") or [])),
            f"- **Produced:**",
            _md_list(list(svc.get("produced_nuggets") or [])),
            "",
            "## Flags and categories",
            "",
            f"- **Flags:** {', '.join(svc.get('flags') or []) or '—'}",
            f"- **Categories:** {', '.join(svc.get('categories') or []) or '—'}",
            f"- **Use cases:** {', '.join(svc.get('use_cases') or []) or '—'}",
        ]
    )
    opts = svc.get("module_opts") or []
    if opts:
        lines.extend(["", "## Module options", ""])
        for opt in opts:
            name = opt.get("name")
            desc = opt.get("description") or ""
            lines.append(f"- `{name}` — {desc}")
    seeds = load_module_test_seeds().get(module_id) or {}
    if seeds:
        lines.extend(["", "## Test seeds", ""])
        for nugget_id, entry in sorted(seeds.items()):
            if not isinstance(entry, dict) or not entry:
                continue
            note = entry.get("notes") or entry.get("validation") or ""
            lines.append(
                f"- `{nugget_id}`: input=`{entry.get('input_value', '')}` "
                f"validation={entry.get('validation', '—')} {note}".strip()
            )
    desc = str(ds.get("description") or "").strip()
    if desc and len(desc) > 80:
        lines.extend(["", "## Catalogue notes", "", desc])
    lines.append("")
    return "\n".join(lines)


def _overview_table(services: List[Dict[str, Any]], key: str) -> List[str]:
    rows = [s for s in services if _collection_key(s) == key]
    rows.sort(key=lambda s: str(s.get("module_id")))
    lines = [
        f"| Module | Name | Tier | State | Test |",
        f"|--------|------|------|-------|------|",
    ]
    for svc in rows:
        mid = svc["module_id"]
        lines.append(
            f"| `{mid}` | {svc.get('name', '')} | {_tier_label(svc)} | "
            f"`{svc.get('service_state')}` | "
            f"`{_test_status(mid, svc.get('route_seed_nugget'))}` |"
        )
    lines.append("")
    lines.append(f"**Count:** {len(rows)}")
    lines.append("")
    return lines


def render_overview(services: List[Dict[str, Any]]) -> str:
    lines = [
        "# OSINT services overview",
        "",
        "Operator reference for all modules in `osint_services.json`. "
        "Per-module detail: [`modules/`](modules/).",
        "",
        f"**Total services:** {len(services)}",
        "",
        "## Collections",
        "",
        "| Collection | Description |",
        "|------------|-------------|",
        "| [Positive API services](#positive-api-services) | External OSINT APIs expecting produced nuggets |",
        "| [Negative API services](#negative-api-services) | External APIs with clean-miss / reputation style fixtures |",
        "| [Local](#local) | In-process logic (DNS, extractors, WHOIS) — no declared third-party OSINT API |",
        "| [CLI tools](#cli-tools) | External CLI wrappers (`sfp_tool_*`) |",
        "| [Other](#other) | Error state or unclassified |",
        "",
        "## Positive API services",
        "",
    ]
    lines.extend(_overview_table(services, "positive-api"))
    lines.extend(["## Negative API services", ""])
    lines.extend(_overview_table(services, "negative-api"))
    lines.extend(["## Local", ""])
    lines.extend(_overview_table(services, "local"))
    lines.extend(["## CLI tools", ""])
    lines.extend(_overview_table(services, "cli"))
    lines.extend(["## Other", ""])
    lines.extend(_overview_table(services, "other"))
    lines.extend(
        [
            "## Regenerate",
            "",
            "```powershell",
            "poetry run python .seed/scripts/fix_catalogue_service_origins.py",
            "poetry run python .seed/scripts/generate_osint_service_docs.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    services = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    MODULES_DIR.mkdir(parents=True, exist_ok=True)
    for svc in services:
        module_id = str(svc["module_id"])
        path = MODULES_DIR / f"{module_id}.md"
        path.write_text(render_module(svc), encoding="utf-8")
    OVERVIEW.write_text(render_overview(services), encoding="utf-8")
    print(f"wrote {len(services)} module docs + {OVERVIEW}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
