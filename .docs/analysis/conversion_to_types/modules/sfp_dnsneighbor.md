# sfp_dnsneighbor

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** DNS Look-aside
- **service_origin:** `local`
- **Summary:** Attempt to reverse-resolve the IP addresses next to your target to see if they are related.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `AFFILIATE_IPADDR` | ENTITY | declared only |
| `IP_ADDRESS` | ENTITY | declared only |

## Consumed nugget types

`IP_ADDRESS`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.resolveHost`
- `sf.resolveIP`
- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_dnsneighbor.py`
