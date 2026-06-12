# sfp_talosintel

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Talos Intelligence
- **service_origin:** `external-api`
- **Summary:** Check if a netblock or IP address is malicious according to TalosIntelligence.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `BLACKLISTED_IPADDR` | DESCRIPTOR | declared only |
| `BLACKLISTED_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `BLACKLISTED_SUBNET` | DESCRIPTOR | declared only |
| `BLACKLISTED_NETBLOCK` | DESCRIPTOR | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_SUBNET` | DESCRIPTOR | declared only |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | declared only |

## Consumed nugget types

`IP_ADDRESS`, `AFFILIATE_IPADDR`, `NETBLOCK_MEMBER`, `NETBLOCK_OWNER`

## Parsing signals (static)

fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_talosintel.py`
