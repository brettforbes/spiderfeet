# Julius CLI Options

Commands: **`probe`**, **`list`**, **`validate`**. Global flags apply to all commands.

## Commands

### `julius probe [targets...]`

Fingerprint LLM / AI inference endpoints over HTTP(S).

**Target input (one of):**

| Method | Example |
|--------|---------|
| CLI args | `julius probe https://a.example.com https://b.example.com:11434` |
| File | `julius probe -f targets.txt` |
| Stdin | `cat urls.txt \| julius probe -` |

**Target normalization:** adds `https://` if no scheme; strips trailing `/`; trims whitespace.  
`192.168.1.10:11434` → `https://192.168.1.10:11434`.

**Probe-only flags:**

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--file` | `-f` | — | Targets file, one per line |
| `--augustus` | — | `false` | Include Augustus generator configs in JSON output |

### `julius list`

List embedded (or custom) probes with metadata columns: NAME, DESCRIPTION, PORT HINT, REQUESTS, SPECIFICITY, CATEGORY.

```bash
julius list
julius list -o json
```

Respects `--output` and `--probes-dir`.

### `julius validate <directory>`

Validate custom probe YAML in a directory (syntax, required fields, specificity 0–100, match rules).

```bash
julius validate ./probes
julius validate /path/to/custom-probes
```

## Global flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | `table` | `table`, `json`, or `jsonl` |
| `--probes-dir` | `-p` | embedded | Override probe definitions directory |
| `--timeout` | `-t` | `5` | HTTP timeout (seconds) |
| `--concurrency` | `-c` | `10` | Max concurrent probe requests **per target** |
| `--verbose` | `-v` | `false` | Debug probe matching |
| `--quiet` | `-q` | `false` | Suppress non-match output |

## Output format selection

| Format | Use |
|--------|-----|
| `table` | Operator review (default) |
| `json` | Single JSON array (all results) |
| `jsonl` | **Preferred for agents** — one JSON object per line |

## Examples by flag

```bash
# Default table
julius probe https://target.example.com

# JSON array
julius probe -o json https://target.example.com

# JSON Lines (streaming)
julius probe -o jsonl -f targets.txt

# Model discovery
julius probe -o json https://ollama.example.com:11434 | jq '.[] | {service, models}'

# Slow / latent services
julius probe -t 15 -c 50 -f targets.txt -o jsonl

# Custom probes (dev)
julius probe -p ./my-probes https://target.example.com

# Quiet — matches only
julius probe -q -f targets.txt -o jsonl

# Augustus configs for downstream scanning
julius probe --augustus -o json https://target.example.com

# Verbose debugging
julius probe -v https://target.example.com

# Stdin from Nmap greppable
nmap -p 8080,11434,4000,7860 192.168.1.0/24 -oG - | grep open | awk '{print $2}' | \
  while read ip; do echo "https://$ip:11434"; done | julius probe - -o jsonl
```
