# sfp_surbl

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** SURBL
- **service_origin:** `external-api`
- **Summary:** Check if a netblock, IP address or domain is in the SURBL blacklist.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `BLACKLISTED_IPADDR` | DESCRIPTOR | declared only |
| `BLACKLISTED_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `BLACKLISTED_SUBNET` | DESCRIPTOR | declared only |
| `BLACKLISTED_NETBLOCK` | DESCRIPTOR | declared only |
| `BLACKLISTED_INTERNET_NAME` | DESCRIPTOR | declared only |
| `BLACKLISTED_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | declared only |
| `BLACKLISTED_COHOST` | DESCRIPTOR | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | declared only |
| `MALICIOUS_SUBNET` | DESCRIPTOR | declared only |
| `MALICIOUS_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_COHOST` | DESCRIPTOR | declared only |

## Consumed nugget types

`IP_ADDRESS`, `AFFILIATE_IPADDR`, `NETBLOCK_OWNER`, `NETBLOCK_MEMBER`, `INTERNET_NAME`, `AFFILIATE_INTERNET_NAME`, `CO_HOSTED_SITE`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.resolveHost`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_surbl.py`
