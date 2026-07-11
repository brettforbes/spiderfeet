# Subfinder CLI Options

Grouped flag reference from Subfinder v2.x (ProjectDiscovery). Run `subfinder -h` on your install to confirm.

## INPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-domain` | `-d` | Domain(s) to enumerate (repeatable) |
| `-list` | `-dL` | File with one domain per line |

```bash
subfinder -d example.com
subfinder -d example.com,example.org
subfinder -dL domains.txt
echo example.com | subfinder
```

## SOURCE

| Flag | Short | Description |
|------|-------|-------------|
| `-sources` | `-s` | Comma-separated passive sources to use |
| `-recursive` | — | Only sources supporting recursive enumeration |
| `-all` | — | All sources (slow) |
| `-exclude-sources` | `-es` | Sources to skip |
| `-list-sources` | `-ls` | List available sources |

```bash
subfinder -ls
subfinder -d example.com -s crtsh,hackertarget
subfinder -d example.com -recursive
subfinder -d example.com -all
subfinder -d example.com -es alienvault,zoomeyeapi
```

## FILTER

| Flag | Short | Description |
|------|-------|-------------|
| `-match` | `-m` | Keep subdomains matching string(s) or file |
| `-filter` | `-f` | Remove subdomains matching string(s) or file |

```bash
subfinder -d example.com -m api,staging
subfinder -d example.com -f test,dev
subfinder -d example.com -m keywords.txt
```

## RATE-LIMIT

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-rate-limit` | `-rl` | — | Max HTTP requests per second (global) |
| `-rls` | — | — | Per-provider limits, e.g. `hackertarget=10/s` |
| `-t` | — | 10 | Concurrent resolver goroutines (**active** mode) |

```bash
subfinder -d example.com -rl 10
subfinder -d example.com -rls "hackertarget=10/s,shodan=15/s"
subfinder -d example.com -active -t 25
```

## OUTPUT

| Flag | Short | Description |
|------|-------|-------------|
| `-output` | `-o` | Write results to file |
| `-json` | `-oJ` | JSON Lines format |
| `-output-dir` | `-oD` | Output directory per domain (`-dL`) |
| `-collect-sources` | `-cs` | Include source list per host (JSON only) |
| `-ip` | `-oI` | Include resolved IP (**requires `-active`**) |

```bash
subfinder -d example.com -o subs.txt
subfinder -d example.com -oJ -o subs.jsonl
subfinder -d example.com -oJ -cs -o subs.jsonl
subfinder -d example.com -active -oJ -oI -o live.jsonl
subfinder -dL domains.txt -oD ./out/
subfinder -d example.com -silent
```

## CONFIGURATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-config` | — | `$CONFIG/subfinder/config.yaml` | Main config file |
| `-provider-config` | `-pc` | `$CONFIG/subfinder/provider-config.yaml` | API keys per source |
| `-resolvers` | `-r` | — | Comma-separated DNS resolvers |
| `-rlist` | `-rL` | — | Resolver list file |
| `-active` | `-nW` | — | Active mode: resolve subdomains |
| `-proxy` | — | — | HTTP proxy for API requests |
| `-exclude-ip` | `-ei` | — | Exclude IPs from domain list output |

```bash
subfinder -d example.com -pc ~/.config/subfinder/provider-config.yaml
subfinder -d example.com -active -r 8.8.8.8,1.1.1.1
subfinder -d example.com -proxy http://127.0.0.1:8080
```

## DEBUG / META

| Flag | Short | Description |
|------|-------|-------------|
| `-silent` | — | Subdomains only (pipe-friendly) |
| `-verbose` | `-v` | Verbose logging |
| `-no-color` | `-nc` | Disable ANSI colors |
| `-version` | — | Print version |
| `-update` | `-up` | Update binary |
| `-disable-update-check` | `-duc` | Skip update check |

## OPTIMIZATION

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `-timeout` | — | 30 | Per-request timeout (seconds) |
| `-max-time` | — | 10 | Max minutes for enumeration |

```bash
subfinder -d example.com -timeout 60 -max-time 30 -v
```

## Common combinations

| Goal | Command |
|------|---------|
| Pipe to httpx | `subfinder -d example.com -silent \| httpx -silent` |
| Corpus JSONL | `subfinder -d example.com -oJ -cs -o out.jsonl` |
| Live hosts + IP JSON | `subfinder -d example.com -active -oJ -oI -o live.jsonl` |
| Batch export | `subfinder -dL domains.txt -oD ./subs/` |
