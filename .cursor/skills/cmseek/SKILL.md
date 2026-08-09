---
name: cmseek
description: Detect CMS platforms (WordPress, Joomla, Drupal, Magento, 170+) with CMSeeK. Trigger on cmseek, CMS fingerprint, cms.json, WEBSERVER_TECHNOLOGY, sfp_tool_cmseek, or SpiderFeet `--follow-redirect --batch -u` scans.
---

# CMSeeK — CMS Detection and Deep Scan

## Purpose

Use when you need to **identify the Content Management System** behind a hostname or URL, optionally enrich with version and CMS-specific deep data, and map results to SpiderFeet **`WEBSERVER_TECHNOLOGY`** from `Result/<host>/cms.json`. Default automation flags: **`--follow-redirect --batch -u`**.

## Step-by-Step Instructions

1. **Confirm install** — Python 3 clone of [Tuhinshubhra/CMSeeK](https://github.com/Tuhinshubhra/CMSeeK). On Windows use WSL2 or repo `.tools/CMSeeK/` (see `.docs/analysis/cli_tool_install_runbook.md`).
2. **Capture help once** — `python3 cmseek.py -h` (version pinned in `references/cli-options.md`).
3. **Normalize target** — CMSeeK accepts hostnames or URLs; `process_url()` adds `http://` when no scheme is present.
4. **Run batch detection (SpiderFeet default)**:

```bash
python3 /path/to/CMSeeK/cmseek.py --follow-redirect --batch -u https://example.com
```

5. **Read structured output** — primary artifact is `<install>/Result/<hostname>/cms.json`, not stdout.
6. **Map to nuggets** — emit `WEBSERVER_TECHNOLOGY` as `"<cms_name> <cms_version>"` when `cms_name` is set (see `references/nugget-mapping.md`).
7. **Adapt on failure** — rotate user agent, redirect policy, or CMS filters per `references/tactics.md`; re-run only when prior pass returned `CMS Detection failed` or empty `cms_name`.
8. **Batch many hosts** — `-l targets.txt` with `--batch`; add `--skip-scanned` on periodic re-runs.

## If/Then Decision Rules

| If | Then |
|----|------|
| stdout contains `CMS Detection failed` | No CMS matched; expect missing or empty `cms_name` in `cms.json` |
| `cms.json` exists but `cms_name` is empty | Treat as clean miss; do not emit `WEBSERVER_TECHNOLOGY` |
| Target redirects (301/302) | Use `--follow-redirect` (SpiderFeet default); read `target_url` in JSON |
| CMS only visible on pre-redirect URL | `--no-redirect` and scan apex/`www` separately |
| Result path mismatch (`Result/` dir not found) | Align seed hostname with directory name CMSeeK created, or check redirect final host |
| Known false positive CMS | `-i wordpress,joomla` (`--ignore-cms` in code; help typo `--ignore--cms`) |
| Hypothesis: one CMS family | `--strict-cms wordpress` |
| Repeat scan of same host | `--skip-scanned` skips targets already in result index |
| Need CMS + version only, low noise | `--light-scan` |
| Need CMS ID only, no version/deep | `-o` / `--only-cms` |
| WAF or bot blocking | `--random-agent`, `--user-agent "..."`, or `--googlebot` (scope only) |
| Multiple URLs | `-l urls.txt` with `--batch` |
| Stale cached results | `--clear-result` wipes entire `Result/` tree |
| Automation / SpiderFeet | Always `--batch`; never rely on interactive menu |
| Deep scan authorized | Omit `--light-scan` and `--only-cms`; inspect extra files under `Result/<host>/` |

## Guardrails & Pitfalls

- **Python 3 only** — Python 2 exits immediately with an error message.
- **Structured-first** — parse `cms.json`; stdout is human-oriented and may include ANSI colour codes.
- **Path sensitivity** — SpiderFeet `cmseekpath` must resolve to install root containing `cmseek.py`; results land in sibling `Result/`.
- **Hostname key** — module reads `Result/{eventData}/cms.json` where `eventData` is the incoming `INTERNET_NAME`; redirect to a different host breaks lookup unless seed matches directory name.
- **Authorization** — scan only permitted targets; deep scan and bruteforce menu options are intrusive.
- **SSL** — upstream disables certificate verification by default (`ssl._create_unverified_context`); environment risk, not a finding.
- **Help typo** — printed help lists `--ignore--cms`; argparse accepts **`--ignore-cms`** (single hyphen pair).
- **`--batch` side effect** — batch mode prints `True` to stdout once; ignore when checking for detection failure.

## Strategies and Tactics

**Maximize detection rate**

1. Baseline: `--follow-redirect --batch -u URL` (SpiderFeet parity).
2. If blocked or empty body → `--random-agent`, then explicit `--user-agent`, then `--googlebot` where policy allows.
3. If redirect hides CMS → scan both `--follow-redirect` and `--no-redirect` variants; compare `target_url` in JSON.
4. If multi-CMS noise → `--strict-cms <id>` to confirm; or `--ignore-cms` to drop known false positives.
5. If version missing → re-run without `--light-scan` / `--only-cms`.

**Combine with other tools**

| Prior tool | Follow-up |
|------------|-----------|
| WAFWOOF | Expect partial fingerprints; tune CMSeeK UA before deep scan |
| httpx / WhatWeb | Broad tech stack → CMSeeK confirms CMS family and version |
| PIUS / Subfinder | Feed `INTERNET_NAME` list into `-l` batch file |
| Nuclei | Use detected CMS/version for tagged templates |

**SpiderFeet integration**

```python
args = [pythonpath, exe, "--follow-redirect", "--batch", "-u", eventData]
# Read: {cmseekpath}/Result/{eventData}/cms.json → WEBSERVER_TECHNOLOGY
```

**Scale and re-scan**

```
Build targets.txt from INTERNET_NAME events
  → cmseek --batch --follow-redirect --skip-scanned -l targets.txt
  → parse each Result/*/cms.json
```

## Examples

One example per CLI option (install path illustrative).

### `-u` / `--url` — single target (SpiderFeet default)

```bash
python3 cmseek.py --follow-redirect --batch -u https://shop.example.com
cat Result/shop.example.com/cms.json
```

### `-l` / `--list` — multi-site file

```bash
python3 cmseek.py --batch --follow-redirect -l targets.txt
```

### `-i` / `--ignore-cms` — skip CMS IDs (false positives)

```bash
python3 cmseek.py --batch --follow-redirect --ignore-cms joomla,drupal -u https://example.com
```

### `--strict-cms` — test only listed CMS IDs

```bash
python3 cmseek.py --batch --follow-redirect --strict-cms wordpress -u https://example.com
```

### `--skip-scanned` — skip hosts already in index

```bash
python3 cmseek.py --batch --follow-redirect --skip-scanned -l domains.txt
```

### `--light-scan` — CMS + version, no deep modules

```bash
python3 cmseek.py --batch --follow-redirect --light-scan -u https://example.com
```

### `-o` / `--only-cms` — detection only

```bash
python3 cmseek.py --batch --follow-redirect --only-cms -u https://example.com
```

### `--follow-redirect` — accept redirect chain

```bash
python3 cmseek.py --batch --follow-redirect -u http://example.com
```

### `--no-redirect` — test input URL only

```bash
python3 cmseek.py --batch --no-redirect -u https://example.com
```

### `-r` / `--random-agent`

```bash
python3 cmseek.py --batch --follow-redirect --random-agent -u https://example.com
```

### `--googlebot`

```bash
python3 cmseek.py --batch --follow-redirect --googlebot -u https://example.com
```

### `--user-agent`

```bash
python3 cmseek.py --batch --follow-redirect \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" \
  -u https://example.com
```

### `-v` / `--verbose`

```bash
python3 cmseek.py --batch --follow-redirect --verbose -u https://example.com
```

### `--update`

```bash
python3 cmseek.py --update
```

### `--version`

```bash
python3 cmseek.py --version
```

### `-h` / `--help`

```bash
python3 cmseek.py -h
```

### `--clear-result`

```bash
python3 cmseek.py --clear-result
```

### `--batch` — non-interactive (required for automation)

```bash
python3 cmseek.py --batch --follow-redirect -u example.com
```

### Interactive menu (manual only)

```bash
python3 cmseek.py
# 1 = single-site detect + deep scan
# 2 = multi-site
# 3 = CMS bruteforce paths
# U = update, R = rebuild bruteforce cache, 0 = exit
```

Do not use the menu in SpiderFeet or harvest manifests.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `cli-options.md` | Captured `-h` output + flag tables |
| `output-schema.md` | `Result/<target>/cms.json` fields |
| `nugget-mapping.md` | `WEBSERVER_TECHNOLOGY` mapping |
| `tactics.md` | Adaptive scan sequences |
| `sources.md` | Upstream URLs, blogs, module paths |

Operator guides: `.docs/docs-for-cli-tools/CMSeeK-Zero-to-Hero.md`, `CMSeeK-CLI-Options.md`.
