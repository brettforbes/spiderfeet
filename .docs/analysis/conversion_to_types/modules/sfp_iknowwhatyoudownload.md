# sfp_iknowwhatyoudownload

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Iknowwhatyoudownload.com
- **service_origin:** `external-api`
- **Summary:** Check iknowwhatyoudownload.com for IP addresses that have been using torrents.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_iknowwhatyoudownload.py`
