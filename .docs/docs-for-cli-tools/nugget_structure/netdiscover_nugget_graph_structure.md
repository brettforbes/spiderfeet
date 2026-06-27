# Netdiscover — proposed nugget graph structure

**Skill:** `.cursor/skills/netdiscover/SKILL.md` · **Epic:** #853 / task #854

Generator: `.seed/scripts/cli_corpus/cli_tool_to_graph.py` · TextFSM: `.seed/scripts/cli_corpus/templates/netdiscover_parsable.textfsm`

## Scan head

`SCAN_RECORD` with `SCAN_CLI`, `SCAN_TARGET` via `had`. Discovered hosts via `contains`.

## Host discovery row (`-P` parseable)

```
SCAN_RECORD --contains--> HOST --contains--> IP_ADDRESS
HOST --had--> MAC_ADDRESS --had--> RAW_RIR_DATA (vendor)
```

## Scenarios examined

| Key | Mode | Semantic output |
|-----|------|-----------------|
| `local_subnet_active_parsable` | Active `-P -N -r 172.18.0.0/24` | IP, MAC, vendor |
| `local_subnet_active_text` | Active TUI snippet | Human table |
| `local_subnet_fast_parsable` | `-f` fast gateway probe | Sparse IP/MAC |
| `passive_snippet_text` | `-p` bounded | Passive banner only |
| `sparse_subnet_parsable` | Empty /24 clean miss | Footer, zero hosts |

Downstream: hand IP list to Nmap → Nerva (see Nmap/Nerva pilots).
