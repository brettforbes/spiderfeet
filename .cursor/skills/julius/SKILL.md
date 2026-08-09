---
name: julius
description: Fingerprint LLM and AI inference services with Julius using JSON/JSONL output mapped to SpiderFeet nuggets. Use for shadow AI discovery, Ollama/vLLM/LiteLLM detection, port-scan→URL chaining, probe adaptation, and Augustus handoff on authorized targets.
---

# Julius — LLM Service Fingerprinting

## Purpose

Use when you must **discover and fingerprint HTTP(S) LLM inference, gateway, MCP, RAG, and cloud AI endpoints**, capture **`julius probe -o json`** or **`-o jsonl`**, and convert matches to SpiderFeet nuggets — especially after **Naabu/Nmap** finds AI-related ports.

**Binary (this host):** `C:\projects\spiderfeet\.tools\julius\julius.exe`  
Release artifact beside the binary: `julius_1.4.10_windows_amd64.zip`.  
**There is no `version` / `--version` command** on this binary (`unknown command "version"` / `unknown flag: --version`). Identify capability via `julius --help` and `julius list`. Help capture: **2026-08-10** (`.tmp_julius_help/`).

## Step-by-Step Instructions

1. **Confirm scope** — Authorized URLs/IPs only. Julius sends unauthenticated HTTP probes; it does not bypass auth.
2. **Validate tooling** — `julius --help` and `julius probe --help` (exact text in `references/cli-options.md` and `.docs/docs-for-cli-tools/Julius-CLI-Options.md`).
3. **Build target URLs** — Args, `-f file`, or stdin (`julius probe -`). Prefer full URLs; bare `host:port` is normalized to `https://` (see wiki/README).
4. **Run structured probe (SpiderFeet / corpus)** — prefer JSONL for streams, JSON for small batches:

```bash
julius probe -o jsonl -f targets.txt > julius_out.jsonl
julius probe -o json https://lab.internal:11434
```

`-o` is **output format only** (`table` | `json` | `jsonl`). Redirect to a file with the shell; do **not** pass a second `-o path`.

5. **Parse results** — JSON array (`-o json`) or one object per line (`-o jsonl`). Fields in `references/json-output-schema.md`.
6. **Map nuggets** — service / models / host / port per `references/nugget-mapping.md` (use `classify_ip` for address nodes).
7. **Adapt on sparse yield** — raise `-t`, lower/raise `-c`, add `-v`, try `--insecure` / `--ca-cert` for lab TLS, `--base-paths` for path-prefixed APIs, `-H` for custom headers when authorized.
8. **Optional Augustus** — `julius probe --augustus -o json` only with explicit approval (see Augustus skill).
9. **Custom probes** — `julius validate ./probes` then `julius probe -p ./probes -o jsonl …`.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-o json` or `-o jsonl`; never parse table alone |
| Only IPs:ports from Naabu | Emit `https://{ip}:{port}` lines → `julius probe - -o jsonl` |
| Timeouts / `error` fields | Increase `-t 15` or `-t 30`; optionally lower `-c` |
| Large target batch | Raise `-c` only with scope approval; reduce on WAF/corp nets |
| TLS verify failures on lab/MITM | `--insecure` or `--ca-cert <pem>` (authorized lab only) |
| API behind prefix (`/api`, `/proxy`) | `--base-paths /api,/proxy` |
| Need auth / custom Host header | `-H "Name: value"` (repeatable); still unauthenticated fingerprinting |
| Only `openai-compatible` @ specificity 1 | Low confidence; `-v` or custom probe before hard claims |
| Need probe catalog | `julius list` (human table; see list JSON note in cli-options) |
| Custom YAML probes | `julius validate ./probes` before `-p` |
| Need model names | Parse `models[]` from JSON when present |
| Clean-miss / negative fixture | Probe known non-AI host (e.g. `https://example.com`) → `[]` / no match lines |
| Downstream LLM safety scan | `--augustus` + Augustus skill on approved targets only |

## Guardrails & Pitfalls

