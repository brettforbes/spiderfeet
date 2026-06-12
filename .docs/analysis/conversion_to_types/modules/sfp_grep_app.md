# sfp_grep_app

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** grep.app
- **service_origin:** `external-api`
- **Summary:** Search grep.app API for links and emails related to the specified domain.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `DOMAIN_NAME` | ENTITY | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | yes |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `helpers.extractEmailsFromText`
- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_grep_app.py`
