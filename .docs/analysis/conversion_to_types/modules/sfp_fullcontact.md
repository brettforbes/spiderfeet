# sfp_fullcontact

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** FullContact
- **service_origin:** `external-api`
- **Summary:** Gather domain and e-mail information from FullContact.com API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `RAW_RIR_DATA` | DATA | yes |
| `PHONE_NUMBER` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `PHYSICAL_ADDRESS` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`, `EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_fullcontact.py`
