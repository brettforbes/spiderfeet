# sfp_duckduckgo

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** DuckDuckGo
- **service_origin:** `external-api`
- **Summary:** Query DuckDuckGo's API for descriptive information about your target.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `DESCRIPTION_CATEGORY` | DESCRIPTOR | declared only |
| `DESCRIPTION_ABSTRACT` | DESCRIPTOR | declared only |
| `AFFILIATE_DESCRIPTION_CATEGORY` | DESCRIPTOR | declared only |
| `AFFILIATE_DESCRIPTION_ABSTRACT` | DESCRIPTOR | declared only |

## Consumed nugget types

`DOMAIN_NAME`, `DOMAIN_NAME_PARENT`, `INTERNET_NAME`, `AFFILIATE_INTERNET_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.hostDomain`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_duckduckgo.py`
