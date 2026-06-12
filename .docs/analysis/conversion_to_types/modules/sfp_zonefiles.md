# sfp_zonefiles

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** ZoneFile.io
- **service_origin:** `external-api`
- **Summary:** Search ZoneFiles.io Domain query API for domain information.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `IP_ADDRESS` | ENTITY | yes |
| `PHONE_NUMBER` | ENTITY | yes |
| `EMAILADDR` | ENTITY | declared only |
| `PROVIDER_DNS` | ENTITY | yes |
| `SOFTWARE_USED` | SUBENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_zonefiles.py`
