# CliTable — Multi-Vendor Template Routing

Canonical: [Cli-Table wiki](https://github.com/google/textfsm/wiki/Cli-Table)

CliTable selects the correct TextFSM template from command metadata, then parses internally.

## Index file format

CSV-like file in templates directory:

```
Template, Hostname, Vendor, Command
cisco_ios_show_ip_arp.textfsm, .*, Cisco, sh[[ow]] ip ar[[p]]
juniper_show_arp.textfsm, .*, Juniper, show ar[[p]]
```

- First line = column headers (mandatory)
- Column 1 = template filename (fixed position)
- Last column = command pattern (fixed position)
- Middle columns = optional metadata (regex allowed except inside `[[]]`)

**Command abbreviation:** `sh[[ow]] ip int[[erface]] br[[ief]]` matches `sh ip int br`.

## Python usage

```python
from textfsm import clitable

cli_table = clitable.CliTable("index", "templates/")
attributes = {"Command": "show ip arp", "Vendor": "Cisco"}
cli_table.ParseCmd(raw_output, attributes)

records = [dict(zip(cli_table.header, row)) for row in cli_table]
formatted = cli_table.FormattedTable()
```

## Import note

| Version | Import |
|---------|--------|
| ≤ 0.4.1 | `import clitable` |
| ≥ 1.1.0 | `from textfsm import clitable` |

## Ecosystem

[ntc-templates](https://github.com/networktocode/ntc-templates) ships hundreds of production templates used by Netmiko/NAPALM workflows. Prefer reusing ntc-templates before writing from scratch.

## Merging tables

Tables with identical columns can merge: `combined = t1 + t2`.
