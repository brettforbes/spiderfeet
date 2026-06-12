# sfp_crt

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Certificate Transparency
- **service_origin:** `external-api`
- **Summary:** Gather hostnames from historical certificates in crt.sh.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `SSL_CERTIFICATE_RAW` | DATA | yes |
| `RAW_RIR_DATA` | DATA | yes |
| `INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `DOMAIN_NAME` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | declared only |
| `CO_HOSTED_SITE_DOMAIN` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`, `INTERNET_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.parseCert`
- `sf.resolveHost`
- `sf.validHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_crt.py`
