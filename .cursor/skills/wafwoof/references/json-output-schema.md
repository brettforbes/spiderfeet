# WAFWOOF JSON Output Schema

## Format

`wafw00f` with `-o- -f json` (or `-o file.json`) emits a **JSON array** of result objects. One URL may produce **multiple** objects when `-a` / `--findall` matches several products or adds a generic detection row.

Parse with `json.loads(stdout)` — expect `list`, not a single object.

## Record schema

Built by `buildResultRecord()` in `wafw00f/main.py`:

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Target URL tested (scheme normalized) |
| `detected` | boolean | `true` if a WAF signature or generic behaviour matched |
| `trigger_url` | string \| null | URL of the request that triggered detection (attack URL) |
| `firewall` | string | Product name, `Generic`, or `None` |
| `manufacturer` | string | Vendor name, `Unknown`, or `None` |

### `firewall` / `manufacturer` values

| Scenario | `detected` | `firewall` | `manufacturer` |
|----------|------------|------------|----------------|
| Named WAF match | `true` | Product (before parenthesis) | Vendor (inside parenthesis) |
| Generic WAF behaviour | `true` | `Generic` | `Unknown` |
| No WAF detected | `false` | `None` | `None` |

Internal WAF names in code look like `"Cloudflare (Cloudflare Inc.)"` — split into `firewall: "Cloudflare"`, `manufacturer: "Cloudflare Inc."`.

## Example: Cloudflare detected

```json
[
  {
    "detected": true,
    "firewall": "Cloudflare",
    "manufacturer": "Cloudflare Inc.",
    "trigger_url": "https://example.com/?xss=...",
    "url": "https://example.com/"
  }
]
```

## Example: findall with generic fallback

With `-a`, you may see multiple named products plus a generic row:

```json
[
  {
    "detected": true,
    "firewall": "Cloudflare",
    "manufacturer": "Cloudflare Inc.",
    "trigger_url": "https://example.com/...",
    "url": "https://example.com/"
  },
  {
    "detected": true,
    "firewall": "Generic",
    "manufacturer": "Unknown",
    "trigger_url": "https://example.com/...",
    "url": "https://example.com/"
  }
]
```

## Example: no WAF

```json
[
  {
    "detected": false,
    "firewall": "None",
    "manufacturer": "None",
    "trigger_url": null,
    "url": "https://example.com/"
  }
]
```

## CSV export (alternative)

With `-o file.csv`, columns match dict keys: `url`, `detected`, `trigger_url`, `firewall`, `manufacturer`.

## Parsing notes

- Empty stdout → no result (SpiderFeet logs debug and returns).
- Non-zero exit code → treat as tool error; stderr may contain diagnostics.
- **Do not use TextFSM** — native JSON.
- When piping, use `-o- -f json` explicitly; `-o json` alone is invalid (must be filename or `-`).

## jq examples

```bash
# All detected product names
wafw00f -a -o- -f json https://example.com | jq '.[].firewall'

# Named WAFs only (exclude Generic/None)
wafw00f -a -o- -f json https://example.com | jq '.[] | select(.firewall != "Generic" and .firewall != "None")'

# Any detection
wafw00f -o- -f json https://example.com | jq 'any(.[]; .detected)'
```

## Python (SpiderFeet pattern)

```python
result_json = json.loads(stdout)
evt = SpiderFeetEvent("RAW_RIR_DATA", json.dumps(result_json), module, parent)
for waf in result_json:
    firewall = waf.get("firewall")
    manufacturer = waf.get("manufacturer")
    if firewall and firewall not in ("Generic", "None") and manufacturer:
        software = f"{manufacturer} {firewall}"
        notify(WEBSERVER_TECHNOLOGY, software)
```
