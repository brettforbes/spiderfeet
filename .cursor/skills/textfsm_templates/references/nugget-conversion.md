# Parsed Rows → Nugget Nodes and Edges

NTC `parse_output` returns **`list[dict]`**. The agent must implement an explicit **`to_nodes_edges()`** layer to match the supplied target hierarchy.

## Input contract (SpiderFeet scenario)

The agent receives one or more pairs:

| Input | Description |
|-------|-------------|
| `raw_text` | CLI stdout sample |
| `target_nodes_edges` | Approved `{nodes: [...], edges: [...]}` from nugget structure doc |

Goal: one reusable **`parse_<tool>_<mode>(raw: str) -> tuple[list, list]`** when samples share structure.

## Implementation pattern

```python
from pathlib import Path
from ntc_templates.parse import parse_output, ParsingException

_TEMPLATE_DIR = Path(".docs/docs-for-cli-tools/textfsm_templates")
PLATFORM = "spiderfeet_netdiscover"
COMMAND = "netdiscover -P"

def parse_netdiscover_parsable(raw: str) -> list[dict]:
    return parse_output(
        platform=PLATFORM,
        command=COMMAND,
        data=raw,
        template_dir=str(_TEMPLATE_DIR),
    )

def to_nodes_edges(rows: list[dict], seed_id: str) -> tuple[list, list]:
    nodes, edges = [], []
    seen = set()

    def add_node(nid: str, ntype: str, data: str):
        if nid in seen:
            return
        seen.add(nid)
        nodes.append({"id": nid, "type": ntype, "data": data})

    for row in rows:
        ip = row.get("ip") or row.get("IP")
        mac = row.get("mac") or row.get("MAC")
        if ip:
            ip_id = f"ip:{ip}"
            add_node(ip_id, "IP_ADDRESS", ip)
            edges.append({"source": seed_id, "target": ip_id, "relation": "discovered"})
        if mac and ip:
            mac_id = f"mac:{mac}"
            add_node(mac_id, "MAC_ADDRESS", mac)
            edges.append({"source": f"ip:{ip}", "target": mac_id, "relation": "has_mac"})
    return nodes, edges

def parse_to_graph(raw: str, seed_id: str) -> tuple[list, list]:
    rows = parse_netdiscover_parsable(raw)
    return to_nodes_edges(rows, seed_id)
```

Adjust field names to match **your** TextFSM `Value` definitions and target hierarchy.

## Unifying multiple samples

| Case | Strategy |
|------|----------|
| Same columns, same row shape | One template + one `parse_*()` |
| Same tool, different flags | Multiple index rows; `parse_*()` accepts `mode` param |
| Different column sets | Separate templates; optional facade function |
| Only banner/prompt differs | One template with skip rules |

Compare approved `proposed_nuggets_edges.json` files — node `type` and `relation` must match exactly.

## Validation against target hierarchy

1. Run parser on fixture text.
2. Deep-compare node `type` + `data` sets (ignore id if target uses different id scheme — align id generation).
3. Compare edge `relation` semantics.
4. Document unmapped template columns as `SPEC_GAP` or extend template.

## Provenance

```python
node["provenance"] = {
    "parser": "ntc_templates.parse_output",
    "platform": PLATFORM,
    "command": COMMAND,
    "raw_row": row,
}
```

## Reference

General row→graph patterns: [`../../textfsm/references/nugget-conversion.md`](../../textfsm/references/nugget-conversion.md)

Nugget vocabulary: `.seed/05_Onotology_for_Nuggets.md`, `.docs/analysis/nuggets.json`
