# tldfinder CLI Options

Evidence: **tldfinder v0.0.2** — `C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe`  
Captured: **2026-08-10** from `.tmp_tldfinder_help/help_long.txt`  
Prefer JSONL: `-oJ` / `-json`

```
A streamlined tool for discovering private TLDs for security research.

Usage:
  C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe [flags]

Flags:
INPUT:
   -d, -domain string[]  domain or list of domains for discovery (file or comma separated)

SOURCE:
   -s, -sources string[]           specific sources to use for discovery (-s censys,dnsrepo). Use -ls to display all available sources.
   -es, -exclude-sources string[]  sources to exclude from enumeration (-es censys,dnsrepo)
   -dm, -discovery-mode value      discovery mode (dns,tld,domain) (default dns)
   -all                            use all sources for enumeration (slow)

FILTER:
   -m, -match string[]   domain or list of domain to match (file or comma separated)
   -f, -filter string[]   domain or list of domain to filter (file or comma separated)

RATE-LIMIT:
   -rl, -rate-limit int      maximum number of http requests to send per second (global)
   -rls, -rate-limits value  maximum number of http requests to send per second four providers in key=value format (-rls hackertarget=10/m) (default ["waybackarchive=15/m", "whoisxmlapi=50/s", "whoisxmlapi=30/s"])
   -t int                    number of concurrent goroutines for resolving (-active only) (default 10)

UPDATE:
   -up, -update                 update tldfinder to latest version
   -duc, -disable-update-check  disable automatic tldfinder update check

OUTPUT:
   -o, -output string       file to write output to
   -oJ, -json               write output in JSONL(ines) format
   -oD, -output-dir string  directory to write output (-dL only)
   -cs, -collect-sources    include all sources in the output (-json only)
   -oI, -ip                 include host IP in output (-active only)

CONFIGURATION:
   -config string                flag config file (default "C:\\Users\\brett\\AppData\\Roaming\\tldfinder\\config.yaml")
   -pc, -provider-config string  provider config file (default "C:\\Users\\brett\\AppData\\Roaming\\tldfinder\\provider-config.yaml")
   -r string[]                   comma separated list of resolvers to use
   -rL, -rlist string            file containing list of resolvers to use
   -nW, -active                  display active domains only
   -proxy string                 http proxy to use with tldfinder
   -ei, -exclude-ip              exclude IPs from the list of domains

DEBUG:
   -silent             show only domains in output
   -version            show version of tldfinder
   -v                  show verbose output
   -nc, -no-color      disable color in output
   -ls, -list-sources  list all available sources
   -stats              report source statistics

OPTIMIZATION:
   -timeout int   seconds to wait before timing out (default 30)
   -max-time int  minutes to wait for enumeration results (default 10)
```

## Sources (`tldfinder -ls`, v0.0.2)

Sources marked `*` need keys/tokens in `provider-config.yaml`:

- censys *
- dnsx
- whoisxmlapi *
- crtsh
- whoxy *
- bufferover *
- dnsrepo *
- netlas *
- waybackarchive

## Notes

- Input is a **private TLD** label (e.g. `google`) or a name under one; see README.
- Prefer `-oJ` for automation and SpiderFeet corpus harvest.
- `-oD` help mentions `-dL`; v0.0.2 INPUT documents only `-d` (file or comma-separated) — do not invent `-dL` unless your binary lists it.
- Skill: `.cursor/skills/tldfinder/SKILL.md`
