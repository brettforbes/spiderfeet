# Naabu Zero to Hero — Port Scanning, JSONL, and Nuggets

From install to orchestrated recon with **`naabu -json`**, nugget mapping, and pipelines to **httpx → Nerva → Nmap → Julius**.

Skill reference: `.cursor/skills/naabu/SKILL.md`

## What Naabu does

Naabu is ProjectDiscovery's **fast port scanner** (Go). It finds **open TCP/UDP ports** using SYN, CONNECT, or UDP probes — optimized for chaining in modern recon stacks.

Naabu does **not**:

- Replace full **Nmap** OS detection / NSE (chain Nmap after)
- Fingerprint application-layer LLM services (use **Julius** on HTTP ports)
- Deep service metadata without `-sV` or **Nerva**

---

## Level 0 — Install

### Prerequisites

| OS | Package |
|----|---------|
| Debian/Ubuntu | `sudo apt install -y libpcap-dev` |
| macOS | `brew install libpcap` |
| Windows | Install [Npcap](https://npcap.com/) |

### Binary

```bash
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
naabu -version
```

Or download from https://github.com/projectdiscovery/naabu/releases

---

## Level 1 — First scan

```bash
naabu -host scanme.sh
```

Default: top 100 ports, CONNECT scan if non-root.

Structured output:

```bash
naabu -host scanme.sh -json
```

```json
{"ip":"45.33.32.156","port":22}
{"ip":"45.33.32.156","port":80}
```

Pipe-friendly:

```bash
naabu -host scanme.sh -json -silent
```

---

## Level 2 — Port selection

```bash
naabu -host scanme.sh -p 22,80,443,8080 -json
naabu -host scanme.sh -top-ports 1000 -json
naabu -host scanme.sh -p - -json                    # full range — single host only
naabu -host scanme.sh -p u:53 -uP -json             # UDP with probes
```

---

## Level 3 — Multiple targets

```bash
naabu -host scanme.sh,example.com -p 443 -json
naabu -l hosts.txt -top-ports 100 -json -o batch.jsonl
subfinder -d example.com -silent | naabu -json -silent
```

---

## Level 4 — Scan types and tuning

| Goal | Command |
|------|---------|
| SYN (fast, root) | `naabu -host TARGET -s s -json` |
| CONNECT (non-root) | `naabu -host TARGET -s c -json` |
| Slower / safer | `naabu -host TARGET -rate 300 -c 10 -json` |
| CDN-aware | `naabu -host TARGET -ec -cdn -json` |
| Passive (InternetDB) | `naabu -host TARGET -passive -json` |

---

## Level 5 — Host discovery

```bash
naabu -host 192.168.1.0/24 -sn
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json
```

Use before port scanning large nets with many dead IPs.

---

## Level 6 — Service enrichment

```bash
naabu -host scanme.sh -sV -json
naabu -host scanme.sh -nmap-cli 'nmap -sV -oX nmap.xml'
```

Requires local Nmap service probes for `-sV`. Details: `.cursor/skills/naabu/references/nmap-integration.md`

---

## Level 7 — Pipelines

### httpx (web)

```bash
naabu -host example.com -json -silent | httpx -silent
```

### Nerva (service fingerprint)

```bash
naabu -host example.com -json -silent | jq -r '(.host//.ip)+":"+(.port|tostring)' | nerva --json
```

### Julius (LLM ports)

```bash
naabu -host corp.internal -p 11434,8000,8080 -json -silent -o ports.jsonl
jq -r '"https://" + .ip + ":" + (.port|tostring)' ports.jsonl | julius probe - -o jsonl
```

### Nmap (deep)

Port list from naabu JSON → targeted Nmap `-oX` (see Nmap Zero to Hero).

---

## Level 8 — Nugget mapping

For each JSONL line:

- `IP_ADDRESS` / `INTERNET_NAME` from `ip` / `host`
- `TCP_PORT_OPEN` or `UDP_PORT_OPEN` for `port`
- Optional `SOFTWARE_USED` when `-sV` populated `service`/`version`

Full rules: `.cursor/skills/naabu/references/nugget-mapping.md`

### Python example

```python
import json

with open("ports.jsonl", encoding="utf-8") as fh:
    for line in fh:
        row = json.loads(line)
        host = row.get("host") or row["ip"]
        print("TCP_PORT_OPEN", f"{host}:{row['port']}")
```

---

## Level 9 — Formal examination (SpiderFeet)

Per `.cursor/skills/cli_app_profiling/SKILL.md`:

| Scenario | Target / flags |
|----------|----------------|
| Positive permissive | `scanme.sh -top-ports 100 -json` |
| Rich | `-sV -json` with version fields |
| UDP | `-p u:53 -uP -json` |
| Passive | `-passive -json` |
| CDN | `-ec -cdn` on Cloudflare site |
| Clean miss | closed port or dead host |
| Pipeline | `-json -silent \| httpx` |

Artifacts: `app_examination_docs/naabu/scenarios/<key>/`

---

## Quick reference

```bash
naabu -host TARGET -json -o out.jsonl           # baseline
naabu -host TARGET -top-ports 1000 -json -silent
naabu -host TARGET -passive -json
naabu -host TARGET -sV -json
naabu -l hosts.txt -rate 500 -json
```

CLI details: `Naabu-CLI-Options.md`
