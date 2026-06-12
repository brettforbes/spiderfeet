# sfp_hybrid_analysis

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Hybrid Analysis
- **service_origin:** `external-api`
- **Summary:** Search Hybrid Analysis for domains and URLs related to the target.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `DOMAIN_NAME` | ENTITY | declared only |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |

_Additional types seen in code but not in producedEvents():_ `INTERNET_NAME_UNRESOLVED`

## Consumed nugget types

`IP_ADDRESS`, `DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.resolveHost`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_hybrid_analysis.py`
