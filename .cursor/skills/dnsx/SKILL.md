---
name: dnsx
description: Resolve DNS records and validate subdomains with dnsx when prompts mention dns resolution, wildcard filtering, A/AAAA/CNAME/MX/TXT lookups, DNS brute force, or recon pipelines from subfinder/httpx/naabu into SpiderFeet INTERNET_NAME and IP_ADDRESS graph nodes.
---

# dnsx - DNS Resolution and Record Enrichment

## Purpose

Use this skill to run `dnsx` for fast DNS validation, record extraction, wildcard-aware subdomain resolution, and structured output conversion into SpiderFeet nuggets.

## Step-by-Step Instructions

1. Confirm scope and authorization for the target domains and resolver traffic.
2. Prepare input candidates (one hostname per line) from seeds or upstream tools.
3. Pick resolver strategy:
   - default public resolvers for broad recon,
   - custom resolver list (`-r`) for controlled infrastructure,
   - trusted resolvers for noisy wildcard zones.
4. Start with lightweight validation:
   - `dnsx -silent -l hosts.txt -a -resp -j`
5. Add record classes needed for the task:
   - infrastructure: `-a -aaaa -cname -ns -mx -txt`
   - edge/verification: `-ptr -soa -srv -any` (if supported by deployed version)
6. If doing discovery, add DNS brute force inputs:
   - `-d target.tld -w wordlist.txt` (or equivalent list mode by version)
7. Enable wildcard handling controls when high false positives appear:
   - use wildcard threshold/filter flags supported by installed version.
8. Capture JSON/JSONL output and parse per line into normalized objects.
9. Convert parsed records into SpiderFeet graph payloads:
   - build `nodes[]` (entity nuggets) and `edges[]` (relationships).
10. Feed validated outputs into downstream tooling (e.g., `httpx`, `naabu`, `nmap`) and rerun targeted dnsx passes on newly found hosts.

## If/Then Decision Rules

| If | Then |
|----|------|
| Input list is mostly dead domains | Use `-retry`/resolver tuning and keep `-silent` to reduce parser noise |
| Multiple wildcard responses pollute results | Enable wildcard filtering controls and compare trusted resolvers |
| Need only live host validation | Run A/AAAA only first, defer heavy record classes |
| Need mail posture intelligence | Add `-mx -txt` to expose mail exchangers/SPF/DKIM hints |
| Need CDN/stack pivoting | Prioritize `-cname` and map aliases as first-class nodes |
| Reverse infrastructure mapping needed | Add PTR sweep on discovered IPs and map back to hostnames |
| Resolver rate limits/errors spike | Lower thread/concurrency and rotate resolver set |
| Downstream HTTP scan misses targets | Re-run with `-aaaa` and CNAME expansion to include IPv6/alias paths |

## Guardrails & Pitfalls

- Resolve only authorized targets.
- Do not trust single-resolver results for wildcard-heavy zones.
- Preserve raw answer text while also storing normalized node values.
- Avoid treating NXDOMAIN/SERVFAIL/transient timeouts as equivalent outcomes.
- Keep parser tolerant: dnsx fields vary between versions and option sets.
- Deduplicate host->IP and host->CNAME edges before ingestion.
- Prefer JSON output for automation; text mode is for quick human inspection only.

## Strategies and Tactics

- **Validate -> enrich -> pivot:** first validate alive hostnames, then collect record classes, then pivot into HTTP/port tools.
- **CNAME-first triage:** cluster by CNAME target to identify shared SaaS/CDN platforms quickly.
- **MX/TXT mail profiling:** use DNS mail records to branch into email/security modules.
- **Resolver differential checks:** rerun suspicious hosts against alternate resolvers to reduce poisoning and cache artifacts.
- **Incremental reruns:** keep prior results and only query new/changed hostnames in long recon loops.

## References directory for details on source material and usage indexed through `SKILLS.md`

See `references/SKILLS.md` for CLI options, output schema/parsing, nugget mapping, tactics/workflows, and source links.
