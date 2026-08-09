# tldfinder Output Schema and Parsing

tldfinder emits **JSON Lines** when `-oJ` / `-json` is set: one JSON object per discovered host per line. Plain text mode prints domains only (plus banners unless `-silent`).

Evidence: **v0.0.2**, samples captured **2026-08-10** against private TLD input `google`.

## Base record (`-oJ`)

Even without `-cs`, v0.0.2 commonly includes `source` and `input`:

```json
{"host":"docs.sandbox.google","input":"google","source":"crtsh"}
```

| Field | Type | Description |
|-------|------|-------------|
| `host` | string | Discovered FQDN / name under the private TLD |
| `input` | string | Seed passed to `-d` |
| `source` | string | Reporting source for this line |

## With multi-source collection (`-oJ -cs`)

```json
{"host":"storage.google","input":"google","sources":["crtsh"]}
```

| Field | Type | Description |
|-------|------|-------------|
| `sources` | string[] | All sources that reported the host |

Use `-cs` for corpus provenance. Merge duplicate `host` lines and union `sources`.

## With IP addresses (`-active -oJ -oI`)

Requires **active** resolution (`-active` / `-nW`):

```json
{"host":"cache2.c.play.google","ip":"142.250.183.46","input":"google","source":"crtsh"}
```

| Field | Type | Description |
|-------|------|-------------|
| `ip` | string | Resolved address from active mode |

Classify IPs with SpiderFeet `core.ip_classify.classify_ip` (never hard-code `IP_ADDRESS` for colon-form values).

## Discovery-mode shape notes

| Mode (`-dm`) | Observed character (v0.0.2 samples) |
|--------------|-------------------------------------|
| `dns` (default) | Hosts under the private TLD (e.g. `*.google`) |
| `tld` | Names combining the label with other TLDs (e.g. `google.wf`) — treat carefully vs public namespace collisions |
| `domain` | Alternate mode; may be slower / sparse depending on sources |

## Plain text variants (not for formal examination)

| Flags | Line format |
|-------|-------------|
| (default) | Banner + progress + host lines |
| `-silent` | Hosts only — good for pipes |
| `-o file` | Hosts written to file |

**Structured-first:** Prefer `-oJ` for SpiderFeet harvest. Do not create a separate text-only examination scenario when JSONL is available. At harvest, wrap JSONL into a single-root JSON bundle (`schema` + `records[]`) for the Structured pane — do not store raw `.jsonl` as the examination structured artifact.

## Parsing workflow

1. Capture stdout (findings) separately from stderr (banners / `[INF]`).
2. Parse each non-empty stdout line as JSON; skip non-JSON lines.
3. Normalize `host` (`lowercase`, strip trailing `.`).
4. Retain `input`, `source` / `sources`, and optional `ip`.
5. Deduplicate on normalized `host` (merge sources; keep IP variants as edges).
6. Build nugget graph from the structured bundle (see `nugget-mapping.md`).

## Python sketch

```python
import json
from pathlib import Path

records = []
for line in Path("google.jsonl").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line.startswith("{"):
        continue
    records.append(json.loads(line))

bundle = {
    "schema": "tldfinder_finding_v1",
    "tool": "tldfinder",
    "record_count": len(records),
    "records": records,
}
```

## Edge handling

- Empty `records: []` is a valid clean-miss structured artifact.
- Distinguish parse failures (invalid JSON lines) from true zero findings.
- Preserve raw `host` strings before normalization for forensic traceability.
