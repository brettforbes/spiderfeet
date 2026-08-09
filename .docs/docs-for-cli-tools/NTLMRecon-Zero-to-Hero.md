# NTLMRecon Zero to Hero — HTTP NTLM Endpoint Discovery

Operator guide from install through JSON capture, parsing NTLM challenge metadata, pipeline tactics, and SpiderFeet nugget mapping.

## 0. What NTLMRecon does

**NTLMRecon** ([praetorian-inc/NTLMRecon](https://github.com/praetorian-inc/NTLMRecon), Go) brute-forces common **HTTP(S) application paths** on a target URL and identifies endpoints that offer **NTLM authentication**. For each hit it sends an unauthenticated NTLM negotiate request and parses the **CHALLENGE_MESSAGE** to extract:

- NetBIOS computer and domain names  
- DNS computer name (FQDN)  
- DNS domain and forest names  

No credentials required. Typical targets: **Exchange autodiscover**, **ADFS**, **OWA**, **EWS**, **Rpc** — web surfaces that expose Windows AD identity metadata via HTTP NTLMSSP.

**Not SMB.** This tool does not speak the SMB protocol. Challenge fields describe Active Directory names leaked over **HTTP**, not SMB share or signing state.

**SpiderFeet uses:** `NTLMRecon -t <url> -o json` → structured JSON lines → `INTERNET_NAME` / `DOMAIN_NAME` / `LINKED_URL_INTERNAL` nuggets.

**Not** the Python `ntlmrecon` fork ([pwnfoo/NTLMRecon](https://github.com/pwnfoo/NTLMRecon)) — different flags and CSV output (skill `references/python-fork.md`).

## 1. Install

### Local SpiderFeet binary (authoritative on this host)

```bash
# WSL
/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon --help

# Windows path to the same file
# C:\projects\spiderfeet\.tools\NTLMRecon\NTLMRecon
```

### Go install (Linux / macOS / WSL)

```bash
go install github.com/praetorian-inc/NTLMRecon/cmd/NTLMRecon@latest
~/go/bin/NTLMRecon --help
```

### Prebuilt release

Download from [GitHub releases](https://github.com/praetorian-inc/NTLMRecon/releases), extract, `chmod +x`, then run `--help`.

### Windows native

No Windows release asset in the common v1.1.0 linux build — use **WSL** with the linux_amd64 binary or Go install inside WSL.

### Verify

```bash
wsl bash -lc "/mnt/c/projects/spiderfeet/.tools/NTLMRecon/NTLMRecon --help"
```

Captured help: `.docs/docs-for-cli-tools/NTLMRecon-CLI-Options.md` (date **2026-08-10**).

## 2. First scan

```bash
NTLMRecon -t https://autodiscover.contoso.com
```

Plaintext — one URL per discovered NTLM path:

```text
https://autodiscover.contoso.com/EWS/
https://autodiscover.contoso.com/OAB/
```

Structured pass (SpiderFeet default):

```bash
NTLMRecon -t https://autodiscover.contoso.com -o json
```

Example line (from upstream README):

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

**Clean miss:** empty stdout when no paths offer NTLM — valid outcome.

## 3. Essential flags

| Flag | Purpose |
|------|---------|
| `-t URL` | **Required** — base URL with `http://` or `https://` |
| `-o json` | JSON metadata per hit (**SpiderFeet / corpus**) |
| `-o plaintext` | URL list only (default) |

The captured binary exposes **only** `-t` and `-o`. README/main may document `-H` / `-debug` — build from source and verify before relying on them.

Full reference: `.docs/docs-for-cli-tools/NTLMRecon-CLI-Options.md`

## 4. Understand results

| Field | Meaning | Typical nugget |
|-------|---------|----------------|
| `url` | Exact path that returned NTLM | `LINKED_URL_INTERNAL` (+ host → `INTERNET_NAME`) |
| `netbiosComputerName` | Short server name | `RAW_RIR_DATA` |
| `netbiosDomainName` | NetBIOS domain | `DOMAIN_NAME` |
| `dnsComputerName` | FQDN of server | `INTERNET_NAME` |
| `dnsDomainName` | DNS domain | `DOMAIN_NAME` |
| `forestName` | AD forest / DNS tree | `DOMAIN_NAME` |

High-value paths: `/EWS/`, `/adfs/services/trust/…/windowstransport`, `/Microsoft-Server-ActiveSync/`.

## 5. Bulk scanning

The Go binary accepts **one URL per run**. Loop externally:

```bash
while read -r url; do
  echo "=== $url ==="
  NTLMRecon -t "$url" -o json
done < live_urls.txt
```

Generate `live_urls.txt` from httpx:

```bash
httpx -l hosts.txt -silent -json | jq -r '.url' > live_urls.txt
```

Do **not** invent `--input` / `--threads` on this binary. For native CIDR/file/threading, the Python fork is a different tool — see skill `references/python-fork.md`. Prefer Go JSON for SpiderFeet corpus.

## 6. Parse in Python

```python
import json
import subprocess

def ntlmrecon_scan(base_url: str, binary: str = "NTLMRecon") -> list[dict]:
    r = subprocess.run(
        [binary, "-t", base_url, "-o", "json"],
        capture_output=True, text=True, timeout=600,
    )
    records = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records

def domains_from_records(records: list[dict]) -> set[str]:
    out = set()
    for row in records:
        ntlm = row.get("ntlm") or {}
        for key in ("dnsDomainName", "forestName", "netbiosDomainName"):
            v = ntlm.get(key)
            if v:
                out.add(v.lower())
    return out
```

## 7. SpiderFeet integration

```
INTERNET_NAME (seed URL/host)
  → NTLMRecon -t https://<host> -o json
  → DOMAIN_NAME, INTERNET_NAME (dnsComputerName), LINKED_URL_INTERNAL
```

Capture family: **structured-native** (JSON lines → bundle `records[]`).  
Skill: `.cursor/skills/NTLMRecon/SKILL.md`  
Mapping: `.cursor/skills/NTLMRecon/references/nugget-mapping.md`

## 8. Operational pipeline

```
PIUS / subfinder → INTERNET_NAME list
    → httpx (live URL confirmation)
    → NTLMRecon -o json (per URL)
    → dnsx (validate dnsDomainName / dnsComputerName)
    → Nuclei (Exchange/ADFS templates on discovered paths)
```

## 9. Safety

Active HTTP probing against NTLM endpoints. Use only on **authorized** targets. Metadata exposure is informational recon — do not conflate with authenticated compromise or SMB access.

## 10. Strategies when yield is thin

| Step | Action |
|------|--------|
| 1 | Confirm URL live with httpx |
| 2 | Try `http://` and `https://` variants |
| 3 | Scan `adfs.`, `autodiscover.`, `mail.`, `owa.` subdomains |
| 4 | Prefer FQDN over IP; use main-branch `-H` only when verified |
| 5 | Use `-debug` (main, if built) to see per-path auth headers |

See `.cursor/skills/NTLMRecon/references/tactics.md`.

## 11. Skill reference

`.cursor/skills/NTLMRecon/SKILL.md` and `references/` directory (index: `references/SKILLS.md`).
