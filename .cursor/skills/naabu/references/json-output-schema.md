# Naabu JSON / JSONL Output Schema

Agents must use **`naabu -json`** (or `-j`). Output is **JSON Lines** — one object per discovered port (not a JSON array).

## Minimal record

```json
{"ip":"104.16.99.52","port":443}
{"ip":"104.16.99.52","port":80}
```

## Common fields (by version / flags)

| Field | Type | When present | Description |
|-------|------|--------------|-------------|
| `ip` | string | Usually | Target IP address |
| `host` | string | DNS scans | Hostname associated with result |
| `port` | int | Always | TCP or UDP port number |
| `protocol` | string | Some builds | `tcp` or `udp` |
| `tls` | bool | Some builds | TLS detected on port |
| `cdn` | bool/string | `-cdn` / `-exclude-cdn` | CDN/WAF attribution when enabled |
| `service` | string | `-sD` / `-sV` | Service name from discovery or version probe |
| `version` | string | `-sV` | Service version string |

Always inspect a sample line from your installed version before hard-coding optional keys.

## Text output (non-JSON)

Default human format:

```
hackerone.com:443
hackerone.com:80
```

Use **`-silent`** for pipe-friendly host:port lines without banner:

```bash
naabu -host example.com -silent
echo example.com | naabu -silent
```

## CSV mode

`-csv` writes spreadsheet-friendly output — use only when operator requests; prefer `-json` for nuggets.

## Parsing rules

1. Parse **line-by-line**; skip empty lines.
2. Deduplicate by `{ip|host}:{port}:{protocol}`.
3. UDP ports in input use `u:53` format; output may include protocol metadata.
4. **Passive mode** (`-passive`) results come from Shodan InternetDB — treat provenance separately from active SYN/CONNECT.
5. Do not emit `TCP_PORT_OPEN` for CDN-excluded skipped ports unless policy says otherwise.

## Python parse sketch

```python
import json

def iter_naabu_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)

for row in iter_naabu_jsonl("naabu.jsonl"):
    host = row.get("host") or row["ip"]
    print(host, row["port"])
```

## Pipe to downstream tools

```bash
naabu -host example.com -json -silent | httpx -silent
naabu -host example.com -json -silent | nerva --json
```

For Nerva, convert JSON lines to `host:port` if needed:

```bash
naabu -host example.com -json -silent | jq -r '(.host // .ip) + ":" + (.port|tostring)'
```
