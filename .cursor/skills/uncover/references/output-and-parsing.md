# uncover Output and Parsing

Prefer **`-json` / `-j`** (JSON Lines) for SpiderFeet corpus, graph derivation, and automation. Do not use banner text as the graph source when JSONL is available.

## Streams

| Stream | Typical content |
|--------|-----------------|
| stdout | JSONL result lines (`-json`) or field-formatted lines (default / `-f`) |
| stderr / logger | Banner, version, warnings, provider errors |

Use `-silent` so stdout is results-only for pipes and harvest capture.

## JSONL schema (`-json`)

Normalized `sources.Result` (from uncover source `sources/result.go`):

| Field | Type | Notes |
|-------|------|-------|
| `timestamp` | int64 | Unix timestamp |
| `source` | string | Engine name (e.g. `shodan`, `shodan-idb`, `fofa`) |
| `ip` | string | IPv4 or IPv6 literal (may be empty) |
| `port` | int | Port number (`0` means absent/unknown for field logic) |
| `host` | string | Hostname when provided by the engine (may be empty) |
| `url` | string | URL when provided (often empty) |

`Raw` and `Error` are not marshaled into JSONL (`json:"-"`).

### Live sample (shodan-idb, **2026-08-10**)

```bash
uncover -q '1.1.1.1' -e shodan-idb -json -l 2
```

Example lines:

```json
{"timestamp":1786295459,"source":"shodan-idb","ip":"1.1.1.1","port":53,"host":"","url":""}
{"timestamp":1786295459,"source":"shodan-idb","ip":"1.1.1.1","port":443,"host":"nusd-ca.schoolloop.com","url":""}
```

## Non-JSON modes

| Mode | Flag | Use |
|------|------|-----|
| Default text | (none) | `ip:port` lines (default `-f ip:port`) |
| Custom fields | `-f` | `ip`, `port`, `host` tokens; custom templates like `https://ip:port` |
| Raw API | `-raw` / `-r` | Vendor JSON/text as returned — exploration only |
| File sink | `-o` | Write chosen format to file |

If `ip` is empty or `port` is `0` and `-f` requests `ip`/`port`, uncover may fall back to emitting **`host`** only (upstream runner logic).

## Parse steps (agents / harvest)

1. Capture stdout with `-json` (optionally `-silent`).
2. Split on newlines; skip empty / non-JSON lines (banner leakage if `-silent` omitted).
3. `json.loads` each line into a dict.
4. Normalize: strip `host`; classify `ip` with `classify_ip`; coerce `port` to int.
5. Deduplicate on `(ip, port, source)` or `(ip, port)` depending on correlation goal.
6. Bundle for Data Viewer: single JSON root with `schema`, scan metadata, and `records[]` — **not** raw `.jsonl` as the Structured pane artifact.

## Python skeleton

```python
import json
from pathlib import Path

def load_uncover_jsonl(path: str) -> list[dict]:
    records = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        records.append(json.loads(line))
    return records
```

## Empty / error shapes

- **Clean miss:** process exit 0, zero JSONL lines (or empty `records[]` after harvest).
- **Auth / quota errors:** often logged with engine label; may yield partial JSONL from other engines in multi-`-e` runs.
- **Invalid combo:** `-silent` + `-v` → fatal exit (`both verbose and silent mode specified`).

## Alignment rules (corpus)

- Text pane for JSON-native runs should be **derived** from `records[]` (e.g. `ip:port` or `host` lines), not a second text-only uncover invocation.
- `record_count` must equal `len(records)`.
