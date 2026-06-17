# CMSeeK Zero to Hero — CMS Detection for OSINT

Guide from install through batch scanning, parsing `cms.json`, and SpiderFeet `WEBSERVER_TECHNOLOGY` integration.

## 0. What CMSeeK does

CMSeeK detects **Content Management Systems** (WordPress, Joomla, Drupal, Magento, and 170+ others) using a five-stage passive fingerprint, then optionally runs **version detection** and **CMS-specific deep scans** (plugins, themes, users).

**SpiderFeet uses CMSeeK for:** `INTERNET_NAME` → `WEBSERVER_TECHNOLOGY` via `cms.json`.

## 1. Install

### Linux / macOS / WSL (recommended)

```bash
git clone https://github.com/Tuhinshubhra/CMSeeK.git
cd CMSeeK
python3 --version   # must be 3.x
python3 cmseek.py --version
```

### Windows

Use WSL2 — see `.docs/analysis/cli_tool_install_runbook.md`. Native Windows is unreliable for CMSeeK.

### SpiderFeet configuration

Set module options:

- `pythonpath`: `python3` (or full path)
- `cmseekpath`: directory containing `cmseek.py` (e.g. `/opt/CMSeeK/`)

## 2. First scan

```bash
python3 cmseek.py --follow-redirect --batch -u https://example.com
```

Check output file:

```bash
cat Result/example.com/cms.json
# or Result/www.example.com/cms.json if redirect changed host
```

Success looks like:

```json
{
    "cms_name": "WordPress",
    "cms_version": "6.4.2",
    "cms_id": "wordpress",
    "detection_param": "source"
}
```

Failure: stdout prints `CMS Detection failed` and `cms_name` is empty.

## 3. Essential flags

| Flag | Why |
|------|-----|
| `--batch` | No interactive prompts — required for SpiderFeet and scripts |
| `--follow-redirect` | CMS often lives on `www` or HTTPS variant |
| `-u URL` | Single target |
| `-l file` | Many targets |
| `--light-scan` | CMS + version without deep intrusive modules |
| `--skip-scanned` | Skip hosts already in result index |

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

## 5. When detection fails

Work through tactics (`.cursor/skills/cmseek/references/tactics.md`):

1. `--random-agent` or custom `--user-agent`
2. Scan both apex and `www`
3. `--strict-cms` if you have a hypothesis
4. Pair with WAFWOOF — WAF may block source inspection

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
    → WEBSERVER_TECHNOLOGY: "<cms_name> <cms_version>"
```

Module: `modules/sfp_tool_cmseek.py`

## 8. Deep scan (authorized engagements only)

Omit `--light-scan` for full CMS modules:

```bash
python3 cmseek.py --batch --follow-redirect -u https://target.example.com
```

Inspect extra files under `Result/target.example.com/`. Higher traffic and sensitivity — not for passive monitoring.

## 9. Pipeline placement

Typical OSINT order:

```
PIUS / subdomain discovery → INTERNET_NAME list
    → WAFWOOF (optional) → WEBSERVER_TECHNOLOGY (WAF)
    → CMSeeK → WEBSERVER_TECHNOLOGY (CMS)
    → Nuclei (CMS templates)
```

## 10. Skill reference

Agent skill: `.cursor/skills/cmseek/SKILL.md`

| Reference | Topic |
|-----------|--------|
| `references/output-schema.md` | `cms.json` fields |
| `references/nugget-mapping.md` | SpiderFeet events |
| `references/tactics.md` | Adaptive sequences |
| `references/cli-options.md` | All flags |

## 11. Safety and scope

CMSeeK sends HTTP requests to target sites. Deep scan and bruteforce modules are intrusive. Use only on authorized targets. SpiderFeet default integration uses detection + version only.
