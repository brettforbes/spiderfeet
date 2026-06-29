# TextFSM NTC Templates Zero to Hero — CLI Text to Nuggets

From install to **`parse_output` → nodes/edges** for SpiderFeet CLI corpus text-only tools.

Skill reference: `.cursor/skills/textfsm_templates/SKILL.md`  
Raw TextFSM grammar: `.cursor/skills/textfsm/SKILL.md`

## What NTC Templates provides

[NTC Templates](https://github.com/networktocode/ntc-templates) is a library of **TextFSM templates** plus a Python wrapper around TextFSM's **CliTable**. You pass:

- **platform** (e.g. `cisco_ios`, `spiderfeet_netdiscover`)
- **command** (e.g. `show vlan`, `netdiscover -P`)
- **data** (raw CLI stdout)

You get back **`list[dict]`** — structured rows ready for nugget mapping.

---

## Level 0 — Install

```bash
pip install ntc-templates textfsm
```

Verify:

```python
from ntc_templates.parse import parse_output
print("OK")
```

On Windows, if import fails, see [NTC FAQ](https://ntc-templates.readthedocs.io/en/latest/user/faq/) for TextFSM/CliTable notes.

---

## Level 1 — First parse (stock template)

```python
from ntc_templates.parse import parse_output

vlan_output = """\
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/1
10   Management                       active
"""

rows = parse_output(platform="cisco_ios", command="show vlan", data=vlan_output)
print(rows[0]["vlan_id"], rows[0]["name"])
```

---

## Level 2 — Understand the index

CliTable uses an **index** file in the template directory:

```
Template, Platform, Command
cisco_ios_show_vlan.textfsm, cisco_ios, show vlan
```

Your `platform` and `command` arguments select the row → `.textfsm` file.

Find bundled templates after install:

```python
from ntc_templates.parse import _get_template_dir
print(_get_template_dir())
```

---

## Level 3 — SpiderFeet OSINT workflow

OSINT CLI tools rarely match stock NTC templates. Create **project-local** templates:

```
.docs/docs-for-cli-tools/textfsm_templates/
  index
  spiderfeet_netdiscover_parsable.textfsm
```

### Index entry

```
Template, Platform, Command
spiderfeet_netdiscover_parsable.textfsm, spiderfeet_netdiscover, netdiscover -P
```

### Parse examination fixture

```python
from pathlib import Path
from ntc_templates.parse import parse_output

TEMPLATE_DIR = Path(".docs/docs-for-cli-tools/textfsm_templates")
raw = Path("app_examination_docs/netdiscover/scenarios/parsable/output_text.txt").read_text()

rows = parse_output(
    platform="spiderfeet_netdiscover",
    command="netdiscover -P",
    data=raw,
    template_dir=str(TEMPLATE_DIR),
)
```

---

## Level 4 — Author a template

1. Open fixture text; mark header vs data lines.
2. Create `.textfsm` with `Value` lines + `Start` state.
3. Validate:

```bash
python -m textfsm.parser .docs/docs-for-cli-tools/textfsm_templates/spiderfeet_netdiscover_parsable.textfsm fixture.txt
```

4. Add index row; retry `parse_output`.

Syntax details: `.cursor/skills/textfsm/references/template-syntax.md`

---

## Level 5 — Map rows to nuggets

Target graph lives in `nugget_structure/*_proposed_nuggets_edges.json`.

```python
def to_nodes_edges(rows: list[dict], seed_id: str) -> tuple[list, list]:
    nodes, edges = [], []
    for row in rows:
        ip_id = f"ip:{row['ip']}"
        nodes.append({"id": ip_id, "type": "IP_ADDRESS", "data": row["ip"]})
        edges.append({"source": seed_id, "target": ip_id, "relation": "discovered"})
    return nodes, edges

def parse_to_graph(raw: str, seed_id: str):
    rows = parse_output(...)  # as above
    return to_nodes_edges(rows, seed_id)
```

Compare output to approved JSON before operator sign-off.

---

## Level 6 — Multiple scenarios, one tool

| Scenario | Command in index | Template file |
|----------|------------------|---------------|
| Parsable | `netdiscover -P` | `spiderfeet_netdiscover_parsable.textfsm` |
| Active scan | `netdiscover -a` | `spiderfeet_netdiscover_active.textfsm` |

Facade:

```python
def parse_netdiscover(raw, mode="parsable"):
    cmd = {"parsable": "netdiscover -P", "active": "netdiscover -a"}[mode]
    return parse_output(platform="spiderfeet_netdiscover", command=cmd, data=raw, template_dir=td)
```

Unify into **one graph function** only when `to_nodes_edges()` logic is identical.

---

## Level 7 — Agent scenario (prompt 03A2)

**Input:** one or more `(text sample, target nodes/edges)` pairs  
**Output:** shared Python function when possible

Checklist:

- [ ] Text-only confirmed (no JSON path)
- [ ] Template parses all samples
- [ ] `parse_output` returns expected dict keys
- [ ] Graph matches target hierarchy
- [ ] Template + index committed under `textfsm_templates/`
- [ ] Unit test with examination fixture

---

## Level 8 — Formal examination integration

Per `.cursor/skills/cli_app_profiling/SKILL.md`:

| Artifact | Content |
|----------|---------|
| `output_text.txt` | Raw CLI stdout |
| `output_structured.json` | `list[dict]` from parser OR native JSON |
| `proposed_nuggets_edges.json` | Target graph |

When tool offers `-json`, capture that **instead** of TextFSM for primary structured artifact; keep TextFSM as fallback or cross-check.

---

## Quick reference

```bash
pip install ntc-templates textfsm
python -m textfsm.parser template.textfsm sample.txt
```

```python
from ntc_templates.parse import parse_output, ParsingException

rows = parse_output(platform="spiderfeet_tool", command="tool -flag", data=raw, template_dir=td)
```

---

## Related docs

| Resource | Path |
|----------|------|
| NTC parse API | `.cursor/skills/textfsm_templates/references/parse-api.md` |
| Platform index | `.cursor/skills/textfsm_templates/references/platform-index.md` |
| Raw TextFSM skill | `.cursor/skills/textfsm/SKILL.md` |
| NTC Read the Docs | https://ntc-templates.readthedocs.io |
