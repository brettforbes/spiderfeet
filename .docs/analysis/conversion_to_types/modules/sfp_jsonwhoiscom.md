# sfp_jsonwhoiscom

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** JsonWHOIS.com
- **service_origin:** `external-api`
- **Summary:** Search JsonWHOIS.com for WHOIS records associated with a domain.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `DOMAIN_REGISTRAR` | ENTITY | yes |
| `DOMAIN_WHOIS` | DATA | yes |
| `PROVIDER_DNS` | ENTITY | yes |
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `PHONE_NUMBER` | ENTITY | yes |
| `PHYSICAL_ADDRESS` | ENTITY | yes |
| `AFFILIATE_DOMAIN_UNREGISTERED` | ENTITY | yes |

_Additional types seen in code but not in producedEvents():_ `AFFILIATE_DOMAIN_WHOIS`, `AFFILIATE_EMAILADDR`

## Consumed nugget types

`DOMAIN_NAME`, `AFFILIATE_DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_jsonwhoiscom.py`
