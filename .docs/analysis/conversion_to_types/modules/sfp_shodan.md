# sfp_shodan

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** SHODAN
- **service_origin:** `external-api`
- **Summary:** Obtain information from SHODAN about identified IP addresses.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `OPERATING_SYSTEM` | DESCRIPTOR | yes |
| `DEVICE_TYPE` | DESCRIPTOR | yes |
| `TCP_PORT_OPEN` | SUBENTITY | yes |
| `TCP_PORT_OPEN_BANNER` | DATA | yes |
| `RAW_RIR_DATA` | DATA | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `IP_ADDRESS` | ENTITY | yes |
| `VULNERABILITY_CVE_CRITICAL` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_HIGH` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_MEDIUM` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_LOW` | DESCRIPTOR | declared only |
| `VULNERABILITY_GENERAL` | DESCRIPTOR | declared only |

_Additional types seen in code but not in producedEvents():_ `BGP_AS_MEMBER`, `SOFTWARE_USED`

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`, `DOMAIN_NAME`, `WEB_ANALYTICS_ID`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.cveInfo`
- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_shodan.py`
