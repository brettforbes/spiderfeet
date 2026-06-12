# sfp_portscan_tcp

**Conversion pattern:** `custom_logic` — Mixed or module-specific logic not captured by heuristics.

## Catalogue

- **Name:** Port Scanner - TCP
- **service_origin:** `local`
- **Summary:** Scans for commonly open TCP ports on Internet-facing systems.

## Produced nugget types

| Nugget ID | Archetype | Emitted in code (static) |
|-----------|-----------|--------------------------|
| `TCP_PORT_OPEN` | SUBENTITY | yes |
| `TCP_PORT_OPEN_BANNER` | DATA | yes |

## Consumed nugget types

`IP_ADDRESS`, `NETBLOCK_OWNER`

## Parsing signals (static)

_(none detected)_

**SpiderFeet/sf helpers used:**

- `sf.optValueToData`

## Conversion notes

SpiderFeet stores each finding as `SpiderFeetEvent(eventType, data: str, module, sourceEvent)`. The **nugget type** is `eventType`; **value** is always a string (`data`). Structured fields (port number, CVE id, geo coordinates) are encoded in that string or split across multiple events.

Module source: `modules/sfp_portscan_tcp.py`
