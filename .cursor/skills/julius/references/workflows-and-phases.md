# Julius Workflows and Phases

## Phase model

```
Intake targets → Normalize URLs → Probe (HTTP) → Parse JSONL → Map nuggets → Optional Augustus
       ↑              ↑                ↑              ↑
   Nmap/Naabu    https:// scheme   -o jsonl      highest specificity wins
```

## Phase 1 — Target intake

**Sources:**

| Source | How |
|--------|-----|
| Known URLs | `julius probe https://corp-ai.internal:11434` |
| File list | `julius probe -f ai_targets.txt -o jsonl` |
| Port scan | Naabu/Nmap on LLM ports → `https://{ip}:{port}` lines |
| Subdomain enum | httpx on 443/8080 → filter AI paths later with Julius |

**LLM-relevant port shortlist for upstream scans:**

`80,443,3000,3001,3080,3210,4000,5000,5001,7860,8000,8080,8443,11434,1234,1337,4891,21001,2242`

## Phase 2 — Baseline probe

```bash
julius probe -o jsonl -f targets.txt -o julius_baseline.jsonl
```

Defaults: timeout 5s, concurrency 10. Use for first pass on a permissive target set.

## Phase 3 — Adapt on sparse results

| Observation | Next action |
|-------------|-------------|
| Timeouts / `error` fields | `-t 15` or `-t 30` |
| Many hosts, slow wall clock | `-c 50` (watch rate limits) |
| TLS / cert issues on internal IPs | Try explicit `https://ip:port`; verify cert policy |
| No matches on known LLM ports | `-v` single target; check WAF blocking probe paths |
| Only `openai-compatible` @ specificity 1 | Re-run with `-v`; may need custom probe |
| Internal shadow AI hunt | Scan full LLM port list from Phase 1 intake |

## Phase 4 — Enrichment

```bash
# Model names
julius probe -o json https://host:11434 | jq '.[] | select(.models) | .models[]'

# Augustus downstream configs
julius probe --augustus -o json https://host:8000
```

## Phase 5 — Custom probe development

1. Copy probe YAML from upstream `probes/` directory.
2. `julius validate ./probes`
3. `julius probe -p ./probes -v -o jsonl https://target`

## Examination capture (SpiderFeet corpus)

Per `cli_app_profiling` skill:

```bash
julius probe -o jsonl -f targets.txt > examination.jsonl
julius probe -o json https://scanme.nmap.org   # clean miss / negative scenario
julius list -o json > probes_catalog.json
```

Always store `{scenario}_command.txt` and structured JSONL in `app_examination_docs/julius/`.
