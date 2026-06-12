# sfp_accounts

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Account Finder
- **service_origin:** `local`
- **Summary:** Look for possible associated accounts on over 500 social and other websites such as Instagram, Reddit, etc.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `USERNAME` | ENTITY | yes |
| `ACCOUNT_EXTERNAL_OWNED` | ENTITY | yes |
| `SIMILAR_ACCOUNT_EXTERNAL` | ENTITY | yes |

## Consumed nugget types

`EMAILADDR`, `DOMAIN_NAME`, `HUMAN_NAME`, `USERNAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_accounts.py`
