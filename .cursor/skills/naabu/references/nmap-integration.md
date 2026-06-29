# Naabu Nmap Integration and Service Detection

## Built-in service version (`-sV`)

Naabu runs **parallel** service version detection using Nmap's `nmap-service-probes` database (read from local Nmap install — not bundled due to license).

```bash
naabu -host scanme.sh -sV
```

Example output:

```
scanme.sh:22 [ssh OpenSSH/6.6.1p1]
scanme.sh:80 [http Apache httpd/2.4.7]
```

With JSON:

```bash
naabu -host scanme.sh -sV -json -o sv.jsonl
```

| Flag | Purpose |
|------|---------|
| `-sV` | Full version probing |
| `-sV-fast` | Port-hinted probes only — faster |
| `-sV-timeout` | Per-probe timeout |
| `-sV-workers` | Concurrency |
| `-sV-probes` | Custom probes file path |

If probes file missing, naabu logs warning and skips version detection.

## Service discovery only (`-sD`)

Maps port number to service name without active version probe — lighter than `-sV`.

```bash
naabu -host scanme.sh -sD -json
```

## UDP probes (`-uP`)

UDP ports often need protocol-specific payloads:

```bash
naabu -host scanme.sh -p u:53,u:123,u:161 -uP -json
```

- Shares probe database with `-sV`.
- `-cp` custom payload overrides automatic probe for that port.

## External Nmap via `-nmap-cli`

Runs arbitrary Nmap command on discovered host:port set:

```bash
naabu -host hackerone.com -nmap-cli 'nmap -sV -oX nmap-output.xml'
```

**Security note:** naabu executes the provided command — only use trusted Nmap invocations.

Deprecated `-nmap` flag replaced by `-nmap-cli`.

### SpiderFeet pattern

1. **Naabu** `-json` for fast port inventory → nuggets.
2. **Nmap** `-oX` for OS/NSE on high-value hosts (separate skill).

Do not parse Nmap text from `-nmap-cli` stdout — capture `-oX` file.

## Comparison matrix

| Need | Tool / flag |
|------|-------------|
| Fast open port list | `naabu -json` |
| Service name hint | `-sD` |
| Version strings in naabu | `-sV` |
| OS detection | Nmap `-O` via `-nmap-cli` or follow-up scan |
| NSE scripts | Nmap `--script` |
| LLM port hunt | `naabu -p 11434,8000,... -json` → Julius |

## Example combined workflow

```bash
naabu -host 10.0.0.50 -p 22,80,443,8080 -json -o naabu.jsonl
nmap -sV -O -p $(jq -r '.port' naabu.jsonl | paste -sd,) 10.0.0.50 -oX nmap.xml
```

Extract port list programmatically rather than manual paste for large result sets.
