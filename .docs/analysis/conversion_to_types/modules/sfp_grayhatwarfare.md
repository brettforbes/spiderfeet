# sfp_grayhatwarfare

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Grayhat Warfare
- **service_origin:** `external-api`
- **Summary:** Find bucket names matching the keyword extracted from a domain from Grayhat API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `CLOUD_STORAGE_BUCKET` | ENTITY | yes |
| `CLOUD_STORAGE_BUCKET_OPEN` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_grayhatwarfare.py`
