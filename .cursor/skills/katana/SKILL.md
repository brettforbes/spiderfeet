---
name: katana
description: Crawl web targets with Katana and convert JSONL discoveries into SpiderFeet nuggets. Trigger on katana, crawl, endpoint discovery, JS crawl, URL enumeration, recon pipeline, or web attack-surface mapping tasks.
---

# Katana

## Purpose

Use Katana to discover web endpoints and assets, then map results into SpiderFeet node/edge graph structures.

## Step-by-Step Instructions

1. Confirm scope and authorization for every domain/URL.
2. Run baseline crawl in JSONL mode.
3. Add depth and scope filters.
4. Enable `-jc` for JS-heavy apps and `-kf` for known-files sweeps when needed.
5. Parse JSONL records safely line-by-line.
6. Convert discovered URLs/hosts into nuggets plus nodes/edges arrays.
7. De-duplicate canonical URLs and persist provenance.
8. Queue high-value findings for follow-up scanning.

### Examples

```bash
katana -u https://example.org -silent -jsonl -depth 3
katana -u https://app.example.org -silent -jsonl -jc -depth 4
katana -list targets.txt -silent -jsonl -kf all -fx
```

## If/Then Decision Rules

- If crawl is too noisy, then tighten include/exclude filters and lower depth.
- If SPA routes are missing, then enable `-jc` or headless mode.
- If target throttles requests, then lower concurrency and increase timeout.
- If JSON parse fails for a line, then skip line and continue parsing.
- If duplicate URL appears, then merge metadata into existing node.

## Guardrails & Pitfalls

- Authorized targets only.
- Prefer `-jsonl`; text output is fragile for automation.
- Avoid unbounded depth on large sites.
- JS/headless crawling can increase load; use deliberately.
- Treat discovered paths as leads until validated.

## references

- `references/SKILLS.md`
- `references/cli-options.md`
- `references/output-and-parsing.md`
- `references/nugget-mapping.md`
- `references/tactics.md`
- `references/sources.md`
