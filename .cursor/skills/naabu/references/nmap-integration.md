# Naabu Nmap Integration and Service Detection

Only flags present in **naabu v2.6.1** live help (`-h` captured **2026-08-10**) are documented here. Do not invent `-sV-fast` or other undocumented switches.

## Built-in service version (`-sV`)

```bash
naabu -host scanme.nmap.org -sV -json -silent -duc
```

| Flag | Purpose |
|------|---------|
| `-sV` / `-service-version` | Service version |
| `-sD` / `-service-discovery` | Service discovery |

If version probing depends on local Nmap probe data and it is missing, inspect stderr/verbose output and fall back to external Nmap.

## External Nmap via `-nmap-cli`

Runs an Nmap command on the discovered host:port set:

```bash
naabu -host hackerone.com -nmap-cli "nmap -sV -oX nmap-output.xml" -duc
```

**Security note:** naabu executes the provided command — only use trusted Nmap invocations.

Deprecated `-nmap` flag is replaced by `-nmap-cli` (still listed as Deprecated in help).

### SpiderFeet pattern

1. **Naabu** `-json` for fast port inventory → nuggets.
2. **Nmap** `-oX` for OS/NSE on high-value hosts (separate skill).

Do not parse Nmap text from `-nmap-cli` stdout as the primary structured artifact — capture `-oX` XML.

## Comparison matrix

| Need | Tool / flag |
|------|-------------|
| Fast open port list | `naabu -json` |
| Service discovery hint | `-sD` |
| Version strings in naabu | `-sV` |
| OS detection | Nmap `-O` via `-nmap-cli` or follow-up scan |
| NSE scripts | Nmap `--script` |
| LLM port hunt | `naabu -p 11434,8000,... -json` → Julius |

## Example combined workflow

```bash
naabu -host 10.0.0.50 -p 22,80,443,8080 -json -o naabu.jsonl -duc
nmap -sV -O -p 22,80,443,8080 10.0.0.50 -oX nmap.xml
```

Build the Nmap `-p` list from JSONL programmatically for large result sets:

```bash
jq -r '.port' naabu.jsonl | sort -n | uniq | paste -sd,
```

## CONNECT payloads

Help also exposes `-connect-payload` / `-cp` for optional CONNECT-scan payloads. Use only when exploring CONNECT-specific behavior — keep formal corpus on plain `-json` port hits unless a scenario explicitly needs payloads.
