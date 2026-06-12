# sfp_multiproxy

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** multiproxy.org Open Proxies
- **service_origin:** `external-api`
- **Summary:** Check if an IP address is an open proxy according to multiproxy.org open proxy list.

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

## Consumed nugget types

`IP_ADDRESS`, `AFFILIATE_IPADDR`, `NETBLOCK_OWNER`, `NETBLOCK_MEMBER`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_multiproxy.py`
