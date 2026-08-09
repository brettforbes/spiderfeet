# mapcidr Output and Parsing

**Capture family:** text-native (no structured CLI flag on v1.1.97).

Prefer `-silent` so stdout is only result lines. Parse those lines into a **single JSON root** with `records[]` for SpiderFeet Data Viewer / harvest — do not leave raw `.txt` as the only structured artifact, and do not invent a JSON flag on the CLI.

## Output shapes (observed)

| Mode | Typical stdout line | Notes |
|------|---------------------|-------|
| Default expand | `10.0.0.1` | One IPv4/IPv6 per line |
| Slice (`-sbc` / `-sbh`) | `10.0.0.0/26` | One CIDR per line |
| Aggregate (`-a` / `-aa`) | `10.0.0.2/31` | Minimum (or approx) subnets |
| Count (`-c`) | `256` | Single integer (not an IP list) |
| IP formats (`-if`) | hex/octal/mapped forms | Multiple lines per input when `-if 0` |
| Shuffle port (`-sp`) | `1.1.1.1:80` | `ip:port` |
| Errors | stderr `[FTL] …` | e.g. ASN without pdcp key → `unauthorized: 401` |

Without `-silent`, banners/warnings may appear; formal captures should use `-silent`.

## Harvest bundle shape (recommended)

```json
{
  "schema": "mapcidr_lines_v1",
  "tool": "mapcidr",
  "version": "v1.1.97",
  "command": "mapcidr -cidr 10.0.0.0/30 -silent",
  "started_at": "2026-08-10T00:00:00Z",
  "exit_code": 0,
  "record_count": 4,
  "records": [
    {"line": "10.0.0.0", "kind": "ipv4", "source_input": "10.0.0.0/30"},
    {"line": "10.0.0.1", "kind": "ipv4", "source_input": "10.0.0.0/30"},
    {"line": "10.0.0.2", "kind": "ipv4", "source_input": "10.0.0.0/30"},
    {"line": "10.0.0.3", "kind": "ipv4", "source_input": "10.0.0.0/30"}
  ]
}
```

`record_count` must equal `len(records)`. Derive the Text pane from `records[].line` (one line each), with a SpiderFeet capture header stating the count.

### Kind classification

| Pattern | `kind` |
|---------|--------|
| IPv4 literal | `ipv4` |
| IPv6 literal | `ipv6` |
| `addr/prefix` | `cidr` |
| `ip:port` | `ip_port` |
| integer only (count mode) | `count` |
| other format index output | `ip_format` |
| unparseable | skip or `raw` with review flag |

## Parsing steps

1. Capture full stdout/stderr; prefer `-silent` for stdout findings.
2. Split stdout on newlines; trim whitespace.
3. Skip empty lines.
4. Classify each line (IP / CIDR / IP:port / count).
5. Attach provenance: source `-cidr`/`-cl` value(s), full command, timestamp, exit code.
6. Deduplicate when building scan queues (preserve first-seen provenance).
7. Write single-root JSON bundle; derive text from `records`.

## Python sketch

```python
import ipaddress
import json
from pathlib import Path

def classify(line: str) -> dict | None:
    line = line.strip()
    if not line:
        return None
    if line.isdigit():
        return {"line": line, "kind": "count"}
    if ":" in line and line.count(":") == 1 and "/" not in line:
        host, _, port = line.partition(":")
        try:
            ipaddress.ip_address(host)
            int(port)
            return {"line": line, "kind": "ip_port", "ip": host, "port": int(port)}
        except ValueError:
            pass
    try:
        return {"line": str(ipaddress.ip_address(line)), "kind": "ipv4" if "." in line else "ipv6"}
    except ValueError:
        pass
    try:
        net = ipaddress.ip_network(line, strict=False)
        return {"line": str(net), "kind": "cidr"}
    except ValueError:
        return {"line": line, "kind": "raw"}

def lines_to_bundle(lines: list[str], command: str, source_input: str) -> dict:
    records = []
    for raw in lines:
        row = classify(raw)
        if not row:
            continue
        row["source_input"] = source_input
        records.append(row)
    return {
        "schema": "mapcidr_lines_v1",
        "tool": "mapcidr",
        "command": command,
        "record_count": len(records),
        "records": records,
    }
```

## Error shapes

Include non-zero `exit_code` and stderr text in the structured bundle when present:

```json
{
  "schema": "mapcidr_lines_v1",
  "tool": "mapcidr",
  "command": "echo AS15133 | mapcidr -silent",
  "exit_code": 1,
  "stderr": "[FTL] unauthorized: 401 (get free api key to configure from https://cloud.projectdiscovery.io/?ref=api_key)",
  "record_count": 0,
  "records": []
}
```

Empty `records: []` with metadata is valid for clean-miss / error scenarios.

## Alignment rules

- Text body line count (excluding header) = `len(records)` for expand/slice/aggregate/port modes.
- Count mode: one record with `kind: count`; text shows that integer.
- Never truncate examination captures with `head`/`tail`.
