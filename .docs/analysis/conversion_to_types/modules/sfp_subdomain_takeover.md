# sfp_subdomain_takeover

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Subdomain Takeover Checker
- **service_origin:** `local`
- **Summary:** Check if affiliated subdomains are vulnerable to takeover.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `AFFILIATE_INTERNET_NAME_HIJACKABLE` | ENTITY | yes |

## Consumed nugget types

`AFFILIATE_INTERNET_NAME`, `AFFILIATE_INTERNET_NAME_UNRESOLVED`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_subdomain_takeover.py`
