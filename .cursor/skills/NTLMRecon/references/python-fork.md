# NTLMRecon — Python Fork (pwnfoo)

**Not the SpiderFeet canonical tool.** Documented only so operators do not confuse CLIs.

| | Praetorian Go (canonical) | pwnfoo Python |
|---|---------------|---------------|
| Binary | `NTLMRecon` | `ntlmrecon` |
| Install | `go install …/cmd/NTLMRecon@latest` or release binary | `python setup.py install` |
| Input | `-t` single URL | `--input` / `--infile` URL, IP, CIDR |
| Output | stdout plaintext or JSON lines | CSV file (`--outfile`) |
| Threads | Sequential (captured binary) | `--threads` (default 10) |
| JSON output | `-o json` | `--output-type` JSON often marked TODO in older docs |

**Do not** invent or apply Python flags (`--input`, `--infile`, `--threads`, `--outfile`, `--wordlist`) against the Praetorian Go binary at `.tools/NTLMRecon/NTLMRecon`.

## Python help (ecosystem reference only)

From [OffSec KB](https://kb.offsec.nl/tools/other/ntlmrecon/) — verify locally with `ntlmrecon --help` when the Python package is installed:

```text
optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Pass input as an IP address, URL or CIDR to enumerate NTLM endpoints
  --infile INFILE, -I INFILE
                        Pass input from a local file
  --wordlist WORDLIST   Override the internal wordlist with a custom wordlist
  --threads THREADS     Set number of threads (Default: 10)
  --output-type, -o     Set output type. JSON (TODO) and CSV supported (Default: CSV)
  --outfile OUTFILE, -O OUTFILE
                        Set output file name (Default: ntlmrecon.csv)
  --random-user-agent   TODO: Randomize user agents when sending requests (Default: False)
  --force-all           Force enumerate all endpoints even if a valid endpoint is found for a URL
  --shuffle             Break order of the input files
  -f, --force           Force replace output file if it already exists
```

## CSV columns

`URL, AD Domain Name, Server Name, DNS Domain Name, FQDN, Parent DNS Domain`

## When to use Python fork

- CIDR expansion and multi-target files without shell loops.
- Custom wordlists (`--wordlist`).
- CSV export for spreadsheet triage.

## When to use Go tool (SpiderFeet default)

- CLI corpus / structured JSON examination (`-o json`).
- Consistent `ntlmrecon_finding_v1` schema.
- Praetorian-maintained path list and JSON field names.

## Sources

- https://github.com/pwnfoo/NTLMRecon
- https://kb.offsec.nl/tools/other/ntlmrecon/
