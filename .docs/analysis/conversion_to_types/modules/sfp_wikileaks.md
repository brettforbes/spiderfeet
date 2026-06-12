# sfp_wikileaks

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Wikileaks
- **service_origin:** `external-api`
- **Summary:** Search Wikileaks for mentions of domain names and e-mail addresses.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `LEAKSITE_CONTENT` | DATA | declared only |
| `LEAKSITE_URL` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`, `EMAILADDR`, `HUMAN_NAME`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `helpers.extractLinksFromHtml`
- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_wikileaks.py`
