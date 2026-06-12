# sfp_spyonweb

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** SpyOnWeb
- **service_origin:** `external-api`
- **Summary:** Search SpyOnWeb for hosts sharing the same IP address, Google Analytics code, or Google Adsense code.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `CO_HOSTED_SITE` | ENTITY | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `AFFILIATE_INTERNET_NAME` | ENTITY | yes |
| `WEB_ANALYTICS_ID` | ENTITY | yes |
| `DOMAIN_NAME` | ENTITY | yes |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | yes |

## Consumed nugget types

`IP_ADDRESS`, `INTERNET_NAME`, `DOMAIN_NAME`, `WEB_ANALYTICS_ID`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_spyonweb.py`
