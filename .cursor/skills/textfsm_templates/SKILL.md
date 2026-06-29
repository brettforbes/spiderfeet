---
name: textfsm_templates
description: Parse CLI text into SpiderFeet nuggets using NTC Templates (parse_output, CliTable index, custom .textfsm). Use when given stdout samples plus target nodes/edges, extending ntc-templates for OSINT tools, or building parse_to_graph functions for text-only CLI corpus scenarios.
---

# TextFSM NTC Templates — CLI Text to Nuggets

## Purpose

Use when an agent receives **CLI text output** and a **target nugget hierarchy** (`nodes` + `edges`) and must deliver a reusable Python parser via **`ntc_templates.parse.parse_output`**, project-local TextFSM templates, and a **`to_nodes_edges()`** mapping — especially for **text-only** OSINT tools in the SpiderFeet CLI corpus.

## Step-by-Step Instructions

1. **Confirm text-only path** — If the tool supports JSON/XML, use native parsing instead (see [`cli_app_profiling`](../cli_app_profiling/SKILL.md)).
2. **Collect pairs** — `(raw_text, target_nodes_edges)` for each scenario; note command string and flags.
3. **Check stock NTC** — Browse bundled templates; OSINT tools usually need **local** templates.
4. **Author `.textfsm`** — Map repeating rows to `Value` columns; validate with `python -m textfsm.parser`.
5. **Update index** — Add `Template, Platform, Command` row under project `template_dir` (see [platform-index.md](references/platform-index.md)).
6. **Wrap `parse_output`** — `platform="spiderfeet_<tool>"`, `command="<exact examined command>"`, `template_dir=...`.
7. **Implement `to_nodes_edges(rows, seed_id)`** — Match approved graph types and relations ([nugget-conversion.md](references/nugget-conversion.md)).
8. **Unify samples** — One function when structure matches; separate modes/templates when not.
9. **Test** — Run on examination fixtures; diff against `proposed_nuggets_edges.json`.
10. **Document** — Template path, platform slug, and parser entry point in nugget structure doc.

## If/Then Decision Rules

| If | Then |
|----|------|
| Output is JSON/XML/YAML | Do **not** use this skill — use structured parser |
| Stock NTC template matches device output | `parse_output(platform="cisco_ios", ...)` with default dir |
| OSINT CLI (netdiscover, naabu text, …) | Local `spiderfeet_*` platform + custom `.textfsm` |
| `ParsingException` | Fix index Platform/Command or template states; use `-v` via raw TextFSM test |
| Multiple samples, same dict keys | Single template + single `parse_to_graph()` |
| Multiple samples, different shapes | Multiple index rows or templates; optional `mode` parameter |
| Windows `ImportError` (CliTable) | Install textfsm; see NTC FAQ for Windows patch |
| Need low-level state machine help | Use sibling [`textfsm`](../textfsm/SKILL.md) skill |
| `try_fallback=True` | Retry bundled ntc-templates after custom dir fails |
| List-valued column (ports, ifaces) | `Value List ...` in template |
| Context hostname on one line | `Value Filldown ...` |

## Guardrails & Pitfalls

- **`parse_output` returns rows, not graphs** — you must implement nugget mapping explicitly.
- **Platform/Command strings must match index exactly** (modulo CliTable abbreviation rules).
- Do not parse interactive TUI output — capture machine-readable flags (`-P`, `-oN`, etc.).
- **`template_dir` must contain `index`** — not a lone `.textfsm` file.
- Blank line inside TextFSM `Value` section breaks parsing.
- Do not over-merge scenarios with different column sets into one template.
- Prefer examination **structured artifact** from JSON mode when the tool provides it.
- Reserved TextFSM names: `Start`, `End`, `EOF` — not column names.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md):

