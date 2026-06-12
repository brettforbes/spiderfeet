# sfp_base64

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Base64 Decoder
- **service_origin:** `local`
- **Summary:** Identify Base64-encoded strings in URLs, often revealing interesting hidden information.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `BASE64_DATA` | DATA | yes |

## Consumed nugget types

`LINKED_URL_INTERNAL`

## Parsing signals (static)

regex

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_base64.py`
