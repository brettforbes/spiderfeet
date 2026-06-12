# sfp_urlscan

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** URLScan.io
- **service_origin:** `external-api`
- **Summary:** Search URLScan.io cache for domain information.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `GEOINFO` | DESCRIPTOR | yes |
| `LINKED_URL_INTERNAL` | SUBENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |
| `DOMAIN_NAME` | ENTITY | yes |
| `INTERNET_NAME` | ENTITY | yes |
| `INTERNET_NAME_UNRESOLVED` | ENTITY | yes |
| `BGP_AS_MEMBER` | ENTITY | yes |
| `WEBSERVER_BANNER` | DATA | yes |

## Consumed nugget types

`INTERNET_NAME`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`
- `sf.isDomain`
- `sf.resolveHost`
- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_urlscan.py`
