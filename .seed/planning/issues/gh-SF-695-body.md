## Problem
Module `sfp_opennic` has no smoke-validated entry in `module_test_seeds.json` (none-tier corpus gap).

## Last validation
| Field | Value |
|-------|-------|
| consumed | `INTERNET_NAME` |
| input | `sbs.com.au` |
| status | `FINISHED` |
| verdict | `clean_miss` |
| produced | `0` |

## Module
- **Name:** OpenNIC DNS
- **Categories:** DNS
- **Summary:** Resolves host names in the OpenNIC alternative DNS system.
- **Produces:** IP_ADDRESS, IPV6_ADDRESS, AFFILIATE_IPADDR, AFFILIATE_IPV6_ADDRESS

## Research tasks
1. Inspect `modules/sfp_opennic.py` for required input shape and external API health.
2. Probe `POST /api/v1/scan_ui` with module-specific targets; use `GET /scans/{id}/logs` on failure.
3. Update `module_test_seeds.json` with validated input (or document `SPEC_GAP` / negative fixture if appropriate).
4. Run `poetry run python .seed/scripts/validate_test_seeds.py --tier none --write` for this module.

## Spec
R2-04-07 (module-validated test corpus)

## Parent epic
SF-674 — Pending none-tier seed research (32 modules)
