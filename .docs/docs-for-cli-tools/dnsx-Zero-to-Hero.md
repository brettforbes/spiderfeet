# dnsx Zero to Hero

Hands-on guide for using `dnsx` from first run to production recon workflows.

## 1) What dnsx is for

`dnsx` is a fast DNS resolution and record-query tool used to validate candidate domains/subdomains and enrich them with DNS record intelligence.

## 2) Install and verify

```bash
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
dnsx -h
```

## 3) First useful command

```bash
dnsx -silent -l hosts.txt -a -resp -j
```

- `-l hosts.txt`: input host list
- `-a`: query A records
- `-resp`: include answer detail
- `-j`: JSON output for parsing

## 4) Major option classes with examples

### A. Input and execution

```bash
cat hosts.txt | dnsx -silent -a -j
dnsx -silent -l hosts.txt -a -j
```

### B. Record classes

```bash
dnsx -silent -l hosts.txt -a -aaaa -cname -ns -mx -txt -j
```

### C. Discovery/bruteforce

```bash
dnsx -silent -d example.com -w subdomains.txt -a -j
```

### D. Resolver strategy

```bash
dnsx -silent -l hosts.txt -a -r resolvers.txt -j
```

### E. Output for automation

```bash
dnsx -silent -l hosts.txt -a -aaaa -j > dnsx.jsonl
```

## 5) Practical workflows

### Workflow 1: Validate passive subdomain results

1. Gather candidates from passive tools.
2. Run dnsx A/AAAA validation.
3. Keep only resolving hostnames for service scans.

### Workflow 2: Alias and platform mapping

1. Run CNAME + NS collection.
2. Group hosts by shared CNAME targets.
3. Prioritize high-value clusters for deeper scans.

### Workflow 3: Mail and policy intelligence

1. Query MX/TXT records.
2. Extract mail exchangers and SPF-like policy clues.
3. Route findings into email security investigation lanes.

## 6) Output to SpiderFeet nuggets (`nodes[]` and `edges[]`)

Use parsed dnsx results to emit graph payloads:

```json
{
  "nodes": [
    { "type": "INTERNET_NAME", "data": "example.com" },
    { "type": "INTERNET_NAME", "data": "mail.example.com" },
    { "type": "IP_ADDRESS", "data": "198.51.100.40" }
  ],
  "edges": [
    { "source": "example.com", "target": "mail.example.com", "relationship": "mx_to" },
    { "source": "mail.example.com", "target": "198.51.100.40", "relationship": "resolves_to" }
  ]
}
```

## 7) Tactics for better results

- Start narrow (`-a -aaaa`) and expand record classes only when needed.
- Use multiple resolver sets to confirm suspicious outputs.
- Enable wildcard controls when zones return synthetic positives.
- Re-run only delta targets to keep recurring scans efficient.

## 8) Common pitfalls

- Treating one failed resolver response as definitive.
- Ignoring wildcard behavior and overcounting false positives.
- Parsing plain text output in automation instead of JSON mode.
- Skipping deduplication before graph ingestion.

## 9) Next references

- `.cursor/skills/dnsx/SKILL.md`
- `.cursor/skills/dnsx/references/SKILLS.md`
- [dnsx usage docs](https://docs.projectdiscovery.io/opensource/dnsx/usage)
