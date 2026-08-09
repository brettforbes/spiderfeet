# NTLMRecon CLI Options

Binary: **`NTLMRecon`** ([praetorian-inc/NTLMRecon](https://github.com/praetorian-inc/NTLMRecon), Go; case-sensitive).

SpiderFeet preferred command:

```bash
NTLMRecon -t https://autodiscover.example.com -o json
```

| Field | Value |
|-------|-------|
| Binary (WSL) | `/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon` |
| Binary (Windows path) | `C:\projects\spiderfeet\.tools\NTLMRecon\NTLMRecon` |
| Capture date | **2026-08-10** |
| Help source | `.tmp_ntlmrecon_help/help.txt` |
| Local README | `.tools/NTLMRecon/README.md` |

> This is the **Praetorian Go** tool (`-t`, `-o`). It is **not** the older Python `pwnfoo/NTLMRecon` (`--input`, `--infile`, …). Do not invent Python flags for this binary.

---

## Captured help

Live help text captured from `/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon` via WSL on **2026-08-10**. Not on Windows PATH, not as a Python module, not in repo `.venv`.

```text
Usage of /mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon:
  -o string
    	the output format of the data plaintext or JSON (default "plaintext")
  -t string
    	the URL of the target to scan
```

### Re-capture

```powershell
New-Item -ItemType Directory -Force -Path .tmp_ntlmrecon_help | Out-Null
wsl bash -lc "/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon --help" | Out-File -Encoding utf8 .tmp_ntlmrecon_help/help.txt
Get-Content .tmp_ntlmrecon_help/help.txt
```

```bash
/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon --help

# After go install (WSL/Linux)
go install github.com/praetorian-inc/NTLMRecon/cmd/NTLMRecon@latest
~/go/bin/NTLMRecon --help
```

---

## Synopsis

```
NTLMRecon -t <url> [-o plaintext|json]
```

## Options reference (captured binary)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-t` | string | *(required)* | Target base URL including scheme (`https://host`) |
| `-o` | string | `plaintext` | Output: `plaintext` (URLs) or `json` (metadata objects) |

Errors when `-t` is missing or malformed, or when `-o` is not `plaintext`/`json`.

## Main-branch flags (README / source — verify before use)

Absent on the captured binary (`-H` → `flag provided but not defined`). May exist when building from **main**:

| Flag | Description |
|------|-------------|
| `-H string` | Set HTTP `Host` header (virtual host / IP literal probing) |
| `-debug` | Verbose per-path probe logging |

```bash
git clone https://github.com/praetorian-inc/NTLMRecon.git
cd NTLMRecon && go build -o NTLMRecon ./cmd/NTLMRecon
./NTLMRecon -t https://192.168.1.100 -H mail.contoso.com -debug -o json
```

## Output modes

| `-o` | stdout | Use case |
|------|--------|----------|
| `plaintext` | One URL per line | Quick manual triage |
| `json` | One JSON object per line | **SpiderFeet structured capture**, graphs, automation |

### JSON object shape

```json
{
  "url": "https://autodiscover.contoso.com/EWS/",
  "ntlm": {
    "netbiosComputerName": "MSEXCH1",
    "netbiosDomainName": "CONTOSO",
    "dnsDomainName": "na.contoso.local",
    "dnsComputerName": "msexch1.na.contoso.local",
    "forestName": "contoso.local"
  }
}
```

## Examples

```bash
# Default — list NTLM URLs
NTLMRecon -t https://autodiscover.contoso.com

# Structured metadata (preferred)
NTLMRecon -t https://autodiscover.contoso.com -o json

# ADFS target
NTLMRecon -t https://adfs.contoso.com -o json

# Invalid output mode
NTLMRecon -t https://example.com -o yaml
# Error output mode should be either plaintext or json
```

## Batch / threading

The captured binary has **no** `-i`, `--input`, `--threads`, or stdin batch flags. Loop in shell:

```bash
while read -r u; do NTLMRecon -t "$u" -o json; done < urls.txt
```

## Legacy Python fork (not this binary)

| Python flag | Go equivalent |
|-------------|---------------|
| `--input` / `-i` | External loop over `-t` |
| `--infile` / `-I` | External loop |
| `--threads` | Not available (sequential) |
| `--outfile` / `-O` | Redirect stdout |
| CSV output | Use `-o json` instead |

## SpiderFeet corpus notes

| Item | Value |
|------|-------|
| Runtime | WSL / Linux |
| Preferred command | `NTLMRecon -t <URL> -o json` |
| Capture family | structured-native (JSON lines → bundle) |
| Text pane | Derived from `records[]` at harvest |
| Nuggets | `INTERNET_NAME`, `DOMAIN_NAME`, `LINKED_URL_INTERNAL`, optional `RAW_RIR_DATA` |

## See also

- `.docs/docs-for-cli-tools/NTLMRecon-Zero-to-Hero.md`
- `.cursor/skills/NTLMRecon/SKILL.md`
- `.cursor/skills/NTLMRecon/references/cli-options.md`
- Upstream: https://github.com/praetorian-inc/NTLMRecon/blob/main/README.md
