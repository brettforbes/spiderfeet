# sfp_opennic

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** OpenNIC DNS
- **service_origin:** `external-api`
- **Summary:** Resolves host names in the OpenNIC alternative DNS system.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | yes |
| `IPV6_ADDRESS` | ENTITY | yes |
| `AFFILIATE_IPADDR` | ENTITY | yes |
| `AFFILIATE_IPV6_ADDRESS` | ENTITY | yes |

## Consumed nugget types

`INTERNET_NAME`, `INTERNET_NAME_UNRESOLVED`, `AFFILIATE_INTERNET_NAME`, `AFFILIATE_INTERNET_NAME_UNRESOLVED`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_opennic.py`
