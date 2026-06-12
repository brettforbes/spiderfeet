# sfp_errors

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Error String Extractor
- **service_origin:** `local`
- **Summary:** Identify common error messages in content like SQL errors, etc.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `ERROR_MESSAGE` | DATA | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`

## Parsing signals (static)

regex

**SpiderFeet/sf helpers used:**

- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_errors.py`
