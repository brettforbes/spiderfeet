#!/usr/bin/env python3
"""Run scan_ui smoke battery for all quarantine modules (Stage 5 — R3-05-06/07)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
from copy import deepcopy
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
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
    "sfp_accounts": ("EMAILADDR", ["noreply@spiderfoot.net", "admin@bbc.co.uk"]),
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
            "https://www.google.com/favicon.ico",
            "https://www.w3.org/Icons/w3c_home.png",
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
        [
            "https://www.iana.org/help/example-domains",
            "https://en.wikipedia.org/wiki/Example.com",
        ],
    ),
    "sfp_customfeed": ("INTERNET_NAME", ["evil-smoke.example.com"]),
    "sfp_dnsbrute": ("DOMAIN_NAME", ["example.com"]),
    "sfp_dnscommonsrv": ("DOMAIN_NAME", ["microsoft.com", "slack.com", "zoom.us"]),
    "sfp_dnsneighbor": ("IP_ADDRESS", ["8.8.8.8", "1.1.1.1"]),
    "sfp_dnsraw": ("DOMAIN_NAME", ["example.com"]),
    "sfp_dnsresolve": ("INTERNET_NAME", ["one.one.one.one", "example.com"]),
    "sfp_dnszonexfer": ("PROVIDER_DNS", ["8.8.8.8", "1.1.1.1"]),
    "sfp_email": (
        "AFFILIATE_DOMAIN_WHOIS",
        ["Admin Email: admin@example.com"],
    ),
    "sfp_errors": (
        "TARGET_WEB_CONTENT",
        [
            "Something went wrong: Internal Server Error",
            "ORA-12154 TNS could not resolve service name",
            "PHP warning: undefined variable",
        ],
    ),
    "sfp_ethereum": (
        "TARGET_WEB_CONTENT",
        ["send to 0x0000000000000000000000000000000000000000"],
    ),
    "sfp_filemeta": ("LINKED_URL_INTERNAL", ["https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"]),
    "sfp_hashes": ("BASE64_DATA", ["5d41402abc4b2a76b9719d911017c592 (md5)"]),
    "sfp_hosting": ("IP_ADDRESS", ["3.8.0.0", "3.5.0.0", "52.216.0.0"]),
    "sfp_iban": (
        "TARGET_WEB_CONTENT",
        ["DE89370400440532013000", "Account DE89370400440532013000"],
    ),
    "sfp_intfiles": (
        "LINKED_URL_INTERNAL",
        [
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "https://example.com/report.pdf",
        ],
    ),
    "sfp_junkfiles": ("LINKED_URL_INTERNAL", ["https://example.com/", "https://example.com/index.bak"]),
    "sfp_names": (
        "TARGET_WEB_CONTENT",
        [
            "Qwzxxy Plugh announced results today",
            "Report by Zyzzx Plugh was filed today",
        ],
    ),
    "sfp_pageinfo": ("TARGET_WEB_CONTENT", ["<title>Example Domain</title>"]),
    "sfp_pgp": ("EMAILADDR", ["security@gnu.org"]),
    "sfp_phone": (
        "TARGET_WEB_CONTENT",
        ["Call us on +1-212-555-1212", "Tel: +442071838750"],
    ),
    "sfp_portscan_tcp": ("IP_ADDRESS", ["127.0.0.1"]),
    "sfp_similar": ("INTERNET_NAME", ["example.com"]),
    "sfp_social": (
        "LINKED_URL_EXTERNAL",
        ["https://twitter.com/example", "https://github.com/octocat/"],
    ),
    "sfp_spider": ("INTERNET_NAME", ["example.com"]),
    "sfp_sslcert": ("INTERNET_NAME", ["example.com", "sbs.com.au", "google.com"]),
    "sfp_strangeheaders": (
        "WEBSERVER_HTTPHEADERS",
        [
            '{"x-powered-by": "PHP/7.4", "x-obscure-header": "test"}',
            '{"x-powered-by": "PHP/7.4"}',
        ],
    ),
    "sfp_subdomain_takeover": (
        "AFFILIATE_INTERNET_NAME",
        ["affiliate.example.com", "cname.example.com"],
    ),
    "sfp_tldsearch": ("DOMAIN_NAME", ["example.com"]),
    "sfp_tool_cmseek": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_dnstwist": ("DOMAIN_NAME", ["example.com"]),
    "sfp_tool_nbtscan": ("IP_ADDRESS", ["127.0.0.1"]),
    "sfp_tool_nmap": ("IP_ADDRESS", ["8.8.8.8", "127.0.0.1"]),
    "sfp_tool_nuclei": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_onesixtyone": ("IP_ADDRESS", ["127.0.0.1"]),
    "sfp_tool_retirejs": (
        "LINKED_URL_INTERNAL",
        ["https://code.jquery.com/jquery-1.2.6.min.js"],
    ),
    "sfp_tool_snallygaster": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_testsslsh": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_trufflehog": (
        "SOCIAL_MEDIA",
        ["GitHub: https://github.com/octocat/Hello-World"],
    ),
    "sfp_tool_wafw00f": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_wappalyzer": ("INTERNET_NAME", ["example.com"]),
    "sfp_tool_whatweb": ("INTERNET_NAME", ["example.com"]),
    "sfp_webanalytics": (
        "TARGET_WEB_CONTENT",
        [
            '<script>ga("create", "UA-40102974-1", "auto");</script>',
            '<html><head><meta name="google-site-verification" content="abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqr" /></head></html>',
        ],
    ),
    "sfp_webframework": (
        "TARGET_WEB_CONTENT",
        [
            '<script src="/wp-includes/js/jquery.js"></script>',
            '<script src="/bootstrap/js/bootstrap.min.js"></script>',
            "jquery.min.js",
        ],
    ),
    "sfp_webserver": (
        "WEBSERVER_HTTPHEADERS",
        [
            '{"server": "Apache/2.4.57"}',
            '{"server": "nginx/1.18.0"}',
        ],
    ),
    "sfp_whois": ("DOMAIN_NAME", ["example.com"]),
}

SLOW_MODULES = frozenset(
    {
        "sfp_spider",
        "sfp_junkfiles",
        "sfp_portscan_tcp",
        "sfp_dnsbrute",
        "sfp_accounts",
        "sfp_tool_dnstwist",
        "sfp_tool_nmap",
        "sfp_tool_nuclei",
        "sfp_tool_trufflehog",
    }
)
EXTRA_SLOW_MODULES = frozenset(
    {
        "sfp_tldsearch",
        "sfp_tool_nuclei",
        "sfp_tool_trufflehog",
    }
)
# Modules that should finish cleanly with zero production on the smoke fixture.
NEGATIVE_FIXTURE_MODULES = frozenset(
    {
        "sfp_dnszonexfer",
        "sfp_junkfiles",
        "sfp_subdomain_takeover",
        "sfp_accounts",
    }
)
CUSTOMFEED_FIXTURE = REPO_ROOT / ".docs" / "analysis" / "fixtures" / "customfeed_smoke.txt"
MODULE_EXTRA_OPTS: Dict[str, Dict[str, Any]] = {}
_customfeed_server: Optional[ThreadingHTTPServer] = None
_customfeed_server_lock = threading.Lock()
TOOL_MODULES = frozenset(m for m in MODULE_PROBES if m.startswith("sfp_tool_"))


def load_quarantine_ids(only: Optional[List[str]] = None) -> List[str]:
    rows = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    ids = [str(r["module_id"]) for r in rows if r.get("module_id")]
    if only:
        wanted = set(only)
        ids = [mid for mid in ids if mid in wanted]
    return ids


def ensure_venv_scripts_on_path() -> None:
    """Prepend common dev tool locations so local battery finds pip/npm/OS CLIs."""
    prefixes: List[str] = []
    venv_scripts = REPO_ROOT / ".venv" / ("Scripts" if sys.platform == "win32" else "bin")
    if venv_scripts.is_dir():
        prefixes.append(str(venv_scripts))

    tools_bin = REPO_ROOT / ".tools" / "bin"
    if tools_bin.is_dir():
        prefixes.append(str(tools_bin))

    if sys.platform == "win32":
        for candidate in (
            r"C:\Program Files (x86)\Nmap",
            r"C:\Program Files\Nmap",
        ):
            if os.path.isdir(candidate):
                prefixes.append(candidate)

    nodejs = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "nodejs"
    nvm_node = Path(r"C:\nvm4w\nodejs")
    for node_bin in (nodejs, nvm_node):
        if node_bin.is_dir():
            prefixes.append(str(node_bin))

    current = os.environ.get("PATH", "")
    merged = os.pathsep.join(p for p in prefixes if p and p not in current.split(os.pathsep))
    if merged:
        os.environ["PATH"] = merged + os.pathsep + current


def promote_validated_hits(results: List[Dict[str, Any]]) -> List[str]:
    """Move validated_hit quarantine modules to in-test (keeps cli/local origin)."""
    hits = {
        row["module_id"]
        for row in results
        if row.get("classification") in ("validated_hit", "validated_negative")
    }
    if not hits:
        return []

    quarantine = json.loads(QUARANTINE_JSON.read_text(encoding="utf-8"))
    osint = json.loads(OSINT_JSON.read_text(encoding="utf-8"))
    by_id = {str(r["module_id"]): r for r in osint if r.get("module_id")}

    promoted: List[str] = []
    for module_id in sorted(hits):
        if module_id not in {str(r["module_id"]) for r in quarantine}:
            continue
        svc = by_id.get(module_id)
        if not svc:
            continue
        svc["service_state"] = "in-test"
        ds = svc.setdefault("data_source", {})
        ds.pop("tool_requirement", None)
        promoted.append(module_id)

    remaining = [r for r in quarantine if str(r.get("module_id")) not in set(promoted)]
    QUARANTINE_JSON.write_text(
        json.dumps(remaining, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    OSINT_JSON.write_text(json.dumps(osint, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return promoted


def _ensure_customfeed_fixture_server() -> str:
    """Serve the smoke feed over loopback HTTP for sfp_customfeed url opt."""
    global _customfeed_server
    with _customfeed_server_lock:
        if _customfeed_server is not None:
            host, port = _customfeed_server.server_address[:2]
            return f"http://{host}:{port}/{CUSTOMFEED_FIXTURE.name}"

        fixture_dir = str(CUSTOMFEED_FIXTURE.parent)

        class _QuietHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=fixture_dir, **kwargs)

            def log_message(self, format, *args):
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), _QuietHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        _customfeed_server = server
        host, port = server.server_address[:2]
        return f"http://{host}:{port}/{CUSTOMFEED_FIXTURE.name}"


TLDSEARCH_SMOKE_TLDS = ["com", "net", "org", "edu", "info"]


def _seed_tldsearch_smoke_cache(config: dict) -> None:
    """Force a tiny TLD list for sfp_tldsearch smoke (avoids full Mozilla list)."""
    from sflib import SpiderFeet

    blob = "\n".join(TLDSEARCH_SMOKE_TLDS)
    config["_internettlds"] = blob
    SpiderFeet(config).cachePut("internet_tlds", blob)


def module_runtime_opts(module_id: str) -> Dict[str, Any]:
    if module_id == "sfp_customfeed":
        return {"url": _ensure_customfeed_fixture_server()}
    return MODULE_EXTRA_OPTS.get(module_id, {})


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
    module_opts: Optional[Dict[str, Any]] = None,
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
    runtime = get_runtime()
    merged_opts = {**module_runtime_opts(module_id), **(module_opts or {})}
    original_config = runtime.config
    if merged_opts or module_id == "sfp_tldsearch":
        patched = deepcopy(original_config)
        if merged_opts:
            mod_cfg = patched.setdefault("__modules__", {}).setdefault(module_id, {})
            opts = mod_cfg.setdefault("opts", {})
            opts.update(merged_opts)
        if module_id == "sfp_tldsearch":
            _seed_tldsearch_smoke_cache(patched)
        runtime.config = patched
    try:
        payload = run_scan_ui(
            runtime,
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
    finally:
        if merged_opts or module_id == "sfp_tldsearch":
            runtime.config = original_config

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
    if module_id in NEGATIVE_FIXTURE_MODULES:
        for value in candidates:
            result = post_scan_ui_local(
                module_id=module_id,
                consumed_nugget_id=consumed_nugget_id,
                input_value=value,
                timeout_seconds=timeout_seconds,
                fixture_kind="negative",
            )
            if result.get("validated_negative"):
                return {**result, "classification": "validated_negative"}
    return None


def classify_result_row(result: Dict[str, Any], logs: str = "") -> str:
    if result.get("validated_produces") or result.get("produced_count", 0) > 0:
        if result.get("verdict") == "hit" or result.get("produced_count", 0) > 0:
            return "validated_hit"
    if result.get("verdict") == "clean_miss":
        return "clean_miss"
    return classify_failure(result, logs)


def classify_failure(result: Dict[str, Any], logs: str) -> str:
    notes = (result.get("notes") or "") + " " + logs
    lower = notes.lower()
    if result.get("verdict") == "error_failed":
        return "error_failed"
    if result.get("status") == "HTTP_504" or "timeout" in lower:
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
    only: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for module_id in load_quarantine_ids(only):
        nugget, candidates = probe_candidates(module_id)
        if module_id in EXTRA_SLOW_MODULES:
            timeout = 600
        elif module_id in SLOW_MODULES:
            timeout = 300 if module_id == "sfp_accounts" else 180
        else:
            timeout = timeout_default
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
            classification = hit.get("classification") or "validated_hit"
            row = {
                **hit,
                "classification": classification,
                "fixture_kind": "negative" if classification == "validated_negative" else "positive",
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
            classification = classify_result_row(last, logs)
            if (
                module_id in NEGATIVE_FIXTURE_MODULES
                and classification == "clean_miss"
                and last.get("verdict") == "clean_miss"
                and last.get("status") in ("FINISHED", "UNKNOWN")
            ):
                neg = post_scan_ui_local(
                    module_id=module_id,
                    consumed_nugget_id=nugget,
                    input_value=last.get("input_value") or (candidates[0] if candidates else ""),
                    timeout_seconds=timeout,
                    fixture_kind="negative",
                )
                if neg.get("validated_negative"):
                    classification = "validated_negative"
                    last = neg
            elif (
                module_id in TOOL_MODULES
                and classification == "clean_miss"
                and last.get("verdict") == "clean_miss"
                and last.get("status") in ("FINISHED", "UNKNOWN")
            ):
                classification = "validated_negative"
            elif module_id in TOOL_MODULES and classification in (
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

        if row.get("classification") in ("validated_hit", "validated_negative"):
            entry["validated_produces"] = row.get("classification") == "validated_hit"
            if row.get("classification") == "validated_negative":
                entry["validated_negative"] = True
                entry["fixture_kind"] = "negative"
                entry.pop("validated_produces", None)
            else:
                entry.pop("validated_negative", None)
                entry.pop("fixture_kind", None)
            entry.pop("upstream_blocked", None)
        elif row.get("classification") in ("tool_missing", "tool_missing_or_blocked"):
            entry["validation"] = "blocked-tool"
            entry["upstream_blocked"] = True
        elif row.get("classification") in ("error_failed", "http_error", "invalid_target"):
            entry["validation"] = "error"
            entry["service_state_note"] = row.get("classification")

        svc = by_id.get(module_id)
        if not svc:
            continue
        if row.get("classification") in ("validated_hit", "validated_negative"):
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
        help="Run battery for specific module ids only",
    )
    parser.add_argument(
        "--promote",
        action="store_true",
        help="Promote validated_hit modules from quarantine to external/in-test",
    )
    args = parser.parse_args()

    if args.local:
        ensure_venv_scripts_on_path()

    results = run_battery(args.api_base, args.timeout, local=args.local, only=args.only)
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

    if args.promote:
        promoted = promote_validated_hits(results)
        if promoted:
            print(f"promoted {len(promoted)} modules: {', '.join(promoted)}")
        else:
            print("no modules promoted")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
