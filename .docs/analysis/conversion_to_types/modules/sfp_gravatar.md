# sfp_gravatar

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Gravatar
- **service_origin:** `external-api`
- **Summary:** Retrieve user information from Gravatar API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `USERNAME` | ENTITY | yes |
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `PHONE_NUMBER` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | declared only |
| `ACCOUNT_EXTERNAL_OWNED` | ENTITY | yes |
| `SOCIAL_MEDIA` | ENTITY | yes |

## Consumed nugget types

`EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_gravatar.py`
