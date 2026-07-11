# httpx Tactics — Maximize Web Surface Data

## Thin or empty JSONL

1. **Validate upstream** — dnsx/subfinder may list dead names; httpx only reports responders.
2. **Scheme fallback** — Retry with `-no-fallback` to catch HTTP-only services.
3. **Ports** — Default 80/443 only; use `-p` for 8080, 8443, 8000, 3000, etc.
4. **Probe all IPs** — `-probe-all-ips` when DNS returns multiple A records.
5. **Direct IP URL** — `httpx -u http://203.0.113.10` when vhost/SNI matters.
6. **Timeouts** — Increase `-timeout`; lower `-threads` on lossy networks.

## CDN / WAF fronted

1. Enable `-cdn` to **label** edge; do not assume origin tech-detect is complete.
2. `-exclude-cdn` when port fan-out is wasteful.
3. Tech-detect may show Cloudflare/Fastly only — document as **edge stack** metadata.
4. Follow redirects (`-include-chain`) — app may live behind multiple edges.
5. Nuclei tags should use edge-visible tech unless origin IP is known.

## Rate limits and blocking

1. Lower `-rate-limit` (50–100) and `-threads` (10–25).
2. Increase `-retries` modestly; set `-max-host-error` to skip stuck hosts.
3. Use `-random-agent` (default) unless custom UA required.
4. Split large `-l` files into batches.
5. Record **blocked** scenarios as corpus outcomes (403/WAF challenge pages).

## Noisy path / soft-404 scans

1. `-filter-error-page` for ML-classified error templates.
2. `-filter-duplicates` when many hosts return identical bodies.
3. `-match-code` to keep 200/401 only.
4. Separate **path scan** scenarios from host-only probes in manifests.

## Tech-detect empty but site is live

1. Add paths: `/`, `/login`, `/api`, language roots.
2. Ensure `-tech-detect` flag set; verify Wappalyzer dataset in httpx version.
3. Compare **webanalyze** pass for second opinion.
4. Check if response is JSON/API with minimal HTML (tech may be in headers only — use `-server`, `-header`).

## Maximize downstream value

| httpx output | Next tool |
|--------------|-----------|
| `tech[]` contains WordPress | nuclei `-tags wordpress` |
| `status_code` 401/403 | nuclei default-login / exposure templates |
| `url` list | nuclei full pass |
| AI ports from naabu | build URLs → **Julius** |
| `jarm` / `favicon` | correlation pivots (metadata) |

## Semantic outcome matrix (corpus)

| Class | Tactic |
|-------|--------|
| Rich web row | permissive lab + full probe flags |
| Redirect chain | `-include-chain` on corporate site |
| 401/403 | do not filter out if scenario is "auth surface" |
| Clean miss | non-web port or dead host — valid negative |
| Stdin pipeline | document in manifest as integration scenario |

## Anti-patterns

- Running `-screenshot` on 10k hosts.
- `-irr` on every row without size limits.
- Confusing ProjectDiscovery httpx with Python `httpx` library in scripts.
- Skipping httpx before nuclei on raw subdomain lists (wastes nuclei time).
