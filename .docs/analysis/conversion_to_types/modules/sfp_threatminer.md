# sfp_threatminer

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** ThreatMiner
- **service_origin:** `external-api`
- **Summary:** Obtain information from ThreatMiner's database for passive DNS and threat intelligence.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | declared only |

_Additional types seen in code but not in producedEvents():_ `INTERNET_NAME_UNRESOLVED`

## Consumed nugget types

`IP_ADDRESS`, `DOMAIN_NAME`, `NETBLOCK_OWNER`, `NETBLOCK_MEMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.resolveHost`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_threatminer.py`
