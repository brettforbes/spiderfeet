# Subfinder Zero to Hero — Subdomain Enumeration, JSONL, and Nuggets

From install to orchestrated recon with **`subfinder -oJ`**, nugget mapping, and pipelines to **dnsx → httpx → naabu → nuclei**.

Skill reference: `.cursor/skills/subfinder/SKILL.md`

## What Subfinder does

Subfinder is ProjectDiscovery's **fast passive subdomain discovery** tool. It queries curated OSINT sources (certificate transparency, APIs, archives) and optionally **validates** names with DNS (`-active`).

Subfinder does **not**:

- Brute-force DNS wordlists (pair with **dnsx** / other tools)
- Port scan (use **naabu**)
- Probe HTTP (use **httpx**)
- Run vulnerability templates (use **nuclei**)

---

## Level 0 — Install

### Binary

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
subfinder -version
```

Or download from https://github.com/projectdiscovery/subfinder/releases

### Provider config (important)

Create API keys file (see skill `references/provider-config.md`):

- Linux/macOS: `~/.config/subfinder/provider-config.yaml`
- Windows: `%APPDATA%\subfinder\provider-config.yaml`

Without keys, free sources still work but results on large orgs may be thin.

---

## Level 1 — First enumeration

```bash
subfinder -d example.com
```

Pipe-friendly:

```bash
subfinder -d example.com -silent
```

Save to file:

```bash
subfinder -d example.com -o subs.txt
```

---

## Level 2 — JSONL for automation

```bash
subfinder -d example.com -oJ -o subs.jsonl
```

Example line:

```json
{"host":"api.example.com"}
```

With source attribution:

```bash
subfinder -d example.com -oJ -cs -o subs.jsonl
```

```json
{"host":"api.example.com","source":"crtsh"}
```

---

## Level 3 — Active validation and IPs

```bash
subfinder -d example.com -active -oJ -oI -o live.jsonl
```

```json
{"host":"api.example.com","ip":"203.0.113.20"}
```

**Passive names are not guaranteed live** — always validate with `-active` or **dnsx** before invasive scans.

---

## Level 4 — Source control

```bash
subfinder -ls
subfinder -d example.com -s crtsh,hackertarget
subfinder -d example.com -all
subfinder -d example.com -es alienvault
```

---

## Level 5 — Filters and rate limits

```bash
subfinder -d example.com -m api,staging,dev
subfinder -d example.com -f test,uat
subfinder -d example.com -rl 10
subfinder -d example.com -max-time 30
```

---

## Level 6 — Batch domains

```bash
subfinder -dL domains.txt -oD ./output/
subfinder -dL domains.txt -oJ -o all.jsonl
```

---

## Level 7 — Pipelines

### Validate then probe web

```bash
subfinder -d example.com -silent | dnsx -silent -a -aaaa | tee live.txt
cat live.txt | httpx -silent -title -status-code
```

### Full recon stack

```bash
subfinder -d example.com -silent \
  | dnsx -silent -a -aaaa \
  | naabu -top-ports 1000 -json -silent \
  | httpx -silent
```

### Docker

```bash
docker run projectdiscovery/subfinder:latest -d example.com -silent
```

---

## Level 8 — Nugget mapping

Convert JSONL to SpiderFeet graph payloads:

| Signal | Nugget |
|--------|--------|
| Discovered FQDN (unvalidated) | `INTERNET_NAME_UNRESOLVED` |
| Resolved FQDN | `INTERNET_NAME` |
| Child of seed domain | `AFFILIATE_INTERNET_NAME` (optional policy) |
| IP from `-oI` | `IP_ADDRESS` + `resolves_to` edge |

Full rules: `.cursor/skills/subfinder/references/nugget-mapping.md`

### Example conversion flow

1. Run `subfinder -d SEED -oJ -cs -o passive.jsonl`
2. Run `dnsx -l hosts.txt -j` on extracted hosts
3. Emit `nodes[]` / `edges[]` with provenance (`source_tool: subfinder`)
4. Feed live hosts to naabu/nuclei corpus scenarios

---

## Level 9 — Adapt when results are weak

1. Configure more API keys in `provider-config.yaml`
2. `subfinder -d DOMAIN -v` — inspect failing sources
3. Retry with `-all` on apex only
4. Add `-recursive` sources
5. Keyword pass: `-m api,admin,vpn`
6. Compare with SpiderFeet `sfp_sublist3r` or other passive modules

Tactics: `.cursor/skills/subfinder/references/tactics.md`

---

## SpiderFeet integration

| Seed type | Typical command |
|-----------|-----------------|
| `DOMAIN_NAME` | `subfinder -d SEED -oJ -cs -o out.jsonl` |
| `INTERNET_NAME` (apex) | derive registrable domain for `-d` |

Module reference pattern: `modules/sfp_sublist3r.py` (API passive enumeration).

---

## Quick reference

| Goal | Command |
|------|---------|
| Quiet list | `subfinder -d example.com -silent` |
| JSONL corpus | `subfinder -d example.com -oJ -cs -o out.jsonl` |
| Live + IP JSON | `subfinder -d example.com -active -oJ -oI -o live.jsonl` |
| Pipe to httpx | `subfinder -d example.com -silent \| httpx -silent` |

CLI details: `SubFinder-CLI-Options.md`
