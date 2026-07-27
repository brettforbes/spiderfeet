# SPEC-008 agent plan — CLI/API Scan UI: content platform + reusable component + live execute

**Spec:** `.governance/specs/SPEC-008-cli-app-scan-ui-content-platform.md`
**Content contract:** `.governance/project/SPEC008_CONTENT_CONTRACT.md`
**Issue index (this repo):** `.governance/project/SPEC008_ISSUE_INDEX.md`
**Issue index (widget repo):** `@spiderfeet-widget/.governance/project/SPEC008_WIDGET_ISSUE_INDEX.md`
**Source prompt:** `.seed/15_CLI_App_UI.md`
**Audience:** Lesser agents — **one child issue at a time**, fully autonomous unless a hard gate says otherwise

---

## 0. Autonomous execution protocol (read this before picking up any SPEC-008 issue)

The operator has explicitly pre-authorized fully autonomous execution for SPEC-008 work: no human review wait is required before merging, because `develop` on both `brettforbes/spiderfeet` and `brettforbes/spiderfeet-widget` has no branch-protection review requirement. This does **not** relax GOV-02/GOV-06 evidence standards — it removes the *waiting*, not the *rigor*.

For **every** SPEC-008 child issue, follow this loop exactly:

1. **Start:** Comment on the issue: "Starting <code> — <one-line intent>." Move the issue to `In progress` on the board if a board is configured.
2. **Branch:** `git checkout develop && git pull && git checkout -b feature/<issue-number>-<slug>`. Branch from `develop` only (GOV-02-GIT-004A) — never stack on another feature branch.
3. **Implement:** Do only the scope listed on the issue. Do not expand scope silently (GOV-02 scope discipline). If you discover adjacent gaps, note them in the issue comment and file a **separate** follow-up issue instead of scope-creeping.
4. **Verify:** Run every command in the issue's "Verification" section. Do not skip verification because "it looks right."
5. **Comment evidence:** Paste the verification command(s) and their pass output (or a summary if very long) as an issue comment **before** opening the PR.
6. **Commit + push:** Conventional commit message referencing the issue number.
7. **Open PR to `develop`:** Title references the issue; body links the issue, cites the SPEC-008 requirement IDs, and repeats the verification evidence. Use `gh pr create --base develop`.
8. **Self-merge:** Once the PR is open and any required CI checks (if configured) are green, merge it yourself: `gh pr merge --squash --delete-branch`. Do not wait for a human reviewer — this is the operator-approved default for SPEC-008. The two exceptions are listed in §0.1 below.
9. **Close the loop:** Comment the final outcome on the issue (PR link, commit SHA, verification evidence), then close the issue (`gh issue close <n> --comment "..."` or let the PR's `Closes #<n>` do it — either way, confirm it actually closed).
10. **Update the index:** Mark the row `done` (with PR link) in the relevant `SPEC008_*_ISSUE_INDEX.md`.
11. **Return to `develop`:** `git checkout develop && git pull`. Never leave the repo parked on a stray branch at the end of a work unit (GOV-02-GIT-004E/F).
12. **Pick the next unblocked child** in execution order (§2) and repeat.

### 0.1 The only two hard gates in SPEC-008

- **Epic X (Live Execute API) issue X1** requires an **explicit operator sign-off comment on issue X1 itself** before X2 may start. Do not infer sign-off from silence, from a merged PR, or from a different issue. If X1 is open with no operator comment approving the design, **stop and escalate** — do not begin X2.
- **Widget Epic AA (Composer live-run wiring)** issue AA2 is blocked on backend X3 being merged **and** the same X1 sign-off having occurred (AA2 consumes the execute API that only exists once the gate clears). Everything else in SPEC-008 (V, W, Y, Z, AA1) proceeds with full autonomy per §0.

Everything else — including opening, merging, and closing PRs for Epics V, W, Y, Z, and AA1/AA3 — requires **no** additional human approval beyond what is already in this plan.

### 0.2 Forbidden (all SPEC-008 issues)

- Do not build a shell-string execute path — argv arrays only (R8-08).
- Do not skip `options_schema.json`'s `review_log` reconciliation — an unreviewed heuristic schema is not `Pass` (SPEC008_CONTENT_CONTRACT §2).
- Do not duplicate Text/Structured/Graph/Report rendering logic between `profiling.js` and the new `CliScanApp` component — extract and share (R8-15).
- Do not invent a new tool-id namespace — reuse `cli_corpus` / `corpus_index.json` ids.
- Do not touch production `sfp_*` modules under this SPEC.
- Do not re-scan the full content directory tree per API request once caching is in place (R8-04).
- Do not mark Epic X done without the R8-11 security/injection pytest suite passing.

---

## 1. Epic map

| Repo | Epic | Code | Intent | Children |
|------|------|------|--------|----------|
| spiderfeet | Content platform foundation | **V** | Content contract, options-schema generator, backfill 8 tools | V0–V2 |
| spiderfeet | Content APIs | **W** | FastAPI `/content/*` routes, tests, backward-compat bridge, onboarding docs | W1–W4 |
| spiderfeet | Live execute API (gated) | **X** | Safety design + execute endpoint + pipeline wiring + security tests | X1–X4 |
| spiderfeet-widget | Reusable CliScanApp component | **Y** | 5-tab component, dynamic form, right rail, shared tab rendering, theme | Y1–Y5 |
| spiderfeet-widget | Cutover CLI Profiling | **Z** | Wire Single Scan page to component, regression review | Z1–Z2 |
| spiderfeet-widget | Composer + live execute wiring (gated) | **AA** | Composer scaffold, execute wiring, exploratory review | AA1–AA3 |

## 2. Execution order (cross-repo)

```text
V0 -> V1 -> V2
  -> W1 -> W2 -> W3 -> W4

Y1 -> Y2 (after W1) -> Y3 -> Y4 (parallel with Y2/Y3, needs only Y1) -> Y5
  -> Z1 (after Y5 + W3) -> Z2

X1 [OPERATOR SIGN-OFF GATE] -> X2 -> X3 -> X4

AA1 (after Y5, no backend blocker) -> AA2 (after AA1 + X3 signed off) -> AA3
```

Backend (V/W) and widget (Y1/Y4) can proceed in parallel from day one. Y2/Y3 wait on W1 landing (they need a real content API to integrate against, not just a mock). Z waits on both sides. X is independent of V/W/Y/Z except for reusing the adapter pipeline (R8-10) — it can be designed (X1) at any time, but implementation (X2+) should not race ahead of the operator sign-off.

---

## Epic V — Content platform foundation

### V0 — Gap inventory vs content contract

**Do**
1. For each of the 8 adapter tools, check what already exists under `.docs/docs-for-cli-tools/` matching the 5 contract files in `SPEC008_CONTENT_CONTRACT.md` §1 (options.md and Zero-to-Hero already exist for all 8 per the 2026-07 audit; graph_structure.md exists per SPEC-006; `manifest.json` and `options_schema.json` do not exist yet anywhere).
2. Write `.governance/project/SPEC008_CONTENT_GAP_INVENTORY.md`: one row per tool, one column per contract file, `Have`/`Missing`/`Needs regen`.

**Verify:** File checked in; all 8 tools listed; every cell filled (no blanks).

### V1 — `options_schema.json` generator

**Do**
1. `.seed/scripts/cli_corpus/generate_options_schema.py --tool <id>` — parses `modules_v2/content/<id>/options.md` (or the `.docs/docs-for-cli-tools/<Tool>-CLI-Options.md` source before backfill) into a draft `options_schema.json` per the format in `SPEC008_CONTENT_CONTRACT.md` §2.
2. Emit `options_schema.review.md` alongside it, listing every flag the heuristic parser could not confidently type/describe.
3. Unit test the parser against 2 tools with different flag styles (e.g. `nmap` single-dash/double-dash mix, `httpx` all-double-dash) — assert required fields are non-null and `choices` is populated whenever `type == "select"`.

**Verify:**
```bash
poetry run python .seed/scripts/cli_corpus/generate_options_schema.py --tool nmap
poetry run pytest .tests/test_generate_options_schema.py -q
```

### V2 — Backfill content bundles for all 8 adapter tools

**Do**
1. For each of nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei: create `modules_v2/content/<id>/` with `manifest.json`, `options.md` (copy), `zero_to_hero.md` (copy), `graph_structure.md` (copy), and `options_schema.json` generated via V1 **with every `review_log` entry resolved** (fill in `description`/`type`/`group` by hand where the generator flagged uncertainty — do not leave placeholders).
2. This is one issue with a checklist of 8 tools; it is not done until all 8 are `Pass` on `SPEC008_CONTENT_CONTRACT.md` §1.

**Verify:**
```bash
poetry run python -c "import json,glob; [print(p, json.load(open(p))['tool_id']) for p in glob.glob('modules_v2/content/*/manifest.json')]"
# manual: options_schema.review.md has zero unresolved entries for each of the 8 tools
```

---

## Epic W — Content APIs

### W1 — FastAPI `/content/*` routes + service layer

**Do**
1. `spiderfeet/api/services/content.py`: registry loader keyed by `tool_id`, in-memory cache invalidated by directory mtime (see anti-pattern warning in `SPEC008_CONTENT_CONTRACT.md` §3 — do not copy `cli_corpus`'s per-request disk read forward).
2. `spiderfeet/api/routes/content.py`: implement the 6 routes from the contract §3, `APIRouter(prefix="/content", tags=["content"])`, mounted in `spiderfeet/api/app.py`.
3. Response models with Pydantic; 404 on unknown `tool_id`.

**Verify:**
```bash
poetry run pytest .tests/test_content_routes.py -q
# manual: ./start.ps1, then curl http://127.0.0.1:8001/api/v1/content/tools
```

### W2 — pytest coverage + OpenAPI accuracy

**Do**
1. Cover all 6 routes: happy path (nmap), 404 (unknown tool), pagination behavior on `/tools` once a synthetic 51st tool fixture is added to the test (do not add a real 51st tool to the repo).
2. Confirm OpenAPI examples render correctly for at least 2 tools in `/docs`.

**Verify:** `poetry run pytest .tests/test_content_routes.py -q` green; manual `/docs` screenshot or description in PR.

### W3 — Backward-compat bridge into `cli_corpus`

**Do**
1. `cli_corpus` service's graph-structure resolution: try `modules_v2/content/<tool>/graph_structure.md` first, fall back to the existing `nugget_structure/<tool>_nugget_graph_structure.md` path unchanged.
2. Scenario detail response gains optional `content_links` pointing at the 3 content-platform documents when a bundle exists for that tool.
3. No behavior change for tools without a content bundle yet.

**Verify:**
```bash
poetry run pytest .tests/api/test_cli_corpus.py -q
# manual: GET /api/v1/cli-corpus/tools/nmap/graph-structure still returns the same content as before this change
```

### W4 — Onboarding + rule updates

**Do**
1. Update `.seed/scripts/cli_corpus/ONBOARDING.md`: add a step "generate/backfill `modules_v2/content/<tool>/` bundle" between the existing Structure-doc step and the operator-visual-review step; formal examination is incomplete without it.
2. Update `.cursor/rules/proj-06-spiderfeet-cli-app-exercising.mdc` and `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` pointers to reference SPEC-008 + the content contract, consistent with how they already reference SPEC-006.

**Verify:** Diff reviewed in PR; grep confirms both rule files reference `SPEC-008` after the change.

---

## Epic X — Live execute API (gated)

### X1 — Execute safety design doc **[OPERATOR SIGN-OFF GATE]**

**Do**
1. Write `.governance/project/SPEC008_EXECUTE_SAFETY_DESIGN.md` locking the strict allowlist model already decided by the operator:
   - Only flags present in the tool's `options_schema.json` are accepted; unknown flags are rejected with a 4xx, not silently dropped.
   - The final command is assembled as an **argv list** (e.g. `["nmap", "-p", "80,443", "scanme.nmap.org"]`) passed to `subprocess`, never interpolated into a shell string.
   - Target values are checked against an explicit target-class allowlist/confirmation step (define the allowlist mechanism: e.g. a per-tool `allowed_target_patterns` in `manifest.json`, or a UI confirmation modal that must be acknowledged before dispatch — pick one and justify it in the doc).
   - Resource/timeout bounds per run (max runtime, output size cap).
2. Post the design doc's summary as a comment on this issue and **explicitly ask the operator to reply with an approval comment on this issue**. Do not proceed to X2 until that comment exists.

**Verify:** Design doc checked in; issue has an operator approval comment (not merely a merged PR) before X2 branch is created.

### X2 — Execute endpoint + async job model

**Do** (only after X1 sign-off)
1. `POST /api/v1/content/tools/{id}/execute` per the signed-off design: validate flags/target against `options_schema.json` + allowlist, build argv, dispatch as a background task, return `run_id`.
2. `GET /api/v1/content/tools/{id}/runs/{run_id}`: status, timestamps, output-so-far.

**Verify:** `poetry run pytest .tests/test_execute_api.py -q`; manual dry run against a permissive lab target only (e.g. `scanme.nmap.org`), never a production/corporate target.

### X3 — Completion pipeline wiring

**Do**
1. On run completion, call the tool's existing adapter `build_outputs` (per `proj-07`) against the captured output.
2. Store results under a run-evidence path distinct from `app_examination_docs/` (e.g. `runs/<tool>/<run_id>/`) — do not pollute the formal examination corpus with ad-hoc operator runs.

**Verify:** After a successful X2 dry run, `runs/<tool>/<run_id>/` contains text+structured+graph+markdown artifacts; formal corpus scenario count is unchanged.

### X4 — Security/injection pytest suite

**Do**
1. Test cases: shell-metacharacter payloads in every field type, a flag not present in `options_schema.json`, a target that fails the allowlist/confirmation check — all must be rejected before dispatch (not after).
2. This suite must pass before Epic X is considered complete.

**Verify:** `poetry run pytest .tests/test_execute_security.py -q` — all rejection cases pass; confirm by reading the test names in the PR description.

---

## Widget epics (Y, Z, AA)

Full detail lives in `@spiderfeet-widget/.governance/project/SPEC008_AGENT_PLAN.md` (mirrors this structure). Summary:

- **Y** — build `window.Widgets.CliScanApp`: skeleton (Y1), Scan-tab dynamic form (Y2), right rail/execute-stub/modals/command-preview (Y3), shared Text/Structured/Graph/Report extraction (Y4), theme/a11y (Y5).
- **Z** — cut the existing CLI Profiling Single Scan page over to `CliScanApp` in view mode (Z1), then run the GOV-08 exploratory regression matrix across all 8 tools/scenarios (Z2).
- **AA** — Composer page scaffold (AA1, no backend blocker), wire `edit-run` mode to the execute API once X3 is signed off and merged (AA2), exploratory review of the live-run flow (AA3).

---

## Definition of done (program)

- [ ] All V/W children merged to `develop` in `spiderfeet`
- [ ] All Y/Z children merged to `develop` in `spiderfeet-widget`
- [ ] Opening CLI Profiling → any of 8 tools → any scenario shows the new 5-tab component with correct Scan/Text/Structured/Graph/Report content (Phase 1 milestone)
- [ ] X1 has an operator sign-off comment before any X2+ work exists
- [ ] If Phase 2 proceeds: X2–X4 merged, AA1–AA3 merged, Composer live-run flow demonstrated end-to-end on a permissive lab target
- [ ] `SPEC008_ISSUE_INDEX.md` and `SPEC008_WIDGET_ISSUE_INDEX.md` show every row `done` with PR links
- [ ] No shell-string execute path exists anywhere in the codebase
- [ ] Continuity note written summarizing Phase 1/Phase 2 outcome

## Future (explicitly NOT SPEC-008)

| Phase | Work |
|-------|------|
| 3 | Import the 3 content documents into TypeDB and switch `/content/*` to query the database instead of `modules_v2/content/` disk files (API contract must not change) |
| 4 | Onboard the remaining ~19 CLI tools with skills under `.cursor/skills/` into the content platform (each needs its own SPEC-004/005/006 formal examination first) |
| 5 | Wire SPEC-007 workflow DSL drivers to reuse `CliScanApp`'s execute contract for multi-step workflows |
