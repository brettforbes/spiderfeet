# Nerva Zero to Hero

From install to orchestrated service fingerprinting with `--json` output, nugget mapping, and the **netdiscover → Nmap → Nerva** pipeline.

## What Nerva does

Nerva answers: **what service is running on this open port?**

It is a fast, open-source **service fingerprinter** (Go binary) supporting 54+ plugins across TCP, UDP, and SCTP. It uses port-aware priority queuing — try SSH on 22 first, HTTPS on 443, etc. — and falls back to broader probes when needed.

Nerva does **not**:

- Discover live hosts (use **netdiscover** or `nmap -sn`)
- Find open ports (use **Nmap**, Naabu, or Masscan)

It expects `host:port` targets where the port is already known open.

---

## Level 0 — Install

### Prebuilt binary

Download from https://github.com/praetorian-inc/nerva/releases for Linux, macOS, or Windows.

### Go install

```bash
go install github.com/praetorian-inc/nerva/cmd/nerva@latest
nerva -h
```

---

## Level 1 — First fingerprint

```bash
nerva -t example.com:22
```

Human output:

```
ssh://example.com:22
```

For automation, always add `--json`:

```bash
nerva -t example.com:22 --json
```

```json
{"host":"example.com","ip":"93.184.216.34","port":22,"protocol":"ssh","transport":"tcp","metadata":{...}}
```

---

## Level 2 — Multiple targets

### Comma-separated

```bash
nerva -t example.com:22,example.com:80,example.com:443 --json
```

### Target file

```bash
cat > targets.txt <<EOF
example.com:22
example.com:80
example.com:443
EOF

nerva -l targets.txt --json -o results.jsonl
```

Each line in `results.jsonl` is one JSON object.

---

## Level 3 — Output formats

| Flag | Format | Use |
|------|--------|-----|
| `--json` | JSON Lines | **SpiderFeet modules** |
| `--csv` | CSV with header | Spreadsheets |
| *(none)* | `protocol://host:port` | Quick manual checks |

### Parse JSON Lines in Python

```python
import json

with open("results.jsonl") as f:
    for line in f:
        line = line.strip()
        if line:
            svc = json.loads(line)
            print(svc["protocol"], svc["host"], svc["port"])
```

---

## Level 4 — UDP and SCTP

### UDP (DNS, SNMP, NTP…)

```bash
sudo nerva -t 10.0.0.1:53 -U --json
```

### SCTP (Diameter, Linux only)

```bash
nerva -t mme.telecom.local:3868 -S --json
```

---

## Level 5 — Performance tuning

| Flag | Effect |
|------|--------|
| `--fast` | Default-port plugins only — much faster |
| `-w 5000` | 5 second timeout per probe |
| `-v` | Verbose stderr for debugging |

```bash
nerva -l huge_targets.txt --fast --json -o fast_pass.jsonl
```

Re-run without `--fast` on hosts that returned no fingerprint.

---

## Level 6 — Pipe from port scanners

### Naabu

```bash
naabu -host example.com -silent | nerva --json
```

### Masscan

```bash
masscan -p1-65535 10.0.0.0/24 --rate=10000 -oL - | \
  grep '^open' | awk '{print $4":"$3}' | \
  nerva --json -o results.jsonl
```

### Nmap

```bash
nmap -p- --open 192.168.1.0/24 -oG /tmp/ports.gnmap

awk '/\/open\//{
  ip=$2; gsub(/.*Ports: /,""); n=split($0,a,",")
  for(i=1;i<=n;i++){split(a[i],f,"/"); if(f[2]=="open") print ip":"f[1]}
}' /tmp/ports.gnmap | sort -u > targets.txt

nerva -l targets.txt --json -o fingerprints.jsonl
```

---

## Level 7 — Full pipeline with Netdiscover

