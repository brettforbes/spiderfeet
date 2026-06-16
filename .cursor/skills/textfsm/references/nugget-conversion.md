# Rows → Nugget Nodes and Edges

TextFSM produces **tabular rows**. SpiderFeet nuggets are a **graph** (`nodes` + `edges`). The mapping layer is explicit application code.

## Node shape (convention)

```python
{
    "id": "ip:10.0.0.1",           # stable dedup key
    "type": "IP_ADDRESS",          # nugget_id from nuggets.json
    "data": "10.0.0.1",            # primary payload (event.data equivalent)
    "attributes": {},              # optional qualifiers
}
```

## Edge shape (convention)

```python
{
    "source": "seed:example.com",
    "target": "ip:10.0.0.1",
    "relation": "discovered",      # semantic link type
}
```

## Mapping workflow

1. Parse text → `list[dict]` via TextFSM
2. For each row, decide which nugget types to emit
3. Create nodes with stable `id` (dedupe across rows)
4. Create edges from seed/parent → child per target hierarchy spec
5. Attach `source_module` and optional `raw_row` for audit

## Common CLI → nugget mappings

| Parsed field | Nugget type | Typical edge |
|--------------|-------------|--------------|
| IP address | `IP_ADDRESS` | seed → discovered |
| MAC address | `MAC_ADDRESS` | IP → has_mac |
| FQDN / hostname | `INTERNET_NAME` | seed → resolved |
| `ip:port` | `TCP_PORT_OPEN` / `UDP_PORT_OPEN` | host → listens_on |
| Banner string | `TCP_PORT_OPEN_BANNER` | port → banner |
| Vendor/OUI | attribute or `RAW_RIR_DATA` | host → metadata |
| OS string | `OPERATING_SYSTEM` | host → runs |

See `.docs/analysis/nuggets.json` for full nugget vocabulary.

## Multiple samples → one function

When given several `(text, nodes_edges)` pairs:

1. Diff column sets — union if compatible
2. Diff row patterns — separate states or templates if structurally different
3. Use CliTable if only vendor/command differs
4. Single `parse_*()` returning `list[dict]`; single `to_nodes_edges(rows, seed_id, schema)` for graph emission

## Provenance

```python
for row in rows:
    node["provenance"] = {"module": "sfp_tool_netdiscover", "raw": row}
```

Matches SpiderFeet `SpiderFeetEvent` source module pattern.
