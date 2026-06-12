# sfp_webanalytics

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Web Analytics Extractor
- **service_origin:** `local`
- **Summary:** Identify web analytics IDs in scraped webpages and DNS TXT records.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `WEB_ANALYTICS_ID` | ENTITY | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`, `DNS_TEXT`

## Parsing signals (static)

regex

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_webanalytics.py`
