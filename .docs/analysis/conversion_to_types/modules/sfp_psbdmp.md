# sfp_psbdmp

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Psbdmp
- **service_origin:** `external-api`
- **Summary:** Check psbdmp.cc (PasteBin Dump) for potentially hacked e-mails and domains.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `LEAKSITE_URL` | ENTITY | yes |
| `LEAKSITE_CONTENT` | DATA | yes |

## Consumed nugget types

`EMAILADDR`, `DOMAIN_NAME`, `INTERNET_NAME`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_psbdmp.py`
