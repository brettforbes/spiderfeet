# sfp_ripe

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** RIPE
- **service_origin:** `external-api`
- **Summary:** Queries the RIPE registry (includes ARIN data) to identify netblocks and other info.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `NETBLOCK_MEMBER` | ENTITY | declared only |
| `NETBLOCK_OWNER` | ENTITY | yes |
| `NETBLOCKV6_MEMBER` | ENTITY | declared only |
| `NETBLOCKV6_OWNER` | ENTITY | yes |
| `BGP_AS_MEMBER` | ENTITY | yes |
| `BGP_AS_OWNER` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `NETBLOCK_MEMBER`, `NETBLOCK_OWNER`, `NETBLOCKV6_MEMBER`, `NETBLOCKV6_OWNER`, `BGP_AS_OWNER`, `BGP_AS_MEMBER`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIpNetwork`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_ripe.py`
