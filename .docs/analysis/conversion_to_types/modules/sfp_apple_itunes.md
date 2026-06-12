# sfp_apple_itunes

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Apple iTunes
- **service_origin:** `external-api`
- **Summary:** Search Apple iTunes for mobile apps.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `APPSTORE_ENTRY` | ENTITY | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |
| `AFFILIATE_INTERNET_NAME` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_apple_itunes.py`
