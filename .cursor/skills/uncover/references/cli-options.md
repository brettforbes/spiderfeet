# uncover CLI Options

Grouped flag reference from live help for **uncover v1.2.1** (`C:\projects\spiderfeet\.tools\uncover\uncover.exe`, captured **2026-08-10**). Run `uncover -h` on your install to confirm. **Do not invent flags.**

Full exact help text: `.docs/docs-for-cli-tools/uncover-CLI-Options.md` → **Captured help**.

SpiderFeet preferred:

```bash
uncover -q 'ssl:"Example Org"' -e shodan -json -silent -o uncover.jsonl
echo '1.1.1.1' | uncover -e shodan-idb -json -silent
```

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-query` | `-q` | Search query; supports stdin, file, or config input (e.g. `-q 'example query'`, `-q 'query.txt'`) |
| `-engine` | `-e` | Search engine(s) to query (default **`shodan`**) |
| `-awesome-search-queries` | `-asq` | Use awesome-search-queries packs (e.g. `-asq 'jira'`) |

**Engines allowed by this binary** (from `-e` help):

`shodan`, `shodan-idb`, `fofa`, `censys`, `quake`, `hunter`, `zoomeye`, `netlas`, `publicwww`, `criminalip`, `hunterhow`, `google`, `odin`, `binaryedge`, `onyphe`, `driftnet`, `greynoise`, `daydaymap`, `nerdydata`

```bash
uncover -q 'ssl:"Example Org"' -e shodan -json -silent
uncover -q dorks.txt -e shodan,censys -json -silent
uncover -asq jira -json -silent
```

## SEARCH-ENGINE (per-provider query)

Each flag takes query string(s) or file path(s). Use **provider-native** filter syntax.

| Flag | Short | Engine |
|------|-------|--------|
| `-shodan` | `-s` | shodan |
| `-shodan-idb` | `-sd` | shodan-idb |
| `-fofa` | `-ff` | fofa |
| `-censys` | `-cs` | censys |
| `-quake` | `-qk` | quake |
| `-hunter` | `-ht` | hunter |
| `-zoomeye` | `-ze` | zoomeye |
| `-netlas` | `-ne` | netlas |
| `-criminalip` | `-cl` | criminalip |
| `-publicwww` | `-pw` | publicwww |
| `-hunterhow` | `-hh` | hunterhow |
| `-google` | `-gg` | google |
| `-odin` | `-od` | odin |
| `-binaryedge` | `-be` | binaryedge |
| `-onyphe` | `-on` | onyphe |
| `-driftnet` | `-df` | driftnet |
| `-greynoise` | `-gn` | greynoise |
| `-daydaymap` | `-ddm` | daydaymap |
| `-nerdydata` | `-nd` | NerdyData |

```bash
uncover -shodan 'http.component:"Atlassian Jira"' -fofa 'app="ATLASSIAN-JIRA"' -json -silent
uncover -shodan-idb '1.1.1.1' -json -silent
```

## CONFIG

| Flag | Short | Default (this host) | Description |
|------|-------|---------------------|-------------|
| `-provider` | `-pc` | `%APPDATA%\uncover\provider-config.yaml` | Provider API key file |
| `-config` | — | `%APPDATA%\uncover\config.yaml` | Flag configuration file |
| `-timeout` | — | `30` | Timeout in seconds |
| `-rate-limit` | `-rl` | — | Max HTTP requests per second |
| `-rate-limit-minute` | `-rlm` | — | Max requests per minute |
| `-retry` | — | `2` | Retries on failed request |
| `-proxy` | — | — | HTTP proxy for uncover |

```bash
uncover -q jira -e shodan -json -silent -timeout 60 -retry 3 -rl 1
```

## UPDATE

| Flag | Short | Description |
|------|-------|-------------|
| `-update` | `-up` | Update uncover to latest version |
| `-disable-update-check` | `-duc` | Disable automatic update check |

## OUTPUT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-output` | `-o` | — | Write results to file |
| `-field` | `-f` | `ip:port` | Fields to display: `ip`, `port`, `host` (also used as template tokens in custom formats) |
| `-json` | `-j` | — | **JSONL** (SpiderFeet preferred) |
| `-raw` | `-r` | — | Raw remote API payload |
| `-limit` | `-l` | `100` | Max results to return |
| `-no-color` | `-nc` | — | Disable colors |

```bash
uncover -q jira -json -silent -o uncover.jsonl
uncover -q jira -f host -silent
uncover -q jira -f https://ip:port -silent
uncover -q jira -json -l 50 -silent
```

## DEBUG

| Flag | Description |
|------|-------------|
| `-silent` | Show only results |
| `-version` | Show version |
| `-v` | Verbose output |

**Do not combine `-silent` and `-v`** — process exits with `both verbose and silent mode specified`.

```bash
uncover -version
uncover -q jira -e shodan -json -silent
uncover -q jira -e shodan -json -v
```

## Behavioral notes (from upstream README + live binary)

- Default engine **`shodan`** for search queries; **`shodan-idb`** when input is **IP/CIDR**.
- **`shodan-idb`** requires **no API key**.
- Most other engines require keys in `-pc` / environment (see `sources.md`).
- Query filters are those supported by the chosen search engine only.
- `-field` can embed `ip` / `port` / `host` tokens inside a larger string (e.g. `https://ip:port/version`) for pipeline shaping.
