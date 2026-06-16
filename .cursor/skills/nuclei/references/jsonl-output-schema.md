# Nuclei JSONL Output Schema

Nuclei with `-jsonl` emits **one JSON object per line** on stdout for each template match. Blank lines and log noise may appear; SpiderFeet skips lines that do not start with `{`.

## Minimal fields (always expect)

These fields are required for `sfp_tool_nuclei` parsing:

| Field | Type | Description |
|-------|------|-------------|
| `matched-at` | string | Full URL or host:port where match occurred — used to derive host |
| `template-id` | string | Template identifier |
| `info` | object | Template metadata block |
| `info.name` | string | Human-readable template name |
| `info.severity` | string | `info`, `low`, `medium`, `high`, `critical`, `unknown` |

## Fields used by SpiderFeet mapping

| Field | Type | SpiderFeet use |
|-------|------|----------------|
| `matcher-name` | string | Presence triggers non-CVE branch; included in event text |
| `info.reference` | array of strings | First reference emitted as `<SFURL>` in event data |
| (raw line) | string | CVE regex `CVE-\d{4}-\d{4,7}` anywhere in line |

## Common additional fields

| Field | Type | Description |
|-------|------|-------------|
| `host` | string | Target host submitted to scan |
| `ip` | string | Resolved IP |
| `timestamp` | string | ISO-8601 match time |
| `type` | string | Protocol: `http`, `dns`, `ssl`, `tcp`, `file`, etc. |
| `url` | string | Request URL |
| `path` | string | URL path |
| `matched-line` | string | Line that satisfied matcher |
| `extracted-results` | array | Extractor output values |
| `extractor-name` | string | Name of extractor that fired |
| `curl-command` | string | Reproducible curl one-liner |
| `request` | string | Raw HTTP request (if not omitted) |
| `response` | string | Raw HTTP response (if not omitted) |
| `interaction` | object | Interactsh OOB data (absent when `-no-interactsh`) |
| `template-path` | string | Filesystem path to template |
| `template-encoded` | string | Base64 template (optional) |
| `matcher-status` | boolean | Matcher result |
| `meta` | object | Extra metadata |
| `classification` | object | CVE/CWE/EPSS under `info.classification` in newer templates |

## `info` object detail

```json
{
  "name": "Apache Tomcat Example",
  "author": ["pdteam"],
  "tags": ["cve", "apache", "tomcat"],
  "description": "Detects ...",
  "reference": ["https://nvd.nist.gov/..."],
  "severity": "high",
  "metadata": {
    "max-request": 1,
    "verified": true
  },
  "classification": {
    "cve-id": ["CVE-2024-1234"],
    "cwe-id": ["CWE-79"],
    "cvss-metrics": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    "cvss-score": 9.8
  }
}
```

SpiderFeet does **not** currently read `classification.cve-id`; it regexes the entire line for CVE strings.

## Example lines

### CVE finding (typical)

```json
{
  "template-id": "CVE-2021-44228",
  "info": {
    "name": "Log4j RCE",
    "severity": "critical",
    "reference": ["https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228"]
  },
  "type": "http",
  "host": "app.example.com",
  "matched-at": "https://app.example.com/api",
  "matcher-name": "log4j",
  "timestamp": "2026-06-15T10:00:00.000Z"
}
```

→ `VULNERABILITY_CVE_CRITICAL` (via `sf.cveInfo("CVE-2021-44228")`).

### Technology / info severity

```json
{
  "template-id": "tech-detect",
  "info": {
    "name": "Wappalyzer Technology Detection",
    "severity": "info"
  },
  "matched-at": "https://www.example.com",
  "matcher-name": "nginx"
}
```

→ `WEBSERVER_TECHNOLOGY`.

### General vulnerability (no CVE in line)

```json
{
  "template-id": "exposed-panel",
  "info": {
    "name": "Exposed Admin Panel",
    "severity": "medium",
    "reference": ["https://owasp.org/..."]
  },
  "matched-at": "https://admin.example.com/login",
  "matcher-name": "title"
}
```

→ `VULNERABILITY_GENERAL`.

## Parsing algorithm (SpiderFeet)

```python
for line in stdout.split("\n"):
    line = line.strip()
    if not line or not line.startswith("{"):
        continue
    data = json.loads(line)
    host = data["matched-at"].split(":")[0]  # naive split; works for https://host:port
    cves = re.findall(r"CVE-\d{4}-\d{4,7}", line)
    if cves:
        for cve in cves:
            etype, text = sf.cveInfo(cve)
            emit(etype, text)
    elif "matcher-name" in data:
        if data["info"]["severity"] == "info":
            emit("WEBSERVER_TECHNOLOGY", format_text(data))
        else:
            emit("VULNERABILITY_GENERAL", format_text(data))
```

## Pitfalls

| Issue | Mitigation |
|-------|------------|
| `matched-at` with IPv6 | Host split on first `:` is fragile; prefer `urllib.parse` for new parsers |
| Duplicate CVE in line | Module emits one event per regex match |
| Missing `matcher-name` | Line ignored for non-CVE branch even if match occurred |
| Large `request`/`response` | Use `-omit-raw` in manual runs; module does not set it |
| Invalid JSON mid-stream | Handle `JSONDecodeError`; partial scan may still be useful |
| stderr mixed into stdout | Use `-silent`; capture stderr separately |

## Related

- [nugget-mapping.md](nugget-mapping.md) — event type rules
- [cli-options.md](cli-options.md) — `-jsonl`, `-omit-raw`, `-include-rr`
