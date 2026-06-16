## Problem
Module `sfp_google_tag_manager` has no smoke-validated entry in `module_test_seeds.json` (none-tier corpus gap).

## Last validation
| Field | Value |
|-------|-------|
| consumed | `WEB_ANALYTICS_ID` |
| input | `sbs.com.au` |
| status | `FINISHED` |
| verdict | `clean_miss` |
| produced | `0` |

## Module
- **Name:** Google Tag Manager
- **Categories:** Passive DNS
- **Summary:** Search Google Tag Manager (GTM) for hosts sharing the same GTM code.
- **Produces:** DOMAIN_NAME, INTERNET_NAME, AFFILIATE_DOMAIN_NAME, AFFILIATE_INTERNET_NAME

## Research tasks
1. Inspect `modules/sfp_google_tag_manager.py` for required input shape and external API health.
2. Probe `POST /api/v1/scan_ui` with module-specific targets; use `GET /scans/{id}/logs` on failure.
3. Update `module_test_seeds.json` with validated input (or document `SPEC_GAP` / negative fixture if appropriate).
4. Run `poetry run python .seed/scripts/validate_test_seeds.py --tier none --write` for this module.

## Spec
R2-04-07 (module-validated test corpus)

## Parent epic
SF-674 — Pending none-tier seed research (32 modules)
