#!/usr/bin/env python3
"""Generate SPEC010_IP_MIGRATION_INVENTORY.md (AH0). Run from repo root."""
from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def normalize(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")


def rg_count(pattern: str, path: str | Path | None = None) -> list[tuple[str, int]]:
    target = str(path or ROOT)
    # --hidden: on Windows, rg skips dot-directories (e.g. .seed, .docs) unless set
    cmd = [
        "rg",
        "-c",
        "--hidden",
        "--glob",
        "!.git/**",
        "--glob",
        "!**/__pycache__/**",
        "--glob",
        "!**/.venv/**",
        "--glob",
        "!**/node_modules/**",
        "--glob",
        "!**/dist/**",
        "--glob",
        "!**/.codegraph/**",
        "--glob",
        "!**/.cursor/**",
        "--glob",
        "!**/agent-transcripts/**",
        "--glob",
        "!**/SPEC010_IP_MIGRATION_INVENTORY.md",
        "--glob",
        "!**/_gen_ip_migration_inventory.py",
        pattern,
        target,
    ]
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL, cwd=ROOT)
    except subprocess.CalledProcessError as e:
        out = e.output or ""
    rows: list[tuple[str, int]] = []
    for line in out.splitlines():
        if ":" not in line:
            continue
        p, n = line.rsplit(":", 1)
        try:
            n_i = int(n)
        except ValueError:
            continue
        # rg may print absolute paths; make relative to ROOT
        pp = Path(normalize(p))
        try:
            rel = pp.resolve().relative_to(ROOT).as_posix()
        except Exception:
            rel = normalize(p)
            if rel.startswith(ROOT.as_posix()):
                rel = rel[len(ROOT.as_posix()) :].lstrip("/")
        rows.append((rel, n_i))
    return rows


def classify(path: str) -> str:
    if path.startswith(".docs/docs-for-cli-tools/nugget_structure/") and (
        path.endswith("_proposed_nuggets_edges.json")
        or path.endswith("_proposed_nuggets_edges_description.md")
        or path.endswith("_proposed_nuggets.json")
    ):
        return "regen-artifact"
    if "/app_examination_docs/" in path or path.startswith(
        ".docs/docs-for-cli-tools/exploration_scratch/"
    ):
        return "regen-artifact"
    if path.startswith(".seed/scripts/cli_corpus/create_spec"):
        return "keep-legacy"
    if path.endswith("_gen_ip_migration_inventory.py"):
        return "keep-legacy"
    if path.endswith("SPEC010_IP_MIGRATION_INVENTORY.md"):
        return "keep-legacy"
    migrate_exact = {
        ".docs/docs-for-cli-tools/_Current_Ontology.md",
        ".seed/spiderfeet_v2_semantic.tql",
    }
    if path in migrate_exact:
        return "migrate"
    migrate_prefixes = (
        ".seed/scripts/cli_corpus/",
        ".docs/analysis/nuggets",
        ".docs/docs-for-cli-tools/",
        "modules_v2/",
        ".cursor/rules/proj-05",
        ".cursor/rules/proj-06",
        ".cursor/rules/proj-07",
        ".governance/specs/SPEC-005",
        ".governance/specs/SPEC-010",
        ".governance/project/SPEC010",
        ".governance/project/SPEC005",
    )
    if any(path.startswith(p) for p in migrate_prefixes):
        return "migrate"
    return "keep-legacy"


def migrate_bucket(p: str) -> str:
    if p.startswith(".seed/scripts/cli_corpus/"):
        return "A. cli_corpus (code + rules)"
    if p.startswith(".docs/analysis/"):
        return "B. catalogues (.docs/analysis)"
    if p.startswith(".docs/docs-for-cli-tools/nugget_structure/") and p.endswith(
        "_nugget_graph_structure.md"
    ):
        return "C. tool structure docs"
    if p == ".docs/docs-for-cli-tools/_Current_Ontology.md":
        return "C. tool structure docs"
    if p.startswith(".docs/docs-for-cli-tools/"):
        return "D. CLI tool guides (Zero-to-Hero / options)"
    if p.startswith("modules_v2/"):
        return "E. modules_v2 content + stubs"
    if "spiderfeet_v2_semantic" in p:
        return "F. v2 TypeDB schema"
    if p.startswith(".cursor/rules/"):
        return "G. project rules"
    if p.startswith(".governance/"):
        return "H. governance / SPEC docs"
    return "I. other migrate"


