# WAFWOOF Zero to Hero — WAF Fingerprinting for OSINT

From install through JSON parsing, adaptive probing, and SpiderFeet nugget mapping. Tool binary: **wafw00f** (three zeros; skill folder `wafwoof`).

Skill reference: `.cursor/skills/wafwoof/SKILL.md`

## What WAFWOOF does

WAFW00F sends benign and malicious HTTP requests (XSS, SQLi, LFI, XXE, command-injection patterns) to a web target and matches responses against signatures for **hundreds of Web Application Firewall products**. It reports specific vendors (Cloudflare, Akamai, AWS WAF, Imperva, …), generic WAF-like behaviour, or no match.

WAFW00F does **not**:

- Enumerate subdomains (use **PIUS**, **subfinder**)
- Fingerprint CMS (use **CMSeeK**)
- Run vulnerability templates (use **Nuclei**)

**SpiderFeet uses:** `wafw00f -a -o- -f json URL` → `RAW_RIR_DATA` + `WEBSERVER_TECHNOLOGY`.

---

## Level 0 — Install

```bash
pip install wafw00f
wafw00f --version
```

SpiderFeet venv:

```powershell
.\.venv\Scripts\pip.exe install wafw00f
.\.venv\Scripts\wafw00f.exe --version
```

Module auto-resolves `wafw00f` on PATH via `shutil.which()`. Optional module opts: `wafw00f_path`, `python_path`.

---

## Level 1 — First scan

```bash
wafw00f https://example.com
```

Human-readable output on stderr/stdout. For automation, always use JSON:

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

---

## Level 2 — Essential flags

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
| `-T` | Request timeout |
| `-v` | Verbose (repeat for more) |
| `--no-colors` | Disable ANSI in terminal output |

Full list: `.docs/docs-for-cli-tools/WAFWOOF-CLI-Options.md`

---

## Level 3 — Understand results

| `firewall` | `detected` | Meaning |
|------------|------------|---------|
| Product name | `true` | Signature match — emit WEBSERVER_TECHNOLOGY |
| `Generic` | `true` | WAF-like filtering, vendor unknown |
| `None` | `false` | No match |

SpiderFeet emits `WEBSERVER_TECHNOLOGY` only for **named** products (skips `Generic`). Full array always stored in `RAW_RIR_DATA`.

With `-a`, you may see **multiple** rows per URL (stacked CDN + WAF, plus optional Generic row).

---

## Level 4 — Adapt when results are thin

### Redirect comparison

```bash
wafw00f -a -o- -f json https://example.com      # follows redirects (default)
wafw00f -r -a -o- -f json https://example.com   # original host only
```

### Custom client fingerprint

`headers.txt`:

```
User-Agent: InternalApp/1.0
Accept: application/json
```

```bash
wafw00f -a -H headers.txt -o- -f json https://example.com
```

**Note:** `-H` **replaces** wafw00f's default Chrome-on-Windows headers entirely.

### Regional / corporate egress

```bash
wafw00f -a -p http://127.0.0.1:8080 -o- -f json https://example.com
wafw00f -a -p socks5://127.0.0.1:1080 -o- -f json https://example.com
```

### Hypothesis-driven single test

```bash
wafw00f -l | findstr /i cloudflare
wafw00f -t "Cloudflare (Cloudflare Inc.)" -o- -f json https://example.com
```

### Debug empty or timeout results

```bash
wafw00f -v -v -T 15 -a -o- -f json https://example.com
```

---

## Level 5 — Bulk scanning

```bash
wafw00f -a -o- -f json https://a.com https://b.com https://c.com
```

JSON input file:

```json
[{"url": "https://a.com"}, {"url": "https://b.com"}]
```

```bash
wafw00f -a -i targets.json -o- -f json
```

CSV input: column named `url`. Plain text: one URL per line.

---

## Level 6 — Parse in Python

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

Schema details: `.cursor/skills/wafwoof/references/json-output-schema.md`

---

## Level 7 — SpiderFeet integration

```
INTERNET_NAME
  → wafw00f -a -o- -f json <url>
  → RAW_RIR_DATA (full JSON string)
  → WEBSERVER_TECHNOLOGY per named WAF ("<manufacturer> <firewall>")
```

Module: `modules/sfp_tool_wafw00f.py`

| Event | When |
|-------|------|
| `RAW_RIR_DATA` | Successful parse, non-empty array |
| `WEBSERVER_TECHNOLOGY` | Each row with named `firewall` + `manufacturer` (not Generic) |

---

## Level 8 — Operational pipeline

```
PIUS domains → INTERNET_NAME
    → WAFWOOF (this tool)
    → CMSeeK (adjust UA if WAF — e.g. --random-agent)
    → Nuclei (WAF-aware templates/rates)
```

Run WAF fingerprint **before** aggressive web scanning to reduce blocks and tune downstream tools.

---

## Level 9 — Safety and OPSEC

- wafw00f sends attack-like payloads — **authorized targets only**
- Expect WAF/IDS alerts on target and in corporate egress logs
- Rate-limit bulk scans; WAFs may temporarily block your source IP
- Generic detection means "something filtered" — not a vendor attribution

---

## Level 10 — Skill and corpus references

| Artifact | Path |
|----------|------|
| Agent skill | `.cursor/skills/wafwoof/SKILL.md` |
| CLI options + captured help | `.docs/docs-for-cli-tools/WAFWOOF-CLI-Options.md` |
| Nugget mapping | `.cursor/skills/wafwoof/references/nugget-mapping.md` |
| Tactics | `.cursor/skills/wafwoof/references/tactics.md` |
| Upstream | https://github.com/EnableSecurity/wafw00f |
