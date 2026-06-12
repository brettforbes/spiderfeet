# sfp_networksdb

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** NetworksDB
- **service_origin:** `external-api`
- **Summary:** Search NetworksDB.io API for IP address and domain information.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | yes |
| `IP_ADDRESS` | ENTITY | yes |
| `IPV6_ADDRESS` | ENTITY | yes |
| `NETBLOCK_MEMBER` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |

_Additional types seen in code but not in producedEvents():_ `DOMAIN_NAME`, `NETBLOCKV6_MEMBER`

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `INTERNET_NAME`, `DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.validIP`
- `sf.validIP6`
- `sf.validIpNetwork`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_networksdb.py`
