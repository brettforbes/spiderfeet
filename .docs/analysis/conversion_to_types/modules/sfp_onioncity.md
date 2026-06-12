# sfp_onioncity

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Onion.link
- **service_origin:** `external-api`
- **Summary:** Search Tor 'Onion City' search engine for mentions of the target domain using Google Custom Search.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `DARKNET_MENTION_URL` | DESCRIPTOR | yes |
| `DARKNET_MENTION_CONTENT` | DATA | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`INTERNET_NAME`, `DOMAIN_NAME`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_onioncity.py`
