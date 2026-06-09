# Stage 4 — seed corpus, test semantics, and operator UI

**Spec:** R2-04-07, R2-04-08, R2-04-09 (SPEC-002)  
**Epic:** [#674](https://github.com/brettforbes/spiderfeet/issues/674) (none-tier seed research, closed 2026-06)

Agent-facing reference for Tests tab behaviour, seed registry, and map `service_state`.

---

## Corpus status (none-tier, 2026-06)

| Metric | Count | Meaning |
|--------|------:|---------|
| OSINT modules in catalogue | 177 | `osint_services.json` |
| None-tier validation pool | 87 | Free, no API key |
| **Smoke-validated** | **79** | Runnable in Tests UI with pass/fail semantics |
| **Upstream-blocked** | **8** | `service_state: error` — hidden from Tests/Subscriptions |
| **Research closed** | **87/87** | Every none-tier module has smoke seed or blocked annotation |

Positive smoke: **14** · Negative smoke: **65**

### Upstream-blocked modules (`service_state: error`)

Do **not** appear in Tests or Subscriptions APIs. Still in TypeDB map (filter in Maps UI is a follow-up).

| module_id | Root cause |
|-----------|------------|
| `sfp_dnsdumpster` | CSRF form removed from site |
| `sfp_sublist3r` | API empty/non-JSON |
| `sfp_searchcode` | API HTTP 404 |
| `sfp_myspace` | Search endpoint failures |
| `sfp_flickr` | API key scrape fails |
| `sfp_commoncrawl` | Index HTML parser broken |
| `sfp_crt` | crt.sh errors/rate limits |
| `sfp_s3bucket` | Scan exceeds practical timeout |

Fix track: **module implementation issues**, not seed tuning.

---

## Source-of-truth files

| Artifact | Path |
|----------|------|
| Module catalogue + `service_state` | `.docs/analysis/osint_services.json` |
| Per-module smoke seeds | `.docs/analysis/module_test_seeds.json` |
| Flat CSV export | `.docs/analysis/test_nugget_data.csv` |
| Research narrative | `.docs/analysis/pending_seed_research.md` |
| Pass JSON reports | `.docs/analysis/pending_seed_research_pass{2,3,finalize}.json` |

---

## Fixture kinds (R2-04-08)

| Kind | Pass condition | Registry flags |
|------|----------------|----------------|
| **positive** | `status=FINISHED` and `produced.length > 0` | `validated_produces: true` |
| **negative** | `status=FINISHED` and `module_execution.verdict = clean_miss` | `validated_negative: true`, `fixture_kind: negative`, `expected_absent_types` |

**Fail** when `verdict` is `error_failed`, `incomplete`, `absent_violation`, or scan does not finish.

Optional `positive_hit` sub-seed on negative rows for dirty-input confirmation during tuning.

`fixture_category` on TypeDB `osint-service` mirrors catalogue (`positive` / `negative` from blocklist-style modules).

---

## `scan_ui` target resolution

`POST /api/v1/scan_ui` uses `spiderfeet/api/services/scan_targets.py`:

- Regex-inferrable types: domain, IP, email, phone, quoted username, etc.
- **Catalogue types** (not CLI-regex): `COMPANY_NAME`, `PHYSICAL_ADDRESS`, `WEB_ANALYTICS_ID`, `LEI` — passed through to `SpiderFeetTarget` with explicit `target_type`.
- `USERNAME` without quotes: bare handles auto-quoted for scan start.

`SpiderFeetTarget._validTypes` includes catalogue types above.

---

## API surfaces

### Tests (`/api/v1/tests/*`)

- Lists only modules where `include_in_operator_ui(svc)` — excludes `service_state: error`.
- Plan rows expose `fixture_kind`, `seed_validated`, `expected_absent_types`.
- Summary includes `seed_validated_count`, `pending_seed_count`, `runnable_count`.

### Subscriptions (`/api/v1/subscriptions/*`)

- Same `error` exclusion (API-key modules only among visible set).

### Maps (`/api/v1/map/*`)

- **No** `error` filter yet — all services remain in graph export.

### Scan logs

- `GET /api/v1/scans/{scan_id}/logs` — diagnostics for failed probes and Tests UI.

### `module_execution` (in `scan_ui` response)

Verdicts: `hit`, `clean_miss`, `error_failed`, `incomplete`, `absent_violation`.  
Widget Tests tab uses `verdict === 'clean_miss'` for negative pass (not produced count alone).

---

## `service_state` (TypeDB + catalogue)

Allowed values: `in-test`, `favourite`, `unique`, `error`, `dominated` (schema `.seed/spiderfeet_map.tql`).

| State | Tests/Subscriptions | Maps (current) | Bootstrap default |
|-------|--------------------|----------------|-------------------|
| `in-test` | visible | visible | default for healthy modules |
| `error` | **hidden** | visible | upstream-broken set (`UPSTREAM_ERROR_MODULE_IDS`) |

**Sync script:** `.seed/scripts/sync_service_state.py --write [--typedb]`

**Code:** `spiderfeet/map/service_states.py` — `include_in_operator_ui()`, `UPSTREAM_ERROR_MODULE_IDS`

---

## Maintenance scripts

| Script | Purpose |
|--------|---------|
| `validate_test_seeds.py --tier none --write` | Batch smoke re-validation |
| `tune_test_seeds.py` | Generic candidate tuning |
| `research_pending_seeds.py` | Pass 1 live probes |
| `research_pending_seeds_pass2.py` | Negative fixtures + upstream notes |
| `research_pending_seeds_pass3.py` | Catalogue nugget probes + silent-search negatives |
| `research_pending_seeds_finalize.py` | Close last pending rows |
| `sync_fixture_category.py --write` | `fixture_category` in `osint_services.json` |
| `sync_service_state.py --write --typedb` | `service_state` in JSON + TypeDB |
| `backfill_expected_absent_types.py` | Negative registry fields |
| `split_negative_positive_hit.py` | Dual-seed split |

Run probes against API: `.\start.ps1 -Mode api` (port 8001).

---

## Adding or changing a seed

1. Probe with `spiderfeet/map/seed_probe.py` or `POST /scan_ui` + `GET /scans/{id}/logs`.
2. Classify positive vs negative (blocklist / silent-search → negative).
3. Merge via `merge_validation_results_into_registry()` or research scripts with `--write`.
4. Re-run `validate_test_seeds.py` for the tier.
5. If upstream is dead: set `upstream_blocked` + `validation: blocked-upstream` in seeds **and** `service_state: error` in catalogue; run `sync_service_state.py`.

---

## Git / delivery note

**Landed** 2026-06-09: spiderfeet PR [#707](https://github.com/brettforbes/spiderfeet/pull/707) → `develop`, promotion [#708](https://github.com/brettforbes/spiderfeet/pull/708) → `master`. Widget [#56](https://github.com/brettforbes/spiderfeet-widget/pull/56) / [#57](https://github.com/brettforbes/spiderfeet-widget/pull/57).
