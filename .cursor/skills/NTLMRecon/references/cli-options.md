# NTLMRecon CLI Options

Invocation: **`NTLMRecon`** (Praetorian Go binary; case-sensitive).

SpiderFeet formal examination default:

```bash
NTLMRecon -t <URL> -o json
```

Authoritative binary paths:

| Path | Notes |
|------|-------|
| `/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon` | WSL |
| `C:\projects\spiderfeet\.tools\NTLMRecon\NTLMRecon` | Windows view of same file |

## Captured help

Live capture from the Praetorian **linux_amd64** binary at the paths above, executed via WSL on **2026-08-10**. Also saved under `.tmp_ntlmrecon_help/help.txt`. Not on Windows PATH, not in `.venv`, not as a Python module.

```text
Usage of /mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon:
  -o string
    	the output format of the data plaintext or JSON (default "plaintext")
  -t string
    	the URL of the target to scan
```

### Re-capture

```powershell
wsl bash -lc "/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon --help" | Out-File -Encoding utf8 .tmp_ntlmrecon_help/help.txt
```

```bash
/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon --help

# Or after go install
go install github.com/praetorian-inc/NTLMRecon/cmd/NTLMRecon@latest
~/go/bin/NTLMRecon --help
```

## Options reference (v1.1.0 release — this binary)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-t` | string | *(required)* | Base URL to scan (must include `http://` or `https://`) |
| `-o` | string | `plaintext` | Output format: `plaintext` (URLs) or `json` (metadata objects) |

Only these two flags exist on the captured binary. Do not invent Python-fork flags (`--input`, `--infile`, `--threads`, `--outfile`) for this tool.

## Release vs main branch

| Flag | Captured binary | main branch source / README |
|------|-----------------|----------------------------|
| `-t` | Yes | Yes |
| `-o` | Yes | Yes |
| `-H` | **No** — `flag provided but not defined` | Yes — custom Host header |
| `-debug` | **No** | Yes — verbose probe logging |

Build from **main** when `-H` or `-debug` are required:

```bash
git clone https://github.com/praetorian-inc/NTLMRecon.git
cd NTLMRecon && go build -o NTLMRecon ./cmd/NTLMRecon
```

## Output mode behaviour

| `-o` value | stdout shape | SpiderFeet use |
|------------|--------------|----------------|
| `plaintext` | One discovered URL per line | Human review / Text pane derivation |
| `json` | One JSON object per line per hit | **Structured capture** → graph/narrative |

Invalid `-o` values print an error and usage text.

## Examples

```bash
# Discover endpoints (plaintext)
NTLMRecon -t https://autodiscover.contoso.com

# Structured metadata (SpiderFeet)
NTLMRecon -t https://autodiscover.contoso.com -o json

# ADFS
NTLMRecon -t https://adfs.contoso.com -o json

# Missing target
NTLMRecon
# Error a target URL must be provided
```

## Main-branch only (not in captured help)

Documented in upstream README; verify after building from main:

```bash
NTLMRecon -t https://192.168.1.100 -H mail.contoso.com -o json
NTLMRecon -t https://autodiscover.contoso.com -debug -o json
```

## Legacy Python fork (different binary)

The pwnfoo **`ntlmrecon`** CLI uses `--input`, `--infile`, `--threads`, `--outfile` — see [`python-fork.md`](python-fork.md). Do not mix flag names with the Go tool.

## See also

- `.docs/docs-for-cli-tools/NTLMRecon-CLI-Options.md`
- [`output-schema.md`](output-schema.md)
- [`endpoints-and-behavior.md`](endpoints-and-behavior.md)
