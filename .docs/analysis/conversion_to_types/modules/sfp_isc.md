# sfp_isc

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Internet Storm Center
- **service_origin:** `external-api`
- **Summary:** Check if an IP address is malicious according to SANS ISC.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `BLACKLISTED_IPADDR` | DESCRIPTOR | declared only |
| `BLACKLISTED_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `AFFILIATE_IPADDR`, `AFFILIATE_IPV6_ADDRESS`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_isc.py`
