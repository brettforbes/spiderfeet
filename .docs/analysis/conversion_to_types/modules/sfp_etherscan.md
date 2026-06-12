# sfp_etherscan

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** Etherscan
- **service_origin:** `external-api`
- **Summary:** Queries etherscan.io to find the balance of identified ethereum wallet addresses.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `ETHEREUM_BALANCE` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`ETHEREUM_ADDRESS`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_etherscan.py`
