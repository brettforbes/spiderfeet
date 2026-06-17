# Netdiscover → Nugget Mapping

Netdiscover `-P` rows become **IP_ADDRESS**, **MAC_ADDRESS**, and vendor metadata nodes linked to the scan seed (NETBLOCK or parent IP).

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

## Target nugget types

| Field | SpiderFeet event / nugget | Notes |
|-------|---------------------------|-------|
| `IP` | `IP_ADDRESS` | Primary discovery output |
| `MAC` | `MAC_ADDRESS` | Layer-2 identifier |
| `VENDOR` | attribute on MAC or `RAW_RIR_DATA` | OUI vendor string |
| hostname suffix | `INTERNET_NAME` | Only if `VENDOR` contains ` / hostname` |
| `COUNT` | attribute `arp_count` | Optional provenance |
| Parent CIDR | `NETBLOCK_OWNER` or seed | Scan range context |

See `.docs/analysis/nuggets.json` for canonical type names.

## Graph shape

```
seed (NETBLOCK_OWNER / scan target)
  └─ discovered → IP_ADDRESS
        └─ has_mac → MAC_ADDRESS
              └─ vendor → attribute / RAW_RIR_DATA
```

For a scan seeded from a single `IP_ADDRESS` (e.g. gateway), link discovered peers as sibling IPs under the same netblock parent.

## Python mapping

```python
def to_nodes_edges(rows: list[dict], seed_id: str) -> tuple[list, list]:
    nodes, edges = [], []
    seen = set()

    def add_node(node_id: str, ntype: str, data: str, attrs: dict | None = None):
        if node_id in seen:
            return
        seen.add(node_id)
        n = {"id": node_id, "type": ntype, "data": data}
        if attrs:
            n["attributes"] = attrs
        nodes.append(n)

    for row in rows:
        ip = row["IP"]
        mac = row["MAC"].lower()
        vendor = row.get("VENDOR", "").strip()
        hostname = None
        if " / " in vendor:
            vendor, hostname = [p.strip() for p in vendor.split(" / ", 1)]

        ip_id = f"ip:{ip}"
        mac_id = f"mac:{mac}"

        add_node(ip_id, "IP_ADDRESS", ip, {"arp_count": row.get("COUNT")})
        add_node(mac_id, "MAC_ADDRESS", mac, {"vendor": vendor} if vendor else None)

        edges.append({"source": seed_id, "target": ip_id, "relation": "discovered"})
        edges.append({"source": ip_id, "target": mac_id, "relation": "has_mac"})

        if hostname:
            hn_id = f"name:{hostname}"
            add_node(hn_id, "INTERNET_NAME", hostname)
            edges.append({"source": ip_id, "target": hn_id, "relation": "resolved"})

        if vendor and vendor.lower() != "unknown vendor":
            edges.append({
                "source": mac_id,
                "target": f"vendor:{vendor}",
                "relation": "oui_vendor",
            })
            add_node(f"vendor:{vendor}", "RAW_RIR_DATA", vendor)

    return nodes, edges
```

## Module integration (`sfp_tool_netdiscover`)

Expected module flow:

1. Receive `NETBLOCK_OWNER` or `IP_ADDRESS` event
2. Run `netdiscover -P -N -r <cidr>` (derive CIDR from netblock)
3. Parse stdout via TextFSM
4. For each IP, emit `SpiderFeetEvent("IP_ADDRESS", ip, ...)`
5. Emit `MAC_ADDRESS` linked to IP
6. Optionally emit vendor string as metadata event

## Downstream handoff to Nmap / Nerva

Netdiscover nuggets supply **IP list only**. Next pipeline stage:

```python
for row in rows:
    ip = row["IP"]
    # nmap port scan → open ports
    # nerva -t f"{ip}:{port}" --json
```

Do not emit `TCP_PORT_OPEN` from netdiscover rows — no port data exists at this layer.

## Deduplication

- Key IPs by address string
- Key MACs by normalized lowercase hex
- Multiple scans of same host: update `arp_count`, do not duplicate nodes

## Provenance

```python
node["provenance"] = {
    "module": "sfp_tool_netdiscover",
    "tool": "netdiscover",
    "flags": "-P -N",
    "raw_row": row,
}
```

## Edge cases

| Case | Handling |
|------|----------|
| `Unknown vendor` | Omit vendor node; keep MAC |
| Randomized MAC (locally administered) | Still emit MAC; flag `attributes.local_admin = True` if second-least bit set |
| Duplicate IP, different MAC | Emit both MAC edges; flag conflict in attributes |
| Passive-only scan without `-P` | Not supported for automated nuggets — rerun with `-P` |

## Cross-reference

- Generic row mapping patterns: [`../../textfsm/references/nugget-conversion.md`](../../textfsm/references/nugget-conversion.md)
- Service fingerprint nuggets: [`../../nerva/references/nugget-mapping.md`](../../nerva/references/nugget-mapping.md)