def main() -> None:
    rows = rg_count("IP_ADDRESS")
    by_class: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for p, n in sorted(rows):
        by_class[classify(p)].append((p, n))

    ip_patterns = (
        ROOT / ".seed/scripts/cli_corpus/rules/_shared/ip_patterns.yaml"
    ).read_text(encoding="utf-8")
    has_ipv4_host = "ipv4: IP_ADDRESS" in ip_patterns
    has_ipv6_host = "ipv6: IPV6_ADDRESS" in ip_patterns

    nug = {
        n["nugget_id"]
        for n in json.loads((ROOT / ".docs/analysis/nuggets.json").read_text(encoding="utf-8"))
    }
    ext_path = ROOT / ".docs/analysis/nuggets_extension.json"
    ext = (
        {n["nugget_id"] for n in json.loads(ext_path.read_text(encoding="utf-8"))}
        if ext_path.exists()
        else set()
    )

    total = sum(n for _, n in rows)
    mig = by_class["migrate"]
    regen = by_class["regen-artifact"]
    keep = by_class["keep-legacy"]

    lines: list[str] = []
    lines += [
        "# SPEC-010 — IP_ADDRESS migration inventory (AH0)",
        "",
        f"**Date:** {date.today().isoformat()}",
        "**Issue:** [#1066](https://github.com/brettforbes/spiderfeet/issues/1066) (AH0)",
        "**Requirement:** R10-01",
        "**Goal:** Split ambiguous `IP_ADDRESS` -> `IPV4_ADDRESS` / `IPV6_ADDRESS` "
        "across the canonical CLI-profiling stack.",
        "",
        "## Summary",
        "",
        "| Classification | Files | Matches |",
        "|---------------|------:|--------:|",
    ]
    for cls in ("migrate", "regen-artifact", "keep-legacy"):
        items = by_class[cls]
        lines.append(f"| `{cls}` | {len(items)} | {sum(n for _, n in items)} |")
    lines += [
        f"| **Total (`rg IP_ADDRESS`)** | **{len(rows)}** | **{total}** |",
        "",
        "### Verification command",
        "",
        "```bash",
        "rg -c --hidden IP_ADDRESS --glob \"!.git/**\" --glob \"!**/__pycache__/**\" "
        "--glob \"!**/.venv/**\" --glob \"!**/node_modules/**\" "
        "--glob \"!**/dist/**\" --glob \"!**/.codegraph/**\" --glob \"!**/.cursor/**\" "
        "--glob \"!**/agent-transcripts/**\" "
        "--glob \"!**/SPEC010_IP_MIGRATION_INVENTORY.md\" "
        "--glob \"!**/_gen_ip_migration_inventory.py\"",
        "# Expected: files and match counts equal the Total row above.",
        "```",
        "",
        f"- Inventory total matches: **{total}**",
        f"- Inventory total files: **{len(rows)}**",
        "",
        "## Central classifier status (`core/ip_classify.py`)",
        "",
        "`classify_ip()` already routes literals through `rules/_shared/ip_patterns.yaml` roles.",
        "",
        "| Role | Current IPv4 mapping | Current IPv6 mapping | AH target IPv4 | AH target IPv6 |",
        "|------|----------------------|----------------------|----------------|----------------|",
        "| host | `IP_ADDRESS` | `IPV6_ADDRESS` | **`IPV4_ADDRESS`** | `IPV6_ADDRESS` |",
        "| internal | `INTERNAL_IP_ADDRESS` | `IPV6_ADDRESS` | keep (or later `INTERNAL_IPV4_ADDRESS`) | keep / follow-up |",
        "| affiliate | `AFFILIATE_IPADDR` | `AFFILIATE_IPV6_ADDRESS` | keep (v1 event name) or follow-up split | keep |",
        "",
        f"- Confirmed host IPv4 currently maps to `IP_ADDRESS`: **{has_ipv4_host}**",
        f"- Confirmed host IPv6 currently maps to `IPV6_ADDRESS`: **{has_ipv6_host}**",
        "- Decision (operator): host IPv4 becomes `IPV4_ADDRESS`; host IPv6 stays `IPV6_ADDRESS`.",
        "",
        "## Catalogue status",
        "",
        "| nugget_id | In `nuggets.json` | In `nuggets_extension.json` | AH action |",
        "|-----------|:-----------------:|:---------------------------:|-----------|",
    ]
    catalogue_rows = [
        (
            "IP_ADDRESS",
            "retire from emitting code; retain in nuggets.json as keep-legacy v1 event type until v1 sunset",
        ),
        ("IPV4_ADDRESS", "**ADD** to nuggets_extension.json (AH1)"),
        ("IPV6_ADDRESS", "already present in nuggets.json — reuse"),
        (
            "INTERNAL_IP_ADDRESS",
            "keep (IPv4-internal); note ambiguity vs IPV4 — follow-up if needed",
        ),
        (
            "AFFILIATE_IPADDR",
            "keep-legacy v1 event name (not host classifier role for v2 graphs)",
        ),
        ("AFFILIATE_IPV6_ADDRESS", "keep"),
        ("BLACKLISTED_IPADDR", "keep-legacy v1"),
        ("BLACKLISTED_AFFILIATE_IPADDR", "keep-legacy v1"),
        ("MALICIOUS_IPADDR", "keep-legacy v1"),
        ("MALICIOUS_AFFILIATE_IPADDR", "keep-legacy v1"),
    ]
    for nid, action in catalogue_rows:
        in_n = "yes" if nid in nug else "no"
        in_e = "yes" if nid in ext else "no"
        lines.append(f"| `{nid}` | {in_n} | {in_e} | {action} |")

    lines += ["", "## `migrate` — must change in AH1–AH3", ""]
    mb: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for p, n in mig:
        mb[migrate_bucket(p)].append((p, n))
    for bucket in sorted(mb):
        items = mb[bucket]
        lines += [
            f"### {bucket} ({sum(n for _, n in items)} matches / {len(items)} files)",
            "",
            "| Matches | Path |",
            "|--------:|------|",
        ]
        for p, n in sorted(items, key=lambda x: (-x[1], x[0])):
            lines.append(f"| {n} | `{p}` |")
        lines.append("")

    lines += [
        "## `regen-artifact` — regenerate in AH4 (do not hand-edit)",
        "",
        f"**{sum(n for _, n in regen)} matches in {len(regen)} files** — graph JSON + narrative MD "
        "under `.docs/docs-for-cli-tools/nugget_structure/` (and exploration scratch).",
        "",
        "Regenerate via:",
        "",
        "```bash",
        "poetry run python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --tool <tool>",
        "# for each of: nmap netdiscover nerva pius subfinder httpx katana nuclei",
        "```",
        "",
        "Also refresh `modules_v2/content/<tool>/graph_structure.md` from the structure docs.",
        "",
        "<details><summary>Full regen-artifact file list</summary>",
        "",
        "| Matches | Path |",
        "|--------:|------|",
    ]
    for p, n in sorted(regen, key=lambda x: (-x[1], x[0])):
        lines.append(f"| {n} | `{p}` |")
    lines += ["", "</details>", ""]

    top: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for p, n in keep:
        key = p.split("/")[0]
        top[key][0] += 1
        top[key][1] += n
    rationale = {
        "modules": "v1 OSINT `sfp_*` event types — SPEC-010 forbids touching these",
        "test": "v1 unit/integration tests bound to v1 event names",
        "spiderfeet": "v1 package (target typing, map seeds, API schemas) — keep until v1 sunset",
        "correlations": "v1 correlation YAML using IP_ADDRESS event names",
        ".seed": "historic issue-generator scripts / unrelated seeds",
        ".docs": "non-canonical docs outside migrate buckets",
        ".governance": "historic SPEC text mentioning IP_ADDRESS as example",
    }
    lines += [
        "## `keep-legacy` — out of AH emitting-path scope",
        "",
        "| Top-level | Files | Matches | Rationale |",
        "|-----------|------:|--------:|-----------|",
    ]
    for key, (fc, mc) in sorted(top.items(), key=lambda x: -x[1][1]):
        lines.append(
            f"| `{key}/` | {fc} | {mc} | "
            f"{rationale.get(key, 'legacy / out of AH emitting scope')} |"
        )
    lines += [
        "",
        f"Total keep-legacy: **{sum(n for _, n in keep)}** matches in **{len(keep)}** files.",
        "",
        "## Derived `*_IPADDR` audit (not host-role rename)",
        "",
        "| Variant | Matches | Files | AH decision |",
        "|---------|--------:|------:|-------------|",
    ]
    decisions = {
        "AFFILIATE_IPADDR": "keep-legacy (v1 event); affiliate role stays AFFILIATE_IPADDR for IPv4 until a later split",
        "BLACKLISTED_IPADDR": "keep-legacy v1",
        "MALICIOUS_IPADDR": "keep-legacy v1",
        "INTERNAL_IP_ADDRESS": "keep for now (internal IPv4); optional follow-up to INTERNAL_IPV4_ADDRESS",
        "AFFILIATE_IPV6_ADDRESS": "keep",
        "IPV6_ADDRESS": "keep / already correct for host IPv6",
        "IPV4_ADDRESS": "add to catalogue (AH1); currently sparse (governance/plan mentions only)",
    }
    for pat in [
        "AFFILIATE_IPADDR",
        "BLACKLISTED_IPADDR",
        "MALICIOUS_IPADDR",
        "INTERNAL_IP_ADDRESS",
        "AFFILIATE_IPV6_ADDRESS",
        "IPV6_ADDRESS",
        "IPV4_ADDRESS",
    ]:
        r = [
            (p, n)
            for p, n in rg_count(pat)
            if not p.startswith(".cursor/") and ".codegraph" not in p
        ]
        lines.append(
            f"| `{pat}` | {sum(n for _, n in r)} | {len(r)} | {decisions[pat]} |"
        )

    lines += [
        "",
        "## AH story mapping",
        "",
        "| Story | Action |",
        "|-------|--------|",
        "| **AH1** | Add `IPV4_ADDRESS` (+ confirm `IPV6_ADDRESS`) to `nuggets_extension.json`; document derived-variant decisions |",
        "| **AH2** | Change `ip_patterns.yaml` host.ipv4 → `IPV4_ADDRESS`; update rules/adapters/topology so emitters use `classify_ip` only |",
        "| **AH3** | Align `spiderfeet_v2_semantic.tql` comments; update structure docs, `_Current_Ontology.md`, proj-07 IP table |",
        "| **AH4** | Backfill all 8 tools; refresh content `graph_structure.md`; prove no non-legacy `IP_ADDRESS` in migrate+regen surfaces |",
        "",
        "## Exit criteria for AH0",
        "",
        "- [x] Every `IP_ADDRESS` occurrence classified `migrate` / `regen-artifact` / `keep-legacy`",
        "- [x] `classify_ip` confirmed as single source of truth for address literals",
        "- [x] Grep totals recorded for verification against a fresh `rg -c IP_ADDRESS`",
        "",
    ]

    out = ROOT / ".governance" / "project" / "SPEC010_IP_MIGRATION_INVENTORY.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")
    print(
        f"total={total} migrate={sum(n for _, n in mig)} "
        f"regen={sum(n for _, n in regen)} keep={sum(n for _, n in keep)}"
    )
    fresh = rg_count("IP_ADDRESS")
    assert len(fresh) == len(rows) and sum(n for _, n in fresh) == total
    print("VERIFY OK")


if __name__ == "__main__":
    main()
