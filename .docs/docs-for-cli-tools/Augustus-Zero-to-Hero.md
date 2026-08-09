# Augustus Zero to Hero — LLM Vulnerability Scanning

Operator guide from install through list/scan, structured JSON/JSONL evidence, and SpiderFeet nugget mapping.

Skill reference: `.cursor/skills/Augustus/SKILL.md`

**Binary name:** `augustus` (Praetorian). Skill folder: `Augustus`.

---

## 0. What Augustus does

**Augustus** ([praetorian-inc/augustus](https://github.com/praetorian-inc/augustus)) is a Go LLM vulnerability scanner. It runs adversarial **probes** against a **generator** (provider or custom REST endpoint), scores responses with **detectors**, optionally transforms prompts with **buffs**, and can run **recon** modules. Outputs include table (default), JSON/JSONL, and HTML reports.

Augustus does **not**:

- Replace HTTP tech fingerprinting (**httpx** / **Julius**)
- Replace conventional web CVE templates (**nuclei**)
- Replace secret scanning (**Titus** / Nosey Parker)

**SpiderFeet uses:** `--format json` and/or `-o` JSONL → harvest `records[]` → `VULNERABILITY_GENERAL` / `RAW_RIR_DATA` (and host nuggets when a REST URI is known).

**This guide matches binary 0.14.15** (Captured help **2026-08-10**). Do not invent flags from newer README sections until they appear in `--help` for your build.

---

## 1. Install

### Local SpiderFeet binary (authoritative on this host)

```bash
# WSL
/mnt/c/projects/spiderfeet/.tools/augustus/augustus version

# Windows path to the same file
# C:\projects\spiderfeet\.tools\augustus\augustus
```

Expected: `augustus 0.14.15`.

### Go install

```bash
go install github.com/praetorian-inc/augustus/cmd/augustus@latest
augustus version
```

### Prebuilt release

Download from [GitHub releases](https://github.com/praetorian-inc/augustus/releases), extract, `chmod +x`, run `augustus version`.

### Verify

```bash
wsl bash -lc "/mnt/c/projects/spiderfeet/.tools/augustus/augustus --help"
```

Captured help: `.docs/docs-for-cli-tools/Augustus-CLI-Options.md` (date **2026-08-10**).

---

## 2. Discover capabilities

```bash
augustus list
```

On this **0.14.15** host (2026-08-10): **239** probes, **3** recon, **48** generators, **129** detectors, **3** harnesses, **35** buffs.

Use exact names from `list` in `--probe`, `--detector`, `-b`, `--recon`, and `<generator>`.

---

## 3. First scan (smoke)

No remote API (parser / CLI check):

```bash
augustus scan test.Blank \
  --probe dan.Dan_11_0 \
  --detector dan.DAN \
  --format json
```

Real provider (set API key via env or config first):

```bash
export OPENAI_API_KEY="your-api-key"
augustus scan openai.OpenAI \
  --probe dan.Dan_11_0 \
  --detector dan.DAN \
  --format json \
  -o out.jsonl
```

Model shorthand:

```bash
augustus scan openai.OpenAI -m gpt-4 \
  --probe dan.Dan_11_0 --detector dan.DAN \
  --format json -o out.jsonl
```

---

## 4. Expand coverage

```bash
augustus scan openai.OpenAI \
  --probes-glob "dan.*,goodside.*,grandma.*" \
  --detectors-glob "*" \
  --config-file config.yaml \
  --format json \
  -o batch.jsonl
```

Full suite (expensive — only after smoke):

```bash
augustus scan anthropic.Anthropic \
  --all \
  --timeout 60m \
  --concurrency 10 \
  -o comprehensive.jsonl \
  --html comprehensive-report.html \
  --format json
```

---

## 5. Buffs (evasion)

```bash
augustus scan openai.OpenAI \
  --probes-glob "dan.*" \
  --buffs-glob "encoding.*,paraphrase.*" \
  --format json \
  -o buffed.jsonl
```

Compare against an unbuffed baseline JSONL for the same probe set.

---

## 6. Custom REST endpoints

```bash
augustus scan rest.Rest \
  --probe dan.Dan_11_0 \
  --detector dan.DAN \
  --config-file rest.yaml \
  --format json \
  -o rest.jsonl \
  --html report.html
```

Configure `uri`, request templates (`$INPUT`), and response JSONPath in YAML/JSON per upstream README. Prefer Julius/httpx first to confirm the inference URL.

---

## 7. Multi-turn strategies

Probes such as `crescendo.Crescendo`, `goat.Goat`, `hydra.Hydra`, and `mischievous.MischievousUser` need judge/attacker configuration in YAML (see upstream README). Raise `--timeout`, keep concurrency modest, always keep structured output:

```bash
augustus scan rest.Rest \
  --probe crescendo.Crescendo \
  --config-file crescendo.yaml \
  --timeout 60m \
  --format json -o crescendo.jsonl --html report.html -v
```

---

## 8. Recon, refusal patterns, hooks

```bash
# MCP-oriented recon (names from augustus list)
augustus scan rest.Rest --recon recon.MCP --config-file mcp.yaml --format json -o recon.jsonl

# Custom guardrail phrasing
augustus scan openai.OpenAI --probe dan.Dan_11_0 --detector dan.DAN \
  --refusal-pattern "I cannot help with that" --format json

# Lifecycle hooks (see Captured help for KEY=VALUE / AUGUSTUS_LAST_RESPONSE)
augustus scan openai.OpenAI --probe dan.Dan_11_0 --detector dan.DAN \
  --setup './prep.sh' --cleanup './teardown.sh' -o hooked.jsonl --format json
```

---

## 9. Convert to SpiderFeet nuggets

1. Parse `--format json` (`attempts[]`) or `-o` JSONL into harvest `records[]`.
2. Map hosts → `INTERNET_NAME` when URI known; findings → `VULNERABILITY_GENERAL`; probe/detector/score → `RAW_RIR_DATA`.
3. Do **not** invent `LLM_*` nugget types without `nuggets_extension.json` approval.
4. Details: `.cursor/skills/Augustus/references/nugget-mapping.md`.

---

## 10. Common pitfalls

- Missing API keys / wrong generator name (use `augustus list`)
- Starting with `--all` on a metered API
- Using default `--format table` as the only capture for corpus work
- Mismatched probe/detector families
- Missing judge config for multi-turn probes
- Over-parallelizing into rate limits (lower `--concurrency`)
- Sharing raw prompts/keys in tickets or chat
- Inventing flags not present in Captured help **2026-08-10**

---

## See also

- `.docs/docs-for-cli-tools/Augustus-CLI-Options.md` — full Captured help
- `.cursor/skills/Augustus/SKILL.md` — agent workflows
- `.cursor/skills/julius/SKILL.md` — fingerprint inference surfaces first
