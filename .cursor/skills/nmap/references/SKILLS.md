# Nmap References Index

| File | Contents |
|------|----------|
| [xml-output-schema.md](xml-output-schema.md) | XML element/attribute reference for `-oX` output and parser design |
| [workflows-and-phases.md](workflows-and-phases.md) | Scan phases, adaptive command sequences, timing tiers |
| [evasion-and-tactics.md](evasion-and-tactics.md) | Firewall/IDS evasion, hostile-network adaptation |
| [cli-flags.md](cli-flags.md) | Major flags grouped by purpose with usage notes |
| [nugget-mapping.md](nugget-mapping.md) | XML elements → SpiderFeet nugget types (nodes/edges) |
| [sources.md](sources.md) | Canonical nmap.org documentation URLs |

**Read order for new agents**

1. `workflows-and-phases.md` — understand discovery → ports → service/OS → NSE sequencing.
2. `xml-output-schema.md` — know what elements exist before writing parsers.
3. `nugget-mapping.md` — map parsed data to `IP_ADDRESS`, `TCP_PORT_OPEN`, `OPERATING_SYSTEM`, etc.
4. `cli-flags.md` — look up flags when composing commands.
5. `evasion-and-tactics.md` — when scans are filtered, throttled, or incomplete.

**Operator docs (repo root)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/NMAP-Zero-to-Hero.md` | End-to-end: scan → XML → Python → nuggets |
| `.docs/docs-for-cli-tools/NMAP-CLI-Options.md` | Comprehensive CLI options reference |
