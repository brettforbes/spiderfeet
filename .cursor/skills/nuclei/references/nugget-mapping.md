# Nuclei → SpiderFeet Nugget Mapping

Maps JSONL output from Nuclei to events produced by `modules/sfp_tool_nuclei.py`.

## Module contract

| Property | Value |
|----------|-------|
| Module | `sfp_tool_nuclei` |
| Watches | `INTERNET_NAME`, `IP_ADDRESS`, `NETBLOCK_OWNER` |
| Produces | `VULNERABILITY_CVE_CRITICAL`, `VULNERABILITY_CVE_HIGH`, `VULNERABILITY_CVE_MEDIUM`, `VULNERABILITY_CVE_LOW`, `VULNERABILITY_GENERAL`, `WEBSERVER_TECHNOLOGY`, `IP_ADDRESS` |

## CLI invocation (fixed)

```python
args = [
    exe,
    "-silent", "-jsonl",
    "-concurrency", "100",
    "-retries", "1",
    "-t", template_path,
    "-no-interactsh",
    "-etags", "dos,fuzz,misc",
]
# targets on stdin
```

## Decision flow

```
JSONL line parsed
    │
    ├─ host from matched-at ≠ seed target?
    │       └─ emit IP_ADDRESS or INTERNET_NAME (parent for findings)
    │
    ├─ CVE-YYYY-NNNN+ in raw line?
    │       └─ for each CVE: sf.cveInfo(cve) → VULNERABILITY_CVE_{CRITICAL|HIGH|MEDIUM|LOW}
    │
    └─ else if "matcher-name" in object
            ├─ info.severity == "info"  → WEBSERVER_TECHNOLOGY
            └─ else                     → VULNERABILITY_GENERAL
```

Lines without CVE and without `matcher-name` produce **no event**.

## Event payloads

### CVE tiers (`VULNERABILITY_CVE_*`)

- **Trigger:** `re.findall(r"CVE-\d{4}-\d{4,7}", line)` on raw JSON string
- **Data:** CVE metadata text from `SpiderFeet.cveInfo(cve)` (not raw JSON)
- **Source event:** Re-typed host event if `matched-at` host differs from scan seed

### `VULNERABILITY_GENERAL`

- **Trigger:** `matcher-name` present, no CVE regex match on line, `info.severity != "info"`
- **Data format:**

  ```
  Template: {info.name}({template-id})
  Matcher: {matcher-name}
  Matched at: {matched-at}
  Reference: <SFURL>{info.reference[0]}</SFURL>   # if reference array non-empty
  ```

### `WEBSERVER_TECHNOLOGY`

- **Trigger:** `matcher-name` present, `info.severity == "info"`
- **Data:** Same text format as `VULNERABILITY_GENERAL`
- **Meaning:** Technology fingerprint / passive detection templates

### `IP_ADDRESS` / `INTERNET_NAME` (auxiliary)

- **Trigger:** `matched-at` host component ≠ original `eventData` and host validates as IP or name
- **Purpose:** Anchor findings on the actual matched host when scan seed was a netblock or alias

## Nugget type reference

| SpiderFeet event | Nugget ID | When |
|------------------|-----------|------|
| `VULNERABILITY_CVE_CRITICAL` | CVE critical tier | CVE in line + CVSS tier |
| `VULNERABILITY_CVE_HIGH` | CVE high tier | CVE in line + CVSS tier |
| `VULNERABILITY_CVE_MEDIUM` | CVE medium tier | CVE in line + CVSS tier |
| `VULNERABILITY_CVE_LOW` | CVE low tier | CVE in line + CVSS tier |
| `VULNERABILITY_GENERAL` | Vulnerability (general) | Matcher hit, non-info severity |
| `WEBSERVER_TECHNOLOGY` | Web technology | Matcher hit, info severity |

## Example mappings

| JSONL snippet | Event type |
|---------------|------------|
| `"severity":"critical"` + `CVE-2021-44228` in line | `VULNERABILITY_CVE_CRITICAL` |
| `"severity":"info"`, `matcher-name":"nginx"` | `WEBSERVER_TECHNOLOGY` |
| `"severity":"medium"`, `matcher-name":"panel`, no CVE | `VULNERABILITY_GENERAL` |
| `matched-at` → `203.0.113.5`, seed was `NETBLOCK` | `IP_ADDRESS` then finding |

## Future / CLI framework generalisation

From `.docs/analysis/conversion_to_types/examples/sfp_tool_nuclei.md`:

- Prefer `JsonLinesParser` with YAML mapping: `template-id` / `matcher-name` → nugget type table
- Consider reading `info.classification.cve-id` instead of line regex
- Map `info.tags` containing `tech` → `WEBSERVER_TECHNOLOGY` even when severity mis-tagged

## Parser guardrails

- Wrap `json.loads` in try/except; skip malformed lines
- `KeyError` on `matched-at`, `info`, `matcher-name` — log and continue
- Do not treat zero JSONL lines as error if process succeeded (clean scan)

## Related

- [jsonl-output-schema.md](jsonl-output-schema.md)
- `modules/sfp_tool_nuclei.py`
- `.docs/analysis/conversion_to_types/examples/sfp_tool_nuclei.md`
