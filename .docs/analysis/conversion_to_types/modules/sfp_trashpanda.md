# sfp_trashpanda

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Trashpanda
- **service_origin:** `external-api`
- **Summary:** Queries Trashpanda to gather intelligence about mentions of target in pastesites

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `LEAKSITE_CONTENT` | DATA | yes |
| `LEAKSITE_URL` | ENTITY | yes |
| `PASSWORD_COMPROMISED` | DATA | yes |

## Consumed nugget types

`DOMAIN_NAME`, `INTERNET_NAME`, `EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_trashpanda.py`
