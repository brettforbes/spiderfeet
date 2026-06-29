# Netdiscover → Nugget Mapping

CLI profiling examinations use `netdiscover_text_to_json.py` → `netdiscover_json_to_graph.py` (approved 06A schema).

## Input row (post-TextFSM)

```python
{
    "IP": "192.168.1.100",
    "MAC": "08:00:27:53:81:2b",
    "COUNT": "1",
    "LEN": "60",
    "VENDOR": "PCS Systemtechnik GmbH",
}
```

## Examination graph nugget types

| Field | Nugget | Relation |
|-------|--------|----------|
| scan | `SCAN_RECORD` | root entity |
| CLI args / timestamps / stats | `SCAN_*` descriptors | `SCAN_RECORD` → `had` |
| host | `SYSTEM` | `SCAN_RECORD` → `contains` |
| L3/L2 container | `NETWORKS` (category) | `SYSTEM` → `contains` |
| `IP` | `IP_ADDRESS` | `NETWORKS` → `contains` |
| `MAC` | `MAC_ADDRESS` | `NETWORKS` → `contains` |
| `VENDOR` | **`MAC_VENDOR`** (descriptor) | `MAC_ADDRESS` → `had` |

Do **not** use `RAW_RIR_DATA` for netdiscover MAC vendor strings in examination graphs.

## Graph shape

```
SCAN_RECORD
  └─ contains → SYSTEM (ipv4)
       └─ contains → NETWORKS
            ├─ contains → IP_ADDRESS
            └─ contains → MAC_ADDRESS
                 └─ had → MAC_VENDOR
```

## Structured JSON

Vendor strings live in `netdiscover_scan.systems[].mac_vendor`. Interactive TUI captures must set:

- `runstats.systems.scan_tries` = number of `Currently scanning:` frames
- `runstats.systems.empty_scans` = frames with **no host table rows**
- `systems` = first non-empty host table only

## Module integration (`sfp_tool_netdiscover`)

Runtime module flow may still emit legacy SpiderFeet events (`IP_ADDRESS`, `MAC_ADDRESS`, etc.). Examination corpus graphs follow the 06A `SYSTEM` / `MAC_VENDOR` contract above.

## Cross-reference

- Converters: `.seed/scripts/cli_corpus/netdiscover_text_to_json.py`, `netdiscover_json_to_graph.py`
- Generic TextFSM patterns: [`../../textfsm/references/nugget-conversion.md`](../../textfsm/references/nugget-conversion.md)
