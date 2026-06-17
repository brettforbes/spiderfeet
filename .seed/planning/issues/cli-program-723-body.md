## Problem

SpiderFeet ships **13 bespoke `sfp_tool_*` Python modules** that wrap external CLIs. Each integration is hand-coded (subprocess args, parsers, opts). Operators cannot register new CLI tools without shipping code.

Battery results (#794): all 13 are `tool_missing_or_blocked` until binaries are installed and paths configured.

## Desired outcome

A **three-phase program**:

| Phase | Focus | Primary issues |
|-------|--------|----------------|
| **1** | Validate & promote existing 13 CLI wrappers | #733, #776–#788 |
| **2** | Generic CLI runner + manifest format + registry API | #796, #797, #798, #799 |
| **3** | Widget **Add Service** navbar tab — operator UI to register CLI tools | spiderfeet-widget #62, #65–#67 |

## Spec binding

- **R3-05-07** — promotion after route validation
- **R3-05-08** — custom OSINT / CLI service registration (manifest + UI)
- SPEC-003 Stage 5 quarantine program

## Non-goals (this epic)

- Cloud API service registration (separate from CLI; may share catalogue shape later)
- Arbitrary shell execution without manifest validation / path allowlisting
- Replacing bespoke modules where logic is non-declarative (Nmap netblocks, Nuclei templates) in Phase 2 — migrate incrementally only

## Phase 1 acceptance (batch #733)

- [ ] Install runbook for all 13 tools (Windows + Linux notes)
- [ ] Each tool: `module_opts` path configured; `run_quarantine_battery.py --local --only sfp_tool_*` → hit or documented negative
- [ ] Promoted to `external` + `in-test` or `service_state: error` with evidence
- [ ] Per-module quarantine issues closed with PR links

## Phase 2 acceptance

- [ ] Manifest schema documented and validated (JSON Schema)
- [ ] `sfp_tool_runner` executes manifest-defined tools with timeout + structured errors
- [ ] REST API: list/create/update/delete custom CLI manifests; probe install (`--version`)
- [ ] At least 3 existing tools migrated to manifest-only (candidates: dnstwist, wafw00f, snallygaster)

## Phase 3 acceptance

- [ ] Navbar tab **Add Service** (between Subscriptions and Tests or after Tests — operator choice in #65)
- [ ] Form: name, summary, executable path, consumed nugget, command template, output mapping preset
- [ ] Smoke test button → `scan_ui`; service appears on Maps + Tests after save
- [ ] GOV-08 exploratory pass on Add Service route

## Execution order

1. Complete Phase 1 (#733) before Phase 2 runner ships
2. Phase 2a schema (#796) before runner (#797)
3. Phase 2c API (#798) before widget wizard (#67)
4. Widget shell (#65) can start in parallel with Phase 2a

## Links

- Backend batch: #733
- Widget epic: [spiderfeet-widget#62](https://github.com/brettforbes/spiderfeet-widget/issues/62)
- Prior promotion work: #794
