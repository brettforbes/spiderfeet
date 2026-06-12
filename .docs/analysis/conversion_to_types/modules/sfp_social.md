# sfp_social

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Social Network Identifier
- **service_origin:** `local`
- **Summary:** Identify presence on social media networks such as LinkedIn, Twitter and others.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `SOCIAL_MEDIA` | ENTITY | yes |
| `USERNAME` | ENTITY | yes |

## Consumed nugget types

`LINKED_URL_EXTERNAL`

## Parsing signals (static)

regex

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_social.py`
