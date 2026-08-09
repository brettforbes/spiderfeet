# Augustus CLI Options

Operator reference for **`augustus`** **0.14.15** ([praetorian-inc/augustus](https://github.com/praetorian-inc/augustus)). Prefer structured artifacts: `--format json` and/or `-o` JSONL (help: JSONL output file path).

## SpiderFeet preferred commands

```bash
# Smoke (no remote API)
augustus scan test.Blank --probe dan.Dan_11_0 --detector dan.DAN --format json

# Single probe + JSON + JSONL file
augustus scan openai.OpenAI \
  --probe dan.Dan_11_0 --detector dan.DAN \
  --format json -o results.jsonl

# Thematic batch
augustus scan openai.OpenAI \
  --probes-glob "dan.*,goodside.*" --detectors-glob "*" \
  --format json -o batch.jsonl

# Custom REST
augustus scan rest.Rest --config-file rest.yaml \
  --probe dan.Dan_11_0 --detector dan.DAN \
  --format json -o rest.jsonl --html report.html
```

| Field | Value |
|-------|-------|
| Version | **0.14.15** (`augustus 0.14.15`) |
| Binary (WSL) | `/mnt/c/projects/spiderfeet/.tools/augustus/augustus` |
| Binary (Windows path) | `C:\projects\spiderfeet\.tools\augustus\augustus` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_augustus_help/*.txt` |
| Skill | `.cursor/skills/Augustus/SKILL.md` |

> Flags below are from live `--help` on **0.14.15** only. Do not invent options. Upstream README may document format enums or examples that are absent from this binary’s help text — verify before use. When they disagree, **Captured help wins**.

---

## Captured help

Live help text captured from `/mnt/c/projects/spiderfeet/.tools/augustus/augustus` via WSL on **2026-08-10**. Each block is the full stdout of the listed command.

### Root (`augustus --help`)

```text
Usage: augustus <command> [flags]

Augustus - LLM Vulnerability Scanner

Flags:
  -h, --help     Show context-sensitive help.
  -d, --debug    Enable debug mode ($AUGUSTUS_DEBUG).

Commands:
  version [flags]
    Print version information.

  list [flags]
    List available probes, detectors, generators.

  scan <generator> [flags]
    Run vulnerability scan against LLM.

  completion <shell> [flags]
    Generate shell completion scripts.

Run "augustus <command> --help" for more information on a command.
```

### `version` (`augustus version` and `augustus version --help`)

```text
augustus 0.14.15
```

```text
Usage: augustus version [flags]

Print version information.

Flags:
  -h, --help     Show context-sensitive help.
  -d, --debug    Enable debug mode ($AUGUSTUS_DEBUG).
```

### `list` (`augustus list --help`)

```text
Usage: augustus list [flags]

List available probes, detectors, generators.

Flags:
  -h, --help     Show context-sensitive help.
  -d, --debug    Enable debug mode ($AUGUSTUS_DEBUG).
```

### `scan` (`augustus scan --help`)

```text
Usage: augustus scan <generator> [flags]

Run vulnerability scan against LLM.

Arguments:
  <generator>    Generator name (e.g., openai.OpenAI, anthropic.Anthropic).

Flags:
  -h, --help                      Show context-sensitive help.
  -d, --debug                     Enable debug mode ($AUGUSTUS_DEBUG).

      --detector=DETECTOR,...     Detector names (repeatable).
      --detectors-glob=STRING     Comma-separated detector glob patterns.
      --refusal-pattern=REFUSAL-PATTERN,...
                                  Target's own refusal/guardrail phrase
                                  to treat as a mitigation (repeatable).
                                  Added to the recognized phrases of the
                                  mitigation/refusal detectors (mitigation.*,
                                  multiagent.*, latentinjection.Detector,
                                  pair.PAIR, divergence.RepeatDiverges) to
                                  avoid false positives on custom guardrails.
                                  YAML equivalent: detectors.refusal_patterns.
  -b, --buff=BUFF,...             Buff names to apply (repeatable).
      --buffs-glob=STRING         Comma-separated buff glob patterns (e.g.,
                                  'encoding.*').
      --config-file=STRING        YAML config file path.
  -c, --config=STRING             JSON config for generator.
  -m, --model=STRING              Model name for generator (shorthand for
                                  --config '{"model":"..."}').
      --profile=STRING            Named profile to apply from config file.
      --harness="probewise.Probewise"
                                  Harness name (default: probewise.Probewise).
      --timeout=DURATION          Overall scan timeout (0 = no timeout).
      --concurrency=INT           Max concurrent probes (default: 10)
                                  ($AUGUSTUS_CONCURRENCY).
      --probe-timeout=DURATION    Per-probe timeout (0 = no timeout).
  -f, --format="table"            Output format.
  -o, --output=STRING             JSONL output file path.
      --html=STRING               HTML report file path.
  -v, --verbose                   Verbose output.
      --setup=STRING              Shell command run once before all probes.
                                  Stdout KEY=VALUE lines are injected into the
                                  generator request template as $KEY.
      --prepare=STRING            Shell command run before each probe.
                                  Receives AUGUSTUS_LAST_RESPONSE env var with
                                  raw response from the previous probe.
      --cleanup=STRING            Shell command run once after all probes
                                  complete.

probes
  -p, --probe=PROBE,...       Probe names (repeatable).
      --probes-glob=STRING    Comma-separated probe glob patterns (e.g.,
                              'dan.*,encoding.*').
      --all                   Run all registered probes.

recon
  --recon=RECON,...    Reconnaissance module names (repeatable). Gather target
                       facts (observations); may run with or without probes.
```

### `completion` (`augustus completion --help`)

```text
Usage: augustus completion <shell> [flags]

Generate shell completion scripts.

Arguments:
  <shell>    Shell type (bash, zsh, fish).

Flags:
  -h, --help     Show context-sensitive help.
  -d, --debug    Enable debug mode ($AUGUSTUS_DEBUG).
```

---

## Options summary (from Captured help)

### Global

| Flag | Description |
|------|-------------|
| `-h, --help` | Context-sensitive help |
| `-d, --debug` | Debug mode (`$AUGUSTUS_DEBUG`) |

### `scan`

| Flag / arg | Default | Description |
|------------|---------|-------------|
| `<generator>` | *(required)* | e.g. `openai.OpenAI`, `anthropic.Anthropic` |
| `--detector` | — | Detectors (repeatable) |
| `--detectors-glob` | — | Detector globs |
| `--refusal-pattern` | — | Custom refusal phrases (repeatable) |
| `-b, --buff` | — | Buffs (repeatable) |
| `--buffs-glob` | — | Buff globs |
| `--config-file` | — | YAML config |
| `-c, --config` | — | JSON generator config |
| `-m, --model` | — | Model shorthand |
| `--profile` | — | Named profile from config file |
| `--harness` | `probewise.Probewise` | Harness name |
| `--timeout` | — | Overall timeout (`0` = none) |
| `--concurrency` | `10` | Max concurrent probes |
| `--probe-timeout` | — | Per-probe timeout (`0` = none) |
| `-f, --format` | `table` | Output format |
| `-o, --output` | — | JSONL output file path |
| `--html` | — | HTML report path |
| `-v, --verbose` | — | Verbose |
| `--setup` / `--prepare` / `--cleanup` | — | Shell hooks (see Captured help) |
| `-p, --probe` | — | Probes (repeatable) |
| `--probes-glob` | — | Probe globs |
| `--all` | — | All registered probes |
| `--recon` | — | Recon modules (repeatable) |

**`--format` values:** Captured help only shows default `table`. Official README documents `table`, `json`, `jsonl`. On this binary, `--format json` was verified (single JSON object with `attempts` / `count`). Prefer `--format json` and/or `-o` for SpiderFeet.

### `completion`

| Arg | Values (help) |
|-----|----------------|
| `<shell>` | `bash`, `zsh`, `fish` |

---

## Structured outputs

| Mode | Flag | Structured form |
|------|------|-----------------|
| JSON document | `--format json` | Single JSON root (`attempts[]`, `count`) |
| JSONL file | `-o file.jsonl` | Line-delimited attempt objects |
| HTML | `--html file.html` | Report (not graph source) |
| Table | `--format table` | TTY only |

Harvest should normalize JSONL into a single JSON bundle with `records[]` for the CLI Profiling Structured pane.

---

## Capability snapshot (live `augustus list`, 2026-08-10)

| Class | Count |
|-------|-------|
| Probes | 239 |
| Recon | 3 (`recon.MCP`, `recon.MCPConfig`, `recon.MCPIdentifiers`) |
| Generators | 48 |
| Detectors | 129 |
| Harnesses | 3 (`agentwise.Agentwise`, `batch.Batch`, `probewise.Probewise`) |
| Buffs | 35 |

---

## Examples

```bash
augustus list
augustus version
augustus scan test.Blank --probe dan.Dan_11_0 --detector dan.DAN --format json
augustus scan openai.OpenAI -m gpt-4 --probe dan.Dan_11_0 --detector dan.DAN -o out.jsonl --format json
augustus scan openai.OpenAI --probes-glob "dan.*" --buffs-glob "encoding.*" --format json -o buffed.jsonl
augustus scan rest.Rest --config-file rest.yaml --all --timeout 60m -o all.jsonl --html report.html
augustus scan openai.OpenAI --recon recon.MCP --format json -o recon.jsonl
augustus completion zsh
```

---

## README / newer-build drift

Documented in upstream README or examples but **not** spelled out in Captured help for this **0.14.15** binary — verify after upgrades:

- Explicit `--format` enum text (`table|json|jsonl`) in README CLI tables
- Multi-turn YAML fields (`judge`, `attacker_*`, `max_turns`, …) — config content, not CLI flags
- Provider-specific env var names beyond what help lists

When Captured help and README disagree, **Captured help wins** for the installed binary.

---

## See also

- `.docs/docs-for-cli-tools/Augustus-Zero-to-Hero.md`
- `.cursor/skills/Augustus/SKILL.md`
- `.cursor/skills/Augustus/references/cli-options.md`
