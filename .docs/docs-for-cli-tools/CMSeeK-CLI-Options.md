# CMSeeK CLI Options

Complete CLI reference for `python3 cmseek.py`. SpiderFeet default invocation:

```bash
python3 cmseek.py --follow-redirect --batch -u <URL>
```

## Captured help

Live capture from CMSeeK **1.1.3** at `C:\projects\spiderfeet\.tools\CMSeeK\cmseek.py` on **2026-08-10**. WSL path `/home/brett/.local/spiderfeet-cli/CMSeeK/cmseek.py` produced identical output. ANSI colour codes removed.

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

### Re-capture

```bash
python C:\projects\spiderfeet\.tools\CMSeeK\cmseek.py -h
# or
wsl bash -lc "python3 /home/brett/.local/spiderfeet-cli/CMSeeK/cmseek.py -h"
```

**Note:** Help text shows `--ignore--cms` (typo); `cmseek.py` argparse accepts **`--ignore-cms`** / `-i`.

## Synopsis

```
python3 cmseek.py [options]
python3 cmseek.py -u <url>
python3 cmseek.py -l <file>
python3 cmseek.py                    # interactive menu
```

## Target selection

| Option | Description |
|--------|-------------|
| `-u`, `--url <url>` | Scan a single site. Hostname or full URL. |
| `-l`, `--list <file>` | File with URLs: one per line or comma-separated. |

## Scan behaviour

| Option | Description |
|--------|-------------|
| `--batch` | Non-interactive mode. Required for automation and SpiderFeet. |
| `--follow-redirect` | Follow HTTP redirects; use final URL as target. SpiderFeet default. |
| `--no-redirect` | Do not follow redirects. |
| `--light-scan` | Detection and version only; skip deep CMS modules. |
| `-o`, `--only-cms` | CMS detection only; no version or deep scan. |
| `--skip-scanned` | Skip URLs already recorded in the result index. |

## CMS filtering

| Option | Description |
|--------|-------------|
| `-i`, `--ignore-cms <ids>` | Comma-separated CMS IDs to exclude (help typo: `--ignore--cms`). |
| `--strict-cms <ids>` | Comma-separated CMS IDs to test exclusively. |

## HTTP client

| Option | Description |
|--------|-------------|
| `-r`, `--random-agent` | Send requests with a random browser user agent. |
| `--user-agent <string>` | Set explicit User-Agent header. |
| `--googlebot` | Use Googlebot user agent. |

## Maintenance and info

| Option | Description |
|--------|-------------|
| `-v`, `--verbose` | Verbose output. |
| `-h`, `--help` | Show help (above). |
| `--version` | Print CMSeeK version and exit. |
| `--update` | Update CMSeeK from upstream (git). |
| `--clear-result` | Delete the `Result/` directory and exit. |

## Interactive menu

Running `python3 cmseek.py` with no `-u`/`-l` opens a menu:

| Key | Function |
|-----|----------|
| `1` | Single-site CMS detection and deep scan |
| `2` | Multi-site scan |
| `3` | CMS bruteforce module |
| `U` | Update |
| `R` | Rebuild bruteforce cache |
| `0` | Exit |

## Detection stages (informational)

Not CLI flags — internal pipeline order:

1. HTTP headers  
2. Generator meta tag  
3. Page source signatures  
4. `robots.txt`  
5. Directory existence checks  

## Output

| Artifact | Path |
|----------|------|
| Primary JSON | `Result/<target>/cms.json` |
| Deep scan extras | `Result/<target>/` (CMS-specific) |

SpiderFeet reads `cms.json` only; maps `cms_name` + `cms_version` → `WEBSERVER_TECHNOLOGY`.

## SpiderFeet module options

| Module opt | Description |
|------------|-------------|
| `pythonpath` | Python 3 executable |
| `cmseekpath` | Path to `cmseek.py` or its parent directory |

## Examples

```bash
# SpiderFeet equivalent
python3 cmseek.py --follow-redirect --batch -u example.com

# Batch file, skip prior scans
python3 cmseek.py --batch --follow-redirect --skip-scanned -l domains.txt

# Fast fingerprint
python3 cmseek.py --batch --follow-redirect --light-scan -u https://example.com

# WordPress-only check
python3 cmseek.py --batch --follow-redirect --strict-cms wordpress -u https://example.com

# WAF bypass attempt
python3 cmseek.py --batch --follow-redirect --random-agent -u https://example.com
```

## See also

- `.docs/docs-for-cli-tools/CMSeeK-Zero-to-Hero.md`
- `.cursor/skills/cmseek/SKILL.md`
- `.cursor/skills/cmseek/references/cli-options.md` (skill copy, kept in sync)
