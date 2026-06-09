# SPEC-003 — Stage 5: Quarantine service conversion

**Status:** Draft (operator-approved program start)  
**Supersedes scope gap:** SPEC-002 non-goals (quarantine)  
**Plan:** `.seed/planning/STAGE5_QUARANTINE_PROGRAM.md`  
**Module inventory:** `.docs/quarantine_modules.md` (54 modules)

## Objective

Promote verified quarantined modules into first-class **osint-service** catalogue + TypeDB map records, with icons, subscription classification, fixture polarity, seeds, and Stage-4-parity route testing. Retire or fix modules that fail validation.

## Requirements

| ID | Stage | Requirement |
|----|-------|-------------|
| R3-05-01 | 5 | Extend catalogue schema for quarantine-origin services (`service_origin`, synthetic `data_source` for local/tool modules) |
| R3-05-02 | 5 | Each quarantine module has a full `osint_services.json` record: consumed/produced nuggets, `access_tier`, `fixture_category`, `module_opts`, `service_state` |
| R3-05-03 | 5 | Each service has `data_source` metadata (website or `spiderfeet://local/{module_id}`) and `fav_icon` / service icon asset |
| R3-05-04 | 5 | Generate missing service icons (SVG) for local and CLI-tool modules; copy to widget `src/assets/icons/` |
| R3-05-05 | 5 | Bootstrap TypeDB map for all promoted services; quarantine services visible on Maps/Tests with distinct styling until promoted |
| R3-05-06 | 5 | Per-module route seeds in `module_test_seeds.json`; positive/negative fixtures per R2-04-08 semantics |
| R3-05-07 | 5 | Module test passes (or documented `service_state: error` / deletion) before promotion from `quarantine` to `external` origin |
| R3-05-08 | 5 | **SPEC_GAP follow-up:** Custom OSINT service registration — spike for operator/user-defined services (with or without API keys) |

## Service record contract (minimum)

```json
{
  "module_id": "sfp_dnsresolve",
  "service_origin": "quarantine",
  "name": "DNS Resolver",
  "summary": "...",
  "flags": [],
  "access_tier": "none",
  "data_source": {
    "website": "spiderfeet://local/sfp_dnsresolve",
    "model": "LOCAL_NOAUTH",
    "description": "...",
    "fav_icon": "/icons/icon_service_dnsresolve.svg"
  },
  "consumed_nuggets": ["INTERNET_NAME"],
  "produced_nuggets": ["IP_ADDRESS"],
  "fixture_category": "positive",
  "service_state": "in-test",
  "module_opts": []
}
```

## Access tier rules (quarantine)

| Pattern | `access_tier` | Notes |
|---------|---------------|-------|
| Pure local DNS/parse/extract | `none` | No external API |
| Optional feed file / API key in opts | `free_auth` or `paid_auth` | e.g. `sfp_customfeed` |
| External CLI tool (no cloud API) | `none` | Tool must be installed; document in `data_source` |
| Tool with cloud API component | per provider | Rare; case-by-case |

## Exit criteria (Stage 5)

- All 54 quarantine modules: **promoted**, **`error`**, or **removed** with tracked rationale
- Maps + Tests exercise every viable route for promoted modules
- Widget distinguishes quarantine vs external services (visual + filters)
- Custom-service spike delivered with recommended architecture (issue closure)

## Non-goals (this spec)

- Favourites / sequences (Stage 6)
- TypeDB storage replacement (Stage 7)
- Main investigation UI (Stage 8)

## Verification

- Extend `analyse_modules.py` / validation scripts for quarantine records
- `pytest .tests/map` + API route tests per module issue
- GOV-08 exploratory pass on Maps/Tests for quarantine services
