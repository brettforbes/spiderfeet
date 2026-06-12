# sfp_dnsgrep

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** DNSGrep
- **service_origin:** `external-api`
- **Summary:** Obtain Passive DNS information from Rapid7 Sonar Project using DNSGrep API.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `INTERNET_NAME` | ENTITY | declared only |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | declared only |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.resolveHost`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_dnsgrep.py`
