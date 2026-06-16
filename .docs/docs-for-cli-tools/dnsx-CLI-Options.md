# dnsx CLI Options

Quick operator reference for `dnsx` option classes and practical command shapes.

## Standard option classes

| Class | Typical options | Notes |
|---|---|---|
| Input | `-l`, `-d`, stdin | Host/domain sources |
| Quiet mode | `-silent` | Cleaner automation output |
| JSON output | `-j` | Best for parsers |
| Basic records | `-a`, `-aaaa` | Core liveness resolution |
| Alias/authority | `-cname`, `-ns`, `-soa` | Ownership and delegation context |
| Mail/security | `-mx`, `-txt` | Mail route/policy clues |

## Advanced option classes

| Class | Typical options | Usage |
|---|---|---|
| Reverse DNS | `-ptr` | IP to hostname pivoting |
| Service records | `-srv` | Service discovery signals |
| Resolver selection | `-r` | Trusted/public resolver control |
| Wildcard controls | wildcard filter flags | Reduce false positives |
| Concurrency/retry | thread/retry flags | Tune for stability and speed |
| Brute force | domain + wordlist flags | Enumerate extra subdomains |

## Examples by major class

```bash
# Standard A/AAAA validation
dnsx -silent -l hosts.txt -a -aaaa -j

# Alias + mail enrichment
dnsx -silent -l hosts.txt -cname -mx -txt -j

# Resolver-controlled validation
dnsx -silent -l hosts.txt -a -r resolvers.txt -j

# Brute-force discovery
dnsx -silent -d example.com -w subdomains.txt -a -j

# Reverse DNS pivot
dnsx -silent -l ips.txt -ptr -j
```

## Parsing reminder

For automation, parse JSON lines and convert to SpiderFeet graph payloads:
- `nodes[]` for `INTERNET_NAME` and `IP_ADDRESS`
- `edges[]` for `resolves_to`, `cname_to`, `mx_to`, `ns_to`

See `.cursor/skills/dnsx/references/nugget-mapping.md`.
