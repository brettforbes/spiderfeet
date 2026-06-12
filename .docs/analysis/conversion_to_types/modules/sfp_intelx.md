# sfp_intelx

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** IntelligenceX
- **service_origin:** `external-api`
- **Summary:** Obtain information from IntelligenceX about identified IP addresses, domains, e-mail addresses and phone numbers.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `LEAKSITE_URL` | ENTITY | declared only |
| `DARKNET_MENTION_URL` | DESCRIPTOR | declared only |
| `INTERNET_NAME` | ENTITY | declared only |
| `DOMAIN_NAME` | ENTITY | yes |
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |

## Consumed nugget types

`IP_ADDRESS`, `AFFILIATE_IPADDR`, `INTERNET_NAME`, `EMAILADDR`, `CO_HOSTED_SITE`, `PHONE_NUMBER`, `BITCOIN_ADDRESS`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_intelx.py`
