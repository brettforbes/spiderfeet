## Problem
Module `sfp_crt` has no smoke-validated entry in `module_test_seeds.json` (none-tier corpus gap).

## Last validation
| Field | Value |
|-------|-------|
| consumed | `DOMAIN_NAME` |
| input | `google.com` |
| status | `FINISHED` |
| verdict | `error_failed` |
| produced | `0` |

## Module
- **Name:** Certificate Transparency
- **Categories:** Search Engines
- **Summary:** Gather hostnames from historical certificates in crt.sh.
- **Produces:** SSL_CERTIFICATE_RAW, RAW_RIR_DATA, INTERNET_NAME, INTERNET_NAME_UNRESOLVED, DOMAIN_NAME, CO_HOSTED_SITE, CO_HOSTED_SITE_DOMAIN

## Research tasks
1. Inspect `modules/sfp_crt.py` for required input shape and external API health.
2. Probe `POST /api/v1/scan_ui` with module-specific targets; use `GET /scans/{id}/logs` on failure.
3. Update `module_test_seeds.json` with validated input (or document `SPEC_GAP` / negative fixture if appropriate).
4. Run `poetry run python .seed/scripts/validate_test_seeds.py --tier none --write` for this module.

## Spec
R2-04-07 (module-validated test corpus)

## Parent epic
SF-674 — Pending none-tier seed research (32 modules)
