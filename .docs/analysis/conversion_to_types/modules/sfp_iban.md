# sfp_iban

**Conversion pattern:** `content_extract` — Parses page/content events with helpers/regex; emits derived identifiers.

## Catalogue

- **Name:** IBAN Number Extractor
- **service_origin:** `local`
- **Summary:** Identify International Bank Account Numbers (IBANs) in any data.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IBAN_NUMBER` | ENTITY | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`, `DARKNET_MENTION_CONTENT`, `LEAKSITE_CONTENT`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `helpers.extractIbansFromText`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_iban.py`
