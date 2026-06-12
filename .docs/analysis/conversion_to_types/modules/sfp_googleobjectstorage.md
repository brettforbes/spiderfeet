# sfp_googleobjectstorage

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Google Object Storage Finder
- **service_origin:** `external-api`
- **Summary:** Search for potential Google Object Storage buckets associated with the target and attempt to list their contents.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `CLOUD_STORAGE_BUCKET` | ENTITY | yes |
| `CLOUD_STORAGE_BUCKET_OPEN` | DESCRIPTOR | yes |

## Consumed nugget types

`DOMAIN_NAME`, `LINKED_URL_EXTERNAL`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_googleobjectstorage.py`
