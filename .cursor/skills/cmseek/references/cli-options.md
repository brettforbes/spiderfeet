# CMSeeK CLI Options

Invocation: `python3 cmseek.py [options]`

SpiderFeet module (`sfp_tool_cmseek`) uses: `--follow-redirect --batch -u <URL>`.

## Captured help

Captured **2026-08-10** from CMSeeK **1.1.3** at `C:\projects\spiderfeet\.tools\CMSeeK\cmseek.py` (identical output from WSL `/home/brett/.local/spiderfeet-cli/CMSeeK/cmseek.py`). ANSI colour codes stripped for readability.

```text
CMSeeK Version 1.1.3
Github: https://github.com/Tuhinshubhra/CMSeeK
Coded By: @r3dhax0r

USAGE:
       python3 cmseek.py (for guided scanning) OR
       python3 cmseek.py [OPTIONS] <Target Specification>

SPECIFING TARGET:
      -u URL, --url URL            Target Url
      -l LIST, --list LIST         Path of the file containing list of sites
                                   for multi-site scan (comma separated or one-per-line)

MANIPULATING SCAN:
      -i cms, --ignore--cms cms    Specify which CMS IDs to skip in order to
                                   avoid flase positive. separated by comma ","

      --strict-cms cms             Checks target against a list of provided
                                   CMS IDs. separated by comma ","

      --skip-scanned               Skips target if it's CMS was previously detected.

      --light-scan                 Skips Deep Scan. Does CMS and version detection only.

      -o, --only-cms               Only detect CMS, ignore deep scan and version detection.

RE-DIRECT:
      --follow-redirect            Follows all/any redirect(s)
      --no-redirect                Skips all redirects and tests the input target(s)

USER AGENT:
      -r, --random-agent           Use a random user agent
      --googlebot                  Use Google bot user agent
      --user-agent USER_AGENT      Specify a custom user agent

OUTPUT:
      -v, --verbose                Increase output verbosity

VERSION & UPDATING:
      --update                     Update CMSeeK (Requires git)
      --version                    Show CMSeeK version and exit

HELP & MISCELLANEOUS:
      -h, --help                   Show this help message and exit
      --clear-result               Delete all the scan result
      --batch                      Never ask you to press enter after every site in a list is scanned

EXAMPLE USAGE:
      python3 cmseek.py -u example.com                           # Scan example.com
      python3 cmseek.py -l /home/user/target.txt                 # Scan the sites specified in target.txt (comma separated)
      python3 cmseek.py -u example.com --user-agent Mozilla 5.0  # Scan example.com using custom user-Agent Mozilla is 5.0 used here
      python3 cmseek.py -u example.com --random-agent            # Scan example.com using a random user-Agent
      python3 cmseek.py -v -u example.com                        # enabling verbose output while scanning example.com
```

### Capture command

```bash
# Windows (.tools install)
python C:\projects\spiderfeet\.tools\CMSeeK\cmseek.py -h

# WSL (spiderfeet-cli layout)
wsl bash -lc "python3 /home/brett/.local/spiderfeet-cli/CMSeeK/cmseek.py -h"
```

## Implementation notes

| Help text | Actual argparse (cmseek.py) |
|-----------|----------------------------|
| `--ignore--cms` (typo in help) | `--ignore-cms` / `-i` |
| All other flags | Match help |

When `--batch` is set, CMSeeK prints `True` to stdout once before scanning.

## Flag reference (structured)

### Target selection

| Flag | Long form | Description |
|------|-----------|-------------|
| `-u` | `--url` | Single target URL or hostname. Processed by `process_url()` (adds scheme if missing). |
| `-l` | `--list` | Path to file: one URL per line or comma-separated list. |

### Scan manipulation

| Flag | Description |
|------|-------------|
| `-i` | `--ignore-cms` — comma-separated CMS IDs to skip (help typo: `--ignore--cms`) |
| | `--strict-cms` — comma-separated CMS IDs to test exclusively |
| | `--skip-scanned` — skip URLs already in result index with a detected CMS |
| | `--light-scan` — detection + version only; skip deep CMS modules |
| `-o` | `--only-cms` — CMS identification only; skip version and deep scan |

### Redirect

| Flag | Description |
|------|-------------|
| | `--follow-redirect` — follow redirects automatically (**SpiderFeet default**) |
| | `--no-redirect` — do not follow redirects |

### User-Agent

| Flag | Description |
|------|-------------|
| `-r` | `--random-agent` — random browser user agent |
| | `--user-agent <string>` — explicit User-Agent header |
| | `--googlebot` — Googlebot user agent string |

### Output and maintenance

| Flag | Description |
|------|-------------|
| `-v` | `--verbose` — verbose logging |
| | `--update` — update CMSeeK from upstream (requires git) |
| | `--version` — print version and exit |
| | `--clear-result` — delete entire `Result/` directory and exit |
| | `--batch` — non-interactive; no `[ENTER]` prompts (**required for automation**) |
| `-h` | `--help` — show help |

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

## SpiderFeet configuration

| Option | Purpose |
|--------|---------|
| `pythonpath` | Python 3 interpreter (default `python3`) |
| `cmseekpath` | Directory containing `cmseek.py` (required) |

Result path: `{cmseekpath}/Result/{target}/cms.json` where `{target}` is the SpiderFeet event string.
