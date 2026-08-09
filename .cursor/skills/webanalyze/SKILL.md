---
name: webanalyze
description: Fingerprint web technologies with webanalyze when prompts mention Wappalyzer-style detection, CMS/framework identification, tech stack inventory, HTTP header/body signature matching, or recon pipelines needing WEBSERVER_TECHNOLOGY nugget extraction from URLs, host lists, or domains.
---

# webanalyze — Web Technology Fingerprinting

## Purpose

Use when you must **detect CMS, frameworks, servers, CDN/WAF, and other web stack components** from HTTP responses (Wappalyzer-style signatures), capture **`-output json`**, and convert matches to SpiderFeet `WEBSERVER_TECHNOLOGY` nuggets — especially after **httpx/subfinder** produce live URLs or host lists.

**Binary (this host):** `C:\projects\spiderfeet\.tools\webanalyze\webanalyze.exe`  
Release zip beside binary: `webanalyze_Windows_x86_64.zip`.  
**There is no `-version` / `--version` flag** (`flag provided but not defined: -version`). Identify capability via `-h` and the stderr header (`:: webanalyze : v…`) when not `-silent`. Help capture: **2026-08-10** (`.tmp_webanalyze_help/`).

## Step-by-Step Instructions

1. **Confirm scope** — Authorized URLs/hosts only. webanalyze issues unauthenticated GET requests (TLS verify skipped in the client).
2. **Ensure `technologies.json`** — Required before any scan. From the working directory (or beside the binary):

```bash
webanalyze -update
```

   Lookup order for `-apps`: `./`, executable directory, then `$HOME`. This host had no bundled definitions until `-update` wrote `technologies.json` under `.tools/webanalyze/`.

3. **Validate tooling** — `webanalyze -h` (exact text in `references/cli-options.md` and `.docs/docs-for-cli-tools/webanalyze-CLI-Options.md`).
4. **Build targets** — Single `-host <url|hostname>` or batch `-hosts hosts.txt` (one host per line). Prefer explicit `https://` / `http://`; bare hostnames default to **`http://`**.
5. **Run structured fingerprint (SpiderFeet / corpus)** — always `-output json`; use `-silent` so only NDJSON hits stdout:

```bash
webanalyze -host https://example.com -output json -silent
webanalyze -hosts hosts.txt -output json -silent -worker 8
```

6. **Parse results** — One JSON object per scanned host line (`hostname` + `matches[]`). Fields in `references/output-schema-and-parsing.md`.
7. **Map nuggets** — Host → `INTERNET_NAME`; each `matches[].app_name` (+ optional `version`) → `WEBSERVER_TECHNOLOGY` per `references/nugget-mapping.md`.
8. **Adapt on sparse yield** — Add `-redirect`, raise `-crawl N`, scan app paths (`/login`, `/admin`), try HTTPS explicitly, or refresh `-update` if signatures are stale (tool warns when `technologies.json` is older than one week).
9. **Chain downstream** — CMS → CMSeeK/Nuclei; CDN/WAF → wafw00f; stack inventory → httpx/Nuclei tag passes.

## If/Then Decision Rules

| If | Then |
|----|------|
| Need automation / corpus / nuggets | Always `-output json` (+ `-silent`); never parse stdout table alone |
| Missing `technologies.json` | Run `webanalyze -update` in cwd or set `-apps <path>` |
| Empty matches on a live host | Try `-redirect`, `-crawl 1`+, alternate paths, explicit `https://` |
| Redirects hide the app | `-redirect` (default **false** — must opt in) |
| Same-base-domain link fan-out unwanted | `-search=false` (default **true**) |
| Large host list | Raise `-worker` carefully; default is `4` |
| Header noise in captures | `-silent` (header is on **stderr**; findings on **stdout** for json/csv) |
| Need human review | Omit `-silent` / use default `-output stdout` for exploration only |
| Need spreadsheet triage | `-output csv` (not for graph source when JSON exists) |
| Clean-miss / negative fixture | Known non-app host with `-output json -silent` → `matches: []` or host error on stderr |
| Conflicting / implied tech | Keep each `app_name`; do not collapse implies away |

## Guardrails & Pitfalls

- **Authorization** — fingerprinting still requires written scope.
- **Do not invent flags** — only options from Captured help (2026-08-10). No `-json` shorthand; use `-output json`.
- **No version flag** — do not pass `-version` / `--version`.
- **Structured-first** — graph/narrative from JSON lines only when `-output json` is available.
- **Default scheme is HTTP** — bare `example.com` becomes `http://example.com`; prefer explicit HTTPS for modern sites.
- **`-redirect` is off by default** — easy false sparse results on redirecting hosts.
- **`-search` is on by default** — can expand to same-base-domain URLs; disable for strict single-URL exams.
- **Do not** treat fingerprint matches as exploitability proof.
- **Stale signatures** — refresh with `-update`; pin `technologies.json` for repeatable corpus runs.
- **Errors** — failed retrieves go to **stderr** (`<host> error: …`); JSON object may be absent for that host.

## Strategies and Tactics

**Breadth first**

```
live URLs/hosts → webanalyze -hosts file -output json -silent → cluster by app_name / category_names
```

**Depth second**

1. Re-scan high-value hosts with `-crawl 1` or `-crawl 2` and `-redirect`.
2. Hit `/login`, `/admin`, app roots as separate `-host` lines.
3. Merge `app_name` sets; keep versions when present.

**Category-driven pivots**

| `category_names` signal | Next tool |
|-------------------------|-----------|
| CMS / blogs | CMSeeK, Nuclei CMS tags |
| CDN / security | wafw00f, rate-limited Nuclei |
| Web servers / frameworks | httpx tech confirm, CVE templates |
| Analytics / JS libs | third-party dependency review |

**Drift**

- Snapshot JSON periodically; diff `app_name` sets for new stack components.

See `references/tactics-and-workflows.md` for full workflows.

## Comprehensive Examples

### Help (no version flag)

```bash
webanalyze -h
# webanalyze -version   # FAILS — not defined
```

### Update definitions

```bash
cd C:\projects\spiderfeet\.tools\webanalyze
webanalyze -update
```

### SpiderFeet default (single host, JSON)

```bash
webanalyze -host https://example.com -output json -silent
```

### Batch hosts

```bash
webanalyze -hosts hosts.txt -output json -silent -worker 8
```

### Crawl + follow redirects

```bash
webanalyze -host https://shop.example.com -crawl 2 -redirect -output json -silent
```

### Strict single URL (no subdomain/link search)

```bash
webanalyze -host https://shop.example.com/login -search=false -output json -silent
```

### Exploration (human stdout)

```bash
webanalyze -host https://example.com -crawl 1
```

### CSV (triage only)

```bash
webanalyze -host https://example.com -output csv -silent
```

## References

Indexed in [`references/SKILLS.md`](references/SKILLS.md).

| File | Topic |
|------|--------|
| `cli-options.md` | Captured help, all flags |
| `output-schema-and-parsing.md` | JSON/CSV/stdout shapes |
| `nugget-mapping.md` | JSON → SpiderFeet graph |
| `tactics-and-workflows.md` | Sequencing and pivots |
| `sources.md` | Official URLs |

**Operator docs:** `.docs/docs-for-cli-tools/webanalyze-Zero-to-Hero.md`, `.docs/docs-for-cli-tools/webanalyze-CLI-Options.md`.
