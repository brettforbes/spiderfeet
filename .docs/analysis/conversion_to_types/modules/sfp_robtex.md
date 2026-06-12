# sfp_robtex

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Robtex
- **service_origin:** `external-api`
- **Summary:** Search Robtex.com for hosts sharing the same IP.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `CO_HOSTED_SITE` | ENTITY | yes |
| `IP_ADDRESS` | ENTITY | yes |
| `IPV6_ADDRESS` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, `NETBLOCK_MEMBER`, `NETBLOCKV6_MEMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_robtex.py`
