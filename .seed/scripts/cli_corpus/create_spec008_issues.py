#!/usr/bin/env python3
"""Create SPEC-008 GitHub epics and child stories (backend: Epics V, W, X) via gh CLI.

Run once from repo root:
  poetry run python .seed/scripts/cli_corpus/create_spec008_issues.py

Writes `.governance/project/SPEC008_ISSUE_INDEX.md`.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

REPO = "brettforbes/spiderfeet"
INDEX = Path(__file__).resolve().parents[3] / ".governance" / "project" / "SPEC008_ISSUE_INDEX.md"

FOOTER = """
## Branch
`feature/<issue>-<slug>` from `develop` · PR into `develop`

## Autonomous execution (no human review wait required)
This repo's `develop` has no branch-protection review requirement, and the operator has
pre-authorized fully autonomous execution for SPEC-008 (see `.governance/project/SPEC008_AGENT_PLAN.md` §0).
Implement -> verify -> comment evidence -> PR -> **self-merge via `gh pr merge --squash --delete-branch`** ->
close this issue with a comment linking the PR and verification evidence -> update
`SPEC008_ISSUE_INDEX.md` -> return to `develop` -> pick the next unblocked child.
The **only** exception in this repo is Epic X issue X1, which requires an explicit operator
sign-off *comment on that issue* before X2 may start.

## Forbidden (all SPEC-008 stories)
- Do not build a shell-string execute path — argv arrays only
- Do not skip `options_schema.json` review_log reconciliation
- Do not duplicate Text/Structured/Graph/Report rendering logic instead of sharing it
- Do not invent a new tool-id namespace outside `cli_corpus` / `corpus_index.json`
- Do not touch production `sfp_*` modules under this SPEC
- Do not re-scan the full content directory tree per API request once caching exists
- Do not mark Epic X done without the security/injection pytest suite passing
- Do not begin X2 without an operator sign-off comment on X1

## Agent instructions
1. Read `.governance/project/SPEC008_AGENT_PLAN.md` for this story's epic section
2. Read `.governance/project/SPEC008_CONTENT_CONTRACT.md` for content bundle / API shape rules
3. Read `.governance/specs/SPEC-008-cli-app-scan-ui-content-platform.md` requirement IDs on this issue
4. One issue -> one PR -> self-merge -> comment verification evidence -> close issue -> update index
"""


def gh_create(title: str, body: str, labels: list[str]) -> int:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as fh:
        fh.write(body.strip() + "\n")
        path = fh.name
    cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body-file", path]
    for lab in labels:
        cmd.extend(["--label", lab])
    out = subprocess.check_output(cmd, text=True).strip()
    Path(path).unlink(missing_ok=True)
    return int(out.rstrip("/").split("/")[-1])


def child(
    code: str,
    title: str,
    parent: int,
    specs: str,
    scope: str,
    verify: str,
    blocked_by: str = "",
    extra: str = "",
) -> int:
    blocked = f"\n## Blocked by\n{blocked_by}\n" if blocked_by else ""
    body = f"""## Problem
See parent epic #{parent}. Bounded unit: **{code}**.

## Desired outcome
Lesser agent can complete this unit with evidence; SPEC-008 content platform / execute API
moves one bounded step closer to the Phase 1 (or Phase 2) milestone in the spec.

## Spec binding
{specs} · Parent epic #{parent} · Related #826 · Spec `.governance/specs/SPEC-008-cli-app-scan-ui-content-platform.md`

## Scope
{scope}
{blocked}
{extra}
## Acceptance criteria
- [ ] Scope completed with evidence (paths + commands in PR/issue comment)
- [ ] Forbidden list respected
- [ ] PR to `develop` links this issue
- [ ] Lesser-agent playbook section for this code followed (`SPEC008_AGENT_PLAN.md`)

## Verification
{verify}
{FOOTER}
"""
    n = gh_create(f"[SPEC-008] {code} - {title}", body, ["enhancement"])
    print(f"{code} = #{n}")
    return n


def main() -> None:
    epic_v = gh_create(
        "[SPEC-008] Epic V - Content platform foundation",
        f"""## Problem
`.seed/15_CLI_App_UI.md` calls for a `modules_v2/content/<tool_id>/` bundle (options, Zero-to-Hero,
graph structure, plus a new machine-readable options schema) as the single source of truth for a
generic CLI/API scan UI. `modules_v2/content/` currently exists but is empty; no options-schema
format or generator exists yet.

