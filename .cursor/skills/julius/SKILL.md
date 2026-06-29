---
name: julius
description: Fingerprint LLM and AI inference services with Julius using JSON/JSONL output mapped to SpiderFeet nuggets. Use for shadow AI discovery, Ollama/vLLM/LiteLLM detection, port-scan→URL chaining, probe adaptation, and Augustus handoff on authorized targets.
---

# Julius — LLM Service Fingerprinting

## Purpose

Use when you must **discover and fingerprint HTTP(S) LLM inference, gateway, and RAG endpoints** (Ollama, vLLM, LiteLLM, Open WebUI, etc.), capture **`julius probe -o jsonl`**, and convert matches to SpiderFeet nuggets — especially after **Naabu/Nmap** finds AI-related ports.

## Step-by-Step Instructions

1. **Confirm scope** — Authorized targets only (URLs, IPs, internal ranges). Julius sends HTTP probes; no auth bypass.
2. **Build target list** — URLs, `-f file`, or stdin from port scanners (see tactics).
3. **Run baseline probe** — `julius probe -o jsonl -f targets.txt -o results.jsonl`.
4. **Parse JSONL** — One object per line; see `references/json-output-schema.md`.
5. **Map to nuggets** — `SOFTWARE_USED`, `TCP_PORT_OPEN`, `LINKED_URL_INTERNAL`, models per `references/nugget-mapping.md`.
6. **Adapt** — On timeouts/sparse hits: raise `-t`, tune `-c`, use `-v`, expand LLM port intake.
7. **Optional Augustus** — `julius probe --augustus -o json` only with explicit approval.
8. **Custom probes** — `julius validate` then `julius probe -p ./probes` for org-specific signatures.

## If/Then Decision Rules

| If | Then |
|----|------|
| Only IPs:ports from Naabu | Emit `https://{ip}:{port}` lines → `julius probe - -o jsonl` |
| Default table output | Re-run with `-o jsonl` for automation |
| Timeouts in `error` field | Increase `-t 15` or `-t 30` |
| Large target batch | `-c 50` with scope approval; watch WAF blocks |
| Only `openai-compatible` @ specificity 1 | Treat as low confidence; use `-v` or custom probe |
| Need probe catalog | `julius list -o json` |
| Custom YAML probes | `julius validate ./probes` before scan |
| Need model names | Parse `models[]` from JSON; probe must support extraction |
| Negative / clean miss test | Probe known non-AI host; expect no service matches |
| Downstream safety scan | `--augustus` + Augustus skill |

## Guardrails & Pitfalls

- **Authorization** — shadow AI hunts still require written scope on IPs/domains.
- **JSONL not table** — never parse ASCII tables for SpiderFeet graphs.
- **Unauthenticated only** — Julius does not supply API keys; auth-walled services may false-negative.
- **HTTPS default** — bare `host:port` becomes `https://`; HTTP-only services may need explicit `http://` if supported.
- **Do not** treat specificity-1 generic OpenAI match as confirmed product name.
- **Rate / concurrency** — high `-c` can trigger WAF; reduce on corporate nets.
- **Augustus configs** — sensitive; store encrypted; run scans only when approved.
- Dedupe by `{host}:{port}:{service}`; prefer highest `specificity`.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Commands and flags |
| `json-output-schema.md` | JSON/JSONL fields |
| `probes-and-services.md` | 32 services, ports |
| `workflows-and-phases.md` | Phase sequences |
| `tactics.md` | Naabu/Nmap chains, shadow AI |
| `nugget-mapping.md` | JSON → nuggets |
| `match-rules-and-probes.md` | Custom probes |
| `sources.md` | URLs |

Operator guides: `.docs/docs-for-cli-tools/Julius-Zero-to-Hero.md`, `Julius-CLI-Options.md`.

## Comprehensive Examples

### Target input

```bash
julius probe https://target.example.com
julius probe https://a.internal:11434 https://b.internal:8000
julius probe -f targets.txt -o jsonl
cat urls.txt | julius probe -
echo "https://10.0.0.5:11434" | julius probe -
```

### `--output` / `-o`

```bash
julius probe -o table https://target.example.com
julius probe -o json https://target.example.com
julius probe -o jsonl -f targets.txt -o out.jsonl
```

### `--file` / `-f`

```bash
julius probe -f corp_ai_urls.txt -o jsonl
```

### `--timeout` / `-t`

```bash
julius probe -t 15 -f slow_targets.txt -o jsonl
julius probe -t 30 -c 5 https://latent.internal:8000 -o json
```

### `--concurrency` / `-c`

```bash
julius probe -c 50 -f many.txt -o jsonl
julius probe -c 3 -t 20 -f fragile.txt -o jsonl
```

### `--verbose` / `-v`

```bash
julius probe -v https://target.example.com:11434
```

### `--quiet` / `-q`

```bash
julius probe -q -f targets.txt -o jsonl
```

### `--probes-dir` / `-p`

```bash
julius probe -p ./custom-probes -o jsonl https://target:9000
```

### `--augustus`

```bash
julius probe --augustus -o json https://llm.internal:8000
```

### `julius list`

```bash
julius list
julius list -o json > probes.json
```

### `julius validate`

```bash
julius validate ./probes
```

### Naabu pipe

```bash
naabu -host 10.0.0.0/24 -p 11434,8000,8080 -json -silent | \
  jq -r '"https://" + .ip + ":" + (.port|tostring)' | julius probe - -o jsonl
```

### JSON parse

```bash
julius probe -o json https://host:11434 | jq '.[] | {service, specificity, models}'
```

## Strategies and Tactics

### Maximize LLM discovery on unknown network

1. **Naabu** LLM port shortlist → JSONL URLs.
2. **Julius** `-o jsonl` baseline pass.
3. **Retry** timeouts with `-t 30 -c 5`.
4. **Verbose** on high-value hosts with no matches.
5. **Extract models** from rows with `models[]` for inventory depth.
6. **Emit nuggets** at specificity ≥ 50; flag generic OpenAI-compatible separately.

### Shadow AI assessment

1. Combine subdomain enum + internal IP ranges.
2. Scan ports `11434,8000,8080,7860,4000,3000,443`.
3. JSONL → sort by specificity → report self-hosted vs gateway vs RAG.
4. Optional `--augustus` for authorized LLM security testing.

### Corpus / formal examination

| Scenario | Command pattern |
|----------|-----------------|
| Positive (Ollama-like) | Permissive lab host on 11434 |
| Rich models | `-o json` + jq models |
| Multi-target | `-f targets.txt -o jsonl` |
| Clean miss | `https://example.com` |
| Probe catalog | `julius list -o json` |
| Custom probe | `validate` + `-p` |

### Pipeline position

**dnsx → httpx → naabu → julius → (augustus)** for web+AI surface.

When Naabu finds no AI ports, do not run Julius on entire /16 — narrow to hosts with web management exposure first.
