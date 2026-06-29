# Julius CLI Options

Complete command-line reference for Julius LLM service fingerprinting.

**Binary:** `julius`  
**Install:** https://github.com/praetorian-inc/julius/releases

---

## Synopsis

```
julius [global flags] <command> [command flags] [args]
```

**Commands:** `probe`, `list`, `validate`

---

## Global flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | `table` | Output format: `table`, `json`, `jsonl` |
| `--probes-dir` | `-p` | embedded | Directory of custom probe YAML files |
| `--timeout` | `-t` | `5` | HTTP request timeout (seconds) |
| `--concurrency` | `-c` | `10` | Max concurrent probe HTTP requests per target |
| `--verbose` | `-v` | `false` | Verbose probe matching diagnostics |
| `--quiet` | `-q` | `false` | Suppress non-match output |

---

## `probe` — scan targets

```
julius probe [targets...] [flags]
```

### Target arguments

Positional URLs/host:port strings, or:

| Input | Example |
|-------|---------|
| Multiple args | `julius probe https://a https://b:11434` |
| File | `julius probe -f targets.txt` |
| Stdin | `julius probe -` |

**Normalization:** adds `https://` if missing; strips trailing `/`.

### Probe flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--file` | `-f` | — | File with one target per line |
| `--augustus` | — | `false` | Include Augustus generator configs in JSON |

### Examples

```bash
julius probe https://target.example.com
julius probe https://host1:11434 https://host2:8000
julius probe -f targets.txt
julius probe -f targets.txt -o jsonl
cat targets.txt | julius probe -
julius probe -o json https://ollama.lab:11434
julius probe -o jsonl -f targets.txt -o results.jsonl
julius probe -t 15 -c 50 -f targets.txt -o jsonl
julius probe -v https://host:8000
julius probe -q -f targets.txt -o jsonl
julius probe -p ./custom-probes https://host:9000 -o jsonl
julius probe --augustus -o json https://host:8000
```

### Output formats

**Table (default):**

```
| TARGET | SERVICE | SPECIFICITY | CATEGORY | MODELS | ERROR |
```

**JSON:** array of result objects.

**JSONL:** one result object per line (preferred for parsers).

Result fields: `target`, `service`, `matched_request`, `category`, `specificity`, `models[]`, `generator_configs[]`, `error`.

---

## `list` — probe catalog

```
julius list [global flags]
```

Displays NAME, DESCRIPTION, PORT HINT, REQUESTS, SPECIFICITY, CATEGORY.

```bash
julius list
julius list -o json
julius list -o jsonl
julius list -p ./custom-probes
```

---

## `validate` — probe YAML QA

```
julius validate <directory>
```

Exactly one argument: directory containing probe YAML files.

**Checks:** valid YAML, required fields (`name`, requests), specificity 0–100, valid `require`, each request has `path` and match rules.

```bash
julius validate ./probes
julius validate /path/to/custom-probes
```

---

## Piping from other tools

```bash
# Nmap greppable → URLs (adjust ports per open port)
nmap -p 11434,8000,8080 10.0.0.0/24 -oG - | grep open | awk '{print "https://" $2 ":11434"}' | julius probe - -o jsonl

# Naabu JSONL → URLs (jq)
naabu -host target -p 11434,8000 -json -silent | jq -r '"https://" + .ip + ":" + (.port|tostring)' | julius probe - -o jsonl
```

---

## Environment and security

- Julius performs **active HTTP(S) probing** against targets.
- Use only on **authorized** systems.
- See https://github.com/praetorian-inc/julius/blob/main/SECURITY.md

---

## Related documentation

| Resource | Path |
|----------|------|
| Agent skill | `.cursor/skills/julius/SKILL.md` |
| Reference index | `.cursor/skills/julius/references/SKILLS.md` |
| Wiki CLI | https://github.com/praetorian-inc/julius/wiki/CLI-Reference |
| Zero to Hero | `Julius-Zero-to-Hero.md` |
