#!/usr/bin/env python3
"""Sequential strategic Nuclei exploration per nuclei_strategy skill.

Phase A (tech) -> analyze stacks -> Phase B (selective tags/paths) -> Phase C (crit/high).
Writes JSONL exports, JSON bundles (records[]), and exploration_report.json/.md.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

CORPUS_DIR = Path(__file__).resolve().parent
REPO_ROOT = CORPUS_DIR.parents[2]
if str(CORPUS_DIR) not in sys.path:
    sys.path.insert(0, str(CORPUS_DIR))

from analyze_nuclei_jsonl import CVE_RE, iter_records, summarize
from convert_nuclei_jsonl_exports import jsonl_to_bundle_path
from nuclei_structured import parse_ndjson

NUCLEI = REPO_ROOT / ".tools" / "bin" / "nuclei.exe"
TEMPLATES = REPO_ROOT / ".tools" / "nuclei-templates"
OUT_ROOT = REPO_ROOT / ".docs" / "docs-for-cli-tools" / "exploration_scratch" / "nuclei" / "strategic"
_out_root = OUT_ROOT  # overridden by --vuln-lab

COMMON = [
    "-silent",
    "-jsonl",
    "-omit-raw",
    "-omit-template",
    "-no-interactsh",
    "-etags",
    "dos,fuzz,misc",
    "-duc",
    "-retries",
    "1",
    "-c",
    "25",
    "-timeout",
    "10",
]

STACK_TAGS = frozenset(
    {
        "wordpress",
        "wp",
        "apache",
        "nginx",
        "joomla",
        "jira",
        "atlassian",
        "tomcat",
        "drupal",
        "aws",
        "cloud",
    }
)


@dataclass
class Target:
    url: str
    slug: str
    note: str = ""
    chain_hints: tuple[str, ...] = ()  # keys into HINT_BATCHES (sqli, xss, graphql, …)


# Intentional vulnerable apps — authorized test targets (2026-07 operator list).
VULN_LAB_TARGETS = [
    Target("https://vulnweb.netlify.app/", "vulnweb_netlify", "Netlify vuln demo"),
    Target("http://www.itsecgames.com/", "itsecgames", "bWAPP / ITSecGames hub"),
    Target("http://www.dvwa.co.uk/", "dvwa_co_uk", "DVWA project site"),
    Target("https://www.hackthissite.org/", "hackthissite", "Hack This Site"),
    Target("https://google-gruyere.appspot.com/", "gruyere", "Google Gruyere"),
    Target("http://testaspnet.vulnweb.com/", "testaspnet_vulnweb", "Acunetix ASP.NET test app"),
    Target("http://testasp.vulnweb.com/", "testasp_vulnweb", "Acunetix ASP test app"),
    Target(
        "https://pentest-ground.com:4280",
        "pg_dvwa",
        "Pentest-ground DVWA — CSRF/XSS/SQLi",
        ("sqli", "xss"),
    ),
    Target(
        "https://pentest-ground.com:5013",
        "pg_graphql",
        "Pentest-ground GraphQL — CMDi/XSS/SQLi",
        ("graphql", "sqli", "xss", "rce"),
    ),
    Target(
        "https://pentest-ground.com:9000",
        "pg_restflaw",
        "Pentest-ground REST API — SQLi/XXE",
        ("sqli", "ssrf"),
    ),
    Target(
        "https://pentest-ground.com:7001",
        "pg_weblogic",
        "Pentest-ground WebLogic — CVE-2023-21839",
        ("weblogic", "rce"),
    ),
    Target(
        "https://pentest-ground.com:81",
        "pg_guardianleaks",
        "Pentest-ground GuardianLeaks — XSS/SSRF",
        ("xss", "ssrf"),
    ),
    Target("http://testphp.vulnweb.com", "testphp_vulnweb", "Acunetix PHP test app (intentional vulns)", ("sqli", "xss")),
    Target("http://testhtml5.vulnweb.com", "testhtml5_vulnweb", "Acunetix HTML5 test app", ("sqli", "xss")),
    Target("http://demo.testfire.net", "testfire_demo", "Demo bank (AppScan testfire)", ("sqli",)),
]

# Skipped (not runnable app URLs): OWASP Juice Shop/WebGoat project pages, bonkersabouttech typo, Redis :6379.


@dataclass
class Batch:
    phase_id: str
    name: str
    extra_args: list[str]
    timeout_s: int = 3600
    chain_from_tech: bool = False  # only run if Phase A found matching stack tag


DEFAULT_TARGETS = [
    Target("https://scanme.sh", "scanme_sh", "Nmap lab sibling — permissive"),
    Target("https://www.k2am.com.au/", "k2am", "Smaller AU site"),
    Target("https://www.venturecapitalopportunitiesfund.com.au", "vco_fund", "Smaller AU fund site"),
    Target("https://www.squarepeg.vc/", "squarepeg", "Smaller AU VC site"),
]

# Lab + intentional test apps (authorized scanning) — widen after AU corporate sweep underwhelmed.
WIDENED_TARGETS = [
    Target("http://scanme.nmap.org", "scanme_nmap_org", "Nmap official lab — proven severity semantics"),
    Target("http://testphp.vulnweb.com", "testphp_vulnweb", "Acunetix test PHP app (intentional vulns)"),
    Target("http://testasp.vulnweb.com", "testasp_vulnweb", "Acunetix test ASP app"),
    Target("http://testhtml5.vulnweb.com", "testhtml5_vulnweb", "Acunetix HTML5 test app"),
    Target("http://demo.testfire.net", "testfire_demo", "Demo bank (AppScan testfire)"),
    Target("https://www.venturecapitalopportunitiesfund.com.au", "vco_fund", "AU Drupal 7 — best AU chain candidate"),
]

PHASE_A = Batch("phase_a_tech", "Tech fingerprint (chaining input)", ["-tags", "tech", "-severity", "info"], 1800)

PHASE_B_ALWAYS = [
    Batch("phase_b_exposure", "Exposure tag sweep", ["-tags", "exposure"], 3600),
    Batch("phase_b_misconfig", "Misconfiguration tag sweep", ["-tags", "misconfiguration"], 3600),
    Batch("phase_b_panel", "Panel/admin tag sweep", ["-tags", "panel,admin"], 3600),
    Batch(
        "phase_b_exposures_path",
        "HTTP exposures template path",
        ["-t", str(TEMPLATES / "http" / "exposures")],
        3600,
    ),
    Batch(
        "phase_b_default_logins",
        "Default logins template path",
        ["-t", str(TEMPLATES / "http" / "default-logins")],
        5400,
    ),
    Batch(
        "phase_b_cve_all",
        "All CVE templates via http/cves path (every severity)",
        ["-t", str(TEMPLATES / "http" / "cves")],
        14400,
    ),
    Batch(
        "phase_b_cves_path",
        "Full http/cves template tree (all severities)",
        ["-t", str(TEMPLATES / "http" / "cves")],
        14400,
    ),
    Batch(
        "phase_b_vulnerabilities_path",
        "HTTP vulnerabilities template tree",
        ["-t", str(TEMPLATES / "http" / "vulnerabilities")],
        7200,
    ),
    Batch(
        "phase_b_misconfig_path",
        "HTTP misconfiguration template tree",
        ["-t", str(TEMPLATES / "http" / "misconfiguration")],
        7200,
    ),
]

PHASE_B_STACK = {
    "wordpress": Batch("phase_b_wordpress", "WordPress tag", ["-tags", "wordpress"], 3600, chain_from_tech=True),
    "wp": Batch("phase_b_wordpress", "WordPress tag", ["-tags", "wordpress"], 3600, chain_from_tech=True),
    "apache": Batch("phase_b_apache", "Apache tag", ["-tags", "apache"], 3600, chain_from_tech=True),
    "nginx": Batch("phase_b_nginx", "Nginx tag", ["-tags", "nginx"], 3600, chain_from_tech=True),
    "joomla": Batch("phase_b_joomla", "Joomla tag", ["-tags", "joomla"], 3600, chain_from_tech=True),
    "drupal": Batch("phase_b_drupal", "Drupal tag", ["-tags", "drupal"], 3600, chain_from_tech=True),
    "jira": Batch("phase_b_jira", "Jira/Atlassian tag", ["-tags", "jira,atlassian"], 3600, chain_from_tech=True),
}

PHASE_C = Batch(
    "phase_c_crit_high",
    "Critical+high (all matching templates)",
    ["-severity", "critical", "-severity", "high"],
    7200,
)


def slug_from_url(url: str) -> str:
    host = urlparse(url).netloc or urlparse(url).path
    host = host.lower().removeprefix("www.")
    return re.sub(r"[^a-z0-9]+", "_", host).strip("_")


def export_path(target: Target, batch: Batch) -> Path:
    return _out_root / f"{target.slug}_{batch.phase_id}.jsonl"


def stderr_path(target: Target, batch: Batch) -> Path:
    return _out_root / f"{target.slug}_{batch.phase_id}.stderr.txt"


def build_command(target: Target, batch: Batch, export: Path) -> list[str]:
    rel_export = export.relative_to(REPO_ROOT)
    # When batch supplies -t <path>, do not also pass the full template root (breaks tag/path scans).
    if "-t" in batch.extra_args:
        template_args = list(batch.extra_args)
    else:
        template_args = ["-t", str(TEMPLATES), *batch.extra_args]
    cmd = [
        str(NUCLEI),
        "-u",
        target.url,
        *COMMON,
        *template_args,
        "-jle",
        str(rel_export).replace("\\", "/"),
    ]
    return cmd


def run_batch(target: Target, batch: Batch, skip_existing: bool) -> dict[str, Any]:
    _out_root.mkdir(parents=True, exist_ok=True)
    export = export_path(target, batch)
    stderr_file = stderr_path(target, batch)

    # Skip when a prior run finished (JSONL exists, including empty clean-miss exports).
    if skip_existing and export.is_file() and stderr_file.is_file():
        records = iter_records(export)
        return {
            "target": target.slug,
            "phase_id": batch.phase_id,
            "skipped": True,
            "record_count": len(records),
            "summary": summarize(records),
        }

    export.parent.mkdir(parents=True, exist_ok=True)
    if export.is_file():
        export.write_text("", encoding="utf-8")

    cmd_list = build_command(target, batch, export)
    cmd_str = " ".join(cmd_list)
    print(f"[strategic] {target.slug} / {batch.phase_id} ...", flush=True)
    t0 = time.monotonic()
    with stderr_file.open("w", encoding="utf-8", errors="replace") as err_f:
        proc = subprocess.run(
            cmd_list,
            cwd=REPO_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=err_f,
            timeout=batch.timeout_s,
            text=True,
        )
    duration = time.monotonic() - t0
    records = iter_records(export) if export.is_file() else []
    summary = summarize(records)

    # JSON bundle alongside JSONL
    if export.is_file():
        jsonl_to_bundle_path(export)

    result = {
        "target": target.slug,
        "url": target.url,
        "phase_id": batch.phase_id,
        "phase_name": batch.name,
        "command": cmd_str,
        "exit_code": proc.returncode,
        "duration_s": round(duration, 2),
        "record_count": len(records),
        "summary": summary,
        "export": str(export.relative_to(REPO_ROOT)).replace("\\", "/"),
        "skipped": False,
    }
    print(
        f"  -> exit={proc.returncode} records={len(records)} "
        f"sev={summary.get('severities', {})} ({duration:.0f}s)",
        flush=True,
    )
    return result


def tech_stack_tags(records: list[dict[str, Any]]) -> set[str]:
    found: set[str] = set()
    for rec in records:
        info = rec.get("info") or {}
        tags = {t.lower() for t in (info.get("tags") or [])}
        tid = str(rec.get("template-id", "")).lower()
        matcher = str(rec.get("matcher-name", "")).lower()
        extracted = " ".join(rec.get("extracted-results") or []).lower()
        found |= tags & STACK_TAGS
        for st in STACK_TAGS:
            if st in tid or st in matcher or st in extracted:
                found.add(st)
    return found


def cve_ids_in_records(records: list[dict[str, Any]]) -> list[str]:
    ids: set[str] = set()
    for rec in records:
        blob = json.dumps(rec)
        ids.update(CVE_RE.findall(blob))
        classification = (rec.get("info") or {}).get("classification") or {}
        cve_id = classification.get("cve-id")
        if isinstance(cve_id, list):
            ids.update(str(c) for c in cve_id)
        elif cve_id:
            ids.add(str(cve_id))
    return sorted(ids)


def score_target(results: list[dict[str, Any]]) -> dict[str, Any]:
    if results and results[0].get("preflight_ok") is False and len(results) == 1:
        return {
            "total_records": 0,
            "severities": {},
            "types": {},
            "cve_ids": [],
            "crit_high_count": 0,
            "medium_count": 0,
            "phases_with_hits": [],
            "signal_score": 0,
            "unreachable": True,
        }
    total = sum(r.get("record_count", 0) for r in results)
    sev: Counter[str] = Counter()
    types: Counter[str] = Counter()
    cves: set[str] = set()
    phases_with_hits: list[str] = []

    for r in results:
        if r.get("record_count", 0) > 0:
            phases_with_hits.append(r["phase_id"])
        for k, v in (r.get("summary") or {}).get("severities", {}).items():
            sev[k] += v
        for k, v in (r.get("summary") or {}).get("types", {}).items():
            types[k] += v
        export = r.get("export")
        if export:
            path = REPO_ROOT / export
            if path.is_file():
                cves.update(cve_ids_in_records(iter_records(path)))

    crit_high = sev.get("critical", 0) + sev.get("high", 0)
    medium = sev.get("medium", 0)
    signal_score = crit_high * 10 + medium * 3 + sev.get("low", 0) + sev.get("info", 0) * 0.1

    return {
        "total_records": total,
        "severities": dict(sev),
        "types": dict(types),
        "cve_ids": sorted(cves),
        "crit_high_count": crit_high,
        "medium_count": medium,
        "phases_with_hits": phases_with_hits,
        "signal_score": round(signal_score, 1),
    }


def write_report(target_results: dict[str, list[dict[str, Any]]], path_json: Path, path_md: Path) -> None:
    scores = {slug: score_target(res) for slug, res in target_results.items()}
    ranked = sorted(scores.items(), key=lambda x: x[1]["signal_score"], reverse=True)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "strategy_skill": ".cursor/skills/nuclei_strategy/SKILL.md",
        "output_dir": str(_out_root.relative_to(REPO_ROOT)).replace("\\", "/"),
        "target_scores": scores,
        "ranking": [{"slug": s, **scores[s]} for s, _ in ranked],
        "batches": target_results,
    }
    path_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Nuclei Strategic Exploration Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Target ranking (signal score)",
        "",
        "| Rank | Target | Score | Records | Critical+High | Medium | CVEs |",
        "|------|--------|-------|---------|---------------|--------|------|",
    ]
    for i, (slug, sc) in enumerate(ranked, 1):
        lines.append(
            f"| {i} | `{slug}` | {sc['signal_score']} | {sc['total_records']} | "
            f"{sc['crit_high_count']} | {sc['medium_count']} | {len(sc['cve_ids'])} |"
        )

    lines.extend(["", "## Per-target detail", ""])
    for slug, res in target_results.items():
        sc = scores[slug]
        lines.append(f"### `{slug}`")
        lines.append(f"- Severities: `{sc['severities']}`")
        if sc["cve_ids"]:
            lines.append(f"- CVE IDs: {', '.join(sc['cve_ids'][:20])}")
        lines.append(f"- Phases with hits: {', '.join(sc['phases_with_hits']) or '(none)'}")
        lines.append("")
        for r in res:
            if r.get("preflight_ok") is False and "phase_id" not in r:
                lines.append(f"- **preflight**: FAIL — `{r.get('preflight_reason', '')}`")
                continue
            if r.get("skipped") and r.get("phase_id") == "preflight":
                lines.append(f"- **preflight**: unreachable — `{r.get('preflight_reason', '')}`")
                continue
            if r.get("skipped"):
                tag = "skipped"
            else:
                tag = f"{r.get('record_count', 0)} hits"
            pid = r.get("phase_id", "unknown")
            lines.append(f"- **{pid}**: {tag} — severities `{r.get('summary', {}).get('severities', {})}`")
        lines.append("")

    best = ranked[0] if ranked else None
    if best and best[1]["crit_high_count"] > 0:
        lines.append("## Recommendation")
        lines.append(f"Promote **`{best[0]}`** batches with critical/high/CVE hits into formal examination scenarios.")
    elif best and best[1]["medium_count"] > 0:
        lines.append("## Recommendation")
        lines.append(
            f"**`{best[0]}`** shows medium-tier signal — harvest selective phases (not full-template) for examination corpus."
        )
    else:
        lines.append("## Recommendation")
        lines.append("No critical/high/medium richness on these four targets — widen target set or add stack-specific repos (e.g. Wordfence CVE).")

    path_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


CVE_BATCHES = [
    b for b in PHASE_B_ALWAYS if b.phase_id in ("phase_b_cve_all", "phase_b_cves_path")
]

# High-signal widen profile (skip noisy full-tree corporate sweeps).
WIDEN_BATCHES = [
    PHASE_A,
    Batch("phase_b_exposure", "Exposure tag sweep", ["-tags", "exposure"], 3600),
    Batch("phase_b_vulnerabilities_path", "HTTP vulnerabilities path", ["-t", str(TEMPLATES / "http" / "vulnerabilities")], 7200),
    Batch("phase_b_cves_path", "Full http/cves path", ["-t", str(TEMPLATES / "http" / "cves")], 14400),
    Batch("phase_b_misconfig_path", "HTTP misconfiguration path", ["-t", str(TEMPLATES / "http" / "misconfiguration")], 7200),
    PHASE_C,
]

HINT_BATCHES: dict[str, Batch] = {
    "graphql": Batch("phase_hint_graphql", "GraphQL templates", ["-tags", "graphql"], 3600),
    "weblogic": Batch("phase_hint_weblogic", "WebLogic + CVE templates", ["-tags", "weblogic,cve"], 5400),
    "sqli": Batch("phase_hint_sqli", "SQLi tag sweep", ["-tags", "sqli"], 5400),
    "xss": Batch("phase_hint_xss", "XSS tag sweep", ["-tags", "xss"], 3600),
    "ssrf": Batch("phase_hint_ssrf", "SSRF tag sweep", ["-tags", "ssrf"], 3600),
    "rce": Batch("phase_hint_rce", "RCE tag sweep", ["-tags", "rce"], 5400),
}

# Vuln-lab profile: tech → core vuln paths → hint chains → stack chains → crit/high.
VULN_LAB_CORE = [
    PHASE_A,
    Batch("phase_b_exposure", "Exposure tag sweep", ["-tags", "exposure"], 3600),
    Batch(
        "phase_b_vulnerabilities_path",
        "HTTP vulnerabilities path",
        ["-t", str(TEMPLATES / "http" / "vulnerabilities")],
        7200,
    ),
    Batch(
        "phase_b_cves_path",
        "Full http/cves path",
        ["-t", str(TEMPLATES / "http" / "cves")],
        10800,
    ),
    Batch(
        "phase_b_misconfig_path",
        "HTTP misconfiguration path",
        ["-t", str(TEMPLATES / "http" / "misconfiguration")],
        5400,
    ),
    Batch(
        "phase_b_default_logins",
        "Default logins path",
        ["-t", str(TEMPLATES / "http" / "default-logins")],
        5400,
    ),
    Batch(
        "phase_b_network",
        "Network detection templates",
        ["-t", str(TEMPLATES / "network")],
        3600,
    ),
    PHASE_C,
]


def preflight_http(url: str, timeout_s: int = 20) -> tuple[bool, str]:
    """Quick reachability check before burning template timeouts."""
    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "SpiderFeet-nuclei-preflight/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as exc:
        # 4xx/5xx still means host is reachable
        if exc.code in (401, 403, 404, 500, 502, 503):
            return True, f"HTTP {exc.code}"
        return False, str(exc)
    except Exception as exc:
        return False, str(exc)


def explore_vuln_lab_target(target: Target, skip_existing: bool) -> list[dict[str, Any]]:
    ok, reason = preflight_http(target.url)
    if not ok:
        print(f"  [skip] preflight failed: {reason}", flush=True)
        return [
            {
                "target": target.slug,
                "url": target.url,
                "phase_id": "preflight",
                "phase_name": "HTTP preflight",
                "record_count": 0,
                "summary": {"severities": {}},
                "skipped": True,
                "preflight_ok": False,
                "preflight_reason": reason,
            }
        ]
    print(f"  [preflight] OK ({reason})", flush=True)

    results: list[dict[str, Any]] = []
    stacks: set[str] = set()
    seen_phase: set[str] = set()

    for batch in VULN_LAB_CORE:
        if batch.phase_id == PHASE_A.phase_id:
            ra = run_batch(target, batch, skip_existing)
            results.append(ra)
            stacks = tech_stack_tags(iter_records(export_path(target, PHASE_A)))
            if stacks:
                print(f"  [chain] {target.slug} tech stacks: {sorted(stacks)}", flush=True)
            seen_phase.add(batch.phase_id)
            continue
        if batch.phase_id not in seen_phase:
            seen_phase.add(batch.phase_id)
            results.append(run_batch(target, batch, skip_existing))

    for hint in target.chain_hints:
        batch = HINT_BATCHES.get(hint)
        if batch and batch.phase_id not in seen_phase:
            seen_phase.add(batch.phase_id)
            print(f"  [hint] {target.slug} -> {hint}", flush=True)
            results.append(run_batch(target, batch, skip_existing))

    for tag in sorted(stacks):
        batch = PHASE_B_STACK.get(tag)
        if batch and batch.phase_id not in seen_phase:
            seen_phase.add(batch.phase_id)
            results.append(run_batch(target, batch, skip_existing))

    return results


def explore_widen_target(target: Target, skip_existing: bool) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    phase_a_export = export_path(target, PHASE_A)
    stacks: set[str] = set()

    for batch in WIDEN_BATCHES:
        if batch.phase_id == PHASE_A.phase_id:
            ra = run_batch(target, batch, skip_existing)
            results.append(ra)
            stacks = tech_stack_tags(iter_records(export_path(target, PHASE_A)))
            if stacks:
                print(f"  [chain] {target.slug} tech stacks: {sorted(stacks)}", flush=True)
            continue
        results.append(run_batch(target, batch, skip_existing))

    seen_phase: set[str] = set()
    for tag in sorted(stacks):
        batch = PHASE_B_STACK.get(tag)
        if batch and batch.phase_id not in seen_phase:
            seen_phase.add(batch.phase_id)
            results.append(run_batch(target, batch, skip_existing))

    return results


def explore_target(target: Target, skip_existing: bool, cve_only: bool = False) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    if cve_only:
        # Reuse Phase A for stack chaining if export already exists
        phase_a_export = export_path(target, PHASE_A)
        stacks: set[str] = set()
        if phase_a_export.is_file():
            stacks = tech_stack_tags(iter_records(phase_a_export))
            if stacks:
                print(f"  [chain] {target.slug} tech stacks: {sorted(stacks)}", flush=True)
        seen_phase: set[str] = set()
        for tag in sorted(stacks):
            batch = PHASE_B_STACK.get(tag)
            if batch and batch.phase_id not in seen_phase:
                seen_phase.add(batch.phase_id)
                results.append(run_batch(target, batch, skip_existing))
        for batch in CVE_BATCHES:
            results.append(run_batch(target, batch, skip_existing))
        results.append(run_batch(target, PHASE_C, skip_existing))
        return results

    # Phase A
    ra = run_batch(target, PHASE_A, skip_existing)
    results.append(ra)

    stacks = tech_stack_tags(iter_records(export_path(target, PHASE_A)) if export_path(target, PHASE_A).is_file() else [])
    if stacks:
        print(f"  [chain] {target.slug} tech stacks: {sorted(stacks)}", flush=True)

    # Phase B — stack-conditional (dedupe by phase_id)
    seen_phase: set[str] = set()
    for tag in sorted(stacks):
        batch = PHASE_B_STACK.get(tag)
        if batch and batch.phase_id not in seen_phase:
            seen_phase.add(batch.phase_id)
            results.append(run_batch(target, batch, skip_existing))

    # Phase B — always
    for batch in PHASE_B_ALWAYS:
        results.append(run_batch(target, batch, skip_existing))

    # Phase C
    results.append(run_batch(target, PHASE_C, skip_existing))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Strategic nuclei exploration (nuclei_strategy skill)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip batches with non-empty JSONL export")
    parser.add_argument("--target", action="append", dest="targets", metavar="SLUG", help="Only run these target slugs")
    parser.add_argument("--phase-a-only", action="store_true", help="Run only Phase A tech fingerprint on all targets")
    parser.add_argument(
        "--cve-only",
        action="store_true",
        help="Run full CVE coverage (cve tag + http/cves path + stack chain + crit/high) on all targets",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-run batches even when JSONL export exists (use with --cve-only)",
    )
    parser.add_argument(
        "--widen",
        action="store_true",
        help="Run widen profile on lab/vuln-test targets (see WIDENED_TARGETS)",
    )
    parser.add_argument(
        "--vuln-lab",
        action="store_true",
        help="Run vuln-lab profile on VULN_LAB_TARGETS (preflight + hint chains)",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Only run HTTP preflight on selected targets; no nuclei scans",
    )
    args = parser.parse_args()

    global _out_root
    if args.vuln_lab:
        _out_root = OUT_ROOT / "vuln_lab"

    if not NUCLEI.is_file() and not args.preflight_only:
        print(f"Missing nuclei binary: {NUCLEI}", file=sys.stderr)
        return 1
    if not TEMPLATES.is_dir():
        print(f"Missing templates: {TEMPLATES}", file=sys.stderr)
        return 1

    pool = {t.slug: t for t in DEFAULT_TARGETS + WIDENED_TARGETS + VULN_LAB_TARGETS}
    if args.vuln_lab:
        targets = VULN_LAB_TARGETS
    elif args.widen:
        targets = WIDENED_TARGETS
    else:
        targets = DEFAULT_TARGETS

    if args.targets:
        wanted = set(args.targets)
        targets = [pool[s] for s in wanted if s in pool]
        if not targets:
            print(f"No matching targets in {wanted}", file=sys.stderr)
            return 1

    _out_root.mkdir(parents=True, exist_ok=True)
    all_results: dict[str, list[dict[str, Any]]] = {}

    if args.preflight_only:
        print("Preflight reachability:\n")
        for target in targets:
            ok, reason = preflight_http(target.url)
            status = "OK" if ok else "FAIL"
            print(f"  [{status}] {target.slug:24} {target.url} — {reason}")
            all_results[target.slug] = [
                {"target": target.slug, "preflight_ok": ok, "preflight_reason": reason}
            ]
        write_report(
            all_results,
            _out_root / "preflight_report.json",
            _out_root / "preflight_report.md",
        )
        return 0

    skip = args.skip_existing and not args.force
    report_stem = (
        "exploration_report_vuln_lab"
        if args.vuln_lab
        else ("exploration_report_widen" if args.widen else "exploration_report")
    )

    for target in targets:
        print(f"\n=== Target: {target.url} ({target.slug}) ===", flush=True)
        if args.vuln_lab:
            all_results[target.slug] = explore_vuln_lab_target(target, skip)
        elif args.widen:
            all_results[target.slug] = explore_widen_target(target, skip)
        elif args.phase_a_only:
            all_results[target.slug] = [run_batch(target, PHASE_A, skip)]
        elif args.cve_only:
            all_results[target.slug] = explore_target(target, skip, cve_only=True)
        else:
            all_results[target.slug] = explore_target(target, skip)

    write_report(
        all_results,
        _out_root / f"{report_stem}.json",
        _out_root / f"{report_stem}.md",
    )
    print(f"\nReport: {_out_root / f'{report_stem}.md'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
