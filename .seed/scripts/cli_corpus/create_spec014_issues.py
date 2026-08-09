#!/usr/bin/env python3
"""Create SPEC-014 GitHub epics and child stories (Epics BA-BH) via gh CLI.

Run once from repo root:
  poetry run python .seed/scripts/cli_corpus/create_spec014_issues.py

Writes `.governance/project/SPEC014_ISSUE_INDEX.md`.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

REPO = "brettforbes/spiderfeet"
INDEX = Path(__file__).resolve().parents[3] / ".governance" / "project" / "SPEC014_ISSUE_INDEX.md"

FOOTER = """
## Branch
`feature/<issue>-<slug>` from `develop` · PR into `develop`

## Autonomous execution (no human review wait required)
`develop` has no branch-protection review requirement; the operator pre-authorized fully
autonomous execution for SPEC-014 (see `.governance/project/SPEC014_AGENT_PLAN.md` §0).
Implement -> verify -> comment evidence -> PR -> **self-merge via `gh pr merge --squash --delete-branch`**
-> close this issue with a comment linking the PR and evidence -> update `SPEC014_ISSUE_INDEX.md`
-> return to `develop` -> pick the next unblocked child.

## Hard gates (only two)
- **BA2** temporary-file deletion needs an explicit operator confirmation comment first.
- **BF1** is an operator visual review gate: regenerate, post the review index, and stop until approved.

## Forbidden (all SPEC-014 stories)
- No per-tool narrative Python — narrative logic lives in `core/` + declarative `rules/<tool>/narrative.yaml`
- No single flat global diagram as the primary graph — per-meta-concept + per-category diagrams
- Do not exceed the diagram shape cap or example cap — overflow goes to the table
- Do not keep the bespoke NarrativeReportBuilder/Netdiscover builders after BD2
- Do not re-scan tools to regenerate — use `backfill_adapter_four_outputs.py --force`
- Nuclei: argv arrays only, never a shell string
- Keep `modules_v2` parity or update `PARITY_DIFFS.md`

## Agent instructions
1. Read `.governance/project/SPEC014_AGENT_PLAN.md` for this story's epic section
2. Read `.governance/specs/SPEC-014-narrative-meta-concept-reports.md` requirement IDs on this issue
3. One issue -> one PR -> self-merge -> comment verification evidence -> close issue -> update index
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


def epic(code: str, title: str, problem: str, specs: str, children: str, success: str) -> int:
    body = f"""## Problem
{problem}

## Spec binding
{specs} · Spec `.governance/specs/SPEC-014-narrative-meta-concept-reports.md`

## Children (order)
{children}

## Success
{success}
{FOOTER}
"""
    n = gh_create(f"[SPEC-014] Epic {code} - {title}", body, ["epic", "enhancement", "spec-014"])
    print(f"Epic {code} = #{n}")
    return n


def child(code: str, title: str, parent: int, specs: str, scope: str, verify: str,
          blocked_by: str = "", extra: str = "") -> int:
    blocked = f"\n## Blocked by\n{blocked_by}\n" if blocked_by else ""
    body = f"""## Problem
See parent epic #{parent}. Bounded unit: **{code}**.

## Desired outcome
A lesser agent completes this unit with evidence; the SPEC-014 narrative engine (or nuclei batching)
moves one bounded step closer to program acceptance.

## Spec binding
{specs} · Parent epic #{parent} · Spec `.governance/specs/SPEC-014-narrative-meta-concept-reports.md`

## Scope
{scope}
{blocked}
{extra}
## Acceptance criteria
- [ ] Scope completed with evidence (paths + commands in the PR / issue comment)
- [ ] Forbidden list respected
- [ ] PR to `develop` links this issue and cites the R14-xx IDs
- [ ] Epic playbook section followed (`SPEC014_AGENT_PLAN.md` §4)

## Verification
{verify}
{FOOTER}
"""
    n = gh_create(f"[SPEC-014] {code} - {title}", body, ["story", "enhancement", "spec-014"])
    print(f"{code} = #{n}")
    return n


