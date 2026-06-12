# sfp_googlesearch

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Google
- **service_origin:** `external-api`
- **Summary:** Obtain information from the Google Custom Search API to identify sub-domains and links.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`INTERNET_NAME`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_googlesearch.py`
