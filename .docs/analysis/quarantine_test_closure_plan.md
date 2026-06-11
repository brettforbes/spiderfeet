# Quarantine test closure plan

**Program:** Stage 5 — SPEC-003 R3-05-06 / R3-05-07  
**Parent epic:** GitHub #722 (`EPIC-SF-05`)  
**CLI epic:** GitHub #733 (`SF-05-10`)  
**Inventory:** 54 modules in `quarantine_services.json`  
**Baseline (2026-06-05):** 18 route-validated, 36 outstanding  
**Status (2026-06-11):** **54/54 route-closed** — all modules have `validated_produces`, `validated_negative`, or `upstream_blocked` on `route_seed_nugget` (see `audit_quarantine_route_seeds.py`). **48 promoted** to `in-test` via `promote_quarantine_from_seeds.py`; **6 blocked CLI tools** remain in quarantine (`cmseek`, `nbtscan`, `onesixtyone`, `testssl.sh`, `wappalyzer`, `whatweb` — issues #806/#807).

## Goal

Reduce the count of quarantine modules that cannot pass route-seed smoke tests by:

1. Aligning `route_seed_nugget` with validated or research-backed seeds
2. Fixing seeds on the wrong consumed nugget
3. Tuning content-extractor inputs (`clean_miss` bucket)
4. Installing Ruby/WSL CLI tools (`cmseek`, `testssl.sh`, `whatweb`)
5. Resolving or documenting blocked native CLIs (`nbtscan`, `onesixtyone`, `wappalyzer`)

## Acceptance

A module is **route-closed** when `module_test_seeds.json` has `validated_produces` or `validated_negative` on the catalogue `route_seed_nugget`, and `run_quarantine_battery.py --only <module>` passes (or `service_state: error` is documented with operator rationale).

## Module matrix (36 outstanding)

### A — Route seed mismatch (validated on different nugget) — 6

| Module | Catalogue route | Validated seed | Fix |
|--------|-----------------|----------------|-----|
| `sfp_countryname` | `DOMAIN_NAME` | `TARGET_WEB_CONTENT` | Override `route_seed_nugget` |
| `sfp_dnsbrute` | `INTERNET_NAME` | `DOMAIN_NAME` | Override `route_seed_nugget` |
| `sfp_dnsraw` | `INTERNET_NAME` | `DOMAIN_NAME` | Override `route_seed_nugget` |
| `sfp_pgp` | `INTERNET_NAME` | `EMAILADDR` | Override `route_seed_nugget` |
| `sfp_similar` | `DOMAIN_NAME` | `INTERNET_NAME` | Override `route_seed_nugget` |
| `sfp_tool_retirejs` | `LINKED_URL_EXTERNAL` | `LINKED_URL_INTERNAL` | Override `route_seed_nugget` |

**Issue:** #804 (`SF-05-12`) — immediate catalogue override; no seed re-run required.

### B — Route seed missing (seed on wrong nugget) — 12

| Module | Route | Seed today | Fix |
|--------|-------|------------|-----|
| `sfp_accounts` | `DOMAIN_NAME` | `EMAILADDR` | Route → `EMAILADDR`; tune seed |
| `sfp_crossref` | `LINKED_URL_EXTERNAL` | `INTERNET_NAME` | Add `LINKED_URL_EXTERNAL` seed |
| `sfp_dnscommonsrv` | `INTERNET_NAME` | `DOMAIN_NAME` | Route → `DOMAIN_NAME`; tune |
| `sfp_dnsneighbor` | `IP_ADDRESS` | `NETBLOCK_MEMBER` | Replace with `IP_ADDRESS` seed |
| `sfp_dnszonexfer` | `PROVIDER_DNS` | `DOMAIN_NAME` | Add `PROVIDER_DNS` seed |
| `sfp_hosting` | `IP_ADDRESS` | `TARGET_WEB_CONTENT` | Replace with `IP_ADDRESS` (AWS range) |
| `sfp_junkfiles` | `LINKED_URL_INTERNAL` | `INTERNET_NAME` | Add `LINKED_URL_INTERNAL` seed |
| `sfp_names` | `EMAILADDR` | `TARGET_WEB_CONTENT` | Route → `TARGET_WEB_CONTENT` |
| `sfp_phone` | `PHONE_NUMBER` | `TARGET_WEB_CONTENT` | Route → `TARGET_WEB_CONTENT` |
| `sfp_social` | `LINKED_URL_EXTERNAL` | `INTERNET_NAME` | Add `LINKED_URL_EXTERNAL` seed |
| `sfp_subdomain_takeover` | `AFFILIATE_INTERNET_NAME` | `INTERNET_NAME` | Add `AFFILIATE_INTERNET_NAME` seed |
| `sfp_tldsearch` | `INTERNET_NAME` | `DOMAIN_NAME` | Route → `DOMAIN_NAME`; extend timeout |

**Issue:** #804 (`SF-05-12`) (alignment) + per-module tuning in category batches.

### C — Seed tune (`clean_miss` on route nugget) — 12

` sfp_binstring`, `sfp_cookie`, `sfp_customfeed`, `sfp_errors`, `sfp_iban`, `sfp_intfiles`, `sfp_pageinfo`, `sfp_sslcert`, `sfp_strangeheaders`, `sfp_webanalytics`, `sfp_webframework`, `sfp_webserver`

Typical pattern: content/header extractors need richer upstream HTML or header fixtures. Many require a spider pass or synthetic `TARGET_WEB_CONTENT` / `WEBSERVER_HTTPHEADERS` with embedded markers.

**Issue:** #805 (`SF-05-13`) — Content extractor seed tuning batch.

### D — Ruby / WSL CLI — 3

| Module | Binary | Notes |
|--------|--------|-------|
| `sfp_tool_cmseek` | `cmseek` | Python + Ruby CMS detector; install in WSL |
| `sfp_tool_testsslsh` | `testssl.sh` | Bash + openssl; WSL recommended on Windows |
| `sfp_tool_whatweb` | `whatweb` | Ruby gem; WSL recommended |

See `.docs/analysis/wsl_ruby_cli_runbook.md`.

**Issue:** #806 (`SF-05-14`)

### E — Blocked native CLI — 3

| Module | Binary | Blocker |
|--------|--------|---------|
| `sfp_tool_nbtscan` | `nbtscan` | No reliable Windows build; WSL/apt or SPEC_GAP |
| `sfp_tool_onesixtyone` | `onesixtyone` | Same |
| `sfp_tool_wappalyzer` | `wappalyzer` | Legacy npm CLI deprecated; consider retire or WSL + fork |

**Issue:** #807 (`SF-05-15`)

### F — CLI seed tune — 1

`sfp_tool_testsslsh` — binary path + `INTERNET_NAME` target; depends on WSL install (bucket D).

## Workflow

```powershell
# Audit route vs seeds
poetry run python _tmp_route_audit.py   # or .seed/scripts/audit_quarantine_route_seeds.py

# Regenerate catalogue after override changes
poetry run python .docs/analysis/analyse_modules.py --quarantine-only --write-quarantine
poetry run python .seed/scripts/merge_quarantine_catalogue.py --write --staging-only

# Probe one module
poetry run python .seed/scripts/run_quarantine_battery.py --local --only sfp_dnsbrute --write

# Batch promote (after validation)
poetry run python .seed/scripts/run_quarantine_battery.py --local --timeout 300 `
  --only sfp_countryname sfp_dnsbrute sfp_dnsraw sfp_pgp sfp_similar sfp_tool_retirejs `
  --write --promote
```

## GitHub issues (created by `.seed/planning/create_quarantine_closure_issues.py`)

| Key | Title | Modules |
|-----|-------|--------:|
| SF-05-12 | Route seed alignment | 18 (buckets A+B) — **#804** |
| SF-05-13 | Content extractor seed tuning | 12 — **#805** |
| SF-05-14 | WSL Ruby CLI install | 3 — **#806** |
| SF-05-15 | Blocked native CLI resolution | 3 — **#807** |

Per-module issues remain in `stage5_quarantine_manifest.json` for deep work; closure epics track batch execution.

## Promotion guard

After `analyse_modules.py --quarantine-only`, always run `merge_quarantine_catalogue.py --write --staging-only` so promoted CLI modules are not dropped from `osint_services.json`.
