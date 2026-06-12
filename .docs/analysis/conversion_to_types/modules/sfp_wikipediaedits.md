# sfp_wikipediaedits

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Wikipedia Edits
- **service_origin:** `external-api`
- **Summary:** Identify edits to Wikipedia articles made from a given IP address or username.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `WIKIPEDIA_PAGE_EDIT` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `USERNAME`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_wikipediaedits.py`
