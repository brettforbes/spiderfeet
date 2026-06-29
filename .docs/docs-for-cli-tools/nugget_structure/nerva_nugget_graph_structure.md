# Nerva — proposed nugget graph structure

**Skill:** `.cursor/skills/nerva/SKILL.md` · **Epic:** #853 / task #855

Generator: `.seed/scripts/cli_corpus/cli_tool_to_graph.py` · Binary: `.tools/bin/nerva.exe`

## Scan head

`SCAN_RECORD` + `SCAN_CLI`. Each JSON line enriches a host:port with protocol and version metadata.

## Service fingerprint row (`--json`)

```
SCAN_RECORD --contains--> HOST --contains--> PORT
PORT --had--> PORT_PROTOCOL
PORT --listens-to--> SERVICE --had--> SERVICE_VERSION (when present)
```

## Scenarios examined

| Key | Target | Notes |
|-----|--------|-------|
| `tcp_scanme_http_json` | scanme.nmap.org:80 | HTTP + Apache metadata |
| `tcp_scanme_ssh_json` | :22 | SSH fingerprint |
| `tcp_multi_target_json` | :80,:22 | Multi-target |
| `tcp_fast_scanme_json` | :443 | `--fast` |
| `tcp_closed_port_clean_miss` | :1 | No JSON line (clean miss) |
| `tcp_scanme_human_text` | :80 | Human `ssh://`-style output |

Upstream: netdiscover/Nmap port discovery. Structured output is **JSON Lines** only for graph derivation.
