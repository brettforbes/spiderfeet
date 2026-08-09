# Augustus CLI Options

Invocation: **`augustus`** (Praetorian; case-sensitive). Skill folder: `Augustus`.

SpiderFeet formal examination defaults:

```bash
# Preferred: single JSON document on stdout + optional JSONL file
augustus scan <generator> --probe <probe> --detector <detector> --format json -o results.jsonl

# Smoke without remote API
augustus scan test.Blank --probe dan.Dan_11_0 --detector dan.DAN --format json
```

| Field | Value |
|-------|-------|
| Binary (WSL) | `/mnt/c/projects/spiderfeet/.tools/augustus/augustus` |
| Binary (Windows path) | `C:\projects\spiderfeet\.tools\augustus\augustus` |
| Version | **0.14.15** |
| Capture date | **2026-08-10** |
| Help source | `.tmp_augustus_help/*.txt` |

> Flags below are from live `--help` on **0.14.15** only. Do not invent options. When README and Captured help disagree, **Captured help wins**.

## Captured help

Live help text from `/mnt/c/projects/spiderfeet/.tools/augustus/augustus` via WSL on **2026-08-10**. Full verbatim blocks: `.docs/docs-for-cli-tools/Augustus-CLI-Options.md` § Captured help.

### Re-capture

```powershell
New-Item -ItemType Directory -Force -Path .tmp_augustus_help | Out-Null
$bin = "/mnt/c/projects/spiderfeet/.tools/augustus/augustus"
wsl bash -lc "$bin --help" | Out-File -Encoding utf8 .tmp_augustus_help/root_help.txt
wsl bash -lc "$bin version" | Out-File -Encoding utf8 .tmp_augustus_help/version.txt
wsl bash -lc "$bin version --help" | Out-File -Encoding utf8 .tmp_augustus_help/version_help.txt
wsl bash -lc "$bin list --help" | Out-File -Encoding utf8 .tmp_augustus_help/list_help.txt
wsl bash -lc "$bin scan --help" | Out-File -Encoding utf8 .tmp_augustus_help/scan_help.txt
wsl bash -lc "$bin completion --help" | Out-File -Encoding utf8 .tmp_augustus_help/completion_help.txt
```

## Command tree (0.14.15)

| Command | Role |
|---------|------|
| `augustus version` | Print version information |
| `augustus list` | List available probes, detectors, generators (also harnesses, buffs, recon on this binary) |
| `augustus scan <generator>` | Run vulnerability scan against LLM |
| `augustus completion <shell>` | Generate shell completion (`bash`, `zsh`, `fish`) |

Global flags (all commands): `-h/--help`, `-d/--debug` (`$AUGUSTUS_DEBUG`).

## Options by command (from Captured help)

### Global

| Flag | Description |
|------|-------------|
| `-h, --help` | Context-sensitive help |
| `-d, --debug` | Enable debug mode (`$AUGUSTUS_DEBUG`) |

### `scan <generator>`

| Argument / flag | Default (help) | Description |
|-----------------|----------------|-------------|
| `<generator>` | — | Generator name (e.g. `openai.OpenAI`, `anthropic.Anthropic`) |
| `--detector` | — | Detector names (repeatable) |
| `--detectors-glob` | — | Comma-separated detector glob patterns |
| `--refusal-pattern` | — | Target refusal/guardrail phrase treated as mitigation (repeatable); YAML: `detectors.refusal_patterns` |
| `-b, --buff` | — | Buff names (repeatable) |
| `--buffs-glob` | — | Comma-separated buff glob patterns (e.g. `encoding.*`) |
| `--config-file` | — | YAML config file path |
| `-c, --config` | — | JSON config for generator |
| `-m, --model` | — | Model name shorthand for `--config '{"model":"..."}'` |
| `--profile` | — | Named profile from config file |
| `--harness` | `probewise.Probewise` | Harness name |
| `--timeout` | — | Overall scan timeout (`0` = no timeout) |
| `--concurrency` | `10` | Max concurrent probes (`$AUGUSTUS_CONCURRENCY`) |
| `--probe-timeout` | — | Per-probe timeout (`0` = no timeout) |
| `-f, --format` | `table` | Output format |
| `-o, --output` | — | **JSONL** output file path |
| `--html` | — | HTML report file path |
| `-v, --verbose` | — | Verbose output |
| `--setup` | — | Shell command once before all probes; stdout `KEY=VALUE` → `$KEY` in request template |
| `--prepare` | — | Shell command before each probe; gets `AUGUSTUS_LAST_RESPONSE` |
| `--cleanup` | — | Shell command once after all probes |
| `-p, --probe` | — | Probe names (repeatable) |
| `--probes-glob` | — | Comma-separated probe glob patterns (e.g. `dan.*,encoding.*`) |
| `--all` | — | Run all registered probes |
| `--recon` | — | Reconnaissance module names (repeatable); may run with or without probes |

**Format note:** Captured help does not enumerate `--format` values (only default `table`). Official README documents `table`, `json`, and `jsonl`. On this **0.14.15** binary, `--format json` was verified to emit a single JSON object with `attempts` / `count`. Prefer that and/or `-o` JSONL for SpiderFeet.

### `list`

No command-specific flags beyond global `-h` / `-d`.

### `completion <shell>`

| Argument | Description |
|----------|-------------|
| `<shell>` | `bash`, `zsh`, or `fish` |

### `version`

No command-specific flags beyond global `-h` / `-d`.

## Capability snapshot (live `augustus list`, 2026-08-10)

| Class | Count (this binary) | Examples |
|-------|---------------------|----------|
| Probes | 239 | `dan.Dan_11_0`, `crescendo.Crescendo`, `goat.Goat` |
| Recon | 3 | `recon.MCP`, `recon.MCPConfig`, `recon.MCPIdentifiers` |
| Generators | 48 | `openai.OpenAI`, `anthropic.Anthropic`, `rest.Rest`, `test.Blank` |
| Detectors | 129 | (see `augustus list`) |
| Harnesses | 3 | `agentwise.Agentwise`, `batch.Batch`, `probewise.Probewise` |
| Buffs | 35 | `encoding.Base64`, … |

## See also

Full Captured help text: `.docs/docs-for-cli-tools/Augustus-CLI-Options.md`.