| File | Topic |
|------|--------|
| `parse-api.md` | `parse_output`, `ParsingException` |
| `platform-index.md` | Index file, `spiderfeet_*` slugs |
| `extending-templates.md` | Author and validate templates |
| `nugget-conversion.md` | Rows → nodes/edges |
| `use-cases-and-workflow.md` | Corpus agent workflow |
| `textfsm-syntax-primer.md` | Template basics → `textfsm` skill |
| `sources.md` | Docs URLs |

Operator guide: `.docs/docs-for-cli-tools/TextFSM-Templates-Zero-to-Hero.md`

Sibling: [`../textfsm/SKILL.md`](../textfsm/SKILL.md) — raw TextFSM authoring.

## Comprehensive Examples

### Install

```bash
pip install ntc-templates textfsm
```

### Stock NTC parse

```python
from ntc_templates.parse import parse_output

rows = parse_output(platform="cisco_ios", command="show vlan", data=vlan_text)
```

### Custom template directory

```python
from ntc_templates.parse import parse_output

rows = parse_output(
    platform="spiderfeet_netdiscover",
    command="netdiscover -P",
    data=raw,
    template_dir=".docs/docs-for-cli-tools/textfsm_templates",
)
```

### `try_fallback`

```python
rows = parse_output(
    platform="cisco_ios",
    command="show ip arp",
    data=raw,
    template_dir="/custom/path",
    try_fallback=True,
)
```

### Error handling

```python
from ntc_templates.parse import parse_output, ParsingException

try:
    rows = parse_output(platform="spiderfeet_naabu", command="naabu", data=raw, template_dir=td)
except ParsingException as e:
    raise RuntimeError("Template/index mismatch") from e
```

### Validate template offline

```bash
python -m textfsm.parser .docs/docs-for-cli-tools/textfsm_templates/spiderfeet_netdiscover_parsable.textfsm fixture.txt
```

### Full parse-to-graph function

```python
def parse_netdiscover_to_graph(raw: str, seed_id: str) -> tuple[list, list]:
    rows = parse_output(
        platform="spiderfeet_netdiscover",
        command="netdiscover -P",
        data=raw,
        template_dir=str(TEMPLATE_DIR),
    )
    return to_nodes_edges(rows, seed_id)
```

### Index row example

```
Template, Platform, Command
spiderfeet_netdiscover_parsable.textfsm, spiderfeet_netdiscover, netdiscover -P
```

### Multi-sample facade

```python
def parse_netdiscover(raw: str, mode: str = "parsable") -> list[dict]:
    commands = {"parsable": "netdiscover -P", "active": "netdiscover -a"}
    return parse_output(
        platform="spiderfeet_netdiscover",
        command=commands[mode],
        data=raw,
        template_dir=str(TEMPLATE_DIR),
    )
```

### CliTable attributes (low-level)

```python
from textfsm import clitable

ct = clitable.CliTable("index", template_dir)
ct.ParseCmd(raw, {"Command": "netdiscover -P", "Platform": "spiderfeet_netdiscover"})
rows = [dict(zip(ct.header, r)) for r in ct]
```

## Strategies and Tactics

### Corpus text-only tool onboarding

1. Run formal examination → save `output_text.txt`.
2. Draft target graph in `nugget_structure/*_proposed_nuggets_edges.json`.
3. Iterate TextFSM until `python -m textfsm.parser` rows cover all fields.
4. Wire `parse_output` + `to_nodes_edges`; operator approves graph match.
5. Store template in repo; reference in scenario manifest.

### Maximize reuse across scenarios

- Union `Value` columns only when row grammar is identical.
- Use **`Filldown`** for repeated scan headers (subnet, interface).
- Use **`List`** for multi-value cells instead of post-splitting strings.
- Share one `to_nodes_edges()` when node types align; branch only on row content.

### When stock NTC helps

- Parsing saved **network device** show command output in lab fixtures.
- Learning template patterns from `cisco_ios`, `juniper_junos` examples before authoring OSINT templates.

### Pipeline position

**CLI tool (text mode) → NTC parse_output → to_nodes_edges → SpiderFeet graph**

Parallel path: **CLI tool (-json) → json.loads → map nuggets** (preferred when available).
