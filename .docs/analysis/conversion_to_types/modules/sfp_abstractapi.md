# sfp_abstractapi

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** AbstractAPI
- **service_origin:** `external-api`
- **Summary:** Look up domain, phone, IP, and email reputation information from AbstractAPI.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `COMPANY_NAME` | ENTITY | yes |
| `SOCIAL_MEDIA` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `PHYSICAL_COORDINATES` | ENTITY | yes |
| `PROVIDER_TELCO` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |
| `EMAILADDR_DELIVERABLE` | DESCRIPTOR | yes |
| `EMAILADDR_UNDELIVERABLE` | DESCRIPTOR | yes |
| `EMAILADDR_DISPOSABLE` | DESCRIPTOR | yes |
| `EMAILADDR_COMPROMISED` | DESCRIPTOR | yes |

## Consumed nugget types

`DOMAIN_NAME`, `PHONE_NUMBER`, `IP_ADDRESS`, `IPV6_ADDRESS`, `EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_abstractapi.py`
