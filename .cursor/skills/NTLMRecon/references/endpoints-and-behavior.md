# NTLMRecon Endpoints and Behaviour

## What the tool does

1. Parses `-t` as a base URL (`scheme://host`).
2. Iterates an **embedded path wordlist** (~70 entries) from `pkg/paths/paths.txt`.
3. For each path, sends GET without auth; checks `WWW-Authenticate` for `NTLM` or `Negotiate`.
4. Sends minimal NTLM NEGOTIATE packet; parses CHALLENGE_MESSAGE for AV pairs.
5. Emits each hit (plaintext URL or JSON object).

Requests use **HTTP/1.1 only**, short timeouts, **TLS InsecureSkipVerify**, limited redirect handling.

This is **HTTP(S) application-path recon**, not SMB dialect negotiation or share enumeration.

## Embedded path wordlist (main branch)

Representative paths (full list in upstream `pkg/paths/paths.txt`):

| Path | Typical service |
|------|-----------------|
| `/Autodiscover`, `/Autodiscover/Autodiscover.xml` | Exchange autodiscover |
| `/EWS/` | Exchange Web Services |
| `/OAB/` | Offline Address Book |
| `/Microsoft-Server-ActiveSync/` | ActiveSync |
| `/Rpc/`, `/RpcWithCert/` | Outlook RPC |
| `/adfs/ls/wia`, `/adfs/services/trust/2005/windowstransport` | ADFS NTLM |
| `/owa/` | Outlook Web App |
| `/PowerShell/` | Exchange remoting |
| `/CertSrv/`, `/CertEnroll/` | AD CS web enrollment |
| `/meet`, `/dialin` | Skype/Lync/Teams legacy |

## Auth detection logic

- **NTLM/Negotiate offered** → send negotiate blob → decode challenge metadata.
- **Other auth (Basic, Kerberos)** → skipped in Go tool (no output line).
- **No auth header** → path skipped silently.

## Performance characteristics

- **Sequential** — one path at a time per target URL.
- **~70 requests** worst case per `-t` invocation.
- README roadmap mentions concurrency and stdin batch as future work.

## High-value findings (operator context)

Per Praetorian research, exposed NTLM endpoints (especially **EWS**) can support legacy auth paths relevant to MFA bypass research on misconfigured Exchange/ADFS — document as **exposed NTLM surface**, not as automatic compromise.

## Virtual host behaviour

When `-t` uses an IP URL but the server expects a mail/autodiscover hostname, probes may fail until **main-branch `-H`** sets `Host:` header. Always prefer FQDN in `-t` when DNS resolves.
