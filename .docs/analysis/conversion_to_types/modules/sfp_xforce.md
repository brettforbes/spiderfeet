# sfp_xforce

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** XForce Exchange
- **service_origin:** `external-api`
- **Summary:** Obtain IP reputation and passive DNS information from IBM X-Force Exchange.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `BLACKLISTED_IPADDR` | DESCRIPTOR | declared only |
| `BLACKLISTED_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `BLACKLISTED_SUBNET` | DESCRIPTOR | declared only |
| `BLACKLISTED_NETBLOCK` | DESCRIPTOR | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | declared only |
| `MALICIOUS_SUBNET` | DESCRIPTOR | declared only |
| `INTERNET_NAME` | ENTITY | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | yes |
| `DOMAIN_NAME` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`IP_ADDRESS`, `AFFILIATE_IPADDR`, `IPV6_ADDRESS`, `AFFILIATE_IPV6_ADDRESS`, `NETBLOCK_MEMBER`, `NETBLOCKV6_MEMBER`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_xforce.py`
