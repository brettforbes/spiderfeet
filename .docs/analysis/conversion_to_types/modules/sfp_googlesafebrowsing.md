# sfp_googlesafebrowsing

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Google SafeBrowsing
- **service_origin:** `external-api`
- **Summary:** Check if the URL is included on any of the Safe Browsing lists.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_COHOST` | DESCRIPTOR | declared only |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`INTERNET_NAME`, `IP_ADDRESS`, `AFFILIATE_INTERNET_NAME`, `AFFILIATE_IPADDR`, `CO_HOSTED_SITE`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_googlesafebrowsing.py`
