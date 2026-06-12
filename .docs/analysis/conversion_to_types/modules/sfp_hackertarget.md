# sfp_hackertarget

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** HackerTarget
- **service_origin:** `external-api`
- **Summary:** Search HackerTarget.com for hosts sharing the same IP.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `CO_HOSTED_SITE` | ENTITY | yes |
| `IP_ADDRESS` | ENTITY | yes |
| `WEBSERVER_HTTPHEADERS` | DATA | yes |
| `RAW_DNS_RECORDS` | DATA | yes |
| `INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `DOMAIN_NAME` | ENTITY | yes |
| `AFFILIATE_DOMAIN_NAME` | ENTITY | yes |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |
| `AFFILIATE_INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`, `DOMAIN_NAME_PARENT`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_hackertarget.py`
