# sfp_binaryedge

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** BinaryEdge
- **service_origin:** `external-api`
- **Summary:** Obtain information from BinaryEdge.io Internet scanning systems, including breaches, vulnerabilities, torrents and passive DNS.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | yes |
| `DOMAIN_NAME` | ENTITY | yes |
| `VULNERABILITY_CVE_CRITICAL` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_HIGH` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_MEDIUM` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_LOW` | DESCRIPTOR | declared only |
| `VULNERABILITY_GENERAL` | DESCRIPTOR | declared only |
| `TCP_PORT_OPEN` | SUBENTITY | declared only |
| `TCP_PORT_OPEN_BANNER` | DATA | declared only |
| `EMAILADDR_COMPROMISED` | DESCRIPTOR | yes |
| `UDP_PORT_OPEN` | SUBENTITY | declared only |
| `UDP_PORT_OPEN_INFO` | DATA | declared only |
| `CO_HOSTED_SITE` | ENTITY | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `DOMAIN_NAME`, `EMAILADDR`, `NETBLOCK_OWNER`, `NETBLOCK_MEMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.cveInfo`
- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_binaryedge.py`
