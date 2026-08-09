# uncover CLI Options

Operator reference for **ProjectDiscovery uncover**. Prefer **`-json` / `-j` (JSONL)** for SpiderFeet corpus and automation.

| Field | Value |
|-------|-------|
| Windows binary | `C:\projects\spiderfeet\.tools\uncover\uncover.exe` |
| Version | **v1.2.1** |
| Capture date | **2026-08-10** |
| Help source | `.tmp_uncover_help/help_h.txt`, `help_long.txt`, `version.txt` |

> Flags below are from live `-h` / `-version` only — **do not invent options**.  
> `help_h.txt` and `help_long.txt` are identical for this capture.

Skill: `.cursor/skills/uncover/SKILL.md`

---

## SpiderFeet preferred commands

```bash
uncover -q 'ssl:"Example Org"' -e shodan -json -silent -o uncover.jsonl
echo '1.1.1.1' | uncover -e shodan-idb -json -silent
uncover -q jira -e shodan,censys,fofa -json -silent -l 50
uncover -asq jira -json -silent
```

---

## Captured help

Live help text captured from `C:\projects\spiderfeet\.tools\uncover\uncover.exe` on **2026-08-10**. Each block is the full stdout of the listed command (ANSI sequences retained where present).

### Version (`uncover -version`)

```text
[INF] Current Version: v1.2.1
[INF] Uncover ConfigDir: C:\Users\brett\AppData\Roaming\uncover
```

### Root help (`uncover -h`)

```text
quickly discover exposed assets on the internet using multiple search engines.

Usage:
  C:\projects\spiderfeet\.tools\uncover\uncover.exe [flags]

Flags:
INPUT:
   -q, -query string[]                     search query, supports: stdin,file,config input (example: -q 'example query', -q 'query.txt')
   -e, -engine string[]                    search engine to query (shodan,shodan-idb,fofa,censys,quake,hunter,zoomeye,netlas,publicwww,criminalip,hunterhow,google,odin,binaryedge,onyphe,driftnet,greynoise,daydaymap,nerdydata) (default shodan)
   -asq, -awesome-search-queries string[]  use awesome search queries to discover exposed assets on the internet (example: -asq 'jira')

SEARCH-ENGINE:
   -s, -shodan string[]       search query for shodan (example: -shodan 'query.txt')
   -sd, -shodan-idb string[]  search query for shodan-idb (example: -shodan-idb 'query.txt')
   -ff, -fofa string[]        search query for fofa (example: -fofa 'query.txt')
   -cs, -censys string[]      search query for censys (example: -censys 'query.txt')
   -qk, -quake string[]       search query for quake (example: -quake 'query.txt')
   -ht, -hunter string[]      search query for hunter (example: -hunter 'query.txt')
   -ze, -zoomeye string[]     search query for zoomeye (example: -zoomeye 'query.txt')
   -ne, -netlas string[]      search query for netlas (example: -netlas 'query.txt')
   -cl, -criminalip string[]  search query for criminalip (example: -criminalip 'query.txt')
   -pw, -publicwww string[]   search query for publicwww (example: -publicwww 'query.txt')
   -hh, -hunterhow string[]   search query for hunterhow (example: -hunterhow 'query.txt')
   -gg, -google string[]      search query for google (example: -google 'query.txt')
   -od, -odin string[]        search query for odin (example: -odin 'query.txt')
   -be, -binaryedge string[]  search query for binaryedge (example: -binaryedge 'query.txt')
   -on, -onyphe string[]      search query for onyphe (example: -onyphe 'query.txt')
   -df, -driftnet string[]    search query for driftnet (example: -driftnet 'query.txt')
   -gn, -greynoise string[]   search query for greynoise (example: -greynoise 'query.txt')
   -ddm, -daydaymap string[]  search query for daydaymap (example: -daydaymap 'query.txt')
   -nd, -nerdydata string[]   search query for NerdyData (example: -nerdydata 'query.txt')

CONFIG:
   -pc, -provider string         provider configuration file (default "C:\\Users\\brett\\AppData\\Roaming\\uncover\\provider-config.yaml")
   -config string                flag configuration file (default "C:\\Users\\brett\\AppData\\Roaming\\uncover\\config.yaml")
   -timeout int                  timeout in seconds (default 30)
   -rl, -rate-limit int          maximum number of http requests to send per second
   -rlm, -rate-limit-minute int  maximum number of requests to send per minute
   -retry int                    number of times to retry a failed request (default 2)
   -proxy string                 http proxy to use with uncover

UPDATE:
   -up, -update                 update uncover to latest version
   -duc, -disable-update-check  disable automatic uncover update check

OUTPUT:
   -o, -output string  output file to write found results
   -f, -field string   field to display in output (ip,port,host) (default "ip:port")
   -j, -json           write output in JSONL(ines) format
   -r, -raw            write raw output as received by the remote api
   -l, -limit int      limit the number of results to return (default 100)
   -nc, -no-color      disable colors in output

DEBUG:
   -silent   show only results in output
   -version  show version of the project
   -v        show verbose output
```

