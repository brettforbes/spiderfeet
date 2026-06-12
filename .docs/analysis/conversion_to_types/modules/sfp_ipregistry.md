# sfp_ipregistry

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** ipregistry
- **service_origin:** `external-api`
- **Summary:** Query the ipregistry.co database for reputation and geo-location.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `GEOINFO` | DESCRIPTOR | declared only |
| `MALICIOUS_IPADDR` | DESCRIPTOR | declared only |
| `PHYSICAL_COORDINATES` | ENTITY | declared only |
| `RAW_RIR_DATA` | DATA | declared only |

## Consumed nugget types

`IP_ADDRESS`, `IPV6_ADDRESS`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_ipregistry.py`
