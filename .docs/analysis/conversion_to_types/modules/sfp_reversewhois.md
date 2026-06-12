# sfp_reversewhois

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** ReverseWhois
- **service_origin:** `external-api`
- **Summary:** Reverse Whois lookups using reversewhois.io.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `AFFILIATE_INTERNET_NAME` | ENTITY | yes |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | yes |
| `DOMAIN_REGISTRAR` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

fetchUrl, regex, BeautifulSoup

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_reversewhois.py`
