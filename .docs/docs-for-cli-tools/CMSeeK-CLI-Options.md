# CMSeeK CLI Options

Complete CLI reference for `python3 cmseek.py`. SpiderFeet default invocation:

```bash
python3 cmseek.py --follow-redirect --batch -u <URL>
```

## Synopsis

```
python3 cmseek.py [options]
python3 cmseek.py -u <url>
python3 cmseek.py -l <file>
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
| `--only-cms` | CMS detection only; no version or deep scan. |
| `--skip-scanned` | Skip URLs already recorded in the result index. |

## CMS filtering

| Option | Description |
|--------|-------------|
| `-i`, `--ignore-cms <ids>` | Comma-separated CMS IDs to exclude from matching. |
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
| `-h`, `--help` | Show help. |
| `--version` | Print CMSeeK version and exit. |
| `--update` | Update CMSeeK from upstream. |
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
```

## See also

- `.docs/docs-for-cli-tools/CMSeeK-Zero-to-Hero.md`
- `.cursor/skills/cmseek/SKILL.md`
