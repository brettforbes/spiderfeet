# sfp_haveibeenpwned

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** HaveIBeenPwned
- **service_origin:** `external-api`
- **Summary:** Check HaveIBeenPwned.com for hacked e-mail addresses identified in breaches.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `EMAILADDR_COMPROMISED` | DESCRIPTOR | yes |
| `PHONE_NUMBER_COMPROMISED` | DESCRIPTOR | yes |
| `LEAKSITE_CONTENT` | DATA | yes |
| `LEAKSITE_URL` | ENTITY | yes |

## Consumed nugget types

`EMAILADDR`, `PHONE_NUMBER`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_haveibeenpwned.py`
