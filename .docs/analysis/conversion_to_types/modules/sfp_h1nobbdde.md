# sfp_h1nobbdde

**Conversion pattern:** `api_text_or_html` — HTTP fetch → text/HTML parsing without structured JSON schema.

## Catalogue

- **Name:** HackerOne (Unofficial)
- **service_origin:** `external-api`
- **Summary:** Check external vulnerability scanning/reporting service h1.nobbd.de to see if the target is listed.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `VULNERABILITY_DISCLOSURE` | DESCRIPTOR | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_h1nobbdde.py`
