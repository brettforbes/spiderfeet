# `parse_output` API

Primary entry point: `ntc_templates.parse.parse_output`.

## Signature

```python
from ntc_templates.parse import parse_output, ParsingException

rows = parse_output(
    platform="cisco_ios",      # CliTable Platform attribute
    command="show vlan",       # CliTable Command attribute
    data=raw_cli_stdout,       # str: full command output
    template_dir=None,         # optional: custom templates root with index
    try_fallback=False,        # retry with default ntc-templates dir on failure
)
```

## Returns

**`list[dict]`** — one dict per parsed row. Keys = TextFSM `Value` names (lowercased in ntc-templates convention, e.g. `vlan_id`, `interfaces`).

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `platform` | Yes* | Platform slug matching index column (e.g. `cisco_ios`, `spiderfeet_netdiscover`) |
| `command` | Yes* | Command string matching index pattern (supports `[[]]` abbreviation syntax) |
| `data` | Yes | Raw CLI stdout (str) |
| `template_dir` | No | Directory containing `index` file + `.textfsm` templates |
| `try_fallback` | No | If custom `template_dir` fails, retry bundled ntc-templates |

\*Both required for CliTable routing.

## Exceptions

| Exception | Cause |
|-----------|--------|
| `ParsingException` | No matching index row, template `Error` state, or CliTable failure |
| `ImportError` | TextFSM/CliTable unavailable (common on Windows without patch) |

## Examples

### Stock NTC template (network device)

```python
vlan_output = """\
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/1
10   Management                       active
"""

rows = parse_output(platform="cisco_ios", command="show vlan", data=vlan_output)
# [{'vlan_id': '1', 'name': 'default', 'status': 'active', 'interfaces': ['Gi0/1']}, ...]
```

### Custom SpiderFeet template directory

```python
from pathlib import Path

TEMPLATE_ROOT = Path(".docs/docs-for-cli-tools/textfsm_templates")

rows = parse_output(
    platform="spiderfeet_netdiscover",
    command="netdiscover -P",
    data=raw_text,
    template_dir=str(TEMPLATE_ROOT),
)
```

### Fallback to bundled templates

```python
rows = parse_output(
    platform="cisco_ios",
    command="show ip arp",
    data=raw,
    template_dir="/path/to/custom",
    try_fallback=True,
)
```

### Error handling

```python
try:
    rows = parse_output(platform="spiderfeet_naabu", command="naabu text", data=raw, template_dir=td)
except ParsingException as exc:
    # No template match — author or extend template
    raise
```

## Internal flow

1. Resolve `template_dir` (arg → env → package default).
2. `clitable.CliTable("index", template_dir)`.
3. `ParseCmd(data, {"Command": command, "Platform": platform})`.
4. Convert table rows to `list[dict]`.

Low-level CliTable details: [`../../textfsm/references/clitable.md`](../../textfsm/references/clitable.md).
