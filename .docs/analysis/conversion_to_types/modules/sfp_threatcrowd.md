# sfp_threatcrowd

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** ThreatCrowd
- **service_origin:** `external-api`
- **Summary:** Obtain information from ThreatCrowd about identified IP addresses, domains and e-mail addresses.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_COHOST` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_INTERNET_NAME` | DESCRIPTOR | declared only |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | declared only |
| `MALICIOUS_NETBLOCK` | DESCRIPTOR | declared only |
| `MALICIOUS_SUBNET` | DESCRIPTOR | declared only |
| `MALICIOUS_EMAILADDR` | DESCRIPTOR | declared only |

## Consumed nugget types

`IP_ADDRESS`, `AFFILIATE_IPADDR`, `INTERNET_NAME`, `CO_HOSTED_SITE`, `NETBLOCK_OWNER`, `EMAILADDR`, `NETBLOCK_MEMBER`, `AFFILIATE_INTERNET_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_threatcrowd.py`
