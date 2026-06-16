---
name: webanalyze
description: Fingerprint web technologies with webanalyze when prompts mention Wappalyzer-style detection, CMS/framework identification, tech stack inventory, HTTP header/body signature matching, or recon pipelines needing WEBSERVER_TECHNOLOGY nugget extraction from URLs, host lists, or domains.
---

# webanalyze - Web Technology Fingerprinting

## Purpose

Use this skill to detect web technologies from responses using `webanalyze`, then convert detections into SpiderFeet technology graph nuggets.

## Step-by-Step Instructions

1. Confirm target authorization and scope (single URL, host list, or domain set).
2. Prepare inputs from prior discovery (`INTERNET_NAME`, live `URL`, HTTP service lists).
3. Run baseline fingerprinting:
   - `webanalyze -host https://target.example`
   - or list mode for multiple targets (by installed version support).
4. Prefer machine-readable output mode if available; otherwise normalize text detections.
5. Capture technology name, categories, confidence/version fields where exposed.
6. Normalize technology identities against canonical names (Wappalyzer-style aliases).
7. Convert each detection to graph payload:
   - `nodes[]` for `INTERNET_NAME` and `WEBSERVER_TECHNOLOGY`
   - `edges[]` linking host/page to detected technology.
8. Use categories to branch follow-up scans:
   - CMS -> CMS checks,
   - CDN/WAF -> perimeter tooling,
   - language/framework -> targeted CVE templates.
9. Re-run after redirects, auth changes, or alternate paths when detection confidence is low.

## If/Then Decision Rules

| If | Then |
|----|------|
| Detection set is empty on known live host | Test alternate URL paths and ensure HTTP/HTTPS scheme correctness |
| Redirect chain masks app response | Follow final URL and re-run against resolved endpoint |
| Multiple frameworks conflict | Keep both detections with confidence metadata, do not collapse prematurely |
| Need version-aware vulnerability follow-up | Preserve version strings and route to CVE checks |
| Only homepage scanned | Add representative paths (`/login`, `/admin`, app root variants) |
| WAF/CDN detected first | Continue scanning but annotate potential masking of origin stack |
| Output is text-only | Use deterministic parser rules and store raw line evidence |

## Guardrails & Pitfalls

- Scan only authorized web assets.
- Do not treat fingerprinting confidence as exploitability proof.
- Avoid single-page conclusions for large applications.
- Keep original detection evidence (headers/body patterns) when available.
- Normalize tech names but retain raw detector labels for traceability.
- Expect false negatives behind auth flows, JS-heavy apps, and anti-bot controls.

## Strategies and Tactics

- **Breadth first:** fingerprint many hosts quickly to cluster by platform.
- **Depth second:** revisit high-value hosts with path-specific passes.
- **Category-driven pivots:** use detected categories to choose next tools/modules.
- **Differential scans:** compare pre-login vs post-login fingerprints.
- **Change tracking:** rerun periodically and diff stacks for drift/new exposures.

## References directory for details on source material and usage indexed through `SKILLS.md`

See `references/SKILLS.md` for CLI options, output schema/parsing, nugget mapping, tactics/workflows, and source links.
