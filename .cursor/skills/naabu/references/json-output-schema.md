# Naabu JSON / JSONL Output Schema

Agents must use **`naabu -json`** (or `-j`). Output is **JSON Lines** — one object per discovered open port (not a JSON array).

Captured from **naabu v2.6.1** on **2026-08-10** (`C:\projects\spiderfeet\.tools\naabu\naabu.exe`).

## Observed CONNECT record (this binary)

```json
{"host":"scanme.nmap.org","ip":"45.33.32.156","timestamp":"2026-08-09T17:10:11.4414392Z","port":80,"protocol":"tcp","tls":false}
{"host":"scanme.nmap.org","ip":"2600:3c01::f03c:91ff:fe18:bb2f","timestamp":"2026-08-09T17:10:11.4367541Z","port":80,"protocol":"tcp","tls":false}
```

PD Running docs also show minimal lines:

```json
{"ip":"104.16.99.52","port":443}
{"ip":"104.16.99.52","port":80}
```

## Fields

| Field | Type | When present | Description |
|-------|------|--------------|-------------|
| `ip` | string | Usually | Target IP (IPv4 or IPv6) |
| `host` | string | Hostname scans | Hostname associated with result |
| `port` | int | Always on hits | Open port number |
| `protocol` | string | This build | e.g. `tcp` (UDP when scanning `u:` ports) |
| `tls` | bool | This build | TLS observed on port |
| `timestamp` | string | This build | UTC timestamp of finding |
| `cdn` | bool/string | `-cdn` / `-ec` context | CDN/WAF attribution when enabled |
| service / version fields | varies | `-sD` / `-sV` | Inspect sample lines from your run before hard-coding keys |

Always sample one line from the installed version before locking parsers.

## Text output (non-JSON)

Default human format (example from PD docs):

```text
hackerone.com:443
hackerone.com:80
```

Use **`-silent`** for pipe-friendly `host:port` lines without banner:

```bash
naabu -host example.com -silent -duc
echo example.com | naabu -silent -duc
```

For SpiderFeet ontology/graph, prefer **`-json`** and derive human text at harvest when needed.

## CSV mode

`-csv` writes spreadsheet-friendly output — use only when the operator requests; prefer `-json` for nuggets.

## Parsing rules

1. Parse **line-by-line**; skip empty / non-JSON lines.
2. Deduplicate by `{ip|host}:{port}:{protocol}`.
3. Classify `ip` with `core.ip_classify.classify_ip` (IPv4 vs IPv6).
4. UDP input uses `u:53` syntax (PD Running docs); map `protocol`/`u:` to `UDP_PORT_OPEN` when applicable.
5. **Passive** (`-passive`) results come from Shodan InternetDB — treat provenance separately from active SYN/CONNECT.
6. Empty file / zero lines with exit success = **clean_miss**.

## Python parse sketch

```python
import json

def iter_naabu_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

for row in iter_naabu_jsonl("naabu.jsonl"):
    host = row.get("host") or row["ip"]
    print(host, row["port"], row.get("protocol", "tcp"))
```

## Pipe to downstream tools

```bash
echo example.com | naabu -silent -duc | httpx -silent
naabu -host example.com -json -silent -duc | jq -r '(.host // .ip) + ":" + (.port|tostring)'
```
