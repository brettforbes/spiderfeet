# Nuclei — Formal Examination Plan (comprehensive)

**Tool:** Nuclei v3.8.0 (Windows)  
**Exploration:** [nuclei_exploration_report.md](nuclei_exploration_report.md)  
**Manifest:** `.seed/scripts/cli_corpus/manifests/nuclei.yaml` v2  
**Strategy:** `.strategy/nuclei_strategy.skill`

## Objectives

Capture **full template-corpus findings** per target (not pinned templates) so semantic variety across templates is evidenced from real multi-template scans.

## Scenarios (7)

| # | ID | Target | Template scope |
|---|-----|--------|----------------|
| 1 | `scanme_all_templates` | `http://scanme.nmap.org` | Full tree |
| 2 | `bbc_all_templates` | `https://www.bbc.co.uk` | Full tree |
| 3 | `scanme_critical_high` | `http://scanme.nmap.org` | critical + high |
| 4 | `bbc_critical_high` | `https://www.bbc.co.uk` | critical + high |
| 5 | `sbs_critical_high` | `https://www.sbs.com.au` | critical + high |
| 6 | `praetorian_critical_high` | `https://praetorian.com` | critical + high |
| 7 | `cloudflare_critical_high` | `https://www.cloudflare.com` | critical + high |

Each scenario:

- Runs module-equivalent flags (`-no-interactsh`, `-etags dos,fuzz,misc`, full `-t .tools/nuclei-templates`)
- Writes JSONL via `-jle` → harvest builds JSON bundle + derived text
- Timeout up to 4h (all-templates) / 2h (critical+high)

## Execution

```bash
# After exploration exports exist:
python .seed/scripts/cli_corpus/harvest.py --tool nuclei --dry-run
python .seed/scripts/cli_corpus/harvest.py --tool nuclei
```

Or run exploration + harvest via:

```bash
.seed/scripts/cli_corpus/run_nuclei_exploration.bat
python .seed/scripts/cli_corpus/harvest.py --tool nuclei
```

## Verification

- [ ] 7 bundles under `app_examination_docs/nuclei/`
- [ ] Each bundle `records[]` reflects all template matches from export (not a single template)
- [ ] Exploration summaries document unique templates matched per target
- [ ] Critical/high sweeps show CVE and high-severity shapes where targets permit
