# sfp_myspace

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** MySpace
- **service_origin:** `external-api`
- **Summary:** Gather username and location from MySpace.com profiles.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `SOCIAL_MEDIA` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | yes |

## Consumed nugget types

`EMAILADDR`, `SOCIAL_MEDIA`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_myspace.py`
