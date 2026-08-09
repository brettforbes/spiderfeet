# CMSeeK Zero to Hero — CMS Detection for OSINT

Operator guide from install through batch scanning, parsing `cms.json`, adaptive tactics when targets resist fingerprinting, and SpiderFeet `WEBSERVER_TECHNOLOGY` integration.

## 0. What CMSeeK does

CMSeeK detects **Content Management Systems** — WordPress, Joomla, Drupal, Magento, and 170+ others — using a five-stage passive fingerprint:

1. HTTP headers  
2. HTML generator meta tag  
3. Page source signatures  
4. `robots.txt` patterns  
5. Well-known CMS directory paths  

After a match it can run **version detection** and **CMS-specific deep scans** (plugins, themes, users, admin paths).

**SpiderFeet uses CMSeeK for:** `INTERNET_NAME` → `WEBSERVER_TECHNOLOGY` via `Result/<host>/cms.json`, with default flags `--follow-redirect --batch -u`.

## 1. Install

### Linux / macOS / WSL (recommended)

```bash
git clone https://github.com/Tuhinshubhra/CMSeeK.git
cd CMSeeK
python3 --version   # must be 3.x
python3 cmseek.py --version
```

### Windows

Prefer WSL2 — see `.docs/analysis/cli_tool_install_runbook.md` and `.docs/analysis/wsl_ruby_cli_runbook.md`. A local copy may exist at `.tools/CMSeeK/` in the spiderfeet repo.

### Verify help

```bash
python3 cmseek.py -h
```

Captured help for v1.1.3 lives in `.docs/docs-for-cli-tools/CMSeeK-CLI-Options.md`.

### SpiderFeet configuration

Module: `sfp_tool_cmseek` (`modules/sfp_tool_cmseek.py`)

| Option | Value |
|--------|--------|
| `pythonpath` | `python3` or full path |
| `cmseekpath` | Directory containing `cmseek.py` (e.g. `/opt/CMSeeK/` or `.tools/CMSeeK/`) |

## 2. First scan

```bash
python3 cmseek.py --follow-redirect --batch -u https://example.com
```

Check structured output (not stdout):

```bash
cat Result/example.com/cms.json
# or Result/www.example.com/cms.json if redirect changed host
```

Success:

```json
{
    "cms_name": "WordPress",
    "cms_version": "6.4.2",
    "cms_id": "wordpress",
    "detection_param": "source",
    "target_url": "https://www.example.com",
    "url": "https://example.com"
}
```

Failure: stdout prints `CMS Detection failed` and `cms_name` is empty or absent.

## 3. Essential flags

| Flag | Why |
|------|-----|
| `--batch` | No interactive prompts — required for SpiderFeet and scripts |
| `--follow-redirect` | CMS often lives on `www` or HTTPS variant |
| `-u URL` | Single target |
| `-l file` | Many targets (one per line or comma-separated) |
| `--light-scan` | CMS + version without deep intrusive modules |
| `--only-cms` | Fastest: CMS family only |
| `--skip-scanned` | Skip hosts already in result index |
| `--ignore-cms` | Drop known false-positive CMS IDs |
| `--strict-cms` | Confirm a single CMS hypothesis |

Full reference: `.docs/docs-for-cli-tools/CMSeeK-CLI-Options.md`

## 4. Batch scanning

Create `targets.txt`:

```
https://shop.example.com
https://blog.example.com
example.org
```

Run:

```bash
python3 cmseek.py --batch --follow-redirect --skip-scanned -l targets.txt
```

Each target gets `Result/<host>/cms.json`.

## 5. When detection fails — adapt

Work through tactics (`.cursor/skills/cmseek/references/tactics.md`):

| Step | Action |
|------|--------|
| 1 | `--random-agent` or custom `--user-agent` |
| 2 | `--googlebot` only where policy allows |
| 3 | Scan apex and `www` separately; try `--no-redirect` vs `--follow-redirect` |
| 4 | `--strict-cms wordpress` if you have a hypothesis |
| 5 | Run WAFWOOF first — WAF may block source inspection |

**Do not** parse stdout for CMS name — always read `cms.json`.

## 6. Parse results in Python

```python
import json
from pathlib import Path

def parse_cmseek_result(result_dir: Path, host: str) -> dict | None:
    path = result_dir / host / "cms.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("cms_name"):
        return None
    return data

def to_webserver_technology(data: dict) -> str:
    return " ".join(filter(None, [data.get("cms_name"), data.get("cms_version")]))
```

## 7. SpiderFeet module flow

```
INTERNET_NAME event
    → python3 cmseek.py --follow-redirect --batch -u <eventData>
    → read Result/<eventData>/cms.json
    → if cms_name: WEBSERVER_TECHNOLOGY = "<cms_name> <cms_version>"
```

**Path pitfall:** if CMSeeK follows a redirect to a different hostname, the result directory may not match `eventData`. Align seeds with final host or scan the canonical URL.

## 8. Deep scan (authorized engagements only)

Omit `--light-scan` and `--only-cms`:

```bash
python3 cmseek.py --batch --follow-redirect -u https://target.example.com
```

Inspect extra files under `Result/target.example.com/`. Higher traffic and sensitivity — not for passive monitoring.

Interactive menu option `3` runs CMS bruteforce modules — use only with explicit scope.

## 9. Pipeline placement

Typical OSINT order:

```
PIUS / subdomain discovery → INTERNET_NAME list
    → WAFWOOF (optional) → WEBSERVER_TECHNOLOGY (WAF)
    → CMSeeK → WEBSERVER_TECHNOLOGY (CMS)
    → Nuclei (CMS-tagged templates)
```

## 10. Agent skill and references

| Artifact | Path |
|----------|------|
| Skill | `.cursor/skills/cmseek/SKILL.md` |
| Reference index | `.cursor/skills/cmseek/references/SKILLS.md` |
| `cms.json` schema | `references/output-schema.md` |
| Nugget mapping | `references/nugget-mapping.md` |
| Adaptive tactics | `references/tactics.md` |
| CLI (skill copy) | `references/cli-options.md` |

## 11. Safety and scope

CMSeeK sends HTTP requests to target sites. Deep scan and bruteforce modules are intrusive. Use only on authorized targets. SpiderFeet default integration uses detection + version from `cms.json` only.

Upstream disables SSL certificate verification by default — treat as a local environment characteristic, not a vulnerability finding.

## 12. Quick command cheat sheet

```bash
# SpiderFeet parity
python3 cmseek.py --follow-redirect --batch -u example.com

# Low-noise fingerprint
python3 cmseek.py --batch --follow-redirect --light-scan -u https://TARGET

# Rescan list, skip known
python3 cmseek.py --batch --follow-redirect --skip-scanned -l hosts.txt

# Clear cache
python3 cmseek.py --clear-result

# Version check / update
python3 cmseek.py --version
python3 cmseek.py --update
```
