---
name: cmseek
description: Detect CMS platforms (WordPress, Joomla, Drupal, etc.) on web targets using CMSeeK. Use when fingerprinting web stacks, mapping WEBSERVER_TECHNOLOGY nuggets, parsing Result/cms.json, or running SpiderFeet sfp_tool_cmseek with --follow-redirect --batch.
---

# CMSeeK — CMS Detection and Deep Scan

## Purpose

Use when you need to **identify the Content Management System** behind a hostname or URL and optionally enrich with version, plugin, or theme data. Primary SpiderFeet output is `WEBSERVER_TECHNOLOGY` from `Result/<target>/cms.json`.

## Step-by-Step Instructions

1. **Confirm install** — CMSeeK is a Python 3 clone of [Tuhinshubhra/CMSeeK](https://github.com/Tuhinshubhra/CMSeeK). On Windows, prefer WSL2 (see `.docs/analysis/cli_tool_install_runbook.md`).
2. **Normalize the target** — SpiderFeet passes `INTERNET_NAME` values (e.g. `example.com`). CMSeeK accepts URLs; `process_url()` adds `http://` when missing.
3. **Run batch detection (SpiderFeet default)** — non-interactive, follows redirects:

```bash
python3 /path/to/CMSeeK/cmseek.py --follow-redirect --batch -u https://example.com
```

4. **Read the result file** — output lands at `<cmseek_dir>/Result/<hostname>/cms.json` (hostname derived from final URL after redirects).
5. **Map to nuggets** — emit `WEBSERVER_TECHNOLOGY` as `"<cms_name> <cms_version>"` when `cms_name` is present (see `references/nugget-mapping.md`).
6. **Optional deep scan** — omit `--light-scan` and `--only-cms` for full CMS-specific enumeration (plugins, themes, users). SpiderFeet module uses detection + version only.
7. **Batch many hosts** — use `-l targets.txt` (one URL per line or comma-separated) with `--batch --skip-scanned` for repeat runs.

## If/Then Decision Rules

| If | Then |
|----|------|
| stdout contains `CMS Detection failed` | No CMS matched; do not expect `cms.json` with `cms_name` |
| Target redirects (301/302) | Use `--follow-redirect` (SpiderFeet default) or answer `y` interactively |
| Redirect must be ignored | `--no-redirect` |
| Known CMS false positive | `--ignore-cms wordpress,joomla` (comma-separated CMS IDs) |
| Hunt one CMS only | `--strict-cms wordpress` |
| Repeat scan of same host | `--skip-scanned` skips targets already in result index |
| Faster footprint only | `--light-scan` (detection + version, no deep scan) |
| Detection only, no version/deep | `--only-cms` |
| WAF or bot blocking | Try `--random-agent`, `--user-agent "..."`, or `--googlebot` |
| Multiple URLs | `-l urls.txt` with `--batch` |
| Stale results | `--clear-result` wipes entire `Result/` tree |

## Guardrails & Pitfalls

- **Python 3 only** — Python 2 exits immediately.
- **Path sensitivity** — SpiderFeet `cmseekpath` must point at the directory containing `cmseek.py`; results go to sibling `Result/`.
- **Hostname in path** — `cms.json` path uses the **event data string** as directory name (`Result/{eventData}/cms.json`). Mismatch between redirect final host and seed name breaks file lookup.
- **Authorization** — scan only targets you are permitted to assess.
- **Deep scan noise** — brute-force and user enumeration are intrusive; keep `--light-scan` or `--only-cms` for passive footprinting.
- **Do not parse stdout for CMS name** — always read `cms.json`; console output is for humans.
- **SSL** — upstream tool disables certificate verification by default; treat as environment risk, not a finding.

## Strategies and Tactics

**Maximize detection rate**

1. Start with default five-stage detection (headers → generator → source → robots → directories).
2. If blocked, rotate user agent (`--random-agent` → custom UA → `--googlebot` for allow-listed bots).
3. If redirect hides CMS on apex, `--follow-redirect` and scan the final URL's `cms.json`.
4. If noisy multi-CMS signals, `--strict-cms` to confirm one candidate.

**Combine with other tools**

| Prior tool | Follow-up |
|------------|-----------|
| WAFWOOF detected WAF | Expect partial detection; try alternate UA or scan origin IP if known |
| Nuclei / WhatWeb | CMSeeK confirms CMS family; use version for targeted templates |
| PIUS domain list | Feed discovered `INTERNET_NAME` hosts into CMSeeK batch file |

**SpiderFeet integration**

```python
args = [pythonpath, exe, '--follow-redirect', '--batch', '-u', eventData]
# Read: {cmseekpath}/Result/{eventData}/cms.json → WEBSERVER_TECHNOLOGY
```

## Examples

### Single URL (SpiderFeet)

```bash
python3 cmseek.py --follow-redirect --batch -u https://shop.example.com
cat Result/shop.example.com/cms.json
```

### List file, skip already scanned

```bash
python3 cmseek.py --batch --follow-redirect --skip-scanned -l domains.txt
```

### Light scan (CMS + version, no deep modules)

```bash
python3 cmseek.py --batch --follow-redirect --light-scan -u https://example.com
```

### Strict WordPress confirmation

```bash
python3 cmseek.py --batch --follow-redirect --strict-cms wordpress -u https://example.com
```

### Ignore false Joomla match

```bash
python3 cmseek.py --batch --follow-redirect --ignore-cms joomla -u https://example.com
```

### Custom user agent (WAF bypass attempt)

```bash
python3 cmseek.py --batch --follow-redirect --user-agent "Mozilla/5.0 (compatible; Googlebot/2.1)" -u https://example.com
```

### Clear all cached results

```bash
python3 cmseek.py --clear-result
```

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `cli-options.md` | Full CLI flag reference |
| `output-schema.md` | `Result/<target>/cms.json` fields |
| `nugget-mapping.md` | `WEBSERVER_TECHNOLOGY` mapping |
| `tactics.md` | Adaptive scan sequences |
| `sources.md` | Upstream URLs and blogs |

Operator guides: `.docs/docs-for-cli-tools/CMSeeK-Zero-to-Hero.md`, `CMSeeK-CLI-Options.md`.
