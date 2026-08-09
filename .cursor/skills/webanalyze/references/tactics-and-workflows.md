# webanalyze Strategies, Tactics, and Workflows

## Strategy: classify fast, pivot smart

Use webanalyze early for broad stack classification on live web hosts, then route targets into specialized tools from `category_names` / `app_name`.

Always prefer:

```bash
webanalyze -hosts live.txt -output json -silent
```

## Workflow 1 — Broad host fingerprinting

1. Collect live URLs/hosts (httpx, subfinder→dnsx→httpx, Naabu web ports).
2. Ensure definitions: `webanalyze -update` (cwd or `.tools/webanalyze`).
3. Batch: `-hosts file -output json -silent -worker 4` (raise workers only with scope approval).
4. Cluster records by `app_name` and `app.category_names`.
5. Prioritize hosts with CMS, outdated versions, or unusual stacks.

## Workflow 2 — Path and crawl deepening

1. Select high-value hosts from Workflow 1.
2. Re-run with `-redirect` when the root only redirects.
3. Add `-crawl 1` or `-crawl 2` to follow same-site links (respect `-search` default).
4. Add explicit path hosts: `/login`, `/admin`, app roots as separate `-host` lines.
5. Merge technology sets; keep versions when present.

## Workflow 3 — Category-driven pivots

| Signal | Next step |
|--------|-----------|
| CMS / blogs | CMSeeK; Nuclei CMS/CVE tags on smaller permissive targets |
| CDN / WAF / security | wafw00f; slow Nuclei; adjust UA/rate |
| Web servers / frameworks | httpx tech confirm; version-aware CVE hunt |
| Analytics / JS libraries | third-party dependency and supply-chain review |
| Empty matches | verify scheme, `-redirect`, path variants before declaring clean miss |

## Workflow 4 — Drift tracking

1. Snapshot `-output json` bundles on a schedule.
2. Diff `app_name` (+ version) sets per host.
3. Investigate newly introduced high-risk components immediately.

## Tactical adaptations

| Observation | Adaptation |
|-------------|------------|
| Sparse on HTTPS site with bare hostname | Use `https://` explicitly (default scheme is HTTP) |
| Only CDN detected | Origin may be masked; continue but annotate; optional origin IP if in scope |
| `technologies.json` week-old warning | `-update` then re-scan |
| Noisy header in captures | `-silent` |
| Unwanted subdomain/link expansion | `-search=false` |
| Auth-gated app | Fingerprint will miss post-login stack; document limitation |
| Batch timeouts / flaky hosts | Lower `-worker`; retry failures from stderr |

## Sequencing with other SpiderFeet skills

```
subfinder/dnsx → httpx (live URLs)
              → webanalyze -output json -silent
              → cmseek | wafw00f | nuclei (by category)
```

## Exploration vs examination

| Phase | Output |
|-------|--------|
| Exploration | May use default stdout to learn shapes; document TUI/human mode |
| Formal examination | **Only** `-output json` (+ `-silent`); derive text from structured; graph mandatory |
