# Julius CLI Options

Operator reference for **Julius** LLM service fingerprinting ([praetorian-inc/julius](https://github.com/praetorian-inc/julius)). Prefer structured JSON/JSONL for SpiderFeet corpus and automation.

## SpiderFeet preferred commands

```bash
julius probe -o jsonl -f targets.txt > julius_out.jsonl
julius probe -o json https://lab.internal:11434
```

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\julius\julius.exe` |
| Release zip (same dir) | `julius_1.4.10_windows_amd64.zip` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_julius_help/*.txt` |

> **No `version` / `--version`.** Live binary rejects both. Identify capability with `julius --help` and `julius list`.  
> Flags below are from live `--help` only — do not invent options. Wiki CLI pages may omit newer globals (`--insecure`, `--ca-cert`, `--base-paths`, `-H`, …).

---

## Captured help

Live help text captured from `.tools/julius/julius.exe` on **2026-08-10**.

### Root (`julius --help`)

```text
Julius is a tool for fingerprinting LLM services by sending HTTP probes
and analyzing responses. It helps identify LLM platforms and available models.

Usage:
  julius [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  help        Help about any command
  list        List all available probe definitions
  probe       Probe targets to identify LLM services
  validate    Validate probe definition files

Flags:
      --banner                  Show ASCII banner (default true)
      --ca-cert string          Path to custom CA certificate file
  -c, --concurrency int         Maximum concurrent probe requests per target (default 10)
  -h, --help                    help for julius
      --insecure                Skip TLS certificate verification
      --max-response-size int   Maximum response body size in bytes (default 10MB) (default 10485760)
      --no-color                Disable color output
  -o, --output string           Output format (table, json, jsonl) (default "table")
  -p, --probes-dir string       Override probe definitions directory
  -q, --quiet                   Suppress non-match output
  -t, --timeout int             HTTP timeout in seconds (default 5)
  -v, --verbose                 Verbose output

Use "julius [command] --help" for more information about a command.
```

### `probe` (`julius probe --help`)

```text
Probe one or more targets to identify which LLM service they are using.

Targets can be specified in three ways:
  1. As command line arguments: julius probe https://api.example.com
  2. From a file: julius probe -f targets.txt
  3. From stdin: cat targets.txt | julius probe -

Examples:
  julius probe https://api.example.com
  julius probe -f targets.txt
  cat targets.txt | julius probe -
  julius probe https://api1.example.com https://api2.example.com

Usage:
  julius probe [targets...] [flags]

Flags:
      --augustus             Include Augustus generator configs in output
      --base-paths string    Comma-separated path prefixes to prepend to probe paths (e.g., /api,/proxy)
  -f, --file string          Read targets from file
  -H, --header stringArray   Custom HTTP header (e.g., "Authorization: Bearer token"). Can be specified multiple times
  -h, --help                 help for probe

Global Flags:
      --banner                  Show ASCII banner (default true)
      --ca-cert string          Path to custom CA certificate file
  -c, --concurrency int         Maximum concurrent probe requests per target (default 10)
      --insecure                Skip TLS certificate verification
      --max-response-size int   Maximum response body size in bytes (default 10MB) (default 10485760)
      --no-color                Disable color output
  -o, --output string           Output format (table, json, jsonl) (default "table")
  -p, --probes-dir string       Override probe definitions directory
  -q, --quiet                   Suppress non-match output
  -t, --timeout int             HTTP timeout in seconds (default 5)
  -v, --verbose                 Verbose output
```

### `list` (`julius list --help`)

```text
List all probe definitions that are available for fingerprinting.
Shows the name, description, port hint, and number of requests for each definition.

Usage:
  julius list [flags]

Flags:
  -h, --help   help for list

Global Flags:
      --banner                  Show ASCII banner (default true)
      --ca-cert string          Path to custom CA certificate file
  -c, --concurrency int         Maximum concurrent probe requests per target (default 10)
      --insecure                Skip TLS certificate verification
      --max-response-size int   Maximum response body size in bytes (default 10MB) (default 10485760)
      --no-color                Disable color output
  -o, --output string           Output format (table, json, jsonl) (default "table")
  -p, --probes-dir string       Override probe definitions directory
  -q, --quiet                   Suppress non-match output
  -t, --timeout int             HTTP timeout in seconds (default 5)
  -v, --verbose                 Verbose output
```

### `validate` (`julius validate --help`)

```text
Validate probe definition YAML files in a directory.
Checks each file for proper YAML syntax and required fields.

Example:
  julius validate ./probes

Usage:
  julius validate [directory] [flags]

Flags:
  -h, --help   help for validate

Global Flags:
      --banner                  Show ASCII banner (default true)
      --ca-cert string          Path to custom CA certificate file
  -c, --concurrency int         Maximum concurrent probe requests per target (default 10)
      --insecure                Skip TLS certificate verification
      --max-response-size int   Maximum response body size in bytes (default 10MB) (default 10485760)
      --no-color                Disable color output
  -o, --output string           Output format (table, json, jsonl) (default "table")
  -p, --probes-dir string       Override probe definitions directory
  -q, --quiet                   Suppress non-match output
  -t, --timeout int             HTTP timeout in seconds (default 5)
  -v, --verbose                 Verbose output
```

### `completion` (`julius completion --help`)

```text
Generate the autocompletion script for julius for the specified shell.
See each sub-command's help for details on how to use the generated script.

Usage:
  julius completion [command]

Available Commands:
  bash        Generate the autocompletion script for bash
  fish        Generate the autocompletion script for fish
  powershell  Generate the autocompletion script for powershell
  zsh         Generate the autocompletion script for zsh
```

### Version attempts (not supported)

```text
Error: unknown flag: --version
...
Error: unknown command "version" for "julius"
Run 'julius --help' for usage.
```

### Re-capture

```powershell
New-Item -ItemType Directory -Force -Path .tmp_julius_help | Out-Null
$j = "C:\projects\spiderfeet\.tools\julius\julius.exe"
& $j --help | Out-File -Encoding utf8 .tmp_julius_help\root_help.txt
& $j probe --help | Out-File -Encoding utf8 .tmp_julius_help\probe_help.txt
& $j list --help | Out-File -Encoding utf8 .tmp_julius_help\list_help.txt
& $j validate --help | Out-File -Encoding utf8 .tmp_julius_help\validate_help.txt
& $j completion --help | Out-File -Encoding utf8 .tmp_julius_help\completion_help.txt
```

---

## Synopsis

```
julius [global flags] <command> [command flags] [args]
```

**Commands:** `probe`, `list`, `validate`, `completion`, `help`

---

## Global flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--banner` | — | `true` | Show ASCII banner |
| `--ca-cert` | — | — | Path to custom CA certificate file |
| `--concurrency` | `-c` | `10` | Max concurrent probe requests per target |
| `--insecure` | — | off | Skip TLS certificate verification |
| `--max-response-size` | — | `10485760` | Max response body size in bytes (10MB) |
| `--no-color` | — | off | Disable color output |
| `--output` | `-o` | `table` | Output format: `table`, `json`, `jsonl` |
| `--probes-dir` | `-p` | embedded | Override probe definitions directory |
| `--quiet` | `-q` | off | Suppress non-match output |
| `--timeout` | `-t` | `5` | HTTP timeout (seconds) |
| `--verbose` | `-v` | off | Verbose output |
| `--help` | `-h` | — | Help |

---

## `probe` — scan targets

```
julius probe [targets...] [flags]
```

### Target arguments

Positional URLs / host:port strings, or:

| Input | Example |
|-------|---------|
| Multiple args | `julius probe https://a https://b:11434` |
| File | `julius probe -f targets.txt` |
| Stdin | `julius probe -` |

**Normalization** (README/wiki): adds `https://` if missing; strips trailing `/`.

### Probe flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--file` | `-f` | — | File with one target per line |
| `--augustus` | — | off | Include Augustus generator configs in output |
| `--base-paths` | — | — | Comma-separated path prefixes to prepend to probe paths |
| `--header` | `-H` | — | Custom HTTP header; repeatable |

### Examples

```bash
julius probe https://target.example.com
julius probe https://host1:11434 https://host2:8000
julius probe -f targets.txt
julius probe -f targets.txt -o jsonl > results.jsonl
cat targets.txt | julius probe -
julius probe -o json https://ollama.lab:11434
julius probe -t 15 -c 50 -f targets.txt -o jsonl
julius probe -v https://host:8000
julius probe -q -f targets.txt -o jsonl
julius probe --insecure -o json https://lab:11434
julius probe --ca-cert ./ca.pem -o jsonl -f internal.txt
julius probe --base-paths /api,/proxy -o json https://edge:8080
julius probe -H "Authorization: Bearer token" -o json https://gw
julius probe -p ./custom-probes https://host:9000 -o jsonl
julius probe --augustus -o json https://host:8000
```

### Output formats

| `-o` | Shape | SpiderFeet use |
|------|-------|----------------|
| `table` | ASCII table | Human review only |
| `json` | JSON array | Small batches / clean-miss `[]` |
| `jsonl` | One object per line | **Preferred automation / harvest stream** |

`-o` is **format only**. Do not pass a filename as a second `-o`; use shell redirect.

**Result fields:** `target`, `service`, `matched_request`, `category`, `specificity`, optional `models[]`, `generator_configs[]`, `error`.

---

## `list` — probe catalog

```
julius list [global flags]
```

Displays NAME, DESCRIPTION, PORT HINT, REQUESTS, SPECIFICITY, CATEGORY.

Live capture on this binary listed **63** probes.

**Observed (2026-08-10):** `julius list -o json` / `-o jsonl` still emitted the human table. Prefer table for catalog scenarios; do not invent alternate export flags.

```bash
julius list
julius list -p ./custom-probes
```

---

## `validate` — probe YAML QA

```
julius validate [directory]
```

```bash
julius validate ./probes
julius validate /path/to/custom-probes
```

Help: checks YAML syntax and required fields. Wiki also describes specificity / `require` / match-rule checks.

---

## `completion`

```bash
julius completion bash
julius completion zsh
julius completion fish
julius completion powershell
```

---

## Piping from other tools

```bash
nmap -p 11434,8000,8080 10.0.0.0/24 -oG - | grep open | awk '{print "https://" $2 ":11434"}' | julius probe - -o jsonl

naabu -host target -p 11434,8000 -json -silent | jq -r '"https://" + .ip + ":" + (.port|tostring)' | julius probe - -o jsonl
```

---

## Environment and security

- Julius performs **active HTTP(S) probing**.
- Use only on **authorized** systems.
- See https://github.com/praetorian-inc/julius/blob/main/SECURITY.md

---

## Related documentation

| Resource | Path |
|----------|------|
| Agent skill | `.cursor/skills/julius/SKILL.md` |
| Reference index | `.cursor/skills/julius/references/SKILLS.md` |
| Zero to Hero | `Julius-Zero-to-Hero.md` |
| Wiki CLI | https://github.com/praetorian-inc/julius/wiki/CLI-Reference |
