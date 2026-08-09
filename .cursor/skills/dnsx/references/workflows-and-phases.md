# dnsx Workflows and Phases

## Phase model

| Phase | Tool | Output |
|-------|------|--------|
| A — Names | subfinder, amass, wordlists | Hostname candidates |
| B — **DNS validate** | **dnsx** | Resolvable FQDNs + IPs + record classes |
| C — HTTP probe | httpx | Live URLs + fingerprint JSONL |
| D — Ports | naabu, nmap | Open TCP/UDP ports |
| E — Vuln / depth | nuclei, nerva | Findings / service fingerprints |

dnsx is the **validation and DNS enrichment** gate between passive names and active service scanning.

## Workflow 1 — Classic recon chain

```bash
subfinder -d example.com -silent | dnsx -silent -a -aaaa -json -o live.jsonl
# hosts for httpx:
jq -r '.host' live.jsonl | httpx -title -tech-detect -status-code -json -silent
```

Text-pipe variant (hostnames only):

```bash
subfinder -d example.com -silent | dnsx -silent -a -aaaa | httpx -json -silent
```

## Workflow 2 — Enrich after validation

```bash
dnsx -l live_hosts.txt -cname -ns -mx -txt -soa -caa -json -silent -o enrich.jsonl
```

Use only on hosts that already passed A/AAAA validation when possible.

## Workflow 3 — Bruteforce discovery

```bash
dnsx -d example.com -w wordlists/dns.txt -silent -a -aaaa -json -auto-wildcard -o brute.jsonl
```

Then validate/enrich as Workflow 1–2. Avoid `-stream` when you need wildcard filtering.

## Workflow 4 — Wildcard-aware pass

```bash
dnsx -l candidates.txt -a -aaaa -json -silent -auto-wildcard -wt 5 -o filtered.jsonl
# or manual domain filter (JSON recommended; mutually exclusive with -auto-wildcard):
dnsx -l candidates.txt -a -json -wd example.com -o wd.jsonl
```

## Workflow 5 — Resolver differential

```bash
dnsx -l suspects.txt -a -aaaa -json -r resolvers-public.txt -o pub.jsonl
dnsx -l suspects.txt -a -aaaa -json -r resolvers-trusted.txt -o trusted.jsonl
```

Compare answers before emitting nuggets.

## Workflow 6 — Reverse DNS pivot

```bash
dnsx -l ips.txt -ptr -json -silent -o ptr.jsonl
```

Feed new hostnames back into A/AAAA validation.

## Workflow 7 — Ports after DNS

```bash
subfinder -d example.com -silent | dnsx -silent -a | naabu -json -silent
```

## Workflow 8 — Corpus / examination capture

```bash
dnsx -l hosts.txt -a -aaaa -cname -resp -json -omit-raw -o examination/dnsx_validate.jsonl
```

Harvest → single-root bundle with `records[]` (not raw `.jsonl` as Structured pane).

## Decision shortcuts

| Goal | Command family |
|------|----------------|
| Live names only | `-a -aaaa -json -silent` |
| Platform/CDN aliases | `-cname` (+ `-cdn`) |
| Mail posture | `-mx -txt` |
| Authority / hosting | `-ns -soa` |
| Full record dump | `-all` / `-recon` (heavy) |
| Brute | `-d` + `-w` |
