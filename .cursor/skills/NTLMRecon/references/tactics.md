# NTLMRecon Strategies and Tactics

## Workflow sequence

1. **Confirm live web surface** — `httpx -silent` on candidate hostnames (`autodiscover`, `mail`, `adfs`, `owa`).
2. **NTLM JSON pass** — `NTLMRecon -t <base-url> -o json` per live URL.
3. **Triage high-value paths** — prioritize `/EWS/`, ADFS trust endpoints, `/Microsoft-Server-ActiveSync/`, `/Rpc/`.
4. **Correlate metadata** — map `forestName` / `dnsDomainName` to `DOMAIN_NAME`; validate with dnsx / PIUS org intel.
5. **Dedupe and graph** — one node per unique FQDN/domain; link paths as `LINKED_URL_INTERNAL`.
6. **Escalate within scope** — document MFA-bypass research surfaces (EWS, legacy auth) as findings, not exploits in this skill.

## Target prioritization

| Target class | Why |
|--------------|-----|
| `autodiscover.*` | Exchange/O365 hybrid; rich path wordlist hits |
| `adfs.*` | Federation metadata via NTLM windowstransport paths |
| Legacy Exchange CAS | EWS/OAB/Rpc/OWA paths |
| IP with unknown vhost | Requires main-branch `-H` or httpx vhost discovery first |

## Maximize yield

| Step | Action |
|------|--------|
| 1 | Run httpx on org subdomains; collect `https://` URLs |
| 2 | NTLMRecon JSON on each URL separately (v1.1.0 limitation) |
| 3 | Retry alternate schemes (`http://` vs `https://`) when httpx shows both |
| 4 | Build from main when IP literal needs `-H` mail FQDN |
| 5 | Use `-debug` (main build) when stderr shows brute-force errors but httpx confirms live host |

## Combine with other tools

| Prior tool | Follow-up |
|------------|-----------|
| PIUS / subfinder | Domain list → httpx → NTLMRecon |
| httpx | Supplies canonical `-t` URLs with scheme |
| dnsx | Validate `dnsComputerName` / `dnsDomainName` from challenge |
| Nuclei | Templates tagged NTLM/Exchange/ADFS on discovered URLs |
| nmap `http-ntlm-info` | Single-path alternative; NTLMRecon brute-forces many paths |
| SMB tooling | **Separate lane** — NTLMRecon does not fingerprint SMB |

## Operational cadence

- **Low noise** — sequential requests (Go tool default); no built-in threading in v1.1.0.
- **Re-probe policy** — re-run only when httpx status changes or prior run had transport errors.
- **Clean miss** — record sparse graph; do not treat as tool failure.

## Proven limitations (captured binary)

- No stdin / file batch input — external shell loop required.
- No custom wordlist flag — embedded paths only (see `endpoints-and-behavior.md`).
- No `-H` / `-debug` in release binary — build from main when needed.
- Sequential HTTP only — large path lists are slow on many hosts.
- **HTTP NTLM only** — does not replace SMB/LDAP/Kerberos recon.

## Python fork tactics

When bulk CIDR or `--threads` is required, see [`python-fork.md`](python-fork.md). Prefer Go JSON output for SpiderFeet corpus consistency when both are available. Never pass Python flags to `NTLMRecon`.
