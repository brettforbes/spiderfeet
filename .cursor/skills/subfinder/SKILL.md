---
name: subfinder
description: Passive subdomain enumeration with ProjectDiscovery Subfinder, JSONL export, and SpiderFeet nugget mapping. Use when discovering subdomains from DOMAIN_NAME seeds, tuning passive sources/API keys, chaining to dnsx/httpx/naabu, or maximizing enumeration on hardened or rate-limited targets.
---

# Subfinder — Subdomain Enumeration to Nuggets

## Purpose

Use when you must **discover subdomains** for authorized domains using [ProjectDiscovery Subfinder](https://github.com/projectdiscovery/subfinder), capture **JSON Lines** (`-oJ`), and map hosts to SpiderFeet **`INTERNET_NAME`** / **`INTERNET_NAME_UNRESOLVED`** (and optional **`IP_ADDRESS`** when actively resolved), then chain to **dnsx → httpx → naabu → nuclei**.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized domains only. Subfinder queries passive OSINT APIs; respect provider ToS and rate limits.
2. **Install binary and provider config** — `subfinder` on `PATH`; configure API keys in `provider-config.yaml` (see `references/provider-config.md`).
3. **Choose enumeration mode** — Default passive (fast, no DNS validation) vs **`-active`** (resolve live hosts, enables `-oI` IPs).
4. **Run with structured output** — Prefer `-oJ` (JSONL) for corpus and nugget conversion; add `-cs` for source attribution, `-oI` with `-active` for IPs.
5. **Parse JSONL** — One object per line; fields vary by flags (see `references/json-output-schema.md`).
6. **Map nuggets** — Each `host` → `INTERNET_NAME` or `INTERNET_NAME_UNRESOLVED`; optional `ip` → `IP_ADDRESS` + `resolves_to` edge (see `references/nugget-mapping.md`).
7. **Validate and enrich** — Pipe to **dnsx** to confirm resolution, filter wildcards, and collect A/AAAA/CNAME; then **httpx** / **naabu** on live names.
8. **Adapt follow-up passes** — If yield is thin, widen sources (`-all`), add recursive sources (`-recursive`), or enable specific high-value sources (`-s crtsh,securitytrails`). If noisy, filter (`-f`) or match (`-m`) and exclude stale APIs (`-es`).

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-oJ`; never parse banner art |
| Need provenance per subdomain | Add `-cs` (JSON only) |
| Need IPs in JSON | Use `-active -oI -oJ` together |
| Passive run returns many names | Pipe to `dnsx -silent -a -aaaa` before port scan |
| Very few subdomains returned | Check provider keys; retry with `-all` or extra `-s` sources |
| API rate limits / 429 errors | Lower `-rl` or per-source `-rls`; exclude failing `-es` |
| Wildcard DNS pollutes results | Re-validate with **dnsx** wildcard filters; use `-active` to drop dead names |
| Target is `INTERNET_NAME` not apex | Extract registrable domain or pass `-d` for parent zone |
| Batch many domains | `-dL domains.txt -oD ./out/` |
| stdin pipeline | `echo domain.com \| subfinder -silent` |
| Duplicate hosts across sources | Deduplicate on normalized FQDN before nugget emit |
| Resolved host | Emit `INTERNET_NAME` |
| Unresolved after dnsx | Emit `INTERNET_NAME_UNRESOLVED` |
| Child subdomain of seed domain | Link `DOMAIN_NAME` → subdomain via affiliate/child edge per mapping doc |

## Guardrails & Pitfalls

- **Authorization** — Only enumerate domains in scope; passive APIs still disclose intent to third parties.
- **API keys** — Many sources require keys in `provider-config.yaml`; empty config → thin results (not a tool failure).
- **`-all` is slow** — Uses every source; reserve for high-value targets or second pass.
- **Passive ≠ live** — Default mode does not prove DNS answers; chain **dnsx** before treating hosts as scannable.
- **`-active` increases noise to resolvers** — Use when you need live hosts; tune `-t` and `-r` if flaky.
- **Do not** emit apex `DOMAIN_NAME` as a new discovery when it equals the seed.
- **JSONL ≠ single JSON array** — Parse line by line.
- **Provider outages** — Use `-v` to see failing sources; exclude with `-es`.
- **Proxy** — `-proxy` affects API calls only, not downstream dnsx/naabu unless configured separately.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | All flags grouped by category |
| `json-output-schema.md` | JSONL field reference |
| `provider-config.md` | API keys and sources |
| `workflows-and-phases.md` | Phase sequences and pipelines |
| `tactics.md` | Adapt when blocked, slow, or thin |
| `nugget-mapping.md` | JSONL → SpiderFeet graph |
| `sources.md` | Official URLs and articles |

Operator guides: `.docs/docs-for-cli-tools/SubFinder-Zero-to-Hero.md`, `SubFinder-CLI-Options.md`.

## Comprehensive Examples

### Basic passive enumeration

```bash
subfinder -d example.com
subfinder -d example.com -silent
subfinder -d example.com -o subs.txt
```

### JSONL for corpus / nuggets

```bash
subfinder -d example.com -oJ -o subs.jsonl
subfinder -d example.com -oJ -cs -o subs_with_sources.jsonl
subfinder -d example.com -active -oJ -oI -o subs_resolved.jsonl
subfinder -d example.com -active -oJ -cs -oI -o subs_full.jsonl
```

### Source selection

```bash
subfinder -ls
subfinder -d example.com -s crtsh,hackertarget,alienvault
subfinder -d example.com -all
subfinder -d example.com -recursive
subfinder -d example.com -es alienvault,zoomeyeapi
```

### Filter and match

```bash
subfinder -d example.com -m api,staging,dev
subfinder -d example.com -f test,uat,internal
subfinder -d example.com -m keywords.txt
```

### Rate limits and timeouts

```bash
subfinder -d example.com -rl 5
subfinder -d example.com -rls "hackertarget=10/s,shodan=15/s"
subfinder -d example.com -timeout 60 -max-time 30
```

### Batch domains

```bash
subfinder -dL domains.txt -oD ./subfinder_out/
subfinder -dL domains.txt -oJ -o all_subs.jsonl
```

### Stdin and pipes

```bash
echo example.com | subfinder -silent
cat domains.txt | subfinder -silent
subfinder -d example.com -silent | dnsx -silent -a -aaaa
subfinder -d example.com -silent | httpx -silent
subfinder -d example.com -silent | naabu -top-ports 1000 -json -silent
```

### Resolver tuning (active mode)

```bash
subfinder -d example.com -active -r 8.8.8.8,1.1.1.1 -t 20
subfinder -d example.com -active -rL resolvers.txt -oJ -oI -o live.jsonl
```

### Docker

```bash
docker run projectdiscovery/subfinder:latest -d example.com
docker run -v $HOME/.config/subfinder:/root/.config/subfinder projectdiscovery/subfinder:latest -d example.com -oJ
```

### Parse one JSONL line (Python)

```python
import json

line = '{"host":"api.example.com","source":"crtsh"}'
data = json.loads(line)
host = data["host"].lower().rstrip(".")
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Passive breadth → active validation** — `-oJ` passive pass, then `-active -oI` or **dnsx** on unique hosts.
2. **Source tiering** — Fast free sources first (`crtsh`, `hackertarget`); add API-backed sources when keys exist; `-all` only on high-value apex.
3. **Keyword second pass** — If `-m api,jenkins,grafana` returns hits, widen with full passive then filter in dnsx/httpx.
4. **Pipeline hygiene** — Always `-silent` between tools; dedupe FQDNs; log stderr with `-v` when debugging sources.
5. **Maximize on defensive targets** — Lower `-rl`, rotate `-s` sources, exclude failing `-es`, increase `-max-time`, configure more provider keys, then confirm with **dnsx** before invasive scans.
