# Subfinder JSONL Output Schema

Subfinder emits **JSON Lines** when `-oJ` / `-json` is set: one JSON object per discovered host per line. Plain text mode prints FQDNs only.

## Base record (passive, `-oJ`)

```json
{"host":"api.example.com"}
```

| Field | Type | Description |
|-------|------|-------------|
| `host` | string | Discovered FQDN (lowercase in practice) |

## With source attribution (`-oJ -cs`)

```json
{"host":"api.example.com","source":"crtsh"}
```

Some versions emit `sources` as an array when multiple providers report the same host:

```json
{"host":"api.example.com","sources":["crtsh","hackertarget"]}
```

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Single reporting passive source (variant) |
| `sources` | string[] | All sources that reported the host |

Use `-cs` for corpus provenance and confidence scoring.

## With IP addresses (`-active -oJ -oI`)

Requires **active** resolution (`-active` / `-nW`):

```json
{"host":"api.example.com","ip":"203.0.113.10"}
```

| Field | Type | Description |
|-------|------|-------------|
| `ip` | string | Resolved IPv4 (or IPv6 depending on resolver) |

Multiple A records may appear as duplicate host lines with different IPs, or a single line depending on version — **dedupe and merge** in conversion scripts.

## Full JSONL example file

```jsonl
{"host":"www.example.com"}
{"host":"api.example.com","source":"crtsh"}
{"host":"staging.example.com","sources":["crtsh","securitytrails"]}
{"host":"mail.example.com","ip":"198.51.100.5"}
```

## Plain text variants (not JSONL)

| Flags | Line format |
|-------|-------------|
| default | `sub.example.com` |
| `-active -oI` (no `-oJ`) | `sub.example.com,203.0.113.10` |
| `-silent` | host only, no banner |

**Do not** parse plain text when `-oJ` is available.

## Parsing rules

1. Skip blank lines and lines not starting with `{`.
2. Normalize `host`: lowercase, strip trailing dot.
3. Ignore hosts not suffix-matching the seed domain unless out-of-scope pivot is intentional.
4. When both `source` and `sources` exist, prefer `sources` array.
5. Treat missing `ip` as passive-only — validate with **dnsx** before port scan.

## Python parser sketch

```python
import json

def iter_subfinder_jsonl(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("{"):
                continue
            row = json.loads(line)
            host = row["host"].lower().rstrip(".")
            yield {
                "host": host,
                "ip": row.get("ip"),
                "sources": row.get("sources") or (
                    [row["source"]] if row.get("source") else []
                ),
            }
```

## Relationship to SpiderFeet

See [`nugget-mapping.md`](nugget-mapping.md) for `nodes[]` / `edges[]` emission from parsed rows.
