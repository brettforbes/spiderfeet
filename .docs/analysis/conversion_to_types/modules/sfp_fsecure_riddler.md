# sfp_fsecure_riddler

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** F-Secure Riddler.io
- **service_origin:** `external-api`
- **Summary:** Obtain network information from F-Secure Riddler.io API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `DOMAIN_NAME` | ENTITY | yes |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | yes |
| `IP_ADDRESS` | ENTITY | yes |
| `PHYSICAL_COORDINATES` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`DOMAIN_NAME`, `INTERNET_NAME`, `INTERNET_NAME_UNRESOLVED`, `IP_ADDRESS`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_fsecure_riddler.py`
