# dnsx JSONL Output Schema

dnsx emits **JSON Lines** when `-j` / `-json` is set: one JSON object per resolved host (fields depend on enabled QUERY/PROBE flags).

**Prefer `-json` for SpiderFeet.** Use `-omit-raw` / `-or` to drop the `all` wire-format array when not needed.

## Core fields (A/AAAA validation)

Captured shape (dnsx **v1.2.3**, `scanme.nmap.org`, `-a -aaaa -cname -resp -json`):

```json
{
  "host": "scanme.nmap.org",
  "ttl": 3600,
  "resolver": ["1.0.0.1:53", "8.8.8.8:53", "8.8.4.4:53"],
  "a": ["45.33.32.156"],
  "aaaa": ["2600:3c01::f03c:91ff:fe18:bb2f"],
  "all": [
    "scanme.nmap.org.\t3600\tIN\tA\t45.33.32.156",
    "scanme.nmap.org.\t807\tIN\tAAAA\t2600:3c01::f03c:91ff:fe18:bb2f"
  ],
  "status_code": "NOERROR",
  "timestamp": "2026-08-10T03:06:05.0186962+10:00",
  "query-time": "896ms"
}
```

| Field | Type | When present |
|-------|------|--------------|
| `host` | string | Queried name (or IP for PTR) |
| `ttl` | int | Answer TTL when available |
| `resolver` | string[] | Resolvers used |
| `a` | string[] | A answers (`-a`) |
| `aaaa` | string[] | AAAA answers (`-aaaa`) |
| `cname` | string[] | CNAME answers (`-cname`) |
| `ns` | string[] | NS answers (`-ns`) |
| `txt` | string[] | TXT answers (`-txt`) |
| `mx` | string[] | MX answers (`-mx`) |
| `soa` | object[] | SOA objects (`-soa`) — `name`, `ns`, `mailbox`, `serial`, … |
| `srv` | varies | SRV answers (`-srv`) |
| `ptr` | string[] | PTR answers (`-ptr`) |
| `caa` | varies | CAA answers (`-caa`) |
| `all` | string[] | Raw RR lines (omit with `-omit-raw`) |
| `status_code` | string | DNS RCODE (e.g. `NOERROR`) |
| `timestamp` | string | Query timestamp |
| `query-time` | string | Duration string |
| CDN / ASN fields | varies | When `-cdn` / `-asn` succeed (version-dependent keys) |

Field presence is **option-dependent**. Guard with `.get()` / empty-list checks. Keys may vary slightly across dnsx versions.

## Enrichment example (MX / TXT / NS / SOA)

```json
{
  "host": "example.com",
  "mx": [""],
  "soa": [{
    "name": "example.com",
    "ns": "elliott.ns.cloudflare.com",
    "mailbox": "dns.cloudflare.com",
    "serial": 2410849323,
    "refresh": 10000,
    "retry": 2400,
    "expire": 604800,
    "minttl": 1800
  }],
  "ns": ["elliott.ns.cloudflare.com", "hera.ns.cloudflare.com"],
  "txt": ["_k2n1y4vw3qtb4skdx9e7dxt97qrmmq9", "v=spf1 -all"],
  "status_code": "NOERROR"
}
```

## PTR example

```json
{
  "host": "8.8.8.8",
  "ptr": ["dns.google"],
  "status_code": "NOERROR"
}
```

## Parsing model

1. Read stdout line by line.
2. Skip empty / non-JSON lines (and `[INF]`/`[WRN]` banners unless `-silent`).
3. `json.loads` each object defensively.
4. Expand multi-value arrays (`a`, `aaaa`, `ns`, …) into separate edges/values.
5. Bundle for harvest: `schema` (e.g. `dnsx_resolve_v1`) + `records[]` — **not** raw `.jsonl` as the Structured pane file.

```python
import json

for line in open("dnsx.jsonl", encoding="utf-8"):
    line = line.strip()
    if not line.startswith("{"):
        continue
    row = json.loads(line)
    host = row.get("host")
    for ip in row.get("a") or []:
        ...
```

## Error and empty handling

| Signal | Treat as |
|--------|----------|
| No JSONL lines | Clean miss or total failure — check stderr / `-verbose` |
| `status_code` SERVFAIL / REFUSED | Resolver/network error class — retry with `-r` / lower `-t` |
| Empty `a`/`aaaa` with NOERROR | Name exists but no address records for requested types |
| Warning: domains failed to resolve | Consider `-retry`, lower `-threads`, alternate resolvers |

Do not equate timeout, NXDOMAIN, and SERVFAIL.
