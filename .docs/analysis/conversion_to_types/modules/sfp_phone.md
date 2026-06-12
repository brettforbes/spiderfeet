# sfp_phone

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Phone Number Extractor
- **service_origin:** `local`
- **Summary:** Identify phone numbers in scraped webpages.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `PHONE_NUMBER` | ENTITY | yes |
| `PROVIDER_TELCO` | ENTITY | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `PHONE_NUMBER`

## Parsing signals (static)

_(none detected)_

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_phone.py`
