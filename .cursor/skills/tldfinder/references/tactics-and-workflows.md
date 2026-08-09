# tldfinder Strategies, Tactics, and Workflows

Use tldfinder as an **upstream private-TLD namespace discovery** stage. Prefer **`-oJ`**, then validate with **dnsx** (or `-active`) before invasive scanning.

Evidence baseline: **v0.0.2**, **2026-08-10**.

## Strategy: seed → enumerate → validate → pivot

1. Choose a private TLD label or in-scope private suffix.
2. Enumerate with `-dm dns -oJ` (add `-cs` for provenance).
3. Deduplicate hosts; validate live names.
4. Map nuggets; feed live hosts to httpx / naabu / nuclei as authorized.

## Workflow 1 — Private-TLD host discovery (primary)

```bash
tldfinder -d google -dm dns -oJ -cs -duc -o google_dns.jsonl
```

1. Seed with private TLD labels from prior recon (certs, leaks, org intel).
2. Capture JSONL; require non-banner stdout for harvest completeness.
3. Rank hosts by source recurrence and keyword interest (`corp`, `sandbox`, `internal`).

## Workflow 2 — Active validation

```bash
tldfinder -d google -dm dns -active -oJ -oI -duc -o google_live.jsonl
# or
tldfinder -d google -silent | dnsx -silent -a -aaaa -j
```

1. Prefer **dnsx** when you need rich record classes; use `-active -oI` when IPs must stay in the same JSONL stream.
2. Promote only resolvable hosts to port/HTTP stages.
3. Keep unresolved names as `INTERNET_NAME_UNRESOLVED` with provenance.

## Workflow 3 — Mode contrast (dns vs tld)

```bash
tldfinder -d google -dm dns -oJ -o dns.jsonl
tldfinder -d google -dm tld -oJ -o tld.jsonl
```

1. `-dm dns` harvests names under the private TLD.
2. `-dm tld` may surface public-TLD combinations — cross-check against PSL/public roots before calling them “private TLD findings”.
3. Use contrast to reduce false private-namespace claims.

## Workflow 4 — Split-horizon / resolver differential

```bash
tldfinder -d google -active -r 8.8.8.8,1.1.1.1 -oJ -oI -o public_resolvers.jsonl
tldfinder -d google -active -rL corp_resolvers.txt -oJ -oI -o corp_resolvers.jsonl
```

1. Re-run with alternate `-r` / `-rL` sets.
2. Diff host sets and resolution success.
3. Flag environment-specific private namespaces; retain both views with metadata.

## Workflow 5 — Source tiering under rate limits

1. First pass: free sources only (`-s crtsh,dnsx,waybackarchive`).
2. Second pass: add keyed sources after editing `provider-config.yaml`.
3. Third pass: `-all` only for high-value labels; tune `-rl` / `-rls`, raise `-max-time`.
4. On failures: `-v -stats`, then `-es` failing providers.

## Adaptive matrix

| Observation | Action |
|---|---|
| Thin results | Configure provider keys; try `-all` or broader `-s` |
| Noisy / irrelevant hosts | Tighten `-m` / `-f`; post-filter in dnsx |
| Rate limits / 429 | Lower `-rl`, adjust `-rls`, exclude `-es` |
| Public-looking FQDNs from `-dm tld` | Do not label private until PSL/context check |
| Passive dead names | Validate with dnsx or `-active` before naabu/httpx |
| Conflicting resolver views | Keep both; annotate vantage |
| Empty run | Valid clean-miss if sources healthy; prove with `-v -stats` |

## Pipeline hygiene

- Use `-silent` when piping.
- Prefer `-duc` in automation to avoid update-check noise in stderr.
- Never truncate examination captures with `head`/`tail` in harvest manifests.
- Structured-first: no text-only formal scenario when `-oJ` exists.
