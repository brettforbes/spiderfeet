# sfp_whois

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Whois
- **service_origin:** `local`
- **Summary:** Perform a WHOIS look-up on domain names and owned netblocks.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `DOMAIN_WHOIS` | DATA | declared only |
| `NETBLOCK_WHOIS` | DATA | declared only |
| `DOMAIN_REGISTRAR` | ENTITY | yes |
| `CO_HOSTED_SITE_DOMAIN_WHOIS` | DATA | declared only |
| `AFFILIATE_DOMAIN_WHOIS` | DATA | declared only |
| `SIMILARDOMAIN_WHOIS` | DATA | declared only |

## Consumed nugget types

`DOMAIN_NAME`, `DOMAIN_NAME_PARENT`, `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, `CO_HOSTED_SITE_DOMAIN`, `AFFILIATE_DOMAIN_NAME`, `SIMILARDOMAIN`

## Parsing signals (static)

_(none detected)_

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_whois.py`
