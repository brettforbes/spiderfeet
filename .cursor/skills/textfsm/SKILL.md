---
name: textfsm
description: Parse semi-structured CLI text into rows and SpiderFeet nugget nodes/edges using TextFSM templates. Use when given CLI stdout samples plus a target nugget hierarchy, writing TextFSM templates, CliTable routing, or Python parsers that emit nodes and edges arrays.
---

# TextFSM — CLI Output to Nuggets

## Purpose

Use when an agent receives **CLI text output** plus a **target nugget hierarchy** (nodes and edges array) and must produce a reusable Python function that parses the text into structured records, then maps those records to SpiderFeet nugget nodes and edges.

## Step-by-Step Instructions

1. **Inspect samples** — Collect one or more `(raw_text, target_nodes_edges)` pairs. Identify repeating row patterns, headers, multi-line blocks, and prompt/banner lines to skip.
2. **Design columns** — List fields needed for nuggets. Mark context fields (`Filldown`), unique keys (`Key`), mandatory fields (`Required`), and list-valued fields (`List`).
3. **Author template** — Create `.textfsm` with `Value` section then `Start` state. Order rules specific → general. Add `-> Record` when a logical row completes.
4. **Validate template** — `python -m textfsm.parser template.textfsm sample.txt` or unit-test with `textfsm.TextFSM`.
5. **Implement parser function** — Load template once; call `ParseTextToDicts()`; map each dict row to nodes/edges per target schema.
6. **Unify multiple samples** — If several samples share structure, one template + one function. If formats differ, use CliTable index or branch on a discriminator line.
7. **Emit nodes and edges** — Each nugget node: `{id, type, data, ...}`. Each edge: `{source, target, relation}`. Attach provenance (`source_module`, `raw_row`).
8. **Test edge cases** — Empty output, partial output (`eof=False`), missing optional columns, `List` columns, trailing filldown-only rows.

## If/Then Decision Rules

| If | Then |
|----|------|
| Same command, different vendors (Cisco/Juniper) | Use CliTable index; separate templates per vendor |
| Field repeats on continuation lines only | `Value List FIELD (...)` + `^prefix -> Continue.Record` before full-row rule |
| Context (hostname) on first line only | `Value Filldown Hostname (\S+)` + `Required` on a data column |
| Only last multi-line block appears | Missing `Record` on intermediate boundaries — add `Continue.Record` |
| Unknown lines must fail loudly | End template with `^. -> Error` |
| Partial/streamed input | `ParseText(text, eof=False)`; define empty `EOF` to suppress final record |
| Multiple samples, same columns | Single template; parameterise only if delimiter/prompt differs |
| Prompt line pollutes data | `^${HOST}[>#].` with `Filldown` or explicit skip rule |
| Output is already JSON/XML | Do **not** use TextFSM — use `json`/`xml` parser instead |

## Guardrails & Pitfalls

- Rules match **line start only** (`^` required). Greedy `.*` in values over-captures — prefer `\S+`, `\d+`.
- Blank line **inside** `Value` section breaks the template.
- `Continue` cannot change state.
- `Filldown` without `Required` on another column causes spurious trailing rows.
- `List` values are Python lists, not comma-separated strings.
- Do not parse interactive/TUI output — capture machine-readable mode (`-P`, `-oX`, `--json`) when available.
- TextFSM returns **rows**, not a graph — nugget hierarchy is a **second mapping step** you implement explicitly.
- Reserved value names and states: `Start`, `End`, `EOF` — do not reuse as column names.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `template-syntax.md` | Value options, states, rules, actions |
| `python-api.md` | `TextFSM`, `ParseText`, `ParseTextToDicts` |
| `clitable.md` | Multi-vendor template routing |
| `nugget-conversion.md` | Rows → nodes/edges mapping patterns |
| `pitfalls-and-examples.md` | Worked templates (ARP, routes, clock) |
| `sources.md` | Canonical URLs |

## Examples

### Minimal Python parser

```python
import textfsm
from pathlib import Path

_TEMPLATE = Path(__file__).with_name("show_ip_arp.textfsm")

def parse_show_ip_arp(raw: str) -> list[dict]:
    with _TEMPLATE.open() as f:
        fsm = textfsm.TextFSM(f)
    return fsm.ParseTextToDicts(raw)

def to_nodes_edges(rows: list[dict], seed_id: str) -> tuple[list, list]:
    nodes, edges = [], []
    for row in rows:
        ip_node = {"id": f"ip:{row['IP_ADDRESS']}", "type": "IP_ADDRESS", "data": row["IP_ADDRESS"]}
        mac_node = {"id": f"mac:{row['MAC_ADDRESS']}", "type": "MAC_ADDRESS", "data": row["MAC_ADDRESS"]}
        nodes.extend([ip_node, mac_node])
        edges.append({"source": seed_id, "target": ip_node["id"], "relation": "discovered"})
        edges.append({"source": ip_node["id"], "target": mac_node["id"], "relation": "has_mac"})
    return nodes, edges
```

### ARP table template (excerpt)

```
Value Required IP_ADDRESS (\d+\.\d+\.\d+\.\d+)
Value Required MAC_ADDRESS (\S+)
Value INTERFACE (\S+)

Start
  ^Protocol\s+Address
  ^\S+\s+${IP_ADDRESS}\s+\S+\s+${MAC_ADDRESS}\s+\S+\s+${INTERFACE} -> Record
  ^\S+\s+${IP_ADDRESS}\s+\S+\s+${MAC_ADDRESS}\s+\S+ -> Record
```

### Multi-line routes (`List` + `Continue.Record`)

```
Value NETWORK (\S+)
Value NEXTHOP (\S+)
Value List HOPS (\S+)

Start
  ^O -> Continue.Record
  ^O\s+${NETWORK}.*via\s+${NEXTHOP},
  ^\s+via\s+${HOPS},
```

### CliTable multi-vendor

```python
from textfsm import clitable

def parse_cmd(output: str, command: str, vendor: str) -> list[dict]:
    ct = clitable.CliTable("index", "templates/")
    ct.ParseCmd(output, {"Command": command, "Vendor": vendor})
    return [dict(zip(ct.header, row)) for row in ct]
```

### Validate from shell

```bash
python -m textfsm.parser templates/cisco_ios_show_ip_arp.textfsm fixtures/arp_sample.txt
```
