# sfp_company

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Company Name Extractor
- **service_origin:** `local`
- **Summary:** Identify company names in any obtained data.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `COMPANY_NAME` | ENTITY | declared only |
| `AFFILIATE_COMPANY_NAME` | ENTITY | declared only |

## Consumed nugget types

`TARGET_WEB_CONTENT`, `SSL_CERTIFICATE_ISSUED`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `AFFILIATE_DOMAIN_WHOIS`, `AFFILIATE_WEB_CONTENT`

## Parsing signals (static)

regex

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_company.py`
