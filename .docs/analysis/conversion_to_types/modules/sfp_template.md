# sfp_template

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Template Module
- **service_origin:** `external-api`
- **Summary:** This is an example module to help developers create their own SpiderFeet modules.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `OPERATING_SYSTEM` | DESCRIPTOR | yes |
| `DEVICE_TYPE` | DESCRIPTOR | declared only |
| `TCP_PORT_OPEN` | SUBENTITY | declared only |
| `TCP_PORT_OPEN_BANNER` | DATA | declared only |
| `RAW_RIR_DATA` | DATA | yes |
| `GEOINFO` | DESCRIPTOR | declared only |
| `VULNERABILITY_GENERAL` | DESCRIPTOR | declared only |

_Additional types seen in code but not in producedEvents():_ `AFFILIATE_IPADDR`, `IP_ADDRESS`

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`, `DOMAIN_NAME`, `WEB_ANALYTICS_ID`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_template.py`
