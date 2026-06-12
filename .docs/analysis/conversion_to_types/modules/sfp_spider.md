# sfp_spider

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Web Spider
- **service_origin:** `local`
- **Summary:** Spidering of web-pages to extract content for searching.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `WEBSERVER_HTTPHEADERS` | DATA | yes |
| `HTTP_CODE` | DATA | yes |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |
| `LINKED_URL_EXTERNAL` | SUBENTITY | declared only |
| `TARGET_WEB_CONTENT` | DATA | yes |
| `TARGET_WEB_CONTENT_TYPE` | DESCRIPTOR | yes |

## Consumed nugget types

`LINKED_URL_INTERNAL`, `INTERNET_NAME`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `helpers.extractLinksFromHtml`
- `sf.fetchUrl`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_spider.py`
