# sfp_zoneh

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Zone-H Defacement Check
- **service_origin:** `external-api`
- **Summary:** Check if a hostname/domain appears on the zone-h.org 'special defacements' RSS feed.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `DEFACED_INTERNET_NAME` | DESCRIPTOR | declared only |
| `DEFACED_IPADDR` | DESCRIPTOR | declared only |
| `DEFACED_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | declared only |
| `DEFACED_COHOST` | DESCRIPTOR | declared only |
| `DEFACED_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |

## Consumed nugget types

`INTERNET_NAME`, `IP_ADDRESS`, `IPV6_ADDRESS`, `AFFILIATE_INTERNET_NAME`, `AFFILIATE_IPADDR`, `AFFILIATE_IPV6_ADDRESS`, `CO_HOSTED_SITE`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_zoneh.py`
