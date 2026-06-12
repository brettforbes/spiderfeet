# sfp_sociallinks

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Social Links
- **service_origin:** `external-api`
- **Summary:** Queries SocialLinks.io to gather intelligence from social media platforms and dark web.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `GEOINFO` | DESCRIPTOR | yes |
| `SOCIAL_MEDIA` | ENTITY | yes |
| `HUMAN_NAME` | ENTITY | yes |
| `JOB_TITLE` | DESCRIPTOR | yes |
| `COMPANY_NAME` | ENTITY | yes |
| `PHONE_NUMBER` | ENTITY | yes |
| `ACCOUNT_EXTERNAL_OWNED` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

_Additional types seen in code but not in producedEvents():_ `USERNAME`

## Consumed nugget types

`USERNAME`, `EMAILADDR`, `PHONE_NUMBER`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_sociallinks.py`
