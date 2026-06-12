# sfp_sslcert

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** SSL Certificate Analyzer
- **service_origin:** `local`
- **Summary:** Gather information about SSL certificates used by the target's HTTPS sites.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `TCP_PORT_OPEN` | SUBENTITY | yes |
| `INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `CO_HOSTED_SITE` | ENTITY | declared only |
| `CO_HOSTED_SITE_DOMAIN` | ENTITY | yes |
| `SSL_CERTIFICATE_ISSUED` | ENTITY | yes |
| `SSL_CERTIFICATE_ISSUER` | ENTITY | yes |
| `SSL_CERTIFICATE_MISMATCH` | DESCRIPTOR | yes |
| `SSL_CERTIFICATE_EXPIRED` | DESCRIPTOR | yes |
| `SSL_CERTIFICATE_EXPIRING` | DESCRIPTOR | yes |
| `SSL_CERTIFICATE_RAW` | DATA | yes |
| `DOMAIN_NAME` | ENTITY | yes |

## Consumed nugget types

`INTERNET_NAME`, `LINKED_URL_INTERNAL`, `IP_ADDRESS`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.isDomain`
- `sf.parseCert`
- `sf.resolveHost`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_sslcert.py`
