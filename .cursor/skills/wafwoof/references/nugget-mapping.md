# WAFWOOF → SpiderFeet Nugget Mapping

## Module

- **ID:** `sfp_tool_wafw00f`
- **Source:** `modules/sfp_tool_wafw00f.py`
- **Watched:** `INTERNET_NAME`
- **Produced:** `RAW_RIR_DATA`, `WEBSERVER_TECHNOLOGY`

## Input event

| Nugget | Role |
|--------|------|
| `INTERNET_NAME` | URL or hostname passed to wafw00f (scheme optional) |

## Output events

### `RAW_RIR_DATA`

| Aspect | Value |
|--------|--------|
| **When** | Any successful JSON parse with non-empty array |
| **Payload** | `json.dumps(result_json)` — full stdout array as string |
| **Purpose** | Preserve complete tool output for downstream parsers and audit |

Despite the nugget name, this module stores **WAF scan JSON**, not RIR registry data — legacy SpiderFoot event type reuse.

### `WEBSERVER_TECHNOLOGY`

| Aspect | Value |
|--------|--------|
| **When** | Each array element with identifiable vendor product |
| **Format** | `"<manufacturer> <firewall>"` |
| **Skipped when** | `firewall` is missing, `Generic`, or `manufacturer` missing |

### Mapping logic

```python
for waf in result_json:
    firewall = waf.get("firewall")
    manufacturer = waf.get("manufacturer")
    if not firewall or firewall == "Generic":
        continue
    if not manufacturer:
        continue
    software = " ".join(filter(None, [manufacturer, firewall]))
    emit(WEBSERVER_TECHNOLOGY, software)
```

### Examples

| JSON row | `WEBSERVER_TECHNOLOGY` |
|----------|------------------------|
| `manufacturer: "Cloudflare Inc."`, `firewall: "Cloudflare"` | `Cloudflare Inc. Cloudflare` |
| `firewall: "Generic"` | *(skipped)* |
| `firewall: "None"`, `detected: false` | *(skipped)* |
| Two named WAF rows | Two separate events |

## Graph pattern

```
INTERNET_NAME
    ├── RAW_RIR_DATA (full JSON blob)
    └── WEBSERVER_TECHNOLOGY (per named WAF)
```

## CLI manifest notes

For manifest-driven runners:

- **Command:** `wafw00f -a -o- -f json {url}`
- **Parser:** JSON array from stdout
- **No artifact file** — all data on stdout

## Clean-miss semantics

- `detected: false` with only `None`/`Generic` rows → valid clean miss for WEBSERVER_TECHNOLOGY
- `RAW_RIR_DATA` may still fire if array is non-empty (includes negative result)

## Related nuggets

WAF as web technology sits alongside CMSeeK `WEBSERVER_TECHNOLOGY` (CMS). Both can attach to the same `INTERNET_NAME` with different descriptor strings.