---

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-query` | `-q` | Search query (stdin, file, or literal) |
| `-engine` | `-e` | Engine list (default `shodan`) |
| `-awesome-search-queries` | `-asq` | Awesome-search-queries pack name |

```bash
uncover -q 'ssl:"Example Org"' -e shodan -json -silent
uncover -q dorks.txt -json -silent
uncover -asq jira -json -silent
```

---

## SEARCH-ENGINE

| Flag | Short | Description |
|------|-------|-------------|
| `-shodan` | `-s` | Shodan-specific query |
| `-shodan-idb` | `-sd` | Shodan InternetDB query |
| `-fofa` | `-ff` | FOFA-specific query |
| `-censys` | `-cs` | Censys-specific query |
| `-quake` | `-qk` | Quake-specific query |
| `-hunter` | `-ht` | Hunter-specific query |
| `-zoomeye` | `-ze` | ZoomEye-specific query |
| `-netlas` | `-ne` | Netlas-specific query |
| `-criminalip` | `-cl` | CriminalIP-specific query |
| `-publicwww` | `-pw` | PublicWWW-specific query |
| `-hunterhow` | `-hh` | HunterHow-specific query |
| `-google` | `-gg` | Google-specific query |
| `-odin` | `-od` | Odin-specific query |
| `-binaryedge` | `-be` | BinaryEdge-specific query |
| `-onyphe` | `-on` | Onyphe-specific query |
| `-driftnet` | `-df` | Driftnet-specific query |
| `-greynoise` | `-gn` | GreyNoise-specific query |
| `-daydaymap` | `-ddm` | DayDayMap-specific query |
| `-nerdydata` | `-nd` | NerdyData-specific query |

```bash
uncover -shodan 'http.component:"Atlassian Jira"' -fofa 'app="ATLASSIAN-JIRA"' -json -silent
```

---

## CONFIG

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-provider` | `-pc` | `%APPDATA%\uncover\provider-config.yaml` | API key file |
| `-config` | — | `%APPDATA%\uncover\config.yaml` | Flag config file |
| `-timeout` | — | `30` | Seconds |
| `-rate-limit` | `-rl` | — | Requests/second |
| `-rate-limit-minute` | `-rlm` | — | Requests/minute |
| `-retry` | — | `2` | Retries |
| `-proxy` | — | — | HTTP proxy |

```bash
uncover -q jira -e shodan -json -silent -timeout 60 -retry 3 -rl 1
```

---

## UPDATE

| Flag | Short | Description |
|------|-------|-------------|
| `-update` | `-up` | Update uncover |
| `-disable-update-check` | `-duc` | Disable update check |

---

## OUTPUT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-output` | `-o` | — | Output file |
| `-field` | `-f` | `ip:port` | Display fields / template tokens (`ip`, `port`, `host`) |
| `-json` | `-j` | — | **JSONL** (SpiderFeet preferred) |
| `-raw` | `-r` | — | Raw remote API body |
| `-limit` | `-l` | `100` | Max results |
| `-no-color` | `-nc` | — | Disable colors |

```bash
uncover -q jira -json -silent -o uncover.jsonl
uncover -q jira -f host -silent
uncover -q jira -f https://ip:port -silent
```

---

## DEBUG

| Flag | Description |
|------|-------------|
| `-silent` | Results only |
| `-version` | Print version |
| `-v` | Verbose |

Do **not** combine `-silent` and `-v`.

---

## Behavioral notes

- Default engine for search strings: **`shodan`**.
- Default engine for **IP/CIDR** input: **`shodan-idb`** (no API key).
- Query language is provider-specific.
- Multiple API keys in `provider-config.yaml` are randomized per run (upstream README).
- Formal SpiderFeet examination uses `-json` only; derive human text from structured records.
