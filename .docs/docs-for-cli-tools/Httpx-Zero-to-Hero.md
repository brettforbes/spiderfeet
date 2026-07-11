# httpx Zero to Hero — HTTP Probing, JSONL, and Nuggets

From install to orchestrated recon with **`httpx -json`**, nugget mapping, and pipelines to **nuclei** and **webanalyze**.

Skill reference: `.cursor/skills/httpx/SKILL.md`

**Important:** This guide covers **ProjectDiscovery httpx** — not the Python `httpx` HTTP client or Kali `httpx-toolkit`.

## What httpx does

httpx is ProjectDiscovery's **fast HTTP probe**: it takes hostnames, URLs, IPs, CIDRs, or ASNs and discovers **live web services**, optionally fingerprinting status, title, technologies, CDN, and more.

httpx does **not**:

- Enumerate subdomains passively (use **subfinder**)
- Port-scan entire ranges (use **naabu** / **nmap**)
- Run vulnerability templates (use **nuclei**)

---

## Level 0 — Install

```bash
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
httpx -version
```

Or: https://github.com/projectdiscovery/httpx/releases

Optional config: `~/.config/httpx/config.yaml`

---

## Level 1 — First probe

```bash
httpx -u https://scanme.sh
```

Silent URL only:

```bash
echo scanme.sh | httpx -silent
```

---

## Level 2 — Fingerprint pass

```bash
httpx -u https://scanme.sh -status-code -title -tech-detect -web-server -cdn
```

Example output:

```
https://scanme.sh [80] [Scan me!] [Apache httpd]
```

---

## Level 3 — JSONL for automation

```bash
httpx -l hosts.txt -json -o results.jsonl
```

Example line:

```json
{"url":"https://scanme.sh","status_code":200,"title":"Scan me!","webserver":"Apache","tech":["Apache httpd"]}
```

Rich JSONL:

```bash
httpx -l hosts.txt -json -include-chain -irh -o full.jsonl
```

---

## Level 4 — Matchers and filters

```bash
httpx -l hosts.txt -match-code 200,301,302 -json -silent
httpx -l hosts.txt -filter-code 404 -json -silent
httpx -l hosts.txt -filter-duplicates -json
```

---

## Level 5 — Ports and paths

```bash
httpx -l hosts.txt -p http:8080,https:8443 -json
httpx -l urls.txt -path /api,/admin -status-code -json
```

---

## Level 6 — Pipelines

### After subfinder

```bash
subfinder -d example.com -silent | httpx -title -tech-detect -status-code -json -silent
```

### After dnsx

```bash
subfinder -d example.com -silent | dnsx -silent -a | httpx -json -silent
```

### After naabu

```bash
naabu -host scanme.sh -json -silent | httpx -json -silent
```

### Into nuclei

```bash
httpx -l hosts.txt -json -silent | nuclei -silent -jsonl
```

---

## Level 7 — Nugget mapping

| httpx signal | SpiderFeet nugget |
|--------------|-------------------|
| `url` | `LINKED_URL_INTERNAL` |
| host | `INTERNET_NAME` |
| `ip` | `IP_ADDRESS` |
| `status_code` | `HTTP_CODE` |
| `webserver` | `WEBSERVER_BANNER` |
| `tech[]` | `WEBSERVER_TECHNOLOGY` |
| headers (`-irh`) | `WEBSERVER_HTTPHEADERS` |

Full rules: `.cursor/skills/httpx/references/nugget-mapping.md`

### Corpus bundle shape

At harvest, convert JSONL → single JSON:

```json
{
  "schema": "httpx_probe_v1",
  "tool": "httpx",
  "record_count": 42,
  "records": [ ... ]
}
```

---

## Level 8 — Adapt when results are weak

1. Try `-no-fallback` for HTTP-only services
2. Add `-p` for non-standard web ports
3. Use `-probe-all-ips`
4. Run **dnsx** first to drop dead names
5. Lower `-rate-limit` if blocked

Tactics: `.cursor/skills/httpx/references/tactics.md`

---

## Level 9 — Ontology context

httpx extends the **web / APPLICATIONS** layer on qualified `HOST` in the unified CLI ontology — see `.docs/docs-for-cli-tools/_Current_Ontology.md`.

Typical investigation:

**Netdiscover** (L2 `SYSTEM`) → **Nmap/Naabu** (ports) → **httpx** (live web) → **nuclei** (vulns)

---

## Quick reference

| Goal | Command |
|------|---------|
| Live URLs | `cat hosts.txt \| httpx -silent` |
| JSONL corpus | `httpx -l hosts.txt -json -o out.jsonl` |
| Tech stack | `httpx -l hosts.txt -td -title -sc -json` |
| Nuclei feed | `httpx -l hosts.txt -mc 200,301,302 -json -silent \| nuclei` |

CLI details: `Httpx-CLI-Options.md`
