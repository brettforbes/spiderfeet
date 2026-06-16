# PIUS NDJSON Output Schema

## Format

`pius run --output ndjson` writes **one JSON object per line** to stdout. Each line is a single `Finding` struct. Internal `cidr-handle` findings are filtered out before output.

For a JSON **array** instead, use `--output json`.

## Finding object

Go `encoding/json` serializes exported struct fields with their field names (capitalized):

| Field | JSON key | Type | Description |
|-------|----------|------|-------------|
| Type | `Type` | string | `domain` or `cidr` |
| Value | `Value` | string | Domain name or CIDR block |
| Source | `Source` | string | Plugin that produced the finding (e.g. `crt-sh`, `arin`) |
| Data | `Data` | object \| null | Plugin-specific metadata |

### Type values

| `Type` | Meaning | Example `Value` |
|--------|---------|-----------------|
| `domain` | Discovered hostname | `api.acme.com` |
| `cidr` | IP network block | `203.0.113.0/24` |

Internal type `cidr-handle` (RIR org handles) is **not** emitted to NDJSON.

## Data object (common keys)

`Data` is `map[string]any`. Keys vary by plugin. Common confidence fields:

| Key | Type | Description |
|-----|------|-------------|
| `confidence` | float | 0.0–1.0 match confidence |
| `needs_review` | bool | `true` when confidence is below high threshold (~0.65) |

Unscored findings omit confidence or default to high confidence in terminal display.

### Example: high-confidence domain

```json
{"Type":"domain","Value":"api.acme.com","Source":"crt-sh","Data":null}
```

### Example: needs review

```json
{"Type":"domain","Value":"acme-holdings.example","Source":"reverse-whois","Data":{"confidence":0.42,"needs_review":true}}
```

### Example: CIDR from ARIN

```json
{"Type":"cidr","Value":"198.51.100.0/22","Source":"arin","Data":null}
```

## Terminal format (reference)

Human output maps to the same fields:

```
[domain] api.acme.com (crt-sh)
[domain] unrelated.com (github-org) ⚠ needs-review [confidence:0.40]
[cidr] 203.0.113.0/24 (arin)
```

## Parsing

### jq (NDJSON stream)

```bash
pius run --org "Acme" --domain acme.com --output ndjson \
  | jq -r 'select(.Type=="domain") | .Value'

pius run --org "Acme" --output ndjson \
  | jq -r 'select(.Type=="cidr") | .Value'

# High confidence only
pius run --org "Acme" --output ndjson \
  | jq 'select(.Data.needs_review != true)'
```

**Note:** Some README examples use lowercase `.type`; actual NDJSON uses `.Type` unless upstream adds `json` struct tags.

### Python

```python
import json
import subprocess

def pius_ndjson(org: str, domain: str | None = None):
    cmd = ["pius", "run", "--org", org, "--output", "ndjson"]
    if domain:
        cmd.extend(["--domain", domain])
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield json.loads(line)
```

## Pipeline integration

| Downstream | Select |
|------------|--------|
| Nuclei | `Type==domain` → `.Value` as URL list |
| Nmap / naabu / Nerva | `Type==cidr` → `.Value` |
| WAFWOOF / CMSeeK | domains → `https://{Value}` |
| SpiderFeet seed | map to `INTERNET_NAME` / `NETBLOCK_OWNER` |

## Negative / empty runs

Exit code 0 with no lines means no assets matched filters. Not necessarily an error — refine org name, add `--domain`, or enable more plugins/API keys.