## Spec binding
SPEC-008 R8-01, R8-02, R8-03 · Related #826

## Children (order)
- V0 Gap inventory vs content contract
- V1 `options_schema.json` generator
- V2 Backfill content bundles for all 8 adapter tools

## Success
`modules_v2/content/<tool>/` exists and is `Pass` on `SPEC008_CONTENT_CONTRACT.md` for all 8
formally-examined tools (nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei).
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic V = #{epic_v}")

    epic_w = gh_create(
        "[SPEC-008] Epic W - Content APIs",
        f"""## Problem
No FastAPI surface serves the 3(4) content-platform documents per tool. The Scan tab UI
(and Composer, later) needs a stable, scale-ready API contract now, file-backed today,
TypeDB-backed later without a contract change.

## Spec binding
SPEC-008 R8-04, R8-05, R8-06, R8-07 · Related #826 · Depends on Epic V

## Children (order)
- W1 FastAPI `/content/*` routes + service layer (cached, scale-ready)
- W2 pytest coverage + OpenAPI accuracy
- W3 Backward-compat bridge into `cli_corpus` graph-structure resolution
- W4 ONBOARDING.md + proj-06/07 rule updates

## Success
`/api/v1/content/*` routes live, tested, documented; existing CLI Profiling Tools-page
Structure button behavior is unchanged for tools without a content bundle yet; onboarding
docs require the bundle going forward.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic W = #{epic_w}")

    epic_x = gh_create(
        "[SPEC-008] Epic X - Live execute API (gated)",
        f"""## Problem
`.seed/15_CLI_App_UI.md` wants a live "Execute" button that runs a CLI tool from the widget.
This is a genuine security boundary (arbitrary CLI execution triggered from a browser).
The operator has approved a strict allowlist model (options-schema-bounded flags, argv-only
dispatch, target-class allowlist/confirmation) but implementation may not start until the
design doc on issue X1 receives an **explicit operator sign-off comment**.

## Spec binding
SPEC-008 R8-08, R8-09, R8-10, R8-11 · Related #826 · Depends on Epic V (options_schema.json shape)

## Children (order)
- X1 Execute safety design doc **[OPERATOR SIGN-OFF GATE — do not skip]**
- X2 Execute endpoint + async job model (blocked until X1 signed off)
- X3 Completion pipeline wiring (adapter four-outputs -> run-evidence path)
- X4 Security/injection pytest suite

## Hard gate
Do **not** open a branch for X2 until issue X1 has an operator comment explicitly approving
the safety design. This is the one place in SPEC-008 where autonomous self-merge does not
apply to starting the next child — X1 itself still gets a normal PR/merge for the design doc,
but the *design's approval* must be a human comment on the issue, not inferred from the PR merge.

## Success
Execute API works end-to-end against a permissive lab target only, with a passing security/
injection pytest suite, and results land under a run-evidence path distinct from the formal
examination corpus.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic X = #{epic_x}")

    # V children
    v0 = child(
        "V0",
        "Gap inventory vs content contract",
        epic_v,
        "R8-01",
        """1. For each of the 8 adapter tools, check what exists under `.docs/docs-for-cli-tools/`
   against the 5 contract files in `SPEC008_CONTENT_CONTRACT.md` Section 1
2. Write `.governance/project/SPEC008_CONTENT_GAP_INVENTORY.md`: one row per tool, one column
   per contract file, Have/Missing/Needs regen""",
        "Inventory MD checked in; all 8 tools listed; no blank cells.",
    )
    v1 = child(
        "V1",
        "options_schema.json generator",
        epic_v,
        "R8-02",
        """1. `.seed/scripts/cli_corpus/generate_options_schema.py --tool <id>` parses a tool's
   CLI-Options.md into a draft `options_schema.json` per `SPEC008_CONTENT_CONTRACT.md` Section 2
2. Emit `options_schema.review.md` listing any flags the parser could not confidently classify
3. Unit test against 2 tools with different flag styles (e.g. nmap, httpx)""",
        "`poetry run pytest .tests/test_generate_options_schema.py -q` green; required fields non-null; `choices` populated for every `select` type.",
        blocked_by=f"#{v0}",
    )
    v2 = child(
        "V2",
        "Backfill content bundles for all 8 adapter tools",
        epic_v,
        "R8-03",
        """For each of nmap, netdiscover, nerva, pius, subfinder, httpx, katana, nuclei:
1. Create `modules_v2/content/<id>/` with manifest.json, options.md (copy), zero_to_hero.md
   (copy), graph_structure.md (copy), and options_schema.json generated via V1
2. Resolve every entry in that tool's `options_schema.review.md` by hand (fill in
   description/type/group where the generator flagged uncertainty) — do not leave placeholders
3. One issue, checklist of all 8 tools; not done until all 8 are Pass on the content contract""",
        "All 8 `manifest.json` files parse and report the correct `tool_id`; zero unresolved review_log entries across all 8 tools.",
        blocked_by=f"#{v1}",
    )

    # W children
    w1 = child(
        "W1",
        "FastAPI /content/* routes + service layer",
        epic_w,
        "R8-04",
        """1. `spiderfeet/api/services/content.py`: registry loader keyed by tool_id, in-memory
   cache invalidated by directory mtime (do not copy cli_corpus's per-request disk-read pattern)
2. `spiderfeet/api/routes/content.py`: implement all 6 routes from the content contract Section 3,
   `APIRouter(prefix="/content", tags=["content"])`, mounted in `spiderfeet/api/app.py`
3. Pydantic response models; 404 on unknown tool_id""",
        "`poetry run pytest .tests/test_content_routes.py -q` green; manual `curl http://127.0.0.1:8001/api/v1/content/tools` returns all backfilled tools.",
        blocked_by=f"#{v2}",
    )
    w2 = child(
        "W2",
        "pytest coverage + OpenAPI accuracy for content routes",
        epic_w,
        "R8-05",
        """1. Cover all 6 routes: happy path (nmap), 404 unknown tool, pagination behavior once a
   synthetic 51st-tool fixture is added to the *test* (do not add a real 51st tool to the repo)
2. Confirm OpenAPI examples render correctly for at least 2 tools in /docs""",
        "`poetry run pytest .tests/test_content_routes.py -q` green; PR description includes /docs confirmation.",
        blocked_by=f"#{w1}",
    )
    w3 = child(
        "W3",
        "Backward-compat bridge into cli_corpus",
        epic_w,
        "R8-06",
        """1. cli_corpus's graph-structure resolution: try modules_v2/content/<tool>/graph_structure.md
   first, fall back to the existing nugget_structure path unchanged
2. Scenario detail response gains optional `content_links` when a bundle exists for that tool
3. No behavior change for tools without a content bundle yet""",
        "`poetry run pytest .tests/api/test_cli_corpus.py -q` green; manual confirm GET .../graph-structure output is unchanged for a tool before/after this change.",
        blocked_by=f"#{w1}",
    )
    w4 = child(
        "W4",
        "ONBOARDING.md + proj-06/07 rule updates",
        epic_w,
        "R8-07",
        """1. Update `.seed/scripts/cli_corpus/ONBOARDING.md`: add a step to generate/backfill the
   `modules_v2/content/<tool>/` bundle between the Structure-doc step and operator visual review
2. Update `.cursor/rules/proj-06-spiderfeet-cli-app-exercising.mdc` and
   `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` pointers to reference SPEC-008 + the
   content contract""",
        "Diff reviewed in PR; grep confirms both rule files reference SPEC-008 after the change.",
        blocked_by=f"#{w3}",
    )

    # X children
    x1 = child(
        "X1",
        "Execute safety design doc [OPERATOR SIGN-OFF GATE]",
        epic_x,
        "R8-08",
        """1. Write `.governance/project/SPEC008_EXECUTE_SAFETY_DESIGN.md` locking the strict
   allowlist model: only options_schema.json flags accepted, argv-array dispatch only (never a
   shell string), explicit target-class allowlist/confirmation step, resource/timeout bounds
2. Post the design summary as a comment on **this issue** and explicitly ask the operator to
   reply with an approval comment on this issue
3. Do not open a branch for X2 until that operator approval comment exists""",
        "Design doc checked in via normal PR/merge; **separately**, this issue has an operator approval comment before X2 starts.",
        blocked_by=f"#{v1}",
        extra="## Hard gate\nThis is the one SPEC-008 issue where merging the PR does **not** unblock the next child. X2 additionally requires an operator comment on this issue.\n",
    )
    x2 = child(
        "X2",
        "Execute endpoint + async job model",
        epic_x,
        "R8-09",
        """1. `POST /api/v1/content/tools/{id}/execute` per the signed-off X1 design: validate
   flags/target against options_schema.json + allowlist, build argv, dispatch as a background
   task, return run_id
2. `GET /api/v1/content/tools/{id}/runs/{run_id}`: status, timestamps, output-so-far""",
        "`poetry run pytest .tests/test_execute_api.py -q` green; manual dry run against a permissive lab target only (e.g. scanme.nmap.org).",
        blocked_by=f"#{x1} (operator sign-off comment required, not just merge)",
    )
    x3 = child(
        "X3",
        "Completion pipeline wiring",
        epic_x,
        "R8-10",
        """1. On run completion, call the tool's existing adapter build_outputs (per proj-07)
   against the captured output
2. Store results under a run-evidence path distinct from app_examination_docs/
   (e.g. runs/<tool>/<run_id>/) — do not pollute the formal examination corpus""",
        "After a successful X2 dry run, runs/<tool>/<run_id>/ contains text+structured+graph+markdown artifacts; formal corpus scenario count unchanged.",
        blocked_by=f"#{x2}",
    )
    x4 = child(
        "X4",
        "Security/injection pytest suite",
        epic_x,
        "R8-11",
        """1. Test cases: shell-metacharacter payloads in every field type, a flag not present in
   options_schema.json, a target that fails the allowlist/confirmation check — all must be
   rejected before dispatch
2. This suite must pass before Epic X is considered complete""",
        "`poetry run pytest .tests/test_execute_security.py -q` — all rejection cases pass.",
        blocked_by=f"#{x3}",
    )

    lines = [
        "# SPEC-008 issue index (backend: spiderfeet)",
        "",
        "Generated by `.seed/scripts/cli_corpus/create_spec008_issues.py`.",
        "",
        "**Plan:** `.governance/project/SPEC008_AGENT_PLAN.md`",
        "**Spec:** `.governance/specs/SPEC-008-cli-app-scan-ui-content-platform.md`",
        "**Content contract:** `.governance/project/SPEC008_CONTENT_CONTRACT.md`",
        "**Widget-side index:** `@spiderfeet-widget/.governance/project/SPEC008_WIDGET_ISSUE_INDEX.md`",
        "",
        "| Code | Issue | Status |",
        "|------|-------|--------|",
        f"| Epic V | [#{epic_v}](https://github.com/brettforbes/spiderfeet/issues/{epic_v}) | open |",
        f"| Epic W | [#{epic_w}](https://github.com/brettforbes/spiderfeet/issues/{epic_w}) | open |",
        f"| Epic X | [#{epic_x}](https://github.com/brettforbes/spiderfeet/issues/{epic_x}) | open (gated) |",
        f"| V0 | [#{v0}](https://github.com/brettforbes/spiderfeet/issues/{v0}) | open |",
        f"| V1 | [#{v1}](https://github.com/brettforbes/spiderfeet/issues/{v1}) | open |",
        f"| V2 | [#{v2}](https://github.com/brettforbes/spiderfeet/issues/{v2}) | open |",
        f"| W1 | [#{w1}](https://github.com/brettforbes/spiderfeet/issues/{w1}) | open |",
        f"| W2 | [#{w2}](https://github.com/brettforbes/spiderfeet/issues/{w2}) | open |",
        f"| W3 | [#{w3}](https://github.com/brettforbes/spiderfeet/issues/{w3}) | open |",
        f"| W4 | [#{w4}](https://github.com/brettforbes/spiderfeet/issues/{w4}) | open |",
        f"| X1 | [#{x1}](https://github.com/brettforbes/spiderfeet/issues/{x1}) | open (OPERATOR SIGN-OFF GATE) |",
        f"| X2 | [#{x2}](https://github.com/brettforbes/spiderfeet/issues/{x2}) | blocked (needs X1 sign-off) |",
        f"| X3 | [#{x3}](https://github.com/brettforbes/spiderfeet/issues/{x3}) | blocked |",
        f"| X4 | [#{x4}](https://github.com/brettforbes/spiderfeet/issues/{x4}) | blocked |",
        "",
        "## Execution order",
        "",
        "```",
        "V0 -> V1 -> V2",
        "  -> W1 -> W2 -> W3 -> W4",
        "",
        "X1 [OPERATOR SIGN-OFF GATE] -> X2 -> X3 -> X4",
        "```",
        "",
        "Lesser agents: pick next unblocked child; read SPEC008_AGENT_PLAN.md epic section first.",
        "Autonomous self-merge applies to every issue except the X1 sign-off gate itself (see plan Section 0.1).",
        "",
    ]
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INDEX}")


if __name__ == "__main__":
    main()
