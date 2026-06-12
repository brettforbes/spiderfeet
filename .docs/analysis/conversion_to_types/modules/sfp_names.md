# sfp_names

**Conversion pattern:** `regex_local` — Primarily regex over event.data or fetched reference files.

## Catalogue

- **Name:** Human Name Extractor
- **service_origin:** `local`
- **Summary:** Attempt to identify human names in fetched content.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `HUMAN_NAME` | ENTITY | yes |

## Consumed nugget types

`TARGET_WEB_CONTENT`, `EMAILADDR`, `DOMAIN_WHOIS`, `NETBLOCK_WHOIS`, `RAW_RIR_DATA`, `RAW_FILE_META_DATA`

## Parsing signals (static)

regex

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_names.py`
