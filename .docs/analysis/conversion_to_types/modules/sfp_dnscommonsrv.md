# sfp_dnscommonsrv

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** DNS Common SRV
- **service_origin:** `local`
- **Summary:** Attempts to identify hostnames through brute-forcing common DNS SRV records.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |

_Additional types seen in code but not in producedEvents():_ `DNS_SRV`

## Consumed nugget types

`INTERNET_NAME`, `DOMAIN_NAME`

## Parsing signals (static)

_(none detected)_

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_dnscommonsrv.py`
