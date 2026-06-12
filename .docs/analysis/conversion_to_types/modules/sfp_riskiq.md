# sfp_riskiq

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** RiskIQ
- **service_origin:** `external-api`
- **Summary:** Obtain information from RiskIQ's (formerly PassiveTotal) Passive DNS and Passive SSL databases.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | declared only |
| `INTERNET_NAME` | ENTITY | yes |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |
| `DOMAIN_NAME` | ENTITY | yes |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | yes |
| `NETBLOCK_OWNER` | ENTITY | declared only |

## Consumed nugget types

`INTERNET_NAME`, `IP_ADDRESS`, `DOMAIN_NAME`, `EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_riskiq.py`
