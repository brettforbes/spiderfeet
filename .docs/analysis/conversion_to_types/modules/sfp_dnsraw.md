# sfp_dnsraw

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** DNS Raw Records
- **service_origin:** `local`
- **Summary:** Retrieves raw DNS records such as MX, TXT and others.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `PROVIDER_MAIL` | ENTITY | yes |
| `PROVIDER_DNS` | ENTITY | yes |
| `RAW_DNS_RECORDS` | DATA | yes |
| `DNS_TEXT` | DATA | yes |
| `DNS_SPF` | DATA | yes |
| `INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |

## Consumed nugget types

`INTERNET_NAME`, `DOMAIN_NAME`, `DOMAIN_NAME_PARENT`

## Parsing signals (static)

regex

**SpiderFeet/sf helpers used:**

- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_dnsraw.py`
