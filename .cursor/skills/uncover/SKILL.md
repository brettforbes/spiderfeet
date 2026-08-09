---
name: uncover
description: Query provider search APIs with uncover to discover exposed internet assets, then convert normalized findings into SpiderFeet nuggets and graph edges. Trigger on uncover, shodan/censys/fofa/netlas queries, dorks, external attack-surface expansion, or provider-backed recon workflows.
---

# uncover — Provider Search to Nuggets

## Purpose

Use when you must **discover internet-facing hosts/services via search-engine APIs** (Shodan, Censys, FOFA, Netlas, Driftnet, …) with [ProjectDiscovery uncover](https://github.com/projectdiscovery/uncover), capture **`-json` JSONL**, and map `ip` / `port` / `host` into SpiderFeet address, port, and name nuggets — then chain to **httpx**, **naabu**, **nuclei**, or **nerva**.

uncover is **passive/provider-backed discovery**, not an active port scanner. Prefer it to expand external attack surface from org/product/SSL dorks or to enrich IP/CIDR open-port lists via **shodan-idb** / **driftnet**.

**Binary (this repo):** `C:\projects\spiderfeet\.tools\uncover\uncover.exe` — **v1.2.1** (captured **2026-08-10**).

## Step-by-Step Instructions

1. **Confirm scope** — Authorized org/domain/IP ranges only. Results come from third-party indexes; you still agree to each provider’s terms (tool warns on start).
2. **Configure API keys** — Most engines need credentials in `provider-config.yaml` or env vars (see README / `references/sources.md`). **`shodan-idb` needs no key** and is the default engine when input looks like **IP/CIDR**.
3. **Draft the query** — Use `-q` (string, file, or stdin). Filters are **provider-native** (Shodan dorks ≠ FOFA syntax). For multi-engine product hunts, prefer per-engine flags (`-shodan`, `-censys`, `-fofa`, …) with engine-correct query text.
4. **Select engines** — `-e shodan` (default) or comma-list / repeated `-e`. Match credentials you actually have.
5. **Run with JSONL** — Always `-json` / `-j` for corpus and nuggets. Add `-silent` for pipe-friendly stdout (results only). Cap with `-l` (default **100**).
6. **Parse JSONL** — One object per line: `timestamp`, `source`, `ip`, `port`, `host`, `url` (see `references/output-and-parsing.md`).
7. **Map nuggets** — IP via `classify_ip`; optional `INTERNET_NAME` from `host`; `TCP_PORT_OPEN` from `ip:port`; keep `source` as provenance (`references/nugget-mapping.md`).
8. **Validate & chain** — Treat hits as leads. Pipe `-f ip` / `-f https://ip:port` into **naabu** / **httpx** / **nuclei** for live confirmation.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-json` (`-j`); never parse banner art alone |
| Input is IP or CIDR | Engine defaults to **`shodan-idb`** (no API key); or set `-e driftnet` for Driftnet port lookup |
| Input is a search dork / product name | Default engine is **`shodan`** unless `-e` overrides |
| API key missing / auth error | Fail fast; configure `-pc` / env; pivot to `shodan-idb` only for IP/CIDR |
| Same logical query across engines | Use per-engine flags with **native** syntax per provider |
| Need awesome curated dorks | `-asq jira` (awesome-search-queries) |
| Too much noise | Narrow with org/ssl/domain/port filters; lower `-l` |
| Provider rate-limits | Set `-rl` / `-rlm`, raise `-retry`, rotate keys in provider config, or switch `-e` |
| Need only IPs for naabu | `-f ip -silent` (text pipe) **or** parse JSONL `ip` |
| Need URL-shaped stdin for httpx | `-f https://ip:port` or similar field template |
| Want raw vendor JSON | `-raw` (exploration); formal exam still prefers normalized `-json` |
| Verbose + silent together | **Invalid** — binary exits: `both verbose and silent mode specified` |

## Guardrails & Pitfalls

- **Authorization** — Only query in-scope orgs/assets; provider indexes are global.
- **Do not invent flags** — Use only options from live `uncover -h` (see CLI docs Captured help). No `-csv` on this **v1.2.1** binary.
- **JSONL ≠ JSON array** — Parse line by line; harvest bundles use `records[]`.
- **Credentials** — Keep keys out of git, logs, and command history; use env or `-pc`.
- **Leads ≠ truth** — Index lag, CDN anycast, and shared hosting create false associations; validate live.
- **Provider syntax** — Blindly reusing a Shodan dork on FOFA/Censys yields empty or wrong results.
- **Default limit 100** — Raise `-l` deliberately; large pulls burn quota.
- **IP nuggets** — Use `core.ip_classify.classify_ip`; never hardcode `IP_ADDRESS` for IPv6 literals.
- **Do not** treat uncover as a substitute for **naabu** / **nmap** active port confirmation.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | All flags by category |
| `output-and-parsing.md` | JSONL fields + parse notes |
| `nugget-mapping.md` | JSONL → SpiderFeet graph |
| `tactics.md` | Query narrowing, multi-engine, pipelines |
| `sources.md` | Official URLs + provider setup |

Operator guides: `.docs/docs-for-cli-tools/uncover-Zero-to-Hero.md`, `uncover-CLI-Options.md`.

Help captures: `.tmp_uncover_help/` (`help_h.txt`, `help_long.txt`, `version.txt`) — **2026-08-10**.

## Comprehensive Examples

### INPUT (`-q` / stdin / file)

```bash
uncover -q 'ssl:"Example Org"' -e shodan -json -silent
echo 'ssl:"Example Org"' | uncover -json -silent
uncover -q dorks.txt -e shodan -json -silent -o uncover.jsonl
```

### ENGINE selection

```bash
uncover -q jira -e shodan,censys,fofa -json -silent
uncover -q '1.1.1.1' -e shodan-idb -json -silent
echo '8.8.8.8/24' | uncover -e driftnet -json -silent
```

### Per-engine queries (native syntax)

```bash
uncover -shodan 'http.component:"Atlassian Jira"' -censys 'services.software.product=`Jira`' -fofa 'app="ATLASSIAN-JIRA"' -json -silent
```

### Awesome search queries

```bash
uncover -asq jira -json -silent
```

### OUTPUT (JSONL preferred)

```bash
uncover -q 'product:"nginx" port:443' -e shodan -json -o uncover.jsonl -silent
uncover -q jira -f host -silent
uncover -q jira -f https://ip:port/version -silent
uncover -q 'org:"Example Inc."' -json -l 50 -silent
```

### CONFIG / rate limits

```bash
uncover -q jira -e shodan -json -silent -pc "%APPDATA%\uncover\provider-config.yaml"
uncover -q jira -e shodan -json -silent -timeout 60 -retry 3 -rl 1
```

### PIPELINES

```bash
uncover -q 'title:"GitLab"' -e shodan -silent | httpx -silent -json
uncover -q 'org:"Example Inc."' -f ip -silent | naabu -json -silent
uncover -q 'org:"Example Inc."' -silent | httpx -silent | nuclei -silent -jsonl
echo '51.83.59.99/24' | uncover -e shodan-idb -silent | httpx -silent
```

### Parse one JSONL line (Python)

```python
import json

line = '{"timestamp":1786295459,"source":"shodan-idb","ip":"1.1.1.1","port":443,"host":"example.com","url":""}'
row = json.loads(line)
# row["ip"], row["port"], row["host"], row["source"]
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Keyless IP enrich first** — `shodan-idb` on in-scope CIDRs before burning paid API quota.
2. **One engine, tight dork** — prove yield, then multi-engine correlate.
3. **Native syntax per provider** — never assume Shodan filters work elsewhere.
4. **JSON always for SpiderFeet** — `-json -silent -o phase.jsonl`.
5. **Validate before severity** — httpx/naabu/nuclei on high-value `ip:port` only.
