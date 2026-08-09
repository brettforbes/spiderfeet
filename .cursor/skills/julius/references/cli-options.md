# Julius CLI Options

Invocation: **`julius`**. SpiderFeet formal examination defaults:

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

> **No version command.** `julius version` → `unknown command "version"`. `julius --version` → `unknown flag: --version`. Do not invent one.

> Flags below are from live `--help` only. Do not invent options.

## Captured help

Live help from `.tools/julius/julius.exe` on **2026-08-10**.

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

(Global flags repeated by Cobra; same set as root.)

### Version attempts (not supported)

```text
Error: unknown flag: --version
...
Error: unknown command "version" for "julius"
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

## Commands

| Command | Role |
|---------|------|
| `probe` | Fingerprint LLM / AI endpoints (primary SpiderFeet path) |
| `list` | Catalog embedded or custom probes |
| `validate` | Validate probe YAML directory |
| `completion` | Shell completion scripts |
| `help` | Help about any command |

### `julius probe [targets...]`

**Target input (one of):**

| Method | Example |
|--------|---------|
| CLI args | `julius probe https://a.example.com https://b.example.com:11434` |
| File | `julius probe -f targets.txt` |
| Stdin | `cat urls.txt \| julius probe -` |

**Target normalization** (upstream docs/README): adds `https://` if no scheme; strips trailing `/`; trims whitespace.  
`192.168.1.10:11434` → `https://192.168.1.10:11434`.

**Probe-only flags:**

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--file` | `-f` | — | Targets file, one per line |
| `--augustus` | — | `false` | Include Augustus generator configs in output |
| `--base-paths` | — | — | Comma-separated path prefixes prepended to probe paths |
| `--header` | `-H` | — | Custom HTTP header; repeatable (`stringArray`) |

### `julius list`

Lists probes: NAME, DESCRIPTION, PORT HINT, REQUESTS, SPECIFICITY, CATEGORY.

**Observed on this binary (2026-08-10):** `julius list -o json` and `julius list -o jsonl` still printed the human **table**. Prefer table capture for catalog scenarios until a future binary emits structured list output. Do not invent alternate list-export flags.

### `julius validate [directory]`

Validate custom probe YAML (syntax + required fields). Example from help: `julius validate ./probes`.

## Global flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--banner` | — | `true` | Show ASCII banner |
| `--ca-cert` | — | — | Path to custom CA certificate file |
| `--concurrency` | `-c` | `10` | Max concurrent probe requests **per target** |
| `--insecure` | — | `false` | Skip TLS certificate verification |
| `--max-response-size` | — | `10485760` | Max response body size (bytes; help: 10MB) |
| `--no-color` | — | `false` | Disable color output |
| `--output` | `-o` | `table` | `table`, `json`, or `jsonl` |
| `--probes-dir` | `-p` | embedded | Override probe definitions directory |
| `--quiet` | `-q` | `false` | Suppress non-match output |
| `--timeout` | `-t` | `5` | HTTP timeout (seconds) |
| `--verbose` | `-v` | `false` | Verbose output |
| `--help` | `-h` | — | Help |

## Output format selection

| Format | Use |
|--------|-----|
| `table` | Operator review (default) |
| `json` | Single JSON array — good for small batches / clean-miss `[]` |
| `jsonl` | **Preferred for agents / harvest streams** — one JSON object per line |

`-o` selects **format only**. Persist with shell redirect:

```bash
julius probe -f targets.txt -o jsonl > results.jsonl   # correct
# julius probe -o jsonl -o results.jsonl               # WRONG — second -o overwrites format
```

## Examples by flag

```bash
# Default table
julius probe https://target.example.com

# JSON array / JSONL
julius probe -o json https://target.example.com
julius probe -o jsonl -f targets.txt > out.jsonl

# Slow / concurrent
julius probe -t 15 -c 50 -f targets.txt -o jsonl

# TLS
julius probe --insecure -o json https://lab:11434
julius probe --ca-cert ./ca.pem -o jsonl -f internal.txt

# Path prefixes + headers
julius probe --base-paths /api,/proxy -o json https://edge:8080
julius probe -H "X-Api-Key: demo" -H "Accept: application/json" -o json https://gw

# Custom probes
julius validate ./my-probes
julius probe -p ./my-probes https://target.example.com -o jsonl

# Quiet / verbose / Augustus
julius probe -q -f targets.txt -o jsonl
julius probe -v https://target.example.com
julius probe --augustus -o json https://target.example.com

# Stdin from discovery
naabu -host 192.168.1.0/24 -p 11434,8000 -json -silent | \
  jq -r '"https://" + .ip + ":" + (.port|tostring)' | julius probe - -o jsonl
```
