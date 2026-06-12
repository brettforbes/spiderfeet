# sfp_ethereum

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Ethereum Address Extractor
- **service_origin:** `local`
- **Summary:** Identify ethereum addresses in scraped webpages.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `ETHEREUM_ADDRESS` | ENTITY | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`

## Parsing signals (static)

regex

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_ethereum.py`
