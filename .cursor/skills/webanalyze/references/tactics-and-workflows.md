# webanalyze Strategies, Tactics, and Workflows

## Strategy: classify fast, pivot smart

Use webanalyze early for broad stack classification, then route targets into specialized modules based on detected categories.

## Workflow 1 - Broad host fingerprinting

1. Feed live web hosts.
2. Run quick fingerprints on root path.
3. Cluster by common stacks (WordPress, React, nginx, Cloudflare, etc.).

## Workflow 2 - Path-aware deepening

1. Re-scan selected hosts on `/login`, `/admin`, API roots.
2. Merge detections from all scanned paths.
3. Raise confidence on technologies seen across multiple paths.

## Workflow 3 - Category-driven pivots

| Category | Next step |
|---|---|
| CMS | run CMS-focused modules and CVE checks |
| Web server/CDN/WAF | run perimeter and service fingerprint modules |
| JS framework | prioritize front-end exposure review |
| Analytics/tracking | enrich third-party dependency graph |

## Workflow 4 - Drift tracking

1. Schedule recurring fingerprints.
2. Diff previous and current tech sets.
3. Alert on newly introduced high-risk components.

## Tactical guidance

- Run pre-auth and post-auth passes for applications with gated content.
- Compare fingerprint results with response headers/body snapshots to reduce false positives.
- Keep Wappalyzer schema alignment in mind when adding custom detection logic.
