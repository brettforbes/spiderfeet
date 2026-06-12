# sfp_greynoise

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** GreyNoise
- **service_origin:** `external-api`
- **Summary:** Obtain IP enrichment data from GreyNoise

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_ASN` | DESCRIPTOR | declared only |
| `MALICIOUS_SUBNET` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | declared only |
| `COMPANY_NAME` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `BGP_AS_MEMBER` | ENTITY | yes |
| `OPERATING_SYSTEM` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`IP_ADDRESS`, `AFFILIATE_IPADDR`, `NETBLOCK_MEMBER`, `NETBLOCK_OWNER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_greynoise.py`
