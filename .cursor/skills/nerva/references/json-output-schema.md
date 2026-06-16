# Nerva JSON Output Schema

Nerva `--json` writes **JSON Lines** (NDJSON): one complete JSON object per line, no wrapping array.

## Record shape (core fields)

Every successful fingerprint line includes these top-level keys:

| Field | Type | Description |
|-------|------|-------------|
| `host` | string | Target hostname or IP as supplied on CLI |
| `ip` | string | Resolved IPv4/IPv6 address used for probing |
| `port` | integer | TCP/UDP/SCTP port number |
| `protocol` | string | Detected service slug (e.g. `ssh`, `http`, `mysql`) |
| `transport` | string | `tcp`, `udp`, or `sctp` |
| `metadata` | object | Protocol-specific details (variable schema) |

### Example (SSH)

```json
{"host":"example.com","ip":"93.184.216.34","port":22,"protocol":"ssh","transport":"tcp","metadata":{"banner":"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.13"}}
```

### Example (HTTPS / HTTP)

```json
{"host":"example.com","ip":"93.184.216.34","port":443,"protocol":"https","transport":"tcp","metadata":{"tls":true,"technologies":["nginx"],"title":"Example"}}
```

Exact `metadata` keys depend on the matched plugin. Common patterns below.

---

## Parsing rules

```python
import json

def parse_nerva_jsonl(text: str) -> list[dict]:
    records = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return records
```

### Streaming

```python
import subprocess, json

proc = subprocess.Popen(
    ["nerva", "-l", "targets.txt", "--json"],
    stdout=subprocess.PIPE, text=True,
)
for line in proc.stdout:
    line = line.strip()
    if line:
        yield json.loads(line)
```

### jq filtering

```bash
nerva -l targets.txt --json | jq 'select(.protocol=="ssh")'
nerva -l targets.txt --json | jq -r 'select(.protocol=="http") | .ip'
```

---

## `metadata` by protocol category

`metadata` is **plugin-defined**. Do not require universal keys; use defensive `.get()`.

### Remote access (ssh, rdp, telnet, vnc)

| Key | Meaning |
|-----|---------|
| `banner` | Service banner string |
| `version` | Parsed version when available |
| `algorithms` | SSH algorithm lists (ssh plugin) |
| `os` | OS hint (RDP) |

### Web (http, https)

| Key | Meaning |
|-----|---------|
| `tls` | boolean |
| `technologies` | Wappalyzer-style tech list |
| `title` | HTML page title |
| `status_code` | HTTP status |
| `server` | Server header |

### Databases (mysql, postgresql, redis, mongodb, …)

| Key | Meaning |
|-----|---------|
| `version` | Server version string |
| `auth_required` | Authentication needed |
| `error` | Error-based fingerprint data |

### Mail (smtp, imap, pop3)

| Key | Meaning |
|-----|---------|
| `banner` | Greeting banner |
| `starttls` | STARTTLS support |

### Network UDP (dns, snmp, ntp)

| Key | Meaning |
|-----|---------|
| `version` | Protocol version |
| `community` | SNMP community (if detected) |

Always inspect raw `metadata` for audit — do not drop unknown keys.

---

## CSV mapping (`--csv`)

CSV flattening uses fixed columns:

| Column | JSON equivalent |
|--------|-----------------|
| `host` | `host` |
| `ip` | `ip` |
| `port` | `port` |
| `protocol` | `protocol` |
| `transport` | `transport` |
| `tls` | often derived from `metadata.tls` for HTTP |

Nested `metadata` is **not** fully expanded in CSV — prefer `--json` for SpiderFeet.

---

## Human-readable default (no `--json`)

```
ssh://example.com:22
http://192.168.1.10:8080
```

Pattern: `{protocol}://{host}:{port}`

**Not suitable for automated parsing** — always run with `--json` in modules.

---

## Negative / empty results

| Situation | Behavior |
|-----------|----------|
| Closed port | Often no line or timeout (no record) |
| Unknown service | May omit line or `protocol` with low confidence — verify with `-v` |
| Wrong transport | Retry with `-U` or `-S` |

Module code should tolerate **zero lines** for a target (clean miss semantics).

---

## Schema stability

- Top-level keys (`host`, `ip`, `port`, `protocol`, `transport`, `metadata`) are stable per CLI reference.
- `metadata` sub-keys evolve with plugins — store raw object on nuggets for forward compatibility.

---

## Cross-reference

- Nugget mapping: [`nugget-mapping.md`](nugget-mapping.md)
- Protocol slugs: [`protocol-list.md`](protocol-list.md)
- CLI flags: [`cli-options.md`](cli-options.md)
