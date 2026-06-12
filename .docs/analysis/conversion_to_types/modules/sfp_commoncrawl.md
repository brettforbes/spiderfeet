# sfp_commoncrawl

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** CommonCrawl
- **service_origin:** `external-api`
- **Summary:** Searches for URLs found through CommonCrawl.org.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |

## Consumed nugget types

`INTERNET_NAME`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_commoncrawl.py`
