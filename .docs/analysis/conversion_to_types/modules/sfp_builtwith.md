# sfp_builtwith

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** BuiltWith
- **service_origin:** `external-api`
- **Summary:** Query BuiltWith.com's Domain API for information about your target's web technology stack, e-mail addresses and more.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | yes |
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `RAW_RIR_DATA` | DATA | yes |
| `WEBSERVER_TECHNOLOGY` | DESCRIPTOR | yes |
| `PHONE_NUMBER` | ENTITY | yes |
| `DOMAIN_NAME` | ENTITY | yes |
| `CO_HOSTED_SITE` | ENTITY | declared only |
| `IP_ADDRESS` | ENTITY | declared only |
| `WEB_ANALYTICS_ID` | ENTITY | yes |

_Additional types seen in code but not in producedEvents():_ `AFFILIATE_DOMAIN_NAME`, `AFFILIATE_INTERNET_NAME`

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.validIP`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_builtwith.py`
