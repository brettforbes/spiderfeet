# sfp_dnsdumpster

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** DNSDumpster
- **service_origin:** `external-api`
- **Summary:** Passive subdomain enumeration using HackerTarget's DNSDumpster

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`, `INTERNET_NAME`

## Parsing signals (static)

fetchUrl, regex, BeautifulSoup

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_dnsdumpster.py`
