# tldfinder CLI Options

Grouped flag reference from **tldfinder v0.0.2** (`tldfinder -h`, captured **2026-08-10**). Re-run `-h` on your install before assuming new switches.

Local binary: `C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe`

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-domain` | `-d` | Domain or list of domains for discovery (**file or comma separated**) |

```bash
tldfinder -d google
tldfinder -d google,internal
tldfinder -d seeds.txt
```

> **Input class:** Private TLD label (e.g. `google`) or a name under a private TLD (e.g. `example.google`). Not a public apex like `example.com`.

> **Note on `-dL` / `-oD`:** Help text for `-oD` says “`-dL` only”, but v0.0.2 INPUT lists only `-d`. Do not invent `-dL` unless your binary’s help shows it. Prefer `-d file.txt -o out.txt` / `-oJ -o out.jsonl`.

## SOURCE

| Flag | Short | Description |
|------|-------|-------------|
| `-sources` | `-s` | Specific sources (`-s censys,dnsrepo`). Use `-ls` to list. |
| `-exclude-sources` | `-es` | Sources to skip |
| `-discovery-mode` | `-dm` | `dns`, `tld`, or `domain` (default **`dns`**) |
| `-all` | — | Use all sources (slow) |
| `-list-sources` | `-ls` | List available sources |

```bash
tldfinder -ls
tldfinder -d google -dm dns
tldfinder -d google -dm tld
tldfinder -d google -s crtsh,dnsx,waybackarchive
tldfinder -d google -all
tldfinder -d google -es censys,whoisxmlapi
```

### Sources observed via `-ls` (v0.0.2)

| Source | Needs key (`*`) |
|--------|-----------------|
| censys | yes |
| dnsx | no |
| whoisxmlapi | yes |
| crtsh | no |
| whoxy | yes |
| bufferover | yes |
| dnsrepo | yes |
| netlas | yes |
| waybackarchive | no |

Keys live in `provider-config.yaml` (see CONFIGURATION).

## FILTER

| Flag | Short | Description |
|------|-------|-------------|
| `-match` | `-m` | Keep domains matching string(s) or file |
| `-filter` | `-f` | Remove domains matching string(s) or file |

```bash
tldfinder -d google -m corp,sandbox
tldfinder -d google -f test,qa
tldfinder -d google -m keywords.txt
```

## RATE-LIMIT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-rate-limit` | `-rl` | — | Max HTTP requests per second (global) |
| `-rate-limits` | `-rls` | waybackarchive / whoisxmlapi defaults | Per-provider limits, e.g. `hackertarget=10/m` |
| `-t` | — | 10 | Concurrent resolver goroutines (**`-active` only**) |

```bash
tldfinder -d google -rl 10
tldfinder -d google -rls "waybackarchive=15/m,whoisxmlapi=30/s"
tldfinder -d google -active -t 25
```

## UPDATE

| Flag | Short | Description |
|------|-------|-------------|
| `-update` | `-up` | Update tldfinder to latest version |
| `-disable-update-check` | `-duc` | Disable automatic update check |

```bash
tldfinder -d google -duc -oJ -o out.jsonl
```

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | File to write output to |
| `-json` | `-oJ` | Write **JSONL(ines)** |
| `-output-dir` | `-oD` | Directory to write output (help: `-dL` only — see INPUT note) |
| `-collect-sources` | `-cs` | Include all sources in output (**`-json` only**) |
| `-ip` | `-oI` | Include host IP (**`-active` only**) |

```bash
tldfinder -d google -o hosts.txt
tldfinder -d google -oJ -o hosts.jsonl
tldfinder -d google -oJ -cs -o hosts.jsonl
tldfinder -d google -active -oJ -oI -o live.jsonl
tldfinder -d google -silent
```

**Prefer `-oJ` for SpiderFeet formal examination and automation.**

## CONFIGURATION

| Flag | Short | Default (Windows evidence) | Description |
|------|-------|----------------------------|-------------|
| `-config` | — | `%APPDATA%\tldfinder\config.yaml` | Flag config file |
| `-provider-config` | `-pc` | `%APPDATA%\tldfinder\provider-config.yaml` | API keys / tokens |
| `-r` | — | — | Comma-separated resolvers |
| `-rlist` | `-rL` | — | Resolver list file |
| `-active` | `-nW` | — | Display active domains only |
| `-proxy` | — | — | HTTP proxy |
| `-exclude-ip` | `-ei` | — | Exclude IPs from domain list |

```bash
tldfinder -d google -pc "%APPDATA%\tldfinder\provider-config.yaml"
tldfinder -d google -active -r 8.8.8.8,1.1.1.1
tldfinder -d google -proxy http://127.0.0.1:8080
```

## DEBUG

| Flag | Short | Description |
|------|-------|-------------|
| `-silent` | — | Show only domains (pipe-friendly) |
| `-version` | — | Show version |
| `-v` | — | Verbose output |
| `-no-color` | `-nc` | Disable color |
| `-list-sources` | `-ls` | List sources |
| `-stats` | — | Report source statistics |

```bash
tldfinder -version
tldfinder -d google -v -stats
```

## OPTIMIZATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-timeout` | — | 30 | Seconds before timing out |
| `-max-time` | — | 10 | Minutes to wait for enumeration results |

```bash
tldfinder -d google -timeout 60 -max-time 30 -oJ -o out.jsonl
```

## Full help text (v0.0.2)

Canonical capture: `.tmp_tldfinder_help/help_long.txt`.
