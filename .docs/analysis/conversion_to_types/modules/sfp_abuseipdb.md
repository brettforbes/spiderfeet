# sfp_abuseipdb

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** AbuseIPDB
- **service_origin:** `external-api`
- **Summary:** Check if an IP address is malicious according to AbuseIPDB.com blacklist.

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

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_abuseipdb.py`
