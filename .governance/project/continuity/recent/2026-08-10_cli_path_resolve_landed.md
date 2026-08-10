# Continuity — CLI path resolve landed (2026-08-10)

## Problem

v2 `modules_v2._base.resolve_executable` was PATH/WSL-only. Twin-fork binaries live under
gitignored `.tools/bin/` (and `.tools/pius`), so workflow step 1 failed with
`subfinder not found on PATH (native or WSL)`. An earlier local fix was never committed
and was lost during SPEC-015.

## Landed

| Item | Status |
|------|--------|
| PR [#1245](https://github.com/brettforbes/spiderfeet/pull/1245) — `.tools/` lookup in `_base` | Merged |
| Hardening — `_base` delegates to `spiderfeet.tools.cli_paths.resolve_cli_binary` | This follow-up |
| CI-discoverable regression — `modules_v2/tests/test_resolve_executable.py` | This follow-up |
| yaml-workflow-widget [#265](https://github.com/brettforbes/yaml-workflow-widget/pull/265) tooltip UI | Merged |
| yaml-workflow-widget [#264](https://github.com/brettforbes/yaml-workflow-widget/pull/264) fit 70%/10px | Merged |
| SPEC-015 Epics A/B/C (+ D1) PRs | Merged on all three repos |

## Operator note

Restart FastAPI after pulling (no `--reload`); port 8001 must be free.

## Residual (not landed from pre-SPEC-015 stashes)

Widget stash previously held `CliScanApp.beforeExecute` / `ComposerTempGraph.hydrateFromServer`
that are **not** on current `develop` (Run Workflow already syncs YAML; Scan Now async path
does not use `beforeExecute`). Stashes dropped after this cleanup — reopen from transcript
if that Scan Now YAML-sync hook is still desired.
