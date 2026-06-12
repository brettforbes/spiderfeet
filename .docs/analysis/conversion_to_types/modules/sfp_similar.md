# sfp_similar

**Conversion pattern:** `dns_network_local` — DNS, sockets, or validation helpers; no third-party OSINT API.

## Catalogue

- **Name:** Similar Domain Finder
- **service_origin:** `local`
- **Summary:** Search various sources to identify similar looking domain names, for instance squatted domains.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `SIMILARDOMAIN` | ENTITY | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_similar.py`
