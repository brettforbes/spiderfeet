# dnsx CLI Options

Use `dnsx -h` to verify your installed version's exact flag set.

## Core input and execution

| Option class | Common flags | Usage |
|---|---|---|
| Target input | `-l`, `-d`, stdin | Read hostnames/domain inputs |
| Quiet automation | `-silent` | Machine-friendly output without banners |
| Concurrency | thread/retry/rate flags | Control throughput and resolver pressure |
| Resolver control | `-r` | Use curated resolver lists |

### Example - list validation pass

```bash
dnsx -silent -l hosts.txt -a -resp -j
```

## Record query classes

| Class | Typical flags | Why |
|---|---|---|
| Address | `-a`, `-aaaa` | Resolve IPv4/IPv6 service endpoints |
| Alias | `-cname` | Discover platform/CDN indirection |
| Mail | `-mx`, `-txt` | Mail routing and policy intelligence |
| Authority | `-ns`, `-soa` | Zone ownership and DNS hosting context |
| Reverse | `-ptr` | Convert discovered IPs to hostnames |
| Service | `-srv` | Discover service-specific DNS entries |

### Example - full enrichment set

```bash
dnsx -silent -l hosts.txt -a -aaaa -cname -mx -txt -ns -j
```

## Brute-force and discovery classes

| Class | Typical flags | Why |
|---|---|---|
| Subdomain brute force | domain + wordlist flags | Enumerate additional candidate names |
| Wildcard handling | wildcard filter/threshold flags | Suppress synthetic wildcard hits |
| Recursive workflows | pipeline with subfinder/amass outputs | Expand coverage iteratively |

### Example - brute force mode

```bash
dnsx -silent -d example.com -w subdomains.txt -a -resp -j
```

## Output classes

| Class | Typical flags | Why |
|---|---|---|
| JSON/JSONL | `-j` | Stable parsing for agents and pipelines |
| Response text | `-resp` | Preserve resolver answer context |
| Raw/verbose | verbose flags | Debug transient resolver behavior |

### Example - parser-safe JSON

```bash
dnsx -silent -l hosts.txt -a -aaaa -cname -j > dnsx.jsonl
```

## Workflow examples by major option class

```bash
# A/AAAA only quick liveness
dnsx -silent -l hosts.txt -a -aaaa -j

# Mail posture focus
dnsx -silent -l hosts.txt -mx -txt -j

# CNAME pivot extraction
dnsx -silent -l hosts.txt -cname -j

# Resolver differential check
dnsx -silent -l hosts.txt -a -r resolvers-public.txt -j
dnsx -silent -l hosts.txt -a -r resolvers-trusted.txt -j
```
