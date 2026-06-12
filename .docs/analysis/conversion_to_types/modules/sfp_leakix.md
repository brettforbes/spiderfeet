# sfp_leakix

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** LeakIX
- **service_origin:** `external-api`
- **Summary:** Search LeakIX for host data leaks, open ports, software and geoip.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `TCP_PORT_OPEN` | SUBENTITY | yes |
| `OPERATING_SYSTEM` | DESCRIPTOR | yes |
| `SOFTWARE_USED` | SUBENTITY | yes |
| `WEBSERVER_BANNER` | DATA | yes |
| `LEAKSITE_CONTENT` | DATA | yes |
| `INTERNET_NAME` | ENTITY | yes |

_Additional types seen in code but not in producedEvents():_ `INTERNET_NAME_UNRESOLVED`, `IP_ADDRESS`

## Consumed nugget types

`IP_ADDRESS`, `DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.resolveHost`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_leakix.py`
