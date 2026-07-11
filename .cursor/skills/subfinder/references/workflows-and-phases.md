# Subfinder Workflows and Phases

## Phase model

| Phase | Goal | Typical command |
|-------|------|-----------------|
| A — Passive breadth | Collect candidate FQDNs | `subfinder -d DOMAIN -oJ -cs -o passive.jsonl` |
| B — Active validation | Keep resolvable hosts | `subfinder -d DOMAIN -active -oJ -oI -o live.jsonl` or pipe to **dnsx** |
| C — Filter / focus | Reduce noise | `-m` / `-f` or dnsx wildcard filter |
| D — Service discovery | HTTP/TCP on live hosts | `httpx`, `naabu` |
| E — Vulnerability depth | Template scans | `nuclei` on confirmed URLs |

## Workflow 1 — Standard recon chain

```bash
subfinder -d example.com -silent | dnsx -silent -a -aaaa -resp | tee live.txt
cat live.txt | httpx -silent -status-code -title -o web.txt
cat live.txt | naabu -top-ports 1000 -json -silent -o ports.jsonl
```

## Workflow 2 — Corpus capture (SpiderFeet CLI exercising)

```bash
subfinder -d example.com -oJ -cs -o .docs/.../subfinder_passive.jsonl
subfinder -d example.com -active -oJ -oI -cs -o .docs/.../subfinder_active.jsonl
```

Convert JSONL → `nodes[]` / `edges[]` per `nugget-mapping.md`.

## Workflow 3 — Batch apex domains

```bash
subfinder -dL apex_domains.txt -oD ./subfinder_batch/
# or single combined JSONL:
subfinder -dL apex_domains.txt -oJ -o all_subs.jsonl
```

## Workflow 4 — Keyword-focused hunt

```bash
subfinder -d example.com -m api,admin,jenkins,grafana,gitlab -oJ -o high_value.jsonl
subfinder -d example.com -m keywords.txt -silent | httpx -silent
```

## Workflow 5 — Second pass after thin results

```bash
subfinder -d example.com -all -oJ -cs -o passive_full.jsonl
subfinder -d example.com -s securitytrails,shodan,crtsh -oJ -o api_backed.jsonl
```

## Workflow 6 — stdin driven

```bash
echo example.com | subfinder -silent
while read d; do subfinder -d "$d" -silent; done < domains.txt
```

## Integration with SpiderFeet modules

| Module pattern | Role |
|----------------|------|
| `sfp_sublist3r` | API-based passive subs → `INTERNET_NAME` |
| Future `sfp_tool_subfinder` | CLI wrapper; same nugget types |
| `sfp_dnsresolve` | Post-process unresolved names |

Seed event: **`DOMAIN_NAME`** or parent **`INTERNET_NAME`**.

## Phase decision

| Observation | Next phase |
|-------------|------------|
| &lt; 5 subs on large org | Configure API keys; `-all`; verify domain scope |
| Hundreds of passive, few resolve | dnsx filter; drop wildcard sinkholes |
| Many `api.*` / `dev.*` | `-m` focused httpx + nuclei |
| Rate limit errors | `-rl`, `-es` failing source, retry later |
