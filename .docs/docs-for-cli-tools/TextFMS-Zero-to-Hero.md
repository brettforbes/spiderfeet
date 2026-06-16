# TextFSM Zero to Hero — Parsing CLI Output into Nuggets

Guide for using Google's TextFSM library to turn semi-structured CLI text into SpiderFeet nugget graphs (nodes + edges).

## 0. Why TextFSM?

OSINT and network CLI tools emit human-readable text: tables, banners, multi-line blocks. Regex alone breaks on format drift. TextFSM uses **template-driven finite state machines** — one template per output shape — producing consistent row dictionaries you map to nuggets.

**Use TextFSM when:** output is line-oriented text (show commands, `-P` parseable mode, CSV-like dumps).

**Do not use TextFSM when:** output is JSON, XML, or JSONL — parse natively.

## 1. Install

```bash
pip install textfsm
python -c "import textfsm; print(textfsm.__version__ if hasattr(textfsm,'__version__') else 'ok')"
```

## 2. Hello World

**sample.txt:**
```
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.0.0.1                -   0011.2233.4455  ARPA   GigabitEthernet0/0
```

**template.textfsm:**
```
Value IP (\d+\.\d+\.\d+\.\d+)
Value MAC (\S+)

Start
  ^Protocol
  ^Internet\s+${IP}\s+\S+\s+${MAC} -> Record
```

**parse.py:**
```python
import textfsm
with open("template.textfsm") as t, open("sample.txt") as s:
    fsm = textfsm.TextFSM(t)
    print(fsm.ParseTextToDicts(s.read()))
```

## 3. Template syntax essentials

### Values (columns)

```
Value Filldown Hostname (\S+)
Value Required IP_ADDRESS (\d+\.\d+\.\d+\.\d+)
Value List NEXTHOP (\S+)
```

| Option | When to use |
|--------|-------------|
| `Filldown` | Hostname/prompt on first line only |
| `Required` | Row invalid without this field |
| `List` | Multiple values per row (next-hops, VLANs) |
| `Key` | Uniqueness for dedup |

### States and rules

```
Start
  ^header line to skip
  ^data ${COL1} ${COL2} -> Record
  ^continuation -> Continue.Record
```

Actions: `Next`, `Continue`, `Record`, `Clear`, `Error`.

Full reference: `.cursor/skills/textfsm/references/template-syntax.md`

## 4. Python API

```python
fsm = textfsm.TextFSM(open("t.textfsm"))
rows = fsm.ParseText(cli_output)           # list of lists
dicts = fsm.ParseTextToDicts(cli_output)   # list of dicts
cols = fsm.header                          # column names
```

Validate: `python -m textfsm.parser template.textfsm sample.txt`

## 5. Multi-vendor CLI (CliTable)

When the same logical command differs by vendor:

```python
from textfsm import clitable
ct = clitable.CliTable("index", "templates/")
ct.ParseCmd(output, {"Command": "show arp", "Vendor": "Cisco"})
records = [dict(zip(ct.header, r)) for r in ct]
```

Reuse [ntc-templates](https://github.com/networktocode/ntc-templates) when possible.

## 6. Convert rows to nuggets

TextFSM stops at structured rows. You implement the graph layer:

```python
def rows_to_graph(rows: list[dict], seed_id: str) -> tuple[list, list]:
    nodes, edges = [], []
    seen = set()
    for row in rows:
        nid = f"ip:{row['IP']}"
        if nid not in seen:
            nodes.append({"id": nid, "type": "IP_ADDRESS", "data": row["IP"]})
            edges.append({"source": seed_id, "target": nid, "relation": "discovered"})
            seen.add(nid)
        if "MAC" in row:
            mid = f"mac:{row['MAC']}"
            nodes.append({"id": mid, "type": "MAC_ADDRESS", "data": row["MAC"]})
            edges.append({"source": nid, "target": mid, "relation": "has_mac"})
    return nodes, edges
```

Nugget types: `.docs/analysis/nuggets.json`

## 7. Agent workflow (SpiderFeet)

When given `(cli_text, target_nodes_edges)` pairs:

1. Analyse target graph — which nugget types and edge relations?
2. Design template columns to supply those fields
3. Author `.textfsm`; test against all samples
4. Write `parse_*()` + `to_nodes_edges()` in Python
5. Unify across samples if structure matches

Skill: `.cursor/skills/textfsm/SKILL.md`

## 8. Tools that pair with TextFSM

| Tool | Capture mode | TextFSM role |
|------|--------------|--------------|
| Netdiscover | `-P` flag | Parse IP/MAC/vendor table |
| airodump-ng | `.csv` export | Parse AP/station sections |
| Generic show commands | stdout redirect | Custom template per command |

Tools with native JSON/XML (Nmap `-oX`, Nerva `--json`, Nuclei `-jsonl`) skip TextFSM.

## 9. Common mistakes

- Forgetting `-> Record` on multi-line records
- Using greedy `.*` — prefer `\S+`, `\d+`
- Parsing interactive TUI — use machine-readable flags
- Expecting TextFSM to emit graphs — mapping is your code

See `.cursor/skills/textfsm/references/pitfalls-and-examples.md`

## 10. Next steps

- Read full skill: `.cursor/skills/textfsm/SKILL.md`
- Browse ntc-templates for your CLI vendor
- Integrate parser into `sfp_tool_*` modules per Stage 4 corpus guide

## Further reading

- `.cursor/skills/textfsm/references/sources.md` — all canonical URLs
- PyNeng chapter 21 — worked network examples
- SpiderFeet parsing primitives — `.docs/analysis/conversion_to_types/03-parsing-primitives.md`
