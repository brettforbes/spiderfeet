# Module test seed registry (Stage 4b)

**File:** `module_test_seeds.json`  
**Requirement:** R2-04-07  
**Issue:** SF-04B-05

## Purpose

Replace generic nugget defaults (`sbs.com.au`, `8.8.8.8` everywhere) with **module-specific** scan targets keyed by `(module_id, consumed_nugget_id)`.

The Tests tab and `/tests/plan` call `sample_target_for_module()`, which reads this registry first, then falls back to nugget-level samples in `test_targets.py`.

## Authoring process

1. Pick a module with `subscription_tier: none` (or configure API keys first for auth modules).
2. Identify the `consumed_nugget_id` for the test row (from `osint_services.json`).
3. Choose a realistic target in **AU**, **UK**, or **US** (or `global` for crypto/hash types).
4. Run a smoke check against `POST /api/v1/scan_ui` with `wait: true` and confirm `produced.length > 0`.
5. Add or update the entry in `module_test_seeds.json`:
   - `validation`: `smoke` when manually verified; `pilot` when best-guess pending SF-04B-06 corpus pass.
   - `expected_produced_nugget_ids`: from module `produced_nuggets` in catalog (documentation only).

## Pilot set (10 `none`-tier modules)

| module_id | primary seed | region | validation |
|-----------|--------------|--------|------------|
| sfp_duckduckgo | `bbc.co.uk` / INTERNET_NAME | UK | smoke |
| sfp_robtex | `8.8.8.8` / IP_ADDRESS | US | smoke |
| sfp_blockchain | genesis BTC address | global | smoke |
| sfp_arin | `arin.net` / DOMAIN_NAME | US | smoke |
| sfp_bgpview | `8.8.8.8` / IP_ADDRESS | US | pilot |
| sfp_crt | `google.com` / DOMAIN_NAME | US | pilot |
| sfp_hackertarget | `8.8.8.8` / IP_ADDRESS | US | pilot |
| sfp_wikipediaedits | `91.198.174.192` / IP_ADDRESS | EU | pilot |
| sfp_threatcrowd | `google.com` / INTERNET_NAME | US | pilot |
| sfp_zoneh | `zone-h.org` / INTERNET_NAME | US | pilot |

Full corpus tuning is **SF-04B-06** (177 modules).

## Corpus validation (SF-04B-06)

**CSV:** `test_nugget_data.csv` — columns: `module_id`, `consumed_nugget_id`, `region`, `input_value`, `validated_produces`, `notes`

**Script:**

```powershell
poetry run python .seed/scripts/validate_test_seeds.py --tier none --write
poetry run python .seed/scripts/validate_test_seeds.py --tier none --offset 35 --write   # batch 2
poetry run python .seed/scripts/validate_test_seeds.py --tier none --offset 60 --write   # batch 3
```

Writes `.docs/analysis/test_seed_validation_report.json` (batch + cumulative registry stats) and optionally updates the registry + CSV when `--write` is passed. Target for `none` tier: ≥60% `validated_produces` (strict pass = `FINISHED` + `produced.length > 0`).

**Cumulative status (2026-06-06):** 10/87 none-tier modules smoke-validated (~11.5%). Blocklist/threat modules often produce zero on clean inputs (`8.8.8.8`, `sbs.com.au`) — tune seeds or mark `negative-fixture` in follow-up.

## Fallback order

1. Registry `(module_id, consumed_nugget_id)`
2. Module `route_seed_nugget` nugget sample (when consumed matches)
3. Generic nugget sample map in `test_targets.py`
