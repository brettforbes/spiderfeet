# sfp_clearbit

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Clearbit
- **service_origin:** `external-api`
- **Summary:** Check for names, addresses, domains and more based on lookups of e-mail addresses on clearbit.com.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `PHONE_NUMBER` | ENTITY | yes |
| `PHYSICAL_ADDRESS` | ENTITY | yes |
| `AFFILIATE_INTERNET_NAME` | ENTITY | declared only |
| `EMAILADDR` | ENTITY | declared only |
| `EMAILADDR_GENERIC` | ENTITY | declared only |
| `INTERNET_NAME` | ENTITY | declared only |

## Consumed nugget types

`EMAILADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_clearbit.py`
