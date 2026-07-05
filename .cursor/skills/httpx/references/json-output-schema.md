# httpx JSONL Output Schema

httpx emits **JSON Lines** when `-j` / `-json` is set: one JSON object per successful probe (or per configured output mode) per line.

## Core fields (typical probe)

```json
{
  "timestamp": "2026-06-01T12:00:00.000000Z",
  "url": "https://api.example.com",
  "input": "api.example.com",
  "status_code": 200,
  "title": "Example API",
  "webserver": "nginx/1.18.0",
  "content_type": "text/html",
  "content_length": 1234,
  "method": "GET",
  "host": "api.example.com",
  "path": "/",
  "scheme": "https",
  "port": "443",
  "response_time": "125ms"
}
```

| Field | Type | When present |
|-------|------|--------------|
| `url` | string | Final probed URL (after redirects if followed) |
| `input` | string | Original input line |
| `status_code` | int | HTTP status |
| `title` | string | HTML `<title>` when `-title` |
| `webserver` | string | Server header when `-server` / `-web-server` |
| `tech` | string[] | Wappalyzer-style names when `-tech-detect` / `-td` |
| `content_type` | string | `-content-type` / `-ct` |
| `content_length` | int | `-content-length` / `-cl` |
| `location` | string | Redirect target when `-location` |
| `host` | string | Host part |
| `ip` | string | When `-ip` |
| `cname` | string | When `-cname` |
| `cdn_name` / `cdn` | string | When `-cdn` |
| `asn` | object/string | When `-asn` |
| `favicon` | string | mmh3 hash when `-favicon` |
| `jarm` | string | When `-jarm` |
| `response_time` | string | When `-response-time` / `-rt` |
| `failed` | bool | Probe failure |
| `probe` | bool | Success flag with `-probe` |

Field names may vary slightly by httpx version — guard parsing with `.get()`.

## With response headers (`-irh`)

Adds `header` map or `response_headers` (version-dependent):

```json
{
  "url": "https://example.com",
  "status_code": 200,
  "header": {
    "server": ["nginx/1.18.0"],
    "content-type": ["text/html"]
  }
}
```

Use for **`WEBSERVER_HTTPHEADERS`** nugget mapping (serialize header map).

## With redirect chain (`-include-chain`)

```json
{
  "url": "https://www.example.com/",
  "status_code": 200,
  "chain": [
    {"url": "http://example.com", "status_code": 301},
    {"url": "https://example.com", "status_code": 301},
    {"url": "https://www.example.com/", "status_code": 200}
  ]
}
```

Emit intermediate URLs as **`LINKED_URL_INTERNAL`** with redirect edges when scenario requires full chain.

## With stored response (`-irr`, `-store-response`)

May include `raw` / `body` / base64 fields — **large**. Use only in explicit examination scenarios; map body to **`TARGET_WEB_CONTENT`** with size caps.

## With screenshot (`-screenshot` + `-json`)

DOM/body preview fields may appear; screenshot paths on disk — reference as metadata, not inline nugget `data`.

## Plain text output (not JSONL)

| Mode | Example line |
|------|----------------|
| `-silent` | `https://example.com` |
| `-status-code -title` | `https://example.com [200] [Title]` |
| `-probe` | `https://example.com [SUCCESS]` |

## Parsing rules

1. Skip blank lines and non-`{` prefixes.
2. Normalize URL: lowercase host when comparing; preserve scheme/path in `LINKED_URL_INTERNAL`.
3. Expand `tech` array to multiple **`WEBSERVER_TECHNOLOGY`** nodes.
4. Deduplicate on canonical URL + status when merging passes.
5. At **harvest**, convert JSONL → bundle: `schema: httpx_probe_v1`, `records[]`, metadata — not raw `.jsonl` as structured artifact.

## Python iterator sketch

```python
import json

def iter_httpx_jsonl(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("{"):
                continue
            yield json.loads(line)
```

See [`nugget-mapping.md`](nugget-mapping.md) for graph emission.
