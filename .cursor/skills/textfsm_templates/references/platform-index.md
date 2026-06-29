# Platform Index and CliTable Routing

NTC Templates uses a TextFSM **CliTable index** file to map `(Platform, Command)` → `.textfsm` template.

## Index file location

Inside `template_dir`:

```
template_dir/
  index                          # routing table (required)
  spiderfeet_netdiscover_parsable.textfsm
  spiderfeet_naabu_text.textfsm
  ...
```

First line of `index` = column headers. **Column 1** = template filename. **Last column** = command regex pattern.

## Index format

```
Template, Platform, Command
spiderfeet_netdiscover_parsable.textfsm, spiderfeet_netdiscover, netdiscover [[-P]]
cisco_ios_show_vlan.textfsm, cisco_ios, show vlan
```

### Column rules

| Column | Role |
|--------|------|
| `Template` | Filename relative to `template_dir` |
| `Platform` | Matched against `parse_output(platform=...)` |
| Middle columns | Optional metadata (regex allowed) |
| `Command` | Matched against `parse_output(command=...)`; use `[[]]` for optional abbreviations |

**Command abbreviation example:** `sh[[ow]] ip int[[erface]]` matches `show ip interface` and `sh ip int`.

## SpiderFeet platform naming

Use predictable platform slugs per CLI tool:

| Platform slug | Tool |
|---------------|------|
| `spiderfeet_netdiscover` | netdiscover `-P` / text modes |
| `spiderfeet_nmap` | nmap normal/grepable text (when not using `-oX`) |
| `spiderfeet_naabu` | naabu default text output |
| `spiderfeet_<tool>` | New corpus tools |

Command string should match the **examined command** in `{scenario}_command.txt` (normalized whitespace).

## Discovering stock templates

Browse https://github.com/networktocode/ntc-templates/tree/master/ntc_templates/templates for existing `.textfsm` files. Unlikely to match OSINT tools — but useful reference for template style.

List installed template path:

```python
import ntc_templates
from ntc_templates.parse import _get_template_dir
print(_get_template_dir())
```

## Testing index match

```python
from ntc_templates.parse import parse_output

try:
    parse_output(platform="spiderfeet_netdiscover", command="netdiscover -P", data=sample, template_dir=td)
except Exception as e:
    print("Index miss or template error:", e)
```

If no match: add index row + template file, or fix `Platform`/`Command` strings.

## Multiple commands, one tool

Separate index rows per distinct output shape:

```
spiderfeet_netdiscover_parsable.textfsm, spiderfeet_netdiscover, netdiscover -P
spiderfeet_netdiscover_active.textfsm, spiderfeet_netdiscover, netdiscover -a
```

Do not force one template to cover structurally different outputs unless states clearly branch.
