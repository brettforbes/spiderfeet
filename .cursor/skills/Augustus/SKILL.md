---
name: Augustus
description: Run LLM vulnerability scans with Augustus for prompt injection, jailbreak, extraction, and adversarial safety testing. Trigger when evaluating model safety posture, scanning prompts at scale, validating guardrails, or generating JSON/JSONL evidence for security reports.
---

# Augustus — LLM Vulnerability Scanner

## Purpose

Use when you must **adversarially test an authorized LLM or chat API** with [Praetorian Augustus](https://github.com/praetorian-inc/augustus) — probes, detectors, buffs, optional recon, and structured evidence (`--format json` and/or `-o` JSONL) mapped into SpiderFeet nugget graphs. Prefer structured artifacts over table TTY for corpus / automation.

| Platform | Path |
|----------|------|
| WSL | `/mnt/c/projects/spiderfeet/.tools/augustus/augustus` |
| Windows path | `C:\projects\spiderfeet\.tools\augustus\augustus` |

**Version:** **0.14.15** (`augustus --version` / `augustus version`). Help capture: **2026-08-10** (`.tmp_augustus_help/`).

Live `augustus list` on this binary (2026-08-10): Probes **239**, Recon **3**, Generators **48**, Detectors **129**, Harnesses **3**, Buffs **35**.

## Step-by-Step Instructions

1. **Confirm authorization** — Augustus sends real adversarial prompts (including offensive content for some probes such as `lmrc`); only test systems you are allowed to attack.
2. **Verify binary** — `augustus version` and `augustus --help` (verbatim Captured help in `.docs/docs-for-cli-tools/Augustus-CLI-Options.md`).
3. **Discover capabilities** — `augustus list` for registered probes, detectors, generators, harnesses, buffs, and recon modules.
4. **Choose generator** — provider name as `<generator>` (help examples: `openai.OpenAI`, `anthropic.Anthropic`). Custom HTTP APIs: `rest.Rest` with `-c` / `--config-file`. Local smoke: `test.Blank` (no remote calls).
5. **Start narrow** — one `--probe` + one `--detector` before globs or `--all`.
6. **Configure model / endpoint** — `-m/--model`, `-c/--config` (JSON), and/or `--config-file` YAML; optional `--profile` from the config file.
7. **Run with structured output (SpiderFeet mandatory path)**  
   - Prefer **`--format json`** for a single JSON document on stdout (`attempts[]` + `count`), and/or  
   - **`-o results.jsonl`** (help: JSONL output file path).  
   Optional `--html report.html` for stakeholders; do not use table-only as the examination source.
8. **Expand coverage** — `--probes-glob` / `--detectors-glob`, then buffs (`-b` / `--buffs-glob`), then `--all` only after baseline validation.
9. **Tune runtime** — `--concurrency` (default 10, `$AUGUSTUS_CONCURRENCY`), `--timeout`, `--probe-timeout`; add `--refusal-pattern` for custom guardrail phrases.
10. **Optional recon** — `--recon` modules (e.g. `recon.MCP`) may run with or without probes (per help).
11. **Hooks** — `--setup` / `--prepare` / `--cleanup` shell hooks when the engagement needs env injection or per-probe prep (see Captured help).
12. **Parse + map nuggets** — read JSON/JSONL attempts; map findings per `references/nugget-mapping.md` (catalogue ids; no invented `LLM_*` types without extension approval).
13. **Chain** — after Julius (or equivalent) fingerprints an inference surface, Augustus validates guardrail posture on that endpoint.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `--format json` and/or `-o …jsonl`; never parse table TTY alone |
| Smoke / connectivity check | `test.Blank` or one probe + one detector on the real generator |
| Hosted OpenAI / Anthropic / etc. | Named generator + API key env / config; set `-m` or `-c` model |
| Custom / proprietary HTTP API | `rest.Rest` with URI + request/response mapping in config |
| Local Ollama | `ollama.Ollama` / `ollama.OllamaChat` with model in config (per `augustus list`) |
| Thematic batch | `--probes-glob "dan.*,goodside.*"` + aligned `--detectors-glob` |
| Evasion / encoding resilience | Baseline without buffs, then `-b` / `--buffs-glob "encoding.*"` |
| Multi-turn strategies | Probes such as `crescendo.Crescendo`, `goat.Goat`, `hydra.Hydra`, `mischievous.MischievousUser` with judge/attacker YAML (upstream README); longer `--timeout` |
| Custom refusal wording false positives | Repeatable `--refusal-pattern` (YAML: `detectors.refusal_patterns`) |
| Rate limits / flaky provider | Lower `--concurrency`; raise `--timeout` / `--probe-timeout` |
| MCP / agent surface recon | `--recon recon.MCP` (and related) before or beside probes |
| Formal examination | Structured JSON/JSONL → harvest bundle `records[]` → graph + narrative |

## Guardrails & Pitfalls

- **Authorized testing only** — outputs and probes may include harmful/offensive content by design.
- **Do not invent flags** — authoritative surface is Captured help **2026-08-10** for **0.14.15**. Upstream README may document wording or defaults that differ; when they disagree, **Captured help wins**.
- **One failed probe ≠ full compromise** — score, detector, and context matter; keep SAFE/VULN together.
- **Redact secrets** — API keys, prompts, and model responses in shared artifacts.
- **Align detectors with probes** — mismatched pairs produce misleading pass/fail.
- **`--format` default is `table`** — unsuitable as the sole SpiderFeet examination artifact.
- **`-o` is JSONL** — help labels it “JSONL output file path”; for a single JSON root prefer `--format json` (confirmed on this binary with `test.Blank`).
- **Multi-turn cost** — Crescendo/GOAT/Hydra/Mischievous need attacker + judge LLMs; expect higher latency and spend.
- **Track run metadata** — generator, model, probe set, buffs, concurrency, timeouts with every report.

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Command tree, SpiderFeet defaults, Captured help pointer |
| `output-and-parsing.md` | JSON / JSONL attempt schema, harvest bundles |
| `nugget-mapping.md` | Findings → SpiderFeet `nodes[]` / `edges[]` |
| `tactics.md` | Sequencing, buffs, multi-turn, recon |
| `sources.md` | Official repo, blog, releases |

Operator guides: `.docs/docs-for-cli-tools/Augustus-Zero-to-Hero.md`, `Augustus-CLI-Options.md`.

## Comprehensive Examples

### SMOKE (LOCAL, NO API)

```bash
augustus scan test.Blank \
  --probe dan.Dan_11_0 \
  --detector dan.DAN \
  --format json
```

### SINGLE PROBE + STRUCTURED

```bash
augustus scan openai.OpenAI \
  --probe dan.Dan_11_0 \
  --detector dan.DAN \
  --format json \
  -o out.jsonl
```

### MODEL SHORTHAND / CONFIG

```bash
augustus scan openai.OpenAI -m gpt-4 --probe dan.Dan_11_0 --detector dan.DAN --format json
augustus scan anthropic.Anthropic \
  --config '{"model":"claude-3-opus-20240229"}' \
  --probe dan.Dan_11_0 --detector dan.DAN -o claude.jsonl
augustus scan openai.OpenAI --config-file config.yaml --profile thorough --probes-glob "dan.*" -o batch.jsonl
```

### GLOBS, BUFFS, FULL SUITE

```bash
augustus scan openai.OpenAI \
  --probes-glob "dan.*,goodside.*,grandma.*" \
  --detectors-glob "*" \
  --buffs-glob "encoding.*,paraphrase.*" \
  --format json -o buffed.jsonl

augustus scan anthropic.Anthropic --all --timeout 60m --concurrency 10 \
  -o comprehensive.jsonl --html report.html
```

### CUSTOM REST ENDPOINT

```bash
augustus scan rest.Rest \
  --probe dan.Dan_11_0 --detector dan.DAN \
  --config-file rest.yaml \
  --format json -o rest.jsonl --html report.html
```

### RECON / REFUSAL / HOOKS

```bash
augustus scan rest.Rest --recon recon.MCP --config-file mcp.yaml --format json -o recon.jsonl
augustus scan openai.OpenAI --probe dan.Dan_11_0 --detector dan.DAN \
  --refusal-pattern "I cannot help with that" --format json
augustus scan openai.OpenAI --probe dan.Dan_11_0 --detector dan.DAN \
  --setup './prep.sh' --prepare './per_probe.sh' --cleanup './teardown.sh' -o hooked.jsonl
```

### PREFERRED SPIDERFEET PATH (WSL)

```bash
/mnt/c/projects/spiderfeet/.tools/augustus/augustus \
  scan openai.OpenAI \
  --probe dan.Dan_11_0 --detector dan.DAN \
  --format json -o results.jsonl
```

### PARSE JSON ATTEMPTS (Python sketch)

```python
import json
from pathlib import Path

# stdout --format json shape (single object)
doc = json.loads(Path("scan.json").read_text(encoding="utf-8"))
for attempt in doc.get("attempts") or []:
    probe = attempt.get("probe")
    scores = attempt.get("scores") or []
    status = attempt.get("status")
    # → VULNERABILITY_GENERAL / RAW_RIR_DATA descriptors
    print(probe, status, scores)
```

## Strategies and Tactics

See [`references/tactics.md`](references/tactics.md). Summary:

1. **Smoke → thematic → broad** — never start with `--all` on a paid API.
2. **Structured-first** — `--format json` and/or `-o` JSONL for examination; table/HTML are operator UX only.
3. **Baseline then buff** — compare vulnerability rate with and without encoding/paraphrase buffs.
4. **Multi-turn last** — after single-turn baseline; budget judge/attacker spend.
5. **Recon when MCP/agent surfaces matter** — `--recon` before deep probe suites.
6. **Fingerprint then attack** — Julius (or similar) to find inference endpoints; Augustus to stress guardrails.