```bash
# Step 1: L2 host discovery (local VLAN)
sudo netdiscover -P -N -r 192.168.1.0/24 | awk '{print $1}' | sort -u > ips.txt

# Step 2: Port discovery
nmap -p- --open -T4 -iL ips.txt -oG /tmp/nmap.gnmap

# Step 3: Build nerva target list
awk '/\/open\//{ip=$2; gsub(/.*Ports: /,""); n=split($0,a,",");
  for(i=1;i<=n;i++){split(a[i],f,"/"); if(f[2]=="open") print ip":"f[1]}}' \
  /tmp/nmap.gnmap | sort -u > targets.txt

# Step 4: Service fingerprint
nerva -l targets.txt --json -o fingerprints.jsonl
```

### Data flow

```
netdiscover (-P)  →  TextFSM  →  IP/MAC nuggets
nmap            →  open ports
nerva (--json)  →  service nuggets (protocol + metadata)
```

Skills:

- `.cursor/skills/netdiscover/SKILL.md`
- `.cursor/skills/nerva/SKILL.md`
- `.cursor/skills/textfsm/SKILL.md`

---

## Level 8 — Convert to SpiderFeet nuggets

For each JSON line:

1. Emit or link `IP_ADDRESS`
2. Emit `TCP_PORT_OPEN` or `UDP_PORT_OPEN` as `{ip}:{port}`
3. Emit `SOFTWARE_USED` / banner from `protocol` and `metadata`
4. Attach full `metadata` as provenance

See `.cursor/skills/nerva/references/nugget-mapping.md`.

---

## Level 9 — Orchestrated playbooks

### Playbook A — Web assessment prep

1. Nmap top ports on discovered IPs
2. `nerva --json` on all open ports
3. `jq 'select(.protocol=="http" or .protocol=="https")'` for web targets
4. Downstream: Nuclei, CMSeeK, WAFWOOF

### Playbook B — Database exposure

```bash
nerva -l targets.txt --json | jq 'select(.protocol | test("mysql|postgresql|redis|mongodb"))'
```

### Playbook C — Telecom / ICS

1. Nmap targeted ports (3868, 502, …)
2. `nerva -S` for SCTP Diameter
3. `nerva` default for Modbus TCP

### Playbook D — Continuous CI check

```bash
nerva -l allowed_services.txt --json | tee out.jsonl
jq -e 'select(.protocol | IN("ssh","http","https") | not)' out.jsonl && exit 1
```

---

## jq recipes

```bash
# SSH services only
nerva -l targets.txt --json | jq 'select(.protocol=="ssh")'

# Count by protocol
nerva -l targets.txt --json | jq -s 'group_by(.protocol) | map({p: .[0].protocol, n: length})'

# Export HTTP IPs
nerva -l targets.txt --json | jq -r 'select(.protocol=="http") | .ip'
```

---

## Protocol coverage

54 plugins documented in the wiki — databases, remote access, web, messaging, ICS, telecom. See:

- `.cursor/skills/nerva/references/protocol-list.md`
- https://github.com/praetorian-inc/nerva/wiki/Protocol-List

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Running nerva on IPs without ports | Port scan first |
| Parsing `ssh://` text | Use `--json` |
| Expecting host discovery | Use netdiscover |
| UDP services missed | Add `-U` and sudo |
| Slow on huge lists | `--fast` first pass |

---

## Further reading

| Topic | Location |
|-------|----------|
| CLI flags | [Nerva-CLI-Options.md](Nerva-CLI-Options.md) |
| JSON schema | `.cursor/skills/nerva/references/json-output-schema.md` |
| Tactics | `.cursor/skills/nerva/references/tactics.md` |
| Netdiscover pipeline | [NetDiscover-Zero-to-Hero.md](NetDiscover-Zero-to-Hero.md) |
| Integration guide | https://github.com/praetorian-inc/nerva/wiki/Integration-Guide |

---

## Authorization

Fingerprint only systems and ports you are authorized to test. Service probes send protocol-specific traffic to open ports.
