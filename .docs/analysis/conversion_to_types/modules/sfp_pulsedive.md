# sfp_pulsedive

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Pulsedive
- **service_origin:** `external-api`
- **Summary:** Obtain information from Pulsedive's API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | declared only |
| `TCP_PORT_OPEN` | SUBENTITY | yes |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `AFFILIATE_IPADDR`, `AFFILIATE_IPV6_ADDRESS`, `INTERNET_NAME`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, `NETBLOCK_MEMBER`, `NETBLOCKV6_MEMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_pulsedive.py`
