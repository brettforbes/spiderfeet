# sfp_crossref

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Cross-Referencer
- **service_origin:** `local`
- **Summary:** Identify whether other domains are associated ('Affiliates') of the target by looking for links back to the target site(s).

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `AFFILIATE_INTERNET_NAME` | ENTITY | yes |
| `AFFILIATE_WEB_CONTENT` | DATA | yes |

## Consumed nugget types

`LINKED_URL_EXTERNAL`, `SIMILARDOMAIN`, `CO_HOSTED_SITE`, `DARKNET_MENTION_URL`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.resolveHost`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_crossref.py`
