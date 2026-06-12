# sfp_hashes

**Conversion pattern:** `content_extract` — Parses page/content events with helpers/regex; emits derived identifiers.

## Catalogue

- **Name:** Hash Extractor
- **service_origin:** `local`
- **Summary:** Identify MD5 and SHA hashes in web content, files and more.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `HASH` | DATA | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`, `BASE64_DATA`, `LEAKSITE_CONTENT`, `RAW_DNS_RECORDS`, `RAW_FILE_META_DATA`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `helpers.extractHashesFromText`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_hashes.py`
