# WAFWOOF Zero to Hero — WAF Fingerprinting for OSINT

Guide from install through JSON parsing and SpiderFeet nugget mapping. Tool binary: **wafw00f**.

## 0. What WAFWOOF does

WAFW00F sends benign and malicious HTTP requests to a web target and matches responses against signatures for **hundreds of Web Application Firewall products**. It can report specific vendors (Cloudflare, Akamai, AWS WAF, Imperva, …) or generic WAF-like behaviour.

**SpiderFeet uses:** `wafw00f -a -o- -f json URL` → `RAW_RIR_DATA` + `WEBSERVER_TECHNOLOGY`.

## 1. Install

```bash
pip install wafw00f
wafw00f --version
```

SpiderFeet venv (see runbook):

```bash
.\.venv\Scripts\pip.exe install wafw00f
```

Module auto-resolves `wafw00f` on PATH via `shutil.which()`.

## 2. First scan

```bash
wafw00f -a -o- -f json https://example.com
```

Example output:

```json
[
  {
    "detected": true,
    "firewall": "Cloudflare",
    "manufacturer": "Cloudflare Inc.",
    "trigger_url": "https://example.com/?...",
    "url": "https://example.com/"
  }
]
```

## 3. Essential flags

| Flag | Purpose |
|------|---------|
| `-a` | Find all matching WAFs (SpiderFeet default) |
| `-o-` | Write JSON to stdout |
| `-f json` | Force JSON format |
| `-l` | List supported products |
| `-t` | Test one specific WAF |
| `-r` | Do not follow redirects |
| `-p` | Proxy URL |
| `-H` | Custom headers file |

Full list: `.docs/docs-for-cli-tools/WAFWOOF-CLI-Options.md`

## 4. Understand results

| `firewall` | Meaning |
|------------|---------|
| Product name | Signature match |
| `Generic` | WAF-like filtering, vendor unknown |
| `None` | No match |

SpiderFeet emits `WEBSERVER_TECHNOLOGY` only for **named** products (skips `Generic`).

## 5. Bulk scanning

```bash
wafw00f -a -o- -f json https://a.com https://b.com https://c.com
```

Or JSON input file:

```json
[{"url": "https://a.com"}, {"url": "https://b.com"}]
```

```bash
wafw00f -a -i targets.json -o- -f json
```

## 6. Parse in Python

```python
import json
import subprocess

def waf_scan(url: str) -> list[dict]:
    r = subprocess.run(
        ["wafw00f", "-a", "-o-", "-f", "json", url],
        capture_output=True, text=True, timeout=300,
    )
    r.check_returncode()
    return json.loads(r.stdout)

def webserver_technologies(results: list[dict]) -> list[str]:
    out = []
    for row in results:
        fw, mfr = row.get("firewall"), row.get("manufacturer")
        if fw and fw not in ("Generic", "None") and mfr:
            out.append(f"{mfr} {fw}")
    return out
```

## 7. SpiderFeet integration

```
INTERNET_NAME
  → wafw00f -a -o- -f json <url>
  → RAW_RIR_DATA (full JSON string)
  → WEBSERVER_TECHNOLOGY per named WAF
```

Module: `modules/sfp_tool_wafw00f.py`

## 8. Operational pipeline

```
PIUS domains → INTERNET_NAME
    → WAFWOOF (this tool)
    → CMSeeK (adjust UA if WAF)
    → Nuclei (WAF-aware templates/rates)
```

## 9. Safety

wafw00f sends attack-like payloads. Use only on authorized targets. Expect WAF/IDS alerts.

## 10. Skill reference

`.cursor/skills/wafwoof/SKILL.md` and `references/` directory.
