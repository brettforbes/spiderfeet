# Nuclei — Exploration Report (comprehensive template-tree)

**Date:** 2026-07-03  
**Phase:** Exploration complete → formal examination harvested  
**Templates:** **12,915** full tree · **4,588** critical+high (`nuclei -tl`)

## Approach

Full template-tree scans with SpiderFeet module-default filters (`-no-interactsh -etags dos,fuzz,misc`) per target. JSONL via `-jle`; semantics derived from **which templates matched**, not pinned single-template runs.

**Important:** Nuclei emits JSONL only for **template matches**. Running all 12,915 templates does not produce 12,915 lines — non-matching templates complete silently.

## Exploration results

| Export | Target | Templates run | Findings | Unique templates matched | Severities observed |
|--------|--------|---------------|----------|--------------------------|---------------------|
| `scanme_all_templates.jsonl` | scanme.nmap.org | 12,915 | **25** | **16** | info, low, medium |
| `bbc_all_templates.jsonl` | bbc.co.uk | 12,915 | **17** | **11** | info only |
| `scanme_critical_high.jsonl` | scanme | 4,588 | **0** | 0 | clean miss |
| `bbc_critical_high.jsonl` | bbc | 4,588 | **0** | 0 | clean miss |
| `sbs_critical_high.jsonl` | sbs.com.au | 4,588 | **0** | 0 | clean miss |
| `praetorian_critical_high.jsonl` | praetorian.com | 4,588 | **0** | 0 | clean miss |
| `cloudflare_critical_high.jsonl` | cloudflare.com | 4,588 | **0** | 0 | clean miss |

Summaries: `exploration_scratch/nuclei/*.summary.json`

### scanme — semantic shapes (16 templates, 25 lines)

| Type | Count | Examples |
|------|-------|----------|
| http | 12 | `http-missing-security-headers` (10 matchers), `apache-detect`, `apache-mod-negotiation-listing` |
| javascript | 10 | SSH enum/misconfig, `CVE-2023-48795` (Terrapin, medium) |
| dns | 2 | `aaaa-fingerprint`, `caa-fingerprint` |
| tcp | 1 | `openssh-detect` |

Shape families: matcher-name multi-line misconfig; extracted-results without matcher (tech/SSH); CVE in line + classification; DNS/SSL fingerprint.

### bbc — semantic shapes (11 templates, 17 lines)

HTTP header misconfig (4), Fastly CDN debug headers (3), TLS version (2), SSL issuer/DNS names, CSP weak, SRI missing, fingerprint hub, DNS SaaS/CAA.

### Critical+high sweeps

Fixed Windows severity flags (`-severity critical -severity high`). All five secondary targets returned **valid clean misses** — no critical/high template produced a match on these hosts during the sweep (~2 min/target).

## Formal examination

**7 scenarios** harvested to `app_examination_docs/nuclei/1_*` … `7_*` via `harvest.py` with `reuse_export: true`.

## Ontology notes

- Matches without `matcher-name` still appear in JSONL (e.g. `apache-detect`, SSH templates) but `sfp_tool_nuclei` ignores them for non-CVE events.
- Multi-matcher templates (`http-missing-security-headers`) emit one JSONL line per matcher.
- To observe critical/high JSONL shapes live, need a target that actually triggers those severities (not present on scanme/bbc/corporate set used here).

## Artifacts

- Exports: `.docs/docs-for-cli-tools/exploration_scratch/nuclei/`
- Manifest v2: `.seed/scripts/cli_corpus/manifests/nuclei.yaml`
- Analyzer: `.seed/scripts/cli_corpus/analyze_nuclei_jsonl.py`
