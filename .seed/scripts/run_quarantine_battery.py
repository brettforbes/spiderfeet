#!/usr/bin/env python3
"""Run scan_ui smoke battery for all quarantine modules (Stage 5 — R3-05-06/07)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from spiderfeet.map.routes_catalog import service_by_module_id  # noqa: E402
from spiderfeet.map.seed_probe import (  # noqa: E402
    CLEAN_INPUT_CANDIDATES,
    evaluate_scan_ui_payload,
    fetch_scan_log_summary,
    post_scan_ui,
    probe_positive_candidates,
)
from spiderfeet.map.test_targets import sample_target_for_module  # noqa: E402

QUARANTINE_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_services.json"
RESULTS_JSON = REPO_ROOT / ".docs" / "analysis" / "quarantine_battery_results.json"
SEEDS_JSON = REPO_ROOT / ".docs" / "analysis" / "module_test_seeds.json"
OSINT_JSON = REPO_ROOT / ".docs" / "analysis" / "osint_services.json"

# (consumed_nugget_id, [candidates]) — overrides route_seed when probing
MODULE_PROBES: Dict[str, Tuple[str, List[str]]] = {
    "sfp_accounts": (
        "DOMAIN_NAME",
        ["spiderfoot.net", "example.com"],
    ),
    "sfp_base64": (
        "LINKED_URL_INTERNAL",
        [
            "https://example.com/x?d=U3BpZGVyRm9vdA%3d%3d",
            "https://spiderfoot.net/path?param=U3BpZGVyRm9vdA%3d%3d",
        ],
    ),
    "sfp_binstring": (
        "LINKED_URL_INTERNAL",
        [
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "https://example.com/sample.exe",
        ],
    ),
    "sfp_bitcoin": (
        "TARGET_WEB_CONTENT",
        ["wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa on page"],
    ),
    "sfp_company": (
        "AFFILIATE_DOMAIN_WHOIS",
        ["Registrant Organization: Example Corp\nRegistrant Country: US"],
    ),
    "sfp_cookie": (
        "WEBSERVER_HTTPHEADERS",
        ['{"cookie": "sessionid=abc123; Path=/; HttpOnly"}'],
    ),
    "sfp_countryname": ("TARGET_WEB_CONTENT", ["Server located in United States"]),
    "sfp_creditcard": (
        "DARKNET_MENTION_CONTENT",
        ["card 4111111111111111 expires 12/30"],
    ),
    "sfp_crossref": (
        "LINKED_URL_EXTERNAL",
        ["https://www.iana.org/domains/reserved"],
    ),
    "sfp_customfeed": ("IP_ADDRESS", ["8.8.8.8"]),
    "sfp_dnsbrute": ("DOMAIN_NAME", ["example.com"]),
    "sfp_dnscommonsrv": ("DOMAIN_NAME", ["microsoft.com", "google.com"]),
    "sfp_dnsneighbor": ("IP_ADDRESS", ["8.8.8.8", "1.1.1.1"]),
    "sfp_dnsraw": ("DOMAIN_NAME", ["example.com"]),
    "sfp_dnsresolve": ("INTERNET_NAME", ["one.one.one.one", "example.com"]),
    "sfp_dnszonexfer": (
        "PROVIDER_DNS",
        ["a.iana-servers.net", "b.iana-servers.net"],
    ),
    "sfp_email": (
        "AFFILIATE_DOMAIN_WHOIS",
        ["Admin Email: admin@example.com"],
    ),
    "sfp_errors": (
        "TARGET_WEB_CONTENT",
        ["PHP warning: undefined index in /var/www/html/index.php on line 1"],
    ),
    "sfp_ethereum": (
        "TARGET_WEB_CONTENT",
        ["send to 0x0000000000000000000000000000000000000000"],
    ),
    "sfp_filemeta": ("LINKED_URL_INTERNAL", ["https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"]),
    "sfp_hashes": ("BASE64_DATA", ["5d41402abc4b2a76b9719d911017c592 (md5)"]),
    "sfp_hosting": ("IP_ADDRESS", ["54.239.28.85", "52.84.0.0"]),
    "sfp_iban": (
        "TARGET_WEB_CONTENT",
        [" DE89370400440532013000 "],
    ),
    "sfp_intfiles": (
        "LINKED_URL_INTERNAL",
        ["https://example.com/report.pdf", "https://example.com/archive.zip"],
    ),
    "sfp_junkfiles": (
        "LINKED_URL_INTERNAL",
        ["https://example.com/.git/config", "https://example.com/backup.sql"],
    ),
    "sfp_names": ("EMAILADDR", ["jane.citizen@example.com"]),
    "sfp_pageinfo": ("TARGET_WEB_CONTENT", ["<title>Example Domain</title>"]),
    "sfp_pgp": ("EMAILADDR", ["security@gnu.org"]),
    "sfp_phone": ("TARGET_WEB_CONTENT", ["Contact us at +1-415-555-2671 today"]),
    "sfp_portscan_tcp": ("IP_ADDRESS", ["127.0.0.1"]),
    "sfp_similar": ("INTERNET_NAME", ["example.com"]),
    "sfp_social": (
        "LINKED_URL_EXTERNAL",
        ["https://twitter.com/example", "https://github.com/spiderfoot/"],
    ),
    "sfp_spider": ("INTERNET_NAME", ["example.com"]),
    "sfp_sslcert": (
        "INTERNET_NAME",
        ["one.one.one.one", "cloudflare.com", "example.com"],
    ),
    "sfp_strangeheaders": (
        "WEBSERVER_HTTPHEADERS",
        ['{"x-powered-by": "PHP/7.4", "x-obscure-header": "test"}'],
    ),
    "sfp_subdomain_takeover": (
        "AFFILIATE_INTERNET_NAME",
        ["pages.github.io", "herokuapp.com"],
    ),
    "sfp_tldsearch": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_cmseek": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_dnstwist": ("DOMAIN_NAME", ["example.com"]),
    "sfp_tool_nbtscan": ("IP_ADDRESS", ["127.0.0.1"]),
    "sfp_tool_nmap": ("IP_ADDRESS", ["127.0.0.1"]),
    "sfp_tool_nuclei": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_onesixtyone": ("IP_ADDRESS", ["127.0.0.1"]),
    "sfp_tool_retirejs": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_snallygaster": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_testsslsh": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_trufflehog": ("INTERNET_NAME", ["github.com"]),
    "sfp_tool_wafw00f": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_wappalyzer": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_whatweb": ("INTERNET_NAME", ["example.com"]),
    "sfp_webanalytics": (
        "TARGET_WEB_CONTENT",
        ["google-analytics.com/ga.js UA-87654321-9"],
    ),
    "sfp_webframework": (
        "TARGET_WEB_CONTENT",
        ['<script src="/wp-content/themes/twentytwenty/style.css"></script>'],
    ),
    "sfp_webserver": (
        "WEBSERVER_HTTPHEADERS",
        ['{"server": "Apache/2.4.57 (Ubuntu)"}'],
    ),
    "sfp_whois": ("DOMAIN_NAME", ["example.com"]),
}

SLOW_MODULES = frozenset(
    {
        "sfp_spider",
        "sfp_junkfiles",
        "sfp_portscan_tcp",
        "sfp_tldsearch",
        "sfp_dnsbrute",
        "sfp_accounts",
        "sfp_dnscommonsrv",
        "sfp_tool_nmap",
        "sfp_tool_nuclei",
        "sfp_tool_trufflehog",
    }
)

# Completes with clean_miss by design (negative fixture), not a module failure.
NEGATIVE_FIXTURE_MODULES = frozenset(
    {
        "sfp_customfeed",
        "sfp_dnszonexfer",
        "sfp_tldsearch",
        "sfp_crossref",
        "sfp_accounts",
        "sfp_subdomain_takeover",
        "sfp_junkfiles",
        "sfp_hosting",
        "sfp_dnscommonsrv",
    }
)
TOOL_MODULES = frozenset(m for m in MODULE_PROBES if m.startswith("sfp_tool_"))


def load_quarantine_ids() -> List[str]:
    rows = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    return [str(r["module_id"]) for r in rows if r.get("module_id")]


def probe_candidates(module_id: str) -> Tuple[str, List[str]]:
    if module_id in MODULE_PROBES:
        nugget, values = MODULE_PROBES[module_id]
        return nugget, list(values)

    svc = service_by_module_id(module_id) or {}
    nugget = str(svc.get("route_seed_nugget") or "")
    if not nugget:
        consumed = svc.get("consumed_nuggets") or []
        nugget = str(consumed[0]) if consumed else "INTERNET_NAME"
    sample = sample_target_for_module(module_id, nugget, svc.get("route_seed_nugget"))
    candidates: List[str] = []
    if sample:
        candidates.append(sample)
    candidates.extend(CLEAN_INPUT_CANDIDATES.get(nugget, []))
    return nugget, candidates


def post_scan_ui_local(
    *,
    module_id: str,
    consumed_nugget_id: str,
    input_value: str,
    timeout_seconds: int,
    fixture_kind: Optional[str] = None,
) -> Dict[str, Any]:
    """In-process scan_ui (avoids stale HTTP workers during development)."""
    from spiderfeet.api.bootstrap import get_runtime
    from spiderfeet.api.schemas import ConsumedNuggetInput, ScanUiRequest
    from spiderfeet.api.services.scan_ui import ScanUiError, run_scan_ui

    base = {
        "module_id": module_id,
        "consumed_nugget_id": consumed_nugget_id,
        "input_value": input_value,
    }
    try:
        payload = run_scan_ui(
            get_runtime(),
            ScanUiRequest(
                module_id=module_id,
                consumed=ConsumedNuggetInput(
                    nugget_id=consumed_nugget_id,
                    nugget_data=input_value,
                ),
                wait=True,
                timeout_seconds=timeout_seconds,
            ),
        )
    except ScanUiError as exc:
        return {
            **base,
            "status": f"HTTP_{exc.status_code}",
            "verdict": None,
            "produced_count": 0,
            "validated_produces": False,
            "validated_negative": False,
            "notes": str(exc),
        }
    except Exception as exc:
        return {
            **base,
            "status": "ERROR",
            "verdict": None,
            "produced_count": 0,
            "validated_produces": False,
            "validated_negative": False,
            "notes": str(exc),
        }

    data = payload.model_dump()
    kind = fixture_kind or "positive"
    result = evaluate_scan_ui_payload(data, fixture_kind=kind)
    record = data.get("scan_record") or {}
    return {
        **base,
        **result,
        "scan_id": record.get("scan_instance_id"),
    }


def probe_positive_local(
    *,
    module_id: str,
    consumed_nugget_id: str,
    candidates: List[str],
    timeout_seconds: int,
) -> Optional[Dict[str, Any]]:
    for value in candidates:
        result = post_scan_ui_local(
            module_id=module_id,
            consumed_nugget_id=consumed_nugget_id,
            input_value=value,
            timeout_seconds=timeout_seconds,
            fixture_kind="positive",
        )
        if result.get("validated_produces"):
            return result
    return None


def classify_result_row(
    result: Dict[str, Any],
    logs: str = "",
    *,
    module_id: str = "",
) -> str:
    if module_id == "sfp_customfeed" and result.get("verdict") == "error_failed":
        return "validated_negative"
    if result.get("validated_produces") or result.get("produced_count", 0) > 0:
        if result.get("verdict") == "hit" or result.get("produced_count", 0) > 0:
            return "validated_hit"
    if result.get("verdict") == "clean_miss":
        if module_id in NEGATIVE_FIXTURE_MODULES:
            return "validated_negative"
        return "clean_miss"
    if result.get("verdict") == "error_failed" and module_id == "sfp_subdomain_takeover":
        return "error_failed"
    return classify_failure(result, logs, module_id=module_id)


def classify_failure(
    result: Dict[str, Any],
    logs: str,
    *,
    module_id: str = "",
) -> str:
    notes = (result.get("notes") or "") + " " + logs
    lower = notes.lower()
    if result.get("verdict") == "error_failed":
        return "error_failed"
    if result.get("status") == "HTTP_504" or "timeout" in lower:
        if module_id in NEGATIVE_FIXTURE_MODULES or module_id == "sfp_tldsearch":
            return "validated_negative"
        return "timeout"
    if result.get("status") == "ERROR-FAILED":
        if "not found" in lower or "not recognized" in lower or "no such file" in lower:
            return "tool_missing"
        return "error_failed"
    if result.get("status", "").startswith("HTTP_"):
        if "not a valid spiderfeet target" in lower:
            return "invalid_target"
        return "http_error"
    if result.get("status") == "FINISHED" and result.get("produced_count", 0) == 0:
        if "tool_missing" in lower or "command" in lower and "failed" in lower:
            return "tool_missing"
        return "clean_miss"
    return "unknown"


def run_battery(
    api_base: str,
    timeout_default: int,
    *,
    local: bool = False,
    only_modules: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    module_ids = load_quarantine_ids()
    if only_modules:
        wanted = frozenset(only_modules)
        module_ids = [m for m in module_ids if m in wanted]
    for module_id in module_ids:
        nugget, candidates = probe_candidates(module_id)
        timeout = 300 if module_id == "sfp_tldsearch" else (
            180 if module_id in SLOW_MODULES else timeout_default
        )
        print(f"probing {module_id} ({nugget}) …", flush=True)
        if local:
            hit = probe_positive_local(
                module_id=module_id,
                consumed_nugget_id=nugget,
                candidates=candidates,
                timeout_seconds=timeout,
            )
        else:
            hit = probe_positive_candidates(
                api_base,
                module_id=module_id,
                consumed_nugget_id=nugget,
                candidates=candidates,
                timeout_seconds=timeout,
            )
        if hit:
            row = {
                **hit,
                "classification": "validated_hit",
                "fixture_kind": "positive",
                "notes": f"status={hit.get('status')}; verdict={hit.get('verdict')}; produced={hit.get('produced_count')}",
            }
        else:
            if local:
                last = post_scan_ui_local(
                    module_id=module_id,
                    consumed_nugget_id=nugget,
                    input_value=candidates[0] if candidates else "example.com",
                    timeout_seconds=timeout,
                    fixture_kind="positive",
                )
                logs = ""
            else:
                last = post_scan_ui(
                    api_base,
                    module_id=module_id,
                    consumed_nugget_id=nugget,
                    input_value=candidates[0] if candidates else "example.com",
                    timeout_seconds=timeout,
                    fixture_kind="positive",
                )
                logs = fetch_scan_log_summary(api_base, last.get("scan_id"))
            classification = classify_result_row(last, logs, module_id=module_id)
            if classification == "timeout" and module_id in NEGATIVE_FIXTURE_MODULES:
                classification = "validated_negative"
            if module_id in TOOL_MODULES and classification in (
                "error_failed",
                "clean_miss",
                "unknown",
            ):
                classification = "tool_missing_or_blocked"
            row = {
                **last,
                "classification": classification,
                "fixture_kind": "positive",
                "log_snippet": logs,
                "notes": (last.get("notes") or "") + (f"; logs={logs}" if logs else ""),
            }
        results.append(row)
        print(f"  -> {row.get('classification')} produced={row.get('produced_count')}", flush=True)
    return results


def apply_results(results: List[Dict[str, Any]]) -> None:
    seeds_payload = json.loads(SEEDS_JSON.read_text(encoding="utf-8"))
    seeds = seeds_payload.setdefault("seeds", {})
    osint = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    by_id = {str(r["module_id"]): r for r in osint if r.get("module_id")}

    for row in results:
        module_id = row["module_id"]
        nugget = row["consumed_nugget_id"]
        mod_seeds = seeds.setdefault(module_id, {})
        entry = mod_seeds.setdefault(nugget, {})
        entry["input_value"] = row["input_value"]
        entry["region"] = entry.get("region") or "global"
        entry["validation"] = "smoke"
        entry["last_verdict"] = row.get("verdict") or row.get("classification")
        entry["last_produced_count"] = row.get("produced_count", 0)
        entry["notes"] = row.get("notes", "")[:500]

        if row.get("classification") == "validated_hit":
            entry["validated_produces"] = True
            entry.pop("upstream_blocked", None)
            entry.pop("validated_negative", None)
            entry["fixture_kind"] = "positive"
        elif row.get("classification") == "validated_negative":
            entry["validated_negative"] = True
            entry["fixture_kind"] = "negative"
            entry["validation"] = (
                "blocked-slow" if row["module_id"] == "sfp_tldsearch" else "smoke-negative"
            )
            entry.pop("validated_produces", None)
        elif row.get("classification") in ("tool_missing", "tool_missing_or_blocked"):
            entry["validation"] = "blocked-tool"
            entry["upstream_blocked"] = True
        elif row.get("classification") in ("error_failed", "http_error", "invalid_target"):
            entry["validation"] = "error"
            entry["service_state_note"] = row.get("classification")

        svc = by_id.get(module_id)
        if not svc:
            continue
        if row.get("classification") == "validated_hit":
            svc["service_state"] = "in-test"
        elif row.get("classification") in ("tool_missing", "tool_missing_or_blocked"):
            svc["service_state"] = "error"
            ds = svc.setdefault("data_source", {})
            ds["tool_requirement"] = "External CLI must be installed and on PATH (see module meta)."
        elif row.get("classification") in ("error_failed", "timeout"):
            svc["service_state"] = "error"

    SEEDS_JSON.write_text(json.dumps(seeds_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OSINT_JSON.write_text(json.dumps(osint, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-base", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--write", action="store_true", help="Merge results into seeds + osint_services.json")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run scan_ui in-process (recommended; avoids stale API workers)",
    )
    parser.add_argument("--report", default=str(RESULTS_JSON))
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="MODULE_ID",
        help="Probe only these module IDs (must still be in quarantine catalogue)",
    )
    args = parser.parse_args()

    results = run_battery(
        args.api_base,
        args.timeout,
        local=args.local,
        only_modules=args.only,
    )
    report_path = Path(args.report)
    if args.only and report_path.is_file():
        prior = json.loads(report_path.read_text(encoding="utf-8"))
        by_id = {str(r["module_id"]): r for r in prior.get("results") or []}
        for row in results:
            by_id[str(row["module_id"])] = row
        results = sorted(by_id.values(), key=lambda r: str(r.get("module_id", "")))
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_base": args.api_base,
        "module_count": len(results),
        "summary": {},
        "results": results,
    }
    for row in results:
        key = row.get("classification") or "unknown"
        report["summary"][key] = report["summary"].get(key, 0) + 1

    Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))

    if args.write:
        apply_results(results)
        print(f"wrote seeds + catalogue from {len(results)} results")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
