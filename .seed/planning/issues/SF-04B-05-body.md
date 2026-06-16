## Problem statement

Pilot test seeds (`sbs.com.au`, `8.8.8.8`, etc.) are too generic. Many modules finish scans but return **zero produced nuggets** (e.g. `sfp_duckduckgo`). Test data that never produces output is useless for Stage 4 validation.

## Desired outcome

Replace one-size-fits-all nugget samples with a **module-validated seed registry**:

- Primary key: `(module_id, consumed_nugget_id)` → `input_value`
- Fallback: nugget-level sample only when module-specific seed absent
- Each seed must be a valid SpiderFeet target for the consumed type
- Seeds sourced from retuned `test_nugget_data.csv` (AU/UK/US) and module `route_seed_nugget`

## Epic

Parent: #61 [Epic] Stage 4b — Test nugget corpus

## Spec binding

- SPEC-002: **R2-04-07** (extends R2-04-02; SPEC_GAP — promote before implementation)

## Acceptance criteria

- [ ] `sample_target_for_module()` backed by registry file (e.g. `module_test_seeds.json` or CSV column `module_id`)
- [ ] `/tests/plan` and `/tests/modules/{id}` use registry values
- [ ] `nuggets_consumed_list.json` reviewed/updated for map alignment
- [ ] Document seed authoring process: tune until `scan_ui` returns `produced.length > 0` for smoke modules

## Verification

- Registry covers at least pilot set: 10 `none`-tier modules with documented expected produced types
- Unit tests for registry lookup and fallback

## Non-goals

- Automating seed discovery for all 177 modules in this story (see SF-04B-06)
