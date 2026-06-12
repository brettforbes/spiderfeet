# sfp_c99

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** C99
- **service_origin:** `external-api`
- **Summary:** Queries the C99 API which offers various data (geo location, proxy detection, phone lookup, etc).

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | yes |
| `PROVIDER_TELCO` | ENTITY | yes |
| `PHYSICAL_ADDRESS` | ENTITY | yes |
| `PHYSICAL_COORDINATES` | ENTITY | yes |
| `PROVIDER_DNS` | ENTITY | declared only |
| `IP_ADDRESS` | ENTITY | yes |
| `USERNAME` | ENTITY | yes |
| `ACCOUNT_EXTERNAL_OWNED` | ENTITY | yes |
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | yes |
| `PROVIDER_HOSTING` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | yes |

_Additional types seen in code but not in producedEvents():_ `DOMAIN_NAME`

## Consumed nugget types

`DOMAIN_NAME`, `PHONE_NUMBER`, `IP_ADDRESS`, `USERNAME`, `EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.validHost`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_c99.py`
