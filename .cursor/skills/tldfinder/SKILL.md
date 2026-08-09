---
name: tldfinder
description: Enumerate private and uncommon top-level domains with tldfinder when prompts mention private TLD discovery, DNS namespace reconnaissance, split-horizon DNS, corp/internal naming leaks, or pivoting from seed domains/organizations into broader INTERNET_NAME expansion for SpiderFeet mapping.
---

# tldfinder — Private TLD Enumeration to Nuggets

## Purpose

Use when you must **discover hostnames under private / non-public TLDs** with [ProjectDiscovery tldfinder](https://github.com/projectdiscovery/tldfinder), capture **JSON Lines** (`-oJ`), and map results to SpiderFeet **`INTERNET_NAME`** / **`INTERNET_NAME_UNRESOLVED`** (and optional IP nodes when `-active -oI`), then chain to **dnsx → httpx → naabu**.

Local binary (this workspace): `C:\projects\spiderfeet\.tools\tldfinder\tldfinder.exe` (v0.0.2, evidence date **2026-08-10**).

## Step-by-Step Instructions

1. **Confirm scope** — Authorized private-TLD research only. Passivefinder queries OSINT sources (and optionally DNS); API-backed sources disclose intent to third parties.
2. **Prepare private-TLD input** — Pass a **private TLD label** (e.g. `google`) or a name under one (e.g. `example.google`). Public apexes like `example.com` are not the intended input class (README: only private TLDs).
3. **Install / locate binary and provider config** — Prefer the workspace binary or `go install github.com/projectdiscovery/tldfinder/cmd/tldfinder@latest`. Configure keys in `provider-config.yaml` (see `references/cli-options.md`).
4. **Choose discovery mode** — `-dm dns` (default: domains under the private TLD), `-dm tld` (TLD-oriented discovery), or `-dm domain`. Prefer **dns** for private-namespace host harvesting.
5. **Run with structured output** — Always use `-oJ` / `-json` for corpus and nugget conversion; add `-cs` for multi-source provenance; use `-active -oI` only when live IPs are required.
6. **Parse JSONL** — One object per line (`host`, `input`, `source` / `sources`, optional `ip`). See `references/output-schema-and-parsing.md`.
7. **Map nuggets** — Each `host` → `INTERNET_NAME` or `INTERNET_NAME_UNRESOLVED`; optional `ip` via `classify_ip`. See `references/nugget-mapping.md`.
8. **Validate and enrich** — Pipe unique hosts to **dnsx**, then **httpx** / **naabu** as needed.
9. **Adapt follow-up** — Thin yield → add provider keys, `-all`, or alternate `-s` sources; noise → `-m` / `-f`, lower `-rl`, exclude failing `-es`.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-oJ`; never parse banner art as findings |
| Need provenance | Add `-cs` (JSON only) |
| Need IPs in JSON | Use `-active -oI -oJ` together |
| Exploring private-TLD host surface | `-dm dns` (default) |
| Exploring TLD-oriented variants | `-dm tld` |
| Large run returns many names | Deduplicate FQDNs; pipe to `dnsx -silent -a -aaaa` before port scan |
| Very few results | Check `provider-config.yaml` keys; retry with `-all` or specific `-s` |
| API rate limits / 429 | Lower `-rl` or tune `-rls`; exclude failing `-es` |
| Passive names may be dead | Validate with `-active` or **dnsx** before invasive scans |
| Split-horizon / internal-only names | Re-run with alternate `-r` / `-rL` resolvers and compare |
| Input is a public FQDN | Extract private-TLD label or in-scope private suffix; do not treat public PSL TLDs as private discoveries |
| Duplicate hosts across sources | Deduplicate on normalized FQDN; merge `sources` |

## Guardrails & Pitfalls

- **Authorization** — Private-TLD research can surface internal naming; keep findings in authorized reporting scope.
- **Input class** — Seeds are private TLD labels / names under them, not ordinary public domains.
- **API keys** — Sources marked `*` in `-ls` need tokens; empty keys → thin results (not a tool failure).
- **`-all` is slow** — Reserve for high-value second passes.
- **Passive ≠ live** — Default mode does not prove DNS answers.
- **`-active` hits resolvers** — Tune `-t`, `-r` / `-rL`, `-timeout`, `-max-time`.
- **JSONL ≠ JSON array** — Parse line by line; harvest into a single-root bundle for SpiderFeet Structured pane.
- **Do not invent flags** — Use only switches from `tldfinder -h` on the installed binary (captured under `.tmp_tldfinder_help/`).
- **`-oD` help text** — Mentions `-dL only`; v0.0.2 INPUT documents only `-d` (file or comma-separated). Prefer `-d seeds.txt -o file` unless your binary exposes `-dL`.

## References directory for details on source material and usage indexed through `SKILLS.md`

See [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Flags by category (from v0.0.2 help) |
| `output-schema-and-parsing.md` | JSONL fields and parsing |
| `nugget-mapping.md` | JSONL → SpiderFeet graph |
| `tactics-and-workflows.md` | Sequencing and adaptation |
| `sources.md` | Official and practitioner URLs |

Operator guides: `.docs/docs-for-cli-tools/tldfinder-Zero-to-Hero.md`, `tldfinder-CLI-Options.md`.

## Comprehensive Examples

### Basic discovery (private TLD label)

```bash
tldfinder -d google
tldfinder -d google -silent
tldfinder -d google -o hosts.txt
```

### JSONL for corpus / nuggets (preferred)

```bash
tldfinder -d google -oJ -o google.jsonl
tldfinder -d google -oJ -cs -o google_sources.jsonl
tldfinder -d google -dm dns -oJ -silent -duc
tldfinder -d google -active -oJ -oI -o google_live.jsonl
```

### Discovery modes

```bash
tldfinder -d google -dm dns -oJ -o dns_mode.jsonl
tldfinder -d google -dm tld -oJ -o tld_mode.jsonl
tldfinder -d google -dm domain -oJ -o domain_mode.jsonl
```

### Source selection

```bash
tldfinder -ls
tldfinder -d google -s crtsh,dnsx,waybackarchive
tldfinder -d google -all
tldfinder -d google -es censys,whoisxmlapi
```

### Filter and match

```bash
tldfinder -d google -m corp,sandbox
tldfinder -d google -f test,qa
tldfinder -d google -m keywords.txt
```

### Rate limits and timeouts

```bash
tldfinder -d google -rl 5
tldfinder -d google -rls "waybackarchive=15/m,whoisxmlapi=30/s"
tldfinder -d google -timeout 60 -max-time 30
```

### File / multi-input via `-d`

```bash
tldfinder -d google,internal
tldfinder -d seeds.txt -oJ -o batch.jsonl
```

### Active resolution and resolvers

```bash
tldfinder -d google -active -r 8.8.8.8,1.1.1.1 -t 20
tldfinder -d google -active -rL resolvers.txt -oJ -oI -o live.jsonl
```

### Pipes

```bash
tldfinder -d google -silent | dnsx -silent -a -aaaa
tldfinder -d google -silent | httpx -silent
```

### Parse one JSONL line (Python)

```python
import json

line = '{"host":"docs.google","input":"google","source":"crtsh"}'
data = json.loads(line)
host = data["host"].lower().rstrip(".")
seed = data.get("input", "")
```

## Strategies and Tactics

See [`references/tactics-and-workflows.md`](references/tactics-and-workflows.md). Summary:

1. **Private-TLD seed → JSONL → validate** — `-dm dns -oJ`, then **dnsx** (or `-active -oI`).
2. **Source tiering** — Free sources (`crtsh`, `dnsx`, `waybackarchive`) first; add keyed sources when configured; `-all` only on high-value labels.
3. **Mode contrast** — Compare `-dm dns` vs `-dm tld` when mapping namespace vs public-TLD collisions.
4. **Split-horizon** — Alternate resolver lists; keep both vantage views with provenance.
5. **Pipeline hygiene** — `-silent` between tools; dedupe FQDNs; use `-v` / `-stats` when debugging sources.
