# sfp_bgpview

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** BGPView
- **service_origin:** `external-api`
- **Summary:** Obtain network information from BGPView API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `BGP_AS_MEMBER` | ENTITY | yes |
| `NETBLOCK_MEMBER` | ENTITY | yes |
| `NETBLOCKV6_MEMBER` | ENTITY | yes |
| `PHYSICAL_ADDRESS` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `BGP_AS_MEMBER`, `NETBLOCK_MEMBER`, `NETBLOCKV6_MEMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIpNetwork`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_bgpview.py`
