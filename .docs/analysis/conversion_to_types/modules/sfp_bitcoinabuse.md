# sfp_bitcoinabuse

**Conversion pattern:** `api_json_map` — HTTP fetch → JSON decode → field mapping into SpiderFeetEvent types.

## Catalogue

- **Name:** BitcoinAbuse
- **service_origin:** `external-api`
- **Summary:** Check Bitcoin addresses against the bitcoinabuse.com database of suspect/malicious addresses.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `MALICIOUS_BITCOIN_ADDRESS` | DESCRIPTOR | yes |
| `RAW_RIR_DATA` | DATA | yes |

## Consumed nugget types

`BITCOIN_ADDRESS`

## Parsing signals (static)

json.loads, fetchUrl

**SpiderFeet/sf helpers used:**

- `sf.fetchUrl`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_bitcoinabuse.py`
