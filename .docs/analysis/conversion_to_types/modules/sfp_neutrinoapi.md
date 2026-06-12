# sfp_neutrinoapi

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** NeutrinoAPI
- **service_origin:** `external-api`
- **Summary:** Search NeutrinoAPI for phone location information, IP address information, and host reputation.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `BLACKLISTED_IPADDR` | DESCRIPTOR | yes |
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |
| `PROXY_HOST` | DESCRIPTOR | yes |
| `VPN_HOST` | DESCRIPTOR | yes |
| `TOR_EXIT_NODE` | DESCRIPTOR | yes |
| `GEOINFO` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `PHONE_NUMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_neutrinoapi.py`
