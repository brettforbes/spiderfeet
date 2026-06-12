# sfp_webframework

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Web Framework Identifier
- **service_origin:** `local`
- **Summary:** Identify the usage of popular web frameworks like jQuery, YUI and others.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `URL_WEB_FRAMEWORK` | DESCRIPTOR | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`

## Parsing signals (static)

regex

**SpiderFeet/sf helpers used:**

- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_webframework.py`
