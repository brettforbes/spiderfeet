# Julius Workflows and Phases

## Phase model

```
Intake targets → Normalize URLs → Probe (HTTP) → Parse JSON/JSONL → Map nuggets → Optional Augustus
       ↑              ↑                ↑              ↑
   Nmap/Naabu    https://scheme   -o json(l)   highest specificity wins
```

## Phase 1 — Target intake

**Sources:**

| Source | How |
|--------|-----|
| Known URLs | `julius probe https://corp-ai.internal:11434` |
| File list | `julius probe -f ai_targets.txt -o jsonl > out.jsonl` |
| Port scan | Naabu/Nmap on LLM ports → `https://{ip}:{port}` lines |
| Subdomain enum | httpx on 443/8080 → Julius fingerprint |

**LLM-relevant port shortlist for upstream scans:**

`80,443,3000,3001,3080,3210,4000,5000,5001,7860,8000,8080,8443,11434,1234,1337,4891,8265,21001,2242,18789,30000`

## Phase 2 — Baseline probe

```bash
julius probe -f targets.txt -o jsonl > julius_baseline.jsonl
```

Defaults: timeout 5s, concurrency 10. Prefer `-o jsonl` for automation.

## Phase 3 — Adapt on sparse results

| Observation | Next action |
|-------------|-------------|
| Timeouts / `error` fields | `-t 15` or `-t 30` |
| Many hosts, slow wall clock | `-c 50` (watch rate limits) |
| TLS / cert issues | `--insecure` or `--ca-cert` (lab/authorized only) |
| APIs under `/api` or `/proxy` | `--base-paths /api,/proxy` |
| Need custom headers | `-H "Name: value"` (repeatable) |
| No matches on known LLM ports | `-v` single target; check WAF blocking probe paths |
| Only `openai-compatible` @ specificity 1 | Re-run with `-v`; may need custom probe |
| Internal shadow AI hunt | Expand LLM port list from Phase 1 |

## Phase 4 — Enrichment

```bash
# Model names
julius probe -o json https://host:11434 | jq '.[] | select(.models) | .models[]'

# Augustus downstream configs
julius probe --augustus -o json https://host:8000
```

## Phase 5 — Custom probe development

1. Author probe YAML (see wiki Probe YAML Reference).
2. `julius validate ./probes`
3. `julius probe -p ./probes -v -o jsonl https://target`

## Examination capture (SpiderFeet corpus)

```bash
julius probe -f targets.txt -o jsonl > examination.jsonl
julius probe -o json https://example.com          # clean miss → []
julius list                                        # probe catalog (table on this binary)
```

Always store command + structured capture. At harvest, wrap JSONL into a single-root JSON bundle; derive Text from records. Graph + narrative required (no `graph_deferred`).
