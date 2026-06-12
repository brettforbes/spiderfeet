# sfp_censys

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Censys
- **service_origin:** `external-api`
- **Summary:** Obtain host information from Censys.io.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `BGP_AS_MEMBER` | ENTITY | yes |
| `UDP_PORT_OPEN` | SUBENTITY | yes |
| `TCP_PORT_OPEN` | SUBENTITY | yes |
| `TCP_PORT_OPEN_BANNER` | DATA | yes |
| `OPERATING_SYSTEM` | DESCRIPTOR | yes |
| `SOFTWARE_USED` | SUBENTITY | yes |
| `WEBSERVER_HTTPHEADERS` | DATA | yes |
| `NETBLOCK_MEMBER` | ENTITY | yes |
| `NETBLOCKV6_MEMBER` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |

_Additional types seen in code but not in producedEvents():_ `IPV6_ADDRESS`, `IP_ADDRESS`

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIpNetwork`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_censys.py`