def main() -> None:
    # ---- Epics ----
    ba = epic(
        "BA", "Repo hygiene (precondition)",
        "Both repos carry pending work and stray files. Before new narrative work starts, land legitimate "
        "changes via governed PRs into `develop` and clean genuine temporary files so the repos are clean.",
        "SPEC-014 precondition",
        "- BA1 Land pending work in both repos via governed PRs\n- BA2 Temporary-file sweep [OPERATOR CONFIRM GATE]",
        "`spiderfeet` and `spiderfeet-widget` are clean on `develop`; no legitimate work lost; temp files removed with operator confirmation.",
    )
    bb = epic(
        "BB", "Meta-concept registry foundation",
        "There is no single meta-concept model driving narratives; the generic path hard-codes a flat diagram. "
        "Introduce a shared registry aligned with `structure_v1.yaml` so Structure docs and narratives tell the same story.",
        "SPEC-014 R14-01",
        "- BB1 Shared meta-concept registry in `narrative_v2.yaml` + loader + tests",
        "`rules/_shared/narrative_v2.yaml` defines every meta-concept (root/category nugget ids, caps, prose/table config); loader + unit test green.",
    )
    bc = epic(
        "BC", "Central meta-concept narrative engine",
        "The generic path emits bullet lists + one flat `flowchart LR` + a duplicated appendix. Build the centralized "
        "progressive-disclosure renderer that draws small per-concept and per-category diagrams from the live graph.",
        "SPEC-014 R14-02, R14-03, R14-04, R14-05",
        "- BC1 `core/meta_narrative.py` primitives\n- BC2 Rewrite `render_narrative` generic path",
        "All non-nmap/netdiscover tools render per-meta-concept overview + per-category example diagrams + tables + prose; appendix deduped.",
    )
    bd = epic(
        "BD", "Unify nmap/netdiscover + retire bespoke builders",
        "nmap/netdiscover use ~950 lines of bespoke Python builders that `render_narrative` hard-branches into — the "
        "one real max-tool-specific violation. Route them through the shared engine and delete the builders.",
        "SPEC-014 R14-06",
        "- BD1 Reference snapshot + match-or-beat criteria\n- BD2 Route through engine + delete bespoke builders",
        "nmap/netdiscover render via the shared engine, match-or-beat their reference snapshots, and the bespoke builders are gone.",
    )
    be = epic(
        "BE", "Validators + max-common invariant gate",
        "Quality and the max-common/min-specific principle must be enforced by tests, not convention.",
        "SPEC-014 R14-07, R14-08",
        "- BE1 Coverage / meta-concept / size / example-cap / appendix-dedupe validators + tests\n- BE2 Max-common invariant test gate",
        "Validators fail bad reports; a test fails if any adapter grows narrative Python or a tool `narrative.yaml` key is unconsumed.",
    )
    bf = epic(
        "BF", "Regenerate all scenarios + operator review",
        "Every CLI App Profiling scenario must be regenerated with the new engine and visually reviewed before locking.",
        "SPEC-014 R14-09",
        "- BF1 `backfill --force` all 8 tools + review index [OPERATOR VISUAL REVIEW GATE]",
        "All ~70 scenario Markdown + graphs regenerated; `SPEC014_REVIEW_INDEX.md` posted; operator approves before BG.",
    )
    bg = epic(
        "BG", "modules_v2 parity",
        "`modules_v2/_core` + `_rules` mirror the active cli_corpus engine and must not drift.",
        "SPEC-014 R14-10",
        "- BG1 Mirror engine + `narrative_v2.yaml`; parity tests; update `PARITY_DIFFS.md`",
        "modules_v2 renders identical narratives; parity tests green; `PARITY_DIFFS.md` updated.",
    )
    bh = epic(
        "BH", "Nuclei large-input batching + progress",
        "`sfp_cli_nuclei.py` builds one argv / one run, so 15,000 URLs go into a single massive invocation. Add automatic "
        "chunking into blocks of 20, option-pass fan-out, result aggregation, and progress reporting.",
        "SPEC-014 R14-11, R14-12",
        "- BH1 Target chunking (blocks of 20) + option-pass fan-out + JSONL aggregation\n- BH2 Progress reporting + large-input tests",
        "A 15k-URL input runs as blocks of 20 across all option passes with progress; aggregated four outputs produced.",
    )

    # ---- Children ----
    ba1 = child(
        "BA1", "Land pending work in both repos via governed PRs", ba, "SPEC-014 precondition",
        "1. In `spiderfeet` and `spiderfeet-widget`, review pending changes and untracked files\n"
        "2. Land legitimate work via `feature/`/`docs/` PRs into `develop` (one coherent PR per concern)\n"
        "3. Leave each repo clean on `develop` (GOV-02-GIT-004E/F). Do not force-push protected branches",
        "`git status` clean on `develop` in both repos; `gh pr list --state merged` shows the landed PRs.",
    )
    ba2 = child(
        "BA2", "Temporary-file sweep [OPERATOR CONFIRM GATE]", ba, "SPEC-014 precondition",
        "1. Enumerate files that look temporary/scratch (build artifacts, stray exports, editor cruft)\n"
        "2. Post the list on this issue and WAIT for an operator confirmation comment\n"
        "3. After confirmation, delete + PR. Do not delete legitimate assets (copied nugget icons, `.cursor` rules/skills) without confirmation",
        "Operator confirmation comment present; deletion PR merged; repos clean.",
        blocked_by=f"#{ba1}",
        extra="## Hard gate\nNo deletion before an explicit operator confirmation comment on this issue.\n",
    )
    bb1 = child(
        "BB1", "Shared meta-concept registry + loader + tests", bb, "R14-01",
        "1. Expand `rules/_shared/narrative_v2.yaml` `meta_concepts` into the full model: per concept `heading`, "
        "`order`, `root_nugget_ids`, `category_nugget_ids`, `example_cap`, `prose`, `table` columns\n"
        "2. Cover scan, host, system, cdn, domain (+subdomain children), url, org, service_port, environment, "
        "security, and trace (category-like), aligned with `rules/_shared/structure_v1.yaml` patterns\n"
        "3. Add a loader in `core/` + unit test proving each concept resolves ids and caps (no hard-coded concept lists in Python)",
        "`poetry run pytest .tests/ -k meta_concept_registry -q` green; loader returns all concepts with non-empty root/category ids.",
    )
    bc1 = child(
        "BC1", "core/meta_narrative.py primitives", bc, "R14-02, R14-04, R14-05",
        "Implement in `.seed/scripts/cli_corpus/core/meta_narrative.py`: `detect_meta_concepts(graph)`, "
        "`concept_overview_mermaid` (root -> categories, type-only), `category_example_mermaid` "
        "(category -> <= example_cap example instances + `+N more`, descriptor branches once by type), "
        "`category_table` (full deduped inventory), `concept_prose` (counts + representative values), "
        "`append_appendix` (deduped nodes AND edges — fix the duplicate-edge bug). Enforce the shape cap.",
        "`poetry run pytest .tests/ -k meta_narrative -q` green; unit tests assert shape cap, example cap, `+N more`, and deduped appendix.",
        blocked_by=f"#{bb1}",
    )
    bc2 = child(
        "BC2", "Rewrite render_narrative generic path", bc, "R14-03",
        "1. Rewrite the generic path in `core/narrative_engine.py` `render_narrative` to compose: Title -> factual "
        "Introduction -> Scan -> per meta-concept (overview diagram + per-category example diagram + full table + prose) "
        "-> Trace -> Conclusion -> deduped Appendix -> Footer, all from the registry (BB1) + `meta_narrative` (BC1)\n"
        "2. Consume `rules/<tool>/narrative.yaml` overrides only; stop using `type_relation_mermaid` as the single global diagram",
        "Regenerate one pius + one subfinder scenario via `backfill_adapter_four_outputs.py --tool pius --tool subfinder --force`; "
        "confirm per-meta-concept diagrams + tables appear and the appendix has no duplicate edges.",
        blocked_by=f"#{bc1}",
    )
    bd1 = child(
        "BD1", "Reference snapshot + match-or-beat criteria", bd, "R14-06",
        "1. Snapshot current `nmap_*` and `netdiscover_*` `*_proposed_nuggets_edges_description.md` into a reference "
        "fixture directory\n2. Define match-or-beat criteria: all prior sections present, `validate_narrative_coverage` "
        "passes, and per-meta-concept diagrams added",
        "Reference fixtures committed; criteria documented in the PR / issue comment.",
        blocked_by=f"#{bc2}",
    )
    bd2 = child(
        "BD2", "Route nmap/netdiscover through engine + delete bespoke builders", bd, "R14-06, R14-07",
        "1. Route `render_narrative` for nmap/netdiscover through the shared engine (registry-driven)\n"
        "2. Delete `NarrativeReportBuilder` and `NetdiscoverNarrativeReportBuilder` from `narrative_report.py` "
        "(keep only shared helpers still used, e.g. `validate_narrative_coverage`, `SemanticGraph`)\n"
        "3. Prove the match-or-beat gate against BD1 snapshots",
        "`poetry run pytest .tests/ -k narrative -q` green; regenerated nmap/netdiscover reports meet the BD1 criteria; bespoke builder classes gone (grep).",
        blocked_by=f"#{bd1}",
    )
    be1 = child(
        "BE1", "Narrative validators + tests", be, "R14-08",
        "Extend `validate_narrative_coverage`; add `validate_meta_concept_coverage` (every present concept has an "
        "overview; every category with instances has an example diagram + full table), a mermaid shape-size guard "
        "(adapt `validate_mermaid_purity` for example-mode), an example-cap + table-completeness check, and an "
        "appendix-dedupe check. Unit tests per validator.",
        "`poetry run pytest .tests/ -k narrative_validators -q` green; each validator has a passing + failing fixture.",
        blocked_by=f"#{bc2}",
    )
    be2 = child(
        "BE2", "Max-common invariant test gate", be, "R14-07",
        "Add a test that fails if any `adapters/<tool>/__init__.py` defines narrative logic beyond the one-line "
        "`to_narrative` shim, or if a key in a tool's `rules/<tool>/narrative.yaml` is not consumed by the engine (no dead YAML).",
        "`poetry run pytest .tests/ -k max_common_invariant -q` green; test proves a synthetic adapter with extra narrative Python fails the gate.",
        blocked_by=f"#{bd2}",
    )
    bf1 = child(
        "BF1", "Regenerate all scenarios + review index [OPERATOR REVIEW GATE]", bf, "R14-09",
        "1. Run `python .seed/scripts/cli_corpus/backfill_adapter_four_outputs.py --force` for all 8 tools\n"
        "2. Confirm every validator (BE1) passes for every scenario\n"
        "3. Build `.governance/project/SPEC014_REVIEW_INDEX.md` (tool -> scenarios -> notes) and post it\n"
        "4. STOP: operator visual review gate — do not lock goldens or start BG until approved",
        "All ~70 `*_description.md` + graph JSON regenerated; validators green across all scenarios; review index posted; operator approval comment obtained.",
        blocked_by=f"#{be1}, #{be2}",
        extra="## Hard gate\nOperator visual review of regenerated Markdown in CLI App Profiling before BG1.\n",
    )
    bg1 = child(
        "BG1", "modules_v2 parity", bg, "R14-10",
        "Mirror the engine (`meta_narrative.py`, `narrative_engine.py` changes) + `narrative_v2.yaml` into "
        "`modules_v2/_core` and `modules_v2/_rules`; run/refresh parity tests; update `modules_v2/_core/tests/PARITY_DIFFS.md`.",
        "`poetry run pytest modules_v2/tests -q` (and parity harness) green; `PARITY_DIFFS.md` reflects the narrative parity state.",
        blocked_by=f"#{bf1}",
    )
    bh1 = child(
        "BH1", "Nuclei target chunking + option-pass fan-out + aggregation", bh, "R14-11",
        "In `modules_v2/sfp_cli_nuclei.py`: collect the full target set from `urls`/`hosts`/`host_list`; chunk into "
        "blocks of `batch_size` (default 20, spec key `batch_size`); iterate every configured option pass (tags/severity/"
        "templates families per `nuclei_strategy`); run nuclei per (pass, block) with argv-only dispatch + per-run timeout; "
        "aggregate all JSONL records into one `nuclei_finding_v1` bundle before the single four-output build. Guard total work.",
        "Unit test with a synthetic 15,000-URL input asserts correct block count (750) and that one aggregated bundle is built; no real binary run required.",
    )
    bh2 = child(
        "BH2", "Nuclei scanning progress reporting", bh, "R14-12",
        "Add progress: total = `ceil(len(targets)/batch_size) * option_passes`; emit `batch i/N (pass: tags=..., "
        "severity=...)` via an optional callback; accumulate a structured `progress` field (`batches_total`, "
        "`batches_done`, `passes`, `bundles_scanned`) on the result; final summary 'bundles scanned across all options: N'.",
        "Unit test asserts progress totals for a large synthetic input across multiple option passes; callback invoked once per batch.",
        blocked_by=f"#{bh1}",
    )

    rows = [
        ("Epic BA", ba, "open (precondition)"),
        ("Epic BB", bb, "open"),
        ("Epic BC", bc, "open"),
        ("Epic BD", bd, "open"),
        ("Epic BE", be, "open"),
        ("Epic BF", bf, "open (operator review gate)"),
        ("Epic BG", bg, "open"),
        ("Epic BH", bh, "open"),
        ("BA1", ba1, "open"),
        ("BA2", ba2, "blocked (operator confirm gate)"),
        ("BB1", bb1, "open"),
        ("BC1", bc1, "blocked (needs BB1)"),
        ("BC2", bc2, "blocked (needs BC1)"),
        ("BD1", bd1, "blocked (needs BC2)"),
        ("BD2", bd2, "blocked (needs BD1)"),
        ("BE1", be1, "blocked (needs BC2)"),
        ("BE2", be2, "blocked (needs BD2)"),
        ("BF1", bf1, "blocked (needs BE1+BE2; operator review gate)"),
        ("BG1", bg1, "blocked (needs BF1 approval)"),
        ("BH1", bh1, "open (independent lane)"),
        ("BH2", bh2, "blocked (needs BH1)"),
    ]
    lines = [
        "# SPEC-014 issue index (backend: spiderfeet)",
        "",
        "Generated by `.seed/scripts/cli_corpus/create_spec014_issues.py`.",
        "",
        "**Plan:** `.governance/project/SPEC014_AGENT_PLAN.md`",
        "**Spec:** `.governance/specs/SPEC-014-narrative-meta-concept-reports.md`",
        "",
        "| Code | Issue | Status |",
        "|------|-------|--------|",
    ]
    for code, num, status in rows:
        lines.append(f"| {code} | [#{num}](https://github.com/brettforbes/spiderfeet/issues/{num}) | {status} |")
    lines += [
        "",
        "## Execution order",
        "",
        "```",
        "BA1 -> BA2 [OPERATOR CONFIRM]",
        "BB1 -> BC1 -> BC2 -> BD1 -> BD2 -> BE1 -> BE2 -> BF1 [OPERATOR REVIEW] -> BG1",
        "BH1 -> BH2 (independent lane)",
        "```",
        "",
        "Lesser agents: pick the next unblocked child; read `SPEC014_AGENT_PLAN.md` §4 for your code first.",
        "Autonomous self-merge applies to every issue except the BA2 and BF1 gates.",
        "",
    ]
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INDEX}")


if __name__ == "__main__":
    main()
