# NTLMRecon Output Schema

## Capture families

| Mode | Flag | Artifact | SpiderFeet role |
|------|------|----------|-----------------|
| Structured-native | `-o json` | One JSON object per stdout line | **Primary** — graph and narrative source |
| Text-native | `-o plaintext` (default) | One URL per line | Human review; derive structured via parser only if JSON unavailable |

Formal examination must use **`-o json`**.

## JSON schema (praetorian-inc)

Each successful endpoint emits one line:

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

| JSON path | NTLMSSP AV pair | Meaning |
|-----------|-----------------|---------|
| `url` | — | Full URL of the NTLM-enabled path |
| `ntlm.netbiosComputerName` | MsvAvNbComputerName | NetBIOS computer name |
| `ntlm.netbiosDomainName` | MsvAvNbDomainName | NetBIOS domain name |
| `ntlm.dnsDomainName` | MsvAvDnsDomainName | DNS domain name |
| `ntlm.dnsComputerName` | MsvAvDnsComputerName | DNS FQDN of computer |
| `ntlm.forestName` | MsvAvDnsTreeName | AD forest / DNS tree name |

Source: `pkg/structs/structs.go` in praetorian-inc/NTLMRecon. Example matches upstream README.

## Plaintext schema

Default output — no metadata, only URLs:

```text
https://autodiscover.contoso.com/Autodiscover
https://autodiscover.contoso.com/EWS/
https://autodiscover.contoso.com/OAB/
https://autodiscover.contoso.com/Rpc/
```

## Collapsed wildcard output

When **every** embedded path returns NTLM metadata, the tool may emit a single synthetic URL:

```json
{"url":"https://autodiscover.contoso.com/*","ntlm":{...}}
```

Treat as “NTLM broadly enabled on host” rather than a literal path.

## Clean miss

- **stdout**: empty
- **exit code**: typically 0 even when brute-force errors are printed to stderr
- Valid structured bundle: `records: []` with scan metadata (command, target, timestamp)

## stderr shapes

| Message | Meaning |
|---------|---------|
| `Error a target URL must be provided` | Missing `-t` |
| `Error the specific target URL (...) must be a valid URL` | Malformed `-t` |
| `Error output mode should be either plaintext or json` | Invalid `-o` |
| `Error brute-forcing NTLM authentication endpoints (error: ...)` | Probe failure (empty wordlist, network, etc.) |

Capture stderr in examination bundles alongside stdout.

## SpiderFeet structured bundle (recommended)

For CLI corpus / harvest adapters, wrap JSONL stdout into a **single JSON root** (not raw `.jsonl` as the Structured pane file):

```json
{
  "schema": "ntlmrecon_finding_v1",
  "tool": "NTLMRecon",
  "command": "NTLMRecon -t https://autodiscover.contoso.com -o json",
  "record_count": 2,
  "records": [
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
  ]
}
```

Derive Text pane lines as: `{url} → {dnsComputerName} ({netbiosDomainName})`.

## Parsing workflow

1. Run with `-o json`; capture full stdout (line-delimited JSON).
2. Filter empty lines; parse each line with `json.loads`.
3. Normalize hostnames to lowercase for deduplication keys.
4. Deduplicate by `(url, netbiosComputerName, dnsDomainName)` tuple.
5. Classify IP literals in URLs via `core.ip_classify.classify_ip` when building graphs.

## Python fork CSV (legacy)

pwnfoo `ntlmrecon` writes CSV columns:

`URL, AD Domain Name, Server Name, DNS Domain Name, FQDN, Parent DNS Domain`

Map to the same semantic fields when ingesting legacy output — see [`python-fork.md`](python-fork.md). Do not treat those CLI flags as available on the Go binary.
