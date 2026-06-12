# sfp_bingsharedip

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Bing (Shared IPs)
- **service_origin:** `external-api`
- **Summary:** Search Bing for hosts sharing the same IP.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `CO_HOSTED_SITE` | ENTITY | yes |
| `IP_ADDRESS` | ENTITY | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.urlFQDN`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_bingsharedip.py`
