# sfp_onyphe

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Onyphe
- **service_origin:** `external-api`
- **Summary:** Check Onyphe data (threat list, geo-location, pastries, vulnerabilities)  about a given IP.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `GEOINFO` | DESCRIPTOR | yes |
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |
| `LEAKSITE_CONTENT` | DATA | yes |
| `VULNERABILITY_CVE_CRITICAL` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_HIGH` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_MEDIUM` | DESCRIPTOR | declared only |
| `VULNERABILITY_CVE_LOW` | DESCRIPTOR | declared only |
| `VULNERABILITY_GENERAL` | DESCRIPTOR | declared only |
| `RAW_RIR_DATA` | DATA | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | yes |
| `PHYSICAL_COORDINATES` | ENTITY | yes |

_Additional types seen in code but not in producedEvents():_ `CO_HOSTED_SITE`, `DOMAIN_NAME`

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.cveInfo`
- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_onyphe.py`
