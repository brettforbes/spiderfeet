# sfp_seon

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Seon
- **service_origin:** `external-api`
- **Summary:** Queries seon.io to gather intelligence about IP Addresses, email addresses, and phone numbers

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `GEOINFO` | DESCRIPTOR | yes |
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |
| `TCP_PORT_OPEN` | SUBENTITY | yes |
| `MALICIOUS_EMAILADDR` | DESCRIPTOR | yes |
| `EMAILADDR_DELIVERABLE` | DESCRIPTOR | yes |
| `EMAILADDR_UNDELIVERABLE` | DESCRIPTOR | yes |
| `SOCIAL_MEDIA` | ENTITY | yes |
| `HUMAN_NAME` | ENTITY | yes |
| `COMPANY_NAME` | ENTITY | yes |
| `EMAILADDR_COMPROMISED` | DESCRIPTOR | yes |
| `MALICIOUS_PHONE_NUMBER` | DESCRIPTOR | yes |
| `PROVIDER_TELCO` | ENTITY | yes |
| `PHONE_NUMBER_TYPE` | DESCRIPTOR | yes |
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |
| `TOR_EXIT_NODE` | DESCRIPTOR | yes |
| `VPN_HOST` | DESCRIPTOR | yes |
| `PROXY_HOST` | DESCRIPTOR | yes |

_Additional types seen in code but not in producedEvents():_ `EMAILADDR_DISPOSABLE`, `PHYSICAL_COORDINATES`

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`, `EMAILADDR`, `PHONE_NUMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_seon.py`
