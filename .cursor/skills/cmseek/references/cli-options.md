# CMSeeK CLI Options

Invocation: `python3 cmseek.py [options]`

SpiderFeet module (`sfp_tool_cmseek`) uses: `--follow-redirect --batch -u <URL>`.

## Detection and scan flags

| Flag | Long form | Description |
|------|-----------|-------------|
| `-u` | `--url` | Single target URL or hostname. Processed by `process_url()` (adds scheme if missing). |
| `-l` | `--list` | Path to file: one URL per line or comma-separated list. |
| | `--follow-redirect` | Automatically accept redirect targets (sets `redirect_conf = '1'`). **SpiderFeet default.** |
| | `--no-redirect` | Do not follow redirects; keep original target. |
| | `--batch` | Non-interactive mode; no `[ENTER]` prompts. **Required for automation.** |
| | `--light-scan` | Detection + version only; skip deep CMS modules. |
| | `--only-cms` | CMS identification only; skip version and deep scan. |
| | `--skip-scanned` | Skip URLs already present in result index with a `cms_id`. |
| `-i` | `--ignore-cms` | Comma-separated CMS IDs to ignore during detection (e.g. `wordpress,drupal`). |
| | `--strict-cms` | Comma-separated CMS IDs to test exclusively. |

## User-Agent and evasion

| Flag | Description |
|------|-------------|
| `-r` | `--random-agent` — pick a random browser user agent |
| | `--user-agent <string>` — explicit User-Agent header |
| | `--googlebot` — use Googlebot user agent string |

## Maintenance

| Flag | Description |
|------|-------------|
| | `--update` — update CMSeeK from upstream |
| | `--clear-result` — delete entire `Result/` directory and exit |
| | `--version` — print version and exit |
| `-v` | `--verbose` — verbose logging |
| `-h` | `--help` — help text |

## Interactive menu (no CLI args)

When run without `-u` or `-l`, CMSeeK presents a menu:

| Option | Action |
|--------|--------|
| `1` | CMS detection and deep scan (single URL prompt) |
| `2` | Scan multiple sites (comma list or file path) |
| `3` | Bruteforce CMS admin paths (per-CMS submodule) |
| `U` | Update CMSeeK |
| `R` | Rebuild bruteforce cache after custom modules |
| `0` | Exit |

Automation should **not** rely on the menu; always pass `-u` or `-l` with `--batch`.

## Detection pipeline (internal)

When `core.main_proc()` runs, CMS detection proceeds in order until a match:

1. **header** — HTTP response headers
2. **generator** — HTML `<meta name="generator">`
3. **source** — page source signatures
4. **robots** — `robots.txt` patterns
5. **dirscheck** — well-known CMS paths

On match, CMSeeK may run **version detection** (`VersionDetect`) and/or **deep scan** (`deepscans`) depending on CMS database flags and CLI options.

## Exit and stdout signals

| Signal | Meaning |
|--------|---------|
| Return code `0` | Process completed (may still mean "no CMS detected") |
| stdout contains `CMS Detection failed` | No CMS signature matched |
| `cms.json` with empty `cms_name` | Scan ran but no named CMS recorded |

## Configuration (SpiderFeet)

| Option | Purpose |
|--------|---------|
| `pythonpath` | Python 3 interpreter (default `python3`) |
| `cmseekpath` | Directory containing `cmseek.py` (required) |

Result path: `{cmseekpath}/Result/{target}/cms.json` where `{target}` is the SpiderFeet event string.