- **Authorization** — shadow AI hunts still require written scope.
- **Do not invent flags** — only options from Captured help (2026-08-10). No `version` subcommand.
- **`-o` is format, not a filename** — never `julius probe -o jsonl -o out.jsonl`; use `> out.jsonl`.
- **Structured-first** — graph/narrative from JSON/JSONL only.
- **Unauthenticated only** — auth-walled services may false-negative.
- **HTTPS default** — bare `host:port` becomes `https://`; use explicit `http://` when the service is HTTP-only.
- **Do not** treat specificity-1 generic OpenAI match as a confirmed product.
- **Concurrency** — high `-c` can trip WAF; dial down on corporate nets.
- **Augustus configs** — sensitive; store carefully; run only when approved.
- **Dedupe** by `{host}:{port}:{service}`; prefer highest `specificity`.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Captured help, all commands/flags |
| `json-output-schema.md` | JSON / JSONL fields |
| `probes-and-services.md` | 63 probes from live `list` |
| `workflows-and-phases.md` | Intake → probe → adapt |
| `tactics.md` | Naabu/Nmap chains, shadow AI |
| `nugget-mapping.md` | JSON → SpiderFeet graph |
| `match-rules-and-probes.md` | Custom probe YAML |
| `sources.md` | Official URLs |

Operator guides: `.docs/docs-for-cli-tools/Julius-Zero-to-Hero.md`, `Julius-CLI-Options.md`.

## Comprehensive Examples

Prefer `C:\projects\spiderfeet\.tools\julius\julius.exe` or put it on `PATH` as `julius`.

### Target input

```bash
julius probe https://target.example.com
julius probe https://a.internal:11434 https://b.internal:8000
julius probe -f targets.txt -o jsonl > out.jsonl
cat urls.txt | julius probe - -o jsonl
echo "https://10.0.0.5:11434" | julius probe - -o json
```

### `--output` / `-o` (format only)

```bash
julius probe -o table https://target.example.com
julius probe -o json https://target.example.com
julius probe -o jsonl -f targets.txt > results.jsonl
```

### `--file` / `-f`

```bash
julius probe -f corp_ai_urls.txt -o jsonl > julius.jsonl
```

### `--timeout` / `-t` and `--concurrency` / `-c`

```bash
julius probe -t 15 -f slow_targets.txt -o jsonl
julius probe -t 30 -c 5 https://latent.internal:8000 -o json
julius probe -c 50 -f many.txt -o jsonl > many.jsonl
```

### TLS / size / UI globals

```bash
julius probe --insecure -o json https://lab.internal:11434
julius probe --ca-cert ./corp-root.pem -o jsonl -f internal.txt
julius probe --max-response-size 20971520 -o json https://host:8000
julius probe --no-color --banner=false -o jsonl https://host:11434
```

### Probe-only: headers, base paths, Augustus

```bash
julius probe -H "Authorization: Bearer token" -o json https://gateway.internal
julius probe --base-paths /api,/proxy -o jsonl https://edge.internal:8080
julius probe --augustus -o json https://llm.internal:8000
```

### Verbose / quiet

```bash
julius probe -v https://target.example.com:11434
julius probe -q -f targets.txt -o jsonl
```

### Custom probes

```bash
julius validate ./probes
julius probe -p ./custom-probes -o jsonl https://target:9000
```

### Catalog / completion

```bash
julius list
julius list -p ./custom-probes
julius completion powershell
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

1. **Naabu** LLM port shortlist → HTTPS URLs.
2. **Julius** `-o jsonl` baseline.
3. **Retry** timeouts with `-t 30 -c 5`.
4. **Verbose** on high-value hosts with no matches; try `--base-paths` if APIs sit under a prefix.
5. **Extract models** from rows with `models[]`.
6. **Emit nuggets** at specificity ≥ 50; flag generic OpenAI-compatible separately.

### Shadow AI assessment

1. Combine subdomain enum + internal ranges.
2. Scan ports such as `11434,8000,8080,7860,4000,3000,443` (expand from probe port hints).
3. JSONL → sort by specificity → report self-hosted vs gateway vs RAG vs cloud vs MCP.
4. Optional `--augustus` for authorized LLM security testing.

### Corpus / formal examination

| Scenario | Command pattern |
|----------|-----------------|
| Positive (Ollama-like) | Permissive lab host on 11434, `-o jsonl` |
| Rich models | `-o json` + jq `models` |
| Multi-target | `-f targets.txt -o jsonl` |
| Clean miss | `julius probe -o json https://example.com` |
| Probe catalog | `julius list` |
| Custom probe | `validate` + `-p` |
| TLS lab | `--insecure` or `--ca-cert` |

### Pipeline position

**dnsx → httpx → naabu → julius → (augustus)** for web+AI surface.

When Naabu finds no AI ports, do not run Julius on an entire `/16` — narrow to hosts with web/management exposure first.
