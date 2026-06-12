# sfp_stackoverflow

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** StackOverflow
- **service_origin:** `external-api`
- **Summary:** Search StackOverflow for any mentions of a target domain. Returns potentially related information.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `EMAILADDR` | ENTITY | yes |
| `AFFILIATE_EMAILADDR` | ENTITY | yes |
| `USERNAME` | ENTITY | yes |
| `AFFILIATE_IPADDR` | ENTITY | declared only |
| `AFFILIATE_IPV6_ADDRESS` | ENTITY | yes |
| `HUMAN_NAME` | ENTITY | declared only |

_Additional types seen in code but not in producedEvents():_ `AFFILIATE_IP_ADDRESS`

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `helpers.extractEmailsFromText`
- `sf.fetchUrl`
- `sf.validIP`
- `sf.validIP6`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_stackoverflow.py`
