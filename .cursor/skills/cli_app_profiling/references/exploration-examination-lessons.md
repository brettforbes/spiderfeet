# Exploration & Examination — Lessons (2026-07)

Captured after Nuclei strategic/pentest-ground matrix work and Pius manifest v4 refresh. Read before onboarding the next CLI tool.

## Target taxonomy (extend permissive / corporate)

| Class | Examples | Use for |
|-------|----------|---------|
| Permissive lab | `scanme.nmap.org`, `scanme.sh` | Full severity / protocol breadth |
| Intentional vuln lab | `pentest-ground.com:*`, Acunetix vulnweb | Critical/high/CVE, app-class vulns (when templates support them) |
| Smaller real org | `squarepeg.vc`, `theupside.com.au`, `k2am.com.au` | Org-intelligence tools (pius gleif stack) — richness scales with org visibility |
| Corporate / CDN | `bbc.co.uk`, major SaaS | Sparse, filtered, or info-only — **negative fixtures**, not primary rich corpus |
| Deferred / offline | Site down today | Placeholder examination + `harvest_deferred`; do not fake live data |

Do not substitute corporate CDN targets when the matrix row needs critical/high or org-enrichment signal.

## Exploration completion gate

Exploration is **not** complete when:

- Phases were **skipped** because empty JSONL already existed (empty file ≠ completed run)
- Only tech-fingerprint or info-level noise was captured while the matrix row needs CVE/critical/org findings
- `exploration_report` / matrix is missing per-target batch results

Each matrix row ends as: **Demonstrated** | **Proven limitation** | **Blocked** | **Deferred** — with evidence path.

## One batch, one goal (multi-mode scanners)

For template/tag scanners (Nuclei, future PD tools):

1. Phase A — tech fingerprint (`-tags tech` or equivalent)
2. Phase B — **separate** passes per tag/path/protocol (exposure, cves, stack tag, `network/`, `javascript/`)
3. Phase C — severity filter only after signal appears

Do **not** default to full template tree on hardened targets. Do **not** mix unrelated goals in one examination scenario.

Tool-specific strategy skills (e.g. `nuclei_strategy`) complement base tool skills; write strategy before locking formal scenarios.

## Protocol and runtime pitfalls

### Nuclei

| Pitfall | Lesson |
|---------|--------|
| `http/cves` only on WebLogic | Also run `javascript/cves` (T3/IIOP) and `network/` (Redis TCP) |
| `-no-interactsh` | Blocks OOB-dependent templates (e.g. CVE-2023-21839); record as **proven limitation** or separate authorized OOB scenario |
| URL as `-u` on lab ports | Fine; app-logic SQLi/XSS often needs endpoint-aware/fuzz templates — empty ≠ scanner failure |
| `--skip-existing` + empty JSONL | Treat as incomplete; require stderr sidecar or force re-run |

### Pius / WSL harvest

| Pitfall | Lesson |
|---------|--------|
| `--domain https://host/` | Use **hostname only** (`squarepeg.vc`, `theupside.com.au`) — URL form yields zero NDJSON |
| `wsl --shutdown` before pius | Breaks DNS on next `wsl bash -lc` — do not shutdown before live pius harvest |
| Obscure org / RIR-only / ultra-sparse | Low examination value for gleif+crt-sh stack; prefer **org-variation** scenarios on real AU/VC firms |
| Target offline | `harvest_deferred: true` in manifest + placeholder bundle; re-harvest when reachable |

## Examination scenario quality bar

Replace examinations when:

- Scenario only produces progress banners or info noise on the stated goal
- A better target class exists (vuln lab, smaller org) that demonstrates the same semantic types
- Command args are provably wrong for the tool (URL domain, wrong protocol family)

Keep **clean miss** scenarios only when clean miss is the semantic type under test — not as filler.

## Harvest patterns

- **JSON bundle tools:** `records[]` in `*_output_structured.json`; never ship raw `.jsonl` as the examination artifact
- **`reuse_export`:** Only when export was produced by the **same** manifest command (or documented manual run with matching command in `command.txt`)
- **`harvest_deferred`:** Manifest flag + exam bundle with empty `records[]` and explicit reason; harvest runner skips live execution

## Subfinder carry-forward

- Explore **JSON vs text** output modes separately if mutually exclusive
- Matrix rows: rich subdomain set, wildcard/filtered parent, zero results, API key missing, rate limit, invalid domain
- Permissive + real org domains before assuming corporate apex is representative
- Capture help → `cli_help_text/` before formal plan
