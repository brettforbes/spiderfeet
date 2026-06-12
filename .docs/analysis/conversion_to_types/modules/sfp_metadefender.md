# sfp_metadefender

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** MetaDefender
- **service_origin:** `external-api`
- **Summary:** Search MetaDefender API for IP address and domain IP reputation.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |
| `MALICIOUS_INTERNET_NAME` | DESCRIPTOR | yes |
| `BLACKLISTED_IPADDR` | DESCRIPTOR | yes |
| `BLACKLISTED_INTERNET_NAME` | DESCRIPTOR | yes |
| `GEOINFO` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `INTERNET_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_metadefender.py`
