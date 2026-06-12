# sfp_circllu

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** CIRCL.LU
- **service_origin:** `external-api`
- **Summary:** Obtain information from CIRCL.LU's Passive DNS and Passive SSL databases.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | yes |
| `SSL_CERTIFICATE_ISSUED` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | yes |

## Consumed nugget types

`INTERNET_NAME`, `NETBLOCK_OWNER`, `IP_ADDRESS`, `DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_circllu.py`
