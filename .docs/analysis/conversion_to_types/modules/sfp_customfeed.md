# sfp_customfeed

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** Custom Threat Feed
- **service_origin:** `local`
- **Summary:** Check if a host/domain, netblock, ASN or IP is malicious according to your custom feed.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_COHOST` | DESCRIPTOR | declared only |

## Consumed nugget types

`INTERNET_NAME`, `IP_ADDRESS`, `AFFILIATE_INTERNET_NAME`, `AFFILIATE_IPADDR`, `CO_HOSTED_SITE`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.hostDomain`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_customfeed.py`
