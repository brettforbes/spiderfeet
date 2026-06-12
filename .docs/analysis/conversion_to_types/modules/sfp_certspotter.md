# sfp_certspotter

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** CertSpotter
- **service_origin:** `external-api`
- **Summary:** Gather information about SSL certificates from SSLMate CertSpotter API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `DOMAIN_NAME` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | declared only |
| `CO_HOSTED_SITE_DOMAIN` | ENTITY | yes |
| `SSL_CERTIFICATE_ISSUED` | ENTITY | yes |
| `SSL_CERTIFICATE_ISSUER` | ENTITY | yes |
| `SSL_CERTIFICATE_MISMATCH` | DESCRIPTOR | declared only |
| `SSL_CERTIFICATE_EXPIRED` | DESCRIPTOR | yes |
| `SSL_CERTIFICATE_EXPIRING` | DESCRIPTOR | yes |
| `SSL_CERTIFICATE_RAW` | DATA | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.parseCert`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_certspotter.py`
