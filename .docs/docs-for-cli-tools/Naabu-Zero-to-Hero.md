# Naabu Zero to Hero — Port Scanning, JSONL, and Nuggets

From install to orchestrated recon with **`naabu -json`**, nugget mapping, and pipelines to **httpx → Nerva → Nmap → Julius**.

Skill reference: `.cursor/skills/naabu/SKILL.md`

**Binary (this repo):** `C:\projects\spiderfeet\.tools\naabu\naabu.exe` — **v2.6.1** (help captured **2026-08-10**).

## What Naabu does

Naabu is ProjectDiscovery's **fast port scanner** (Go). It finds **open ports** using **SYN** or **CONNECT** (and optional UDP port syntax from PD Running docs), optimized for chaining in modern recon stacks.

Naabu does **not**:

- Replace full **Nmap** OS detection / NSE (chain Nmap after)
- Fingerprint application-layer LLM services (use **Julius** on candidate ports)
- Deep service metadata without `-sV` / `-sD` or **Nerva**

### Windows / privileges

| Fact | Implication |
|------|-------------|
| Help default `-s` is **`c` (CONNECT)** | Unprivileged Windows scans should stay on CONNECT |
| `naabu -hc` may show `Privileged/NET_RAW: Ko` | SYN (`-s s`) needs elevation + Npcap |
| Npcap recommended for SYN | Install from https://npcap.com/ when you need raw scans |

---

## Level 0 — Install

### Prerequisites

| OS | Package |
|----|---------|
| Debian/Ubuntu | `sudo apt install -y libpcap-dev` |
| macOS | `brew install libpcap` |
| Windows | [Npcap](https://npcap.com/) for SYN / raw; CONNECT works without it |

### Binary

```bash
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
naabu -version
```

Or download from https://github.com/projectdiscovery/naabu/releases

This workspace: `C:\projects\spiderfeet\.tools\naabu\naabu.exe`

---

## Level 1 — First scan

```bash
naabu -host scanme.nmap.org -duc
```

Default: top 100 ports; on this Windows binary, CONNECT scan (`-s c`).

Structured output:

```bash
naabu -host scanme.nmap.org -json -silent -duc
```

Example line (v2.6.1):

```json
{"host":"scanme.nmap.org","ip":"45.33.32.156","timestamp":"2026-08-10T00:00:00Z","port":80,"protocol":"tcp","tls":false}
```

---

## Level 2 — Port selection

```bash
naabu -host scanme.nmap.org -p 22,80,443,8080 -json -silent -duc
naabu -host scanme.nmap.org -top-ports 1000 -json -silent -duc
naabu -host scanme.nmap.org -top-ports full -json -silent -duc
naabu -host scanme.nmap.org -p - -json -silent -duc
```

`-top-ports` accepts `100`, `1000`, or `full` (from help). Full range via `-p -` is documented in PD Running docs — use on single high-value hosts only.

UDP ports (Running docs): express as `u:port`, e.g. `-p 80,443,u:53`. There is **no** separate `-uP` flag in this binary’s `-h`.

---

## Level 3 — Multiple targets

```bash
naabu -host a.example,b.example -p 80,443 -json -silent -duc
naabu -l hosts.txt -top-ports 100 -json -o ports.jsonl -duc
echo AS14421 | naabu -p 80,443 -json -silent -duc
subfinder -d example.com -silent | naabu -json -silent -duc
```

---

## Level 4 — Scan type, rate, CDN

```bash
naabu -host target.com -s c -json -silent -duc
naabu -host target.com -s s -json -silent -duc
naabu -host target.com -rate 300 -c 10 -json -silent -duc
naabu -host cdn.example.com -ec -cdn -json -silent -duc
```

PD defaults assume VPS-class capacity — lower `-rate` on laptops.

---

## Level 5 — Host discovery

```bash
naabu -host 10.0.0.0/24 -sn -duc
naabu -host 10.0.0.0/24 -wn -ps 80,443 -p 22,80,443 -json -silent -duc
naabu -host 10.0.0.0/24 -Pn -top-ports 100 -json -silent -duc
```

| Flag | Meaning |
|------|---------|
| `-sn` | Discovery only |
| `-wn` | Enable discovery before port scan |
| `-Pn` | Skip discovery |

---

## Level 6 — Passive (InternetDB)

```bash
naabu -host example.com -passive -json -silent -duc
```

No active packets to the target — useful for low-touch recon. Confirm actively when allowed.

---

## Level 7 — Service enrichment and Nmap

Flags in live help:

```bash
naabu -host scanme.nmap.org -sD -json -silent -duc
naabu -host scanme.nmap.org -sV -json -silent -duc
naabu -host scanme.nmap.org -nmap-cli "nmap -sV -oX detail.xml" -duc
```

Prefer separate Nmap `-oX` captures for SpiderFeet Nmap corpus work.

---

## Level 8 — Pipelines

```bash
echo example.com | naabu -silent -duc | httpx -silent
subfinder -d example.com -silent | dnsx -silent -a | naabu -top-ports 1000 -json -silent -duc
naabu -host example.com -json -silent -duc | jq -r '(.host//.ip)+":"+(.port|tostring)' | nerva --json
naabu -host corp.internal -p 11434,8000,8080,7860,4000,3000 -json -silent -o ai.jsonl -duc
```

---

## Level 9 — SpiderFeet nuggets

Map JSONL → graph (`nodes[]` / `edges[]`):

| Signal | Nugget |
|--------|--------|
| `host` | `INTERNET_NAME` |
| `ip` | `classify_ip` → IPv4 / IPv6 types |
| TCP open port | `TCP_PORT_OPEN` |
| UDP open port | `UDP_PORT_OPEN` |
| CDN label (`-cdn`) | `PROVIDER_HOSTING` when applicable |

Full mapping: `.cursor/skills/naabu/references/nugget-mapping.md`

**Always prefer `-json` for SpiderFeet** — parse line by line into harvest `records[]`.

---

## Tactics for better results

- Discover → top ports → full sweep only on winners.
- On Windows, assume CONNECT until SYN is proven with `-hc`.
- Use `-ec`/`-cdn` on edge hosts; do not full-sweep CDN IPs.
- Drop `-rate` under IDS pressure; add `-verify` when noisy.
- Gap-fill with `-passive`, then active-confirm.
- Pipeline: `subfinder → dnsx → naabu -json → httpx / nerva / julius`.

---

## Common pitfalls

- Parsing text banners instead of **`-json`**
- Inventing flags not in `naabu -h` (e.g. undocumented `-sV-fast` / `-uP`)
- Assuming SYN works on Windows without NET_RAW/Npcap
- Running `-top-ports full` / `-p -` across huge CIDRs
- Treating InternetDB passive hits as live confirmation
- Emitting IPv6 as `IP_ADDRESS` without `classify_ip`
- Using `-stream` when you still need `-resume`, `-verify`, or `-nmap-cli`

---

## Next references

- `.cursor/skills/naabu/SKILL.md`
- `.cursor/skills/naabu/references/SKILLS.md`
- `Naabu-CLI-Options.md` (includes **Captured help**)
- [Naabu usage docs](https://docs.projectdiscovery.io/opensource/naabu/usage)
- [Naabu running docs](https://docs.projectdiscovery.io/opensource/naabu/running)
