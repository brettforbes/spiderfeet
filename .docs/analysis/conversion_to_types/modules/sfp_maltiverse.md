# sfp_maltiverse

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Maltiverse
- **service_origin:** `external-api`
- **Summary:** Obtain information about any malicious activities involving IP addresses

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `IP_ADDRESS` | ENTITY | yes |
| `MALICIOUS_IPADDR` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |
| `MALICIOUS_AFFILIATE_IPADDR` | DESCRIPTOR | yes |

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`, `NETBLOCK_MEMBER`, `AFFILIATE_IPADDR`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_maltiverse.py`
