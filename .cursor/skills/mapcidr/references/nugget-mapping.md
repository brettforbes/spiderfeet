# mapcidr → SpiderFeet Nugget Mapping

Derive the graph from the **parsed JSON bundle** (`records[]`), not from banners. Address nodes must go through `core.ip_classify.classify_ip` (SPEC-005).

## Primary mappings

| Input / record | Nugget type | Notes |
|----------------|-------------|-------|
| Source CIDR (IPv4) | `NETBLOCK_OWNER` | One node per unique network string |
| Source CIDR (IPv6) | `NETBLOCKV6_OWNER` | IPv6 blocks |
| Expanded / listed IPv4 | via `classify_ip` → usually `IPV4_ADDRESS` or `INTERNAL_IP_ADDRESS` | Never invent a separate mapper UUID scheme |
| Expanded / listed IPv6 | via `classify_ip` → `IPV6_ADDRESS` | Colon-form must not become `IPV4_ADDRESS` |
| Slice/aggregate CIDR line | `NETBLOCK_OWNER` / `NETBLOCKV6_OWNER` | Treat output CIDR as netblock entity |
| `ip:port` (`-sp`) | address + `TCP_PORT_OPEN` (or UDP if known) | Port only when explicitly present |
| Count-only (`-c`) | scan metadata / descriptor | Do not invent fake hosts for a count integer |
| Approx aggregate (`-aa`) | same netblock types | Annotate that covering range may include non-input IPs |

Catalogue: reuse `NETBLOCK_OWNER`, `NETBLOCKV6_OWNER`, and classify_ip results from `.docs/analysis/nuggets.json` + `nuggets_extension.json`. Prefer `IPV4_ADDRESS` / `IPV6_ADDRESS` over ambiguous `IP_ADDRESS` when the classifier returns them.

## Edge rules

| From | Relation | To |
|------|----------|-----|
| Scan head | `contains` | each source netblock |
| `NETBLOCK_*` | `contains` | each address expanded from that block |
| Address | `listens-to` | `TCP_PORT_OPEN` when `kind=ip_port` |

Allowed default relations: `contains`, `had`, `listens-to`. Do **not** emit invented `CONTAINS_IP` / `RESOLVES_TO` unless a seed/spec adds them.

## Identity

```text
nugget_instance_id = f"{nugget_id}--{uuid5(ONTOLOGY_NAMESPACE, nugget_data)}"
```

Exactly one node per `(nugget_id, nugget_data)`. Shared IPs from overlapping CIDRs reuse the same address node and link from each owning netblock via `contains`.

## Example (expand `/30`)

Input command: `mapcidr -cidr 198.51.100.0/30 -silent`

Records: `198.51.100.0` … `198.51.100.3`

Conceptual graph:

- `NETBLOCK_OWNER` = `198.51.100.0/30`
- four address nodes from `classify_ip`
- edges: netblock `contains` each address; scan `contains` netblock

```json
{
  "nodes": [
    {
      "nugget_id": "NETBLOCK_OWNER",
      "nugget_data": "198.51.100.0/30"
    },
    {
      "nugget_id": "IPV4_ADDRESS",
      "nugget_data": "198.51.100.1"
    }
  ],
  "edges": [
    {
      "from_nugget_id": "NETBLOCK_OWNER",
      "to_nugget_id": "IPV4_ADDRESS",
      "relation": "contains"
    }
  ]
}
```

(Instance ids omitted; emit via shared `graph_builder` only.)

## Provenance fields

Attach on nodes or scan metadata:

- `source_tool`: `mapcidr`
- `source_command`: full CLI
- `source_input`: original CIDR/range/file
- `mapcidr_mode`: `expand` | `slice_sbc` | `slice_sbh` | `aggregate` | `aggregate_approx` | `count` | `format` | `shuffle_port`

## Do not emit

- Hosts outside authorized scope
- Fake IPs to “fill” approx aggregates without labeling
- Graph from banner/version text alone
- Orphan address nodes with no scan/netblock edge
