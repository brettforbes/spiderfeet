# sfp_pastebin

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** PasteBin
- **service_origin:** `external-api`
- **Summary:** PasteBin search (via Google Search API) to identify related content.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `LEAKSITE_CONTENT` | DATA | yes |
| `LEAKSITE_URL` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`, `INTERNET_NAME`, `EMAILADDR`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_pastebin.py`
