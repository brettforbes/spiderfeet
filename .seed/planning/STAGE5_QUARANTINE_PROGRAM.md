# Stage 5 — Quarantine service conversion program

**Epic (backend):** GitHub issue created as `EPIC-SF-05`  
**Spec:** `.governance/specs/SPEC-003-stage5-quarantine.md`  
**Inventory:** 54 modules in `.docs/quarantine_modules.md`

## Executive summary

Stage 4 validated **177 external OSINT services** already in `osint_services.json`. Stage 5 adds the **54 quarantined modules** (no `dataSource` in module meta today) to the same map/tests/subscriptions model, proves each route, then promotes or retires them.

This is **not** a single PR — it is a phased program with framework work first, then category batches, then per-module delivery.

## Phases

### Phase 0 — Governance & schema (blocks everything)

| Deliverable | Issue key |
|-------------|-----------|
| SPEC-003 finalized | SF-05-01 |
| `service_origin` field, `LOCAL_NOAUTH` model, merge strategy | SF-05-01 |
| Extend `analyse_modules.py` for quarantine extraction | SF-05-02 |
| Bootstrap + sync scripts updated | SF-05-02 |

### Phase 1 — Icons & catalogue shell

| Deliverable | Issue key |
|-------------|-----------|
| Icon naming convention `icon_service_{slug}.svg` | SF-05-03 |
| Favicon URL where external brand exists (whois, nmap, etc.) | SF-05-03 |
| Generated SVG for pure-local modules | SF-05-03 |
| Copy icons spiderfeet → spiderfeet-widget | SF-05-03 |

### Phase 2 — Category conversion (parallel after Phase 0–1)

Each category issue owns a module checklist. Per module:

1. Read `watchedEvents()` / `producedEvents()` from `modules/sfp_*.py`
2. Build `osint_services.json` row (or `quarantine_services.json` staging → merge)
3. Classify `access_tier` (none / free_auth / paid_auth)
4. Set `fixture_category` (positive vs negative) via smoke probe
5. Add `module_test_seeds.json` entries
6. Run Tests tab / API route test; tune seed input
7. Set `service_state`: `in-test` | `error` | delete module

| Category | Modules | Issue |
|----------|--------:|-------|
| DNS & Domain Intelligence | 10 | SF-05-04 |
| Web Crawling & Scanning | 6 | SF-05-05 |
| Content Analysis & Extraction | 21 | SF-05-06 |
| Social & Identity | 2 | SF-05-07 |
| Reputation | 1 | SF-05-08 |
| Public Registries | 1 | SF-05-09 |
| External Tool Wrappers | 13 | SF-05-10 |

### Phase 3 — Widget parity

| Deliverable | Issue key |
|-------------|-----------|
| Map: quarantine service colour/ring/filter | SFW-05-01 |
| Tests: quarantine modules in plan | SFW-05-02 |
| Subscriptions: only when `access_tier` requires keys | SFW-05-02 |

### Phase 4 — Custom service registration (spike)

| Deliverable | Issue key |
|-------------|-----------|
| Architecture options doc | X-05-01 |
| Backend API sketch (CRUD custom service defs) | SF-05-11 |
| Widget UI wireframes / spike | SFW-05-03 |

**Recommended approach (spike hypothesis):**

- Store custom definitions in TypeDB (`custom-osint-service` entity) or JSON catalogue extension
- Fields mirror `osint_services.json` + optional Python module path or webhook URL
- Subscriptions API already supports secret opts — reuse for custom API keys
- Widget: “Add service” drawer on Subscriptions or Maps admin panel
- **Non-goal for v1:** arbitrary user-uploaded Python modules (security); prefer declarative HTTP templates or admin-only module paths

## Per-module issue template

Each of 54 modules gets `[Quarantine] {module_id}: {name}` with:

- Category + epic links
- Checklist (catalogue, icon, seeds, tests, promotion)
- Spec: R3-05-02, R3-05-06, R3-05-07

## Dependencies

- Stage 4 corpus machinery (`module_test_seeds.json`, `module_execution.verdict`, `sync_service_state.py`)
- TypeDB `spiderfeet-map` bootstrapped
- API + widget running (ports 8001 / 4001)

## Risks

| Risk | Mitigation |
|------|------------|
| Tool modules need CLI on host | Document `tool` flag; skip or `error` in CI |
| Content extractors need `TARGET_WEB_CONTENT` upstream | Chain seeds / composite test scans |
| 21 content modules = large batch | SF-05-06 split into sub-PRs per module issue |
| No SPEC until now | SF-05-01 gates implementation |

## Suggested execution order

1. SF-05-01 → SF-05-02 → SF-05-03 (serial)
2. SF-05-04 DNS (highest backlog priority per BL-009)
3. SF-05-05 crawling (spider, intfiles — feeds content extractors)
4. SF-05-06 content (depends on crawl outputs)
5. SF-05-10 tools (parallel where CLI available)
6. X-05-01 / SF-05-11 / SFW-05-03 custom service spike (can run parallel to late Phase 2)

## Module manifest

See `.seed/planning/stage5_quarantine_manifest.json` (generated with issue IDs after bootstrap).
