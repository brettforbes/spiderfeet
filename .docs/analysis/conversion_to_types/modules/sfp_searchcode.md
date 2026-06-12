# sfp_searchcode

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** searchcode
- **service_origin:** `external-api`
- **Summary:** Search searchcode for code repositories mentioning the target domain.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |
| `PUBLIC_CODE_REPO` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

_Additional types seen in code but not in producedEvents():_ `INTERNET_NAME`, `INTERNET_NAME_UNRESOLVED`

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `helpers.extractEmailsFromText`
- `sf.fetchUrl`
- `sf.resolveHost`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_searchcode.py`
