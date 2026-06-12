# sfp_zetalytics

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Zetalytics
- **service_origin:** `external-api`
- **Summary:** Query the Zetalytics database for hosts on your target domain(s).

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |

## Consumed nugget types

`INTERNET_NAME`, `DOMAIN_NAME`, `EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_zetalytics.py`
