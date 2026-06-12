# sfp_keybase

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Keybase
- **service_origin:** `external-api`
- **Summary:** Obtain additional information about domain names and identified usernames.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `RAW_RIR_DATA` | DATA | yes |
| `SOCIAL_MEDIA` | ENTITY | yes |
| `USERNAME` | ENTITY | yes |
| `GEOINFO` | DESCRIPTOR | yes |
| `BITCOIN_ADDRESS` | ENTITY | yes |
| `PGP_KEY` | DATA | yes |

## Consumed nugget types

`USERNAME`, `LINKED_URL_EXTERNAL`, `DOMAIN_NAME`

## Parsing signals (static)

json.loads, fetchUrl, regex

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_keybase.py`
