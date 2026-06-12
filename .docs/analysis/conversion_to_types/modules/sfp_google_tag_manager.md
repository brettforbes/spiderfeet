# sfp_google_tag_manager

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Google Tag Manager
- **service_origin:** `external-api`
- **Summary:** Search Google Tag Manager (GTM) for hosts sharing the same GTM code.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `DOMAIN_NAME` | ENTITY | declared only |
| `INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |

## Consumed nugget types

`WEB_ANALYTICS_ID`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_google_tag_manager.py`
