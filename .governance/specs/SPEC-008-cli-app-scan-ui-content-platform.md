# SPEC-008 — CLI/API Scan UI: content platform, reusable 5-tab component, live execute

**Status:** Active
**Parent coordination:** [#826](https://github.com/brettforbes/spiderfeet/issues/826) (CLI Profiling), follow-on to SPEC-004/005/006/007
**Plan / agent playbook:** `.governance/project/SPEC008_AGENT_PLAN.md`
**Content contract / quality bar:** `.governance/project/SPEC008_CONTENT_CONTRACT.md`
**Issue index (backend):** `.governance/project/SPEC008_ISSUE_INDEX.md`
**Issue index (widget):** `@spiderfeet-widget/.governance/project/SPEC008_WIDGET_ISSUE_INDEX.md`
**Source prompt:** `.seed/15_CLI_App_UI.md`

## Objective

Turn the CLI Profiling examination UI into a **generic, reusable "5-tab mini app"** (Scan · Text · Structured Data · Graph · Report) that can render or drive **any** CLI tool or API service, backed by a **content platform** that serves three canonical reference documents per tool/service — options, Zero-to-Hero guide, proposed nugget graph structure — from a single scalable location (`modules_v2/content/<tool_id>/`), file-based today, TypeDB-backed later without changing the API contract.

Two consumers of the same component:

1. **CLI Profiling Single Scan page** (existing) — view-only mode, sourced from `.docs/docs-for-cli-tools/` examination bundles + the new content platform.
2. **Composer page** (new, currently a disabled nav stub) — edit-and-run mode, sourced from the content platform + a new live Execute API.

## Non-goals

- Migrating content storage to TypeDB (file-based `modules_v2/content/` is the interim source of truth; API contract must not need to change when that migration happens later).
- Rewriting production `sfp_*` modules.
- Building a general workflow/DSL runtime (that is SPEC-007's scope — this SPEC may later call SPEC-007 drivers but does not depend on them).
- Free-form/arbitrary CLI argv execution from the UI (Epic X locks a strict allowlist model — see R8-08).
- Onboarding new CLI tools beyond the 8 already-formally-examined adapter tools (nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei). New tools follow `.seed/scripts/cli_corpus/ONBOARDING.md` (updated by R8-07) and pick up the content bundle automatically once onboarded.

## Requirements

### Content platform (backend)

| ID | Requirement |
|----|-------------|
| R8-01 | `modules_v2/content/<tool_id>/` directory contract defined and checked in (`.governance/project/SPEC008_CONTENT_CONTRACT.md`): `manifest.json`, `options.md`, `options_schema.json`, `zero_to_hero.md`, `graph_structure.md` |
| R8-02 | `options_schema.json` format spec defined: machine-readable flag list (`id`, `flag`, `aliases`, `label`, `description`, `type`, `default`, `required`, `choices`, `group`, `placeholder`, `advanced`) sufficient to drive the Scan tab form generator without further parsing |
| R8-03 | Content bundles backfilled for all 8 existing adapter tools into `modules_v2/content/<tool_id>/`, `options_schema.json` reviewed by a human-legible spot check (not blind heuristic output) |
| R8-04 | FastAPI `GET /api/v1/content/tools`, `GET /api/v1/content/tools/{id}`, `GET /api/v1/content/tools/{id}/options`, `GET /api/v1/content/tools/{id}/options-schema`, `GET /api/v1/content/tools/{id}/zero-to-hero`, `GET /api/v1/content/tools/{id}/graph-structure` implemented, designed to scale to ≥200 API services and ≥30 CLI apps (no O(n) full-directory rescans per request; mtime-keyed in-memory cache) |
| R8-05 | pytest coverage for content routes; OpenAPI examples accurate for at least 2 tools |
| R8-06 | `cli_corpus` service's `graph-structure` resolution prefers the content platform bundle when present, falls back to legacy `nugget_structure/` path unchanged (no regression for existing 8-tool examination pages) |
| R8-07 | `.seed/scripts/cli_corpus/ONBOARDING.md` + `proj-06`/`proj-07` rule pointers updated: onboarding/formal-examination is incomplete without a `modules_v2/content/<tool_id>/` bundle |

### Live execute (backend, Phase 2 — gated)

| ID | Requirement |
|----|-------------|
| R8-08 | Execute safety design doc locks a **strict allowlist model**: only flags present in the tool's `options_schema.json` are accepted, the resulting command is built as an **argv array** (never a shell string), and target values are checked against an explicit target-class allowlist/confirmation step before dispatch. This design doc requires an **explicit operator sign-off comment** on its GitHub issue before any execute-endpoint code is written. |
| R8-09 | `POST /api/v1/content/tools/{id}/execute` + `GET /api/v1/content/tools/{id}/runs/{run_id}` implemented per the signed-off R8-08 design; async job execution, run status (`queued`/`running`/`complete`/`error`), started/finished timestamps |
| R8-10 | On run completion, the existing adapter `build_outputs` four-output pipeline (per `proj-07`) runs against the captured output and results are stored under a distinct run-evidence path (not mixed into the formal examination corpus under `app_examination_docs/`) |
| R8-11 | Security/injection pytest suite: shell-metacharacter payloads, disallowed flags, and disallowed targets are all rejected before dispatch; suite must pass before Epic X is considered done |

### Widget component (frontend, `spiderfeet-widget`)

| ID | Requirement |
|----|-------------|
| R8-12 | Reusable `window.Widgets.CliScanApp` component: five-tab shell (Scan/Text/Structured/Graph/Report), config-driven (`mode: 'view' \| 'edit-run'`), registered per the existing namespace/`watchDOMForComponent` convention, wired into webpack |
| R8-13 | Scan tab dynamic form renderer consumes `options_schema.json`: string→text, boolean→checkbox, integer/float→number, fixed-choice→select, path→text+browse-hint; required flags get a red asterisk; >10 flags grouped into collapsible sections; live **Command Preview** panel reflects current field values |
| R8-14 | Right rail: Execute button (wired to `POST .../execute` when `mode: 'edit-run'`, disabled/hidden in `view` mode), three modal buttons (`Options`, `Graph Structure`, `User Guide`) rendering the three content-platform documents via `Widgets.Markdown`, created/progress/finished timestamps, and a progress bar while a run is active |
| R8-15 | Text/Structured/Graph/Report tabs extracted from `profiling.js` into the shared component using the existing `DataViewerHost`, `Viz.ForceGraph`, and `Widgets.Markdown` contracts — **no duplicated rendering logic** between the old and new code paths |
| R8-16 | Dark/light theme integration (`Widgets.Theme`) and a basic accessibility pass (labelled inputs, `aria-*` on tabs/modals) |
| R8-17 | CLI Profiling **Single Scan** page (`#pane-profiling` detail view) cut over to `CliScanApp` in `view` mode for all 8 existing tools / all existing scenarios, sourced from `/cli-corpus` + `/content` APIs |
| R8-18 | Exploratory regression review (GOV-08 scenario matrix) across every tool/scenario combination post-cutover; classified `Validated`/`Invalidated`/`Blocked`/`Uncovered-spec-gap` per scenario with tracked follow-ups for anything not `Validated` |
| R8-19 | Composer page (replace the disabled nav stub) wired to `CliScanApp` in `edit-run` mode against the content platform + Execute API; **blocked on R8-08 operator sign-off and R8-09/R8-10 backend completion** |
| R8-20 | Exploratory review (GOV-08) of the Composer live-run flow; completeness label recorded |

## Milestone (what "done" looks like for the operator)

**Phase 1 (content platform + view-only cutover — R8-01…R8-07, R8-12…R8-18):** Opening CLI Profiling → any of the 8 tools → any scenario shows the new 5-tab component; the Scan tab renders the tool's real options as a read-only form matching the command actually used to produce that scenario's evidence; Options/Graph Structure/User Guide modals open the three content-platform documents; Text/Structured/Graph/Report tabs are pixel-equivalent in information content to the current `profiling.js` rendering. **This is the "see the results in the scans for each examination scenario" milestone the operator asked for.**

**Phase 2 (live execute + Composer — R8-08…R8-11, R8-19…R8-20):** Composer page lets an operator fill in a tool's options, see a live command preview, click Execute, watch progress, and land on the same 5-tab view once the run completes — gated behind the signed-off safety design.

## Architecture

```text
modules_v2/content/<tool_id>/
  manifest.json          → tool_id, display_name, kind (cli|api), category, executable, content_version
  options.md             → copy of *-CLI-Options.md (raw --help-derived reference)
  options_schema.json    → machine-readable form-driving schema (R8-02)
  zero_to_hero.md         → copy of *-Zero-to-Hero.md
  graph_structure.md     → copy/symlink of nugget_structure/<tool>_nugget_graph_structure.md

spiderfeet/api/routes/content.py       → new FastAPI router, prefix /content
spiderfeet/api/services/content.py     → registry + bundle loader, mtime cache

spiderfeet-widget/src/js/cli-scan-app.js   → window.Widgets.CliScanApp (new reusable component)
spiderfeet-widget/src/js/profiling.js      → refactored to host CliScanApp in view mode
spiderfeet-widget/src/html/content.html    → Composer pane added; Profiling detail delegates to component
```

## Traceability

Implementation: GitHub epics under `[SPEC-008]` — backend in `brettforbes/spiderfeet`, frontend in `brettforbes/spiderfeet-widget` (see both issue indexes). Epic letters `V`–`AA` (continuing after SPEC-007's `P`–`U`).
