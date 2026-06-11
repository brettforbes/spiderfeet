# Analysis artefacts (current state)

**As of 2026-06-11** — Stage 4–5 catalogue and test registry. Interim session files from battery runs have been removed.

## Operator reference (UI)

| Path | Purpose |
|------|---------|
| [`.docs/osint-services/OVERVIEW.md`](../osint-services/OVERVIEW.md) | Tables by collection (API ±, local, CLI, other) |
| [`.docs/osint-services/modules/`](../osint-services/modules/) | One markdown file per module |

Regenerate: `poetry run python .seed/scripts/generate_osint_service_docs.py`

## Canonical JSON

| File | Purpose |
|------|---------|
| `osint_services.json` | 231 OSINT services — routes, tiers, `service_origin`, `service_state` |
| `module_test_seeds.json` | Stage 4b test seeds and smoke validation markers |
| `quarantine_services.json` | Empty — quarantine programme complete |
| `quarantine_catalogue_overrides.json` | Route-seed overrides for promoted modules |
| `test_nugget_data.csv` | Corpus export for none-tier validated seeds |

## Generators and maintenance

| Script | Purpose |
|--------|---------|
| `.docs/analysis/analyse_modules.py` | Regenerate catalogue from `modules/sfp_*.py` |
| `.seed/scripts/fix_catalogue_service_origins.py` | Normalize `service_origin` in JSON |
| `.seed/scripts/merge_quarantine_catalogue.py` | Merge quarantine staging into main catalogue |
| `.seed/scripts/generate_osint_service_docs.py` | Build `osint-services/` docs |
| `.seed/scripts/audit_local_module_network.py` | Audit local modules for HTTP/DNS patterns |

## `service_origin` semantics

| Value | Meaning |
|-------|---------|
| `external-api` | Module declares `meta.dataSource` (third-party OSINT API) |
| `local` | No `dataSource` — DNS, parsing, crawl, reference datasets |
| `cli` | `sfp_tool_*` subprocess wrapper |

**Local modules with HTTP** (e.g. GitHub fingerprint JSON, keyservers) are still `local` unless they declare a third-party OSINT `dataSource`. See `local_module_network_audit.json` for the static audit.

## Test coverage (none-tier, operator UI)

- **121/121** modules with route-seed validation or documented `upstream_blocked` / `error`
- **Quarantine:** 0 modules remaining
- **`sfp_tool_wappalyzer`:** `service_state: error` (legacy OSS CLI retired)

## Assets (unchanged)

- `nugget_icons/`, `osint-service-icons/` — SVG assets for map/UI
- `force_graph_colour_scheme.md` — D3 graph colours
- `generic_icon_design_briefs.md` — Icon design notes

## Runbooks

- `cli_tool_install_runbook.md` — CLI tool install (incl. WSL)
- `wsl_ruby_cli_runbook.md` — WSL Ubuntu-22.04 batch for quarantine CLIs
