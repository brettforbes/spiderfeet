#!/usr/bin/env python3
"""Create SPEC-007 GitHub epics and child stories via gh CLI.

Run once from repo root:
  poetry run python .seed/scripts/cli_corpus/create_spec007_issues.py

Rewrites `.governance/project/SPEC007_ISSUE_INDEX.md`.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

REPO = "brettforbes/spiderfeet"
INDEX = Path(__file__).resolve().parents[3] / ".governance" / "project" / "SPEC007_ISSUE_INDEX.md"

FOOTER = """
## Branch
`feature/<issue>-<slug>` from `develop` · PR into `develop`

## Forbidden (all SPEC-007 stories)
- Do not redesign GSE without updating `.seed/12C_Graph_Select_Language.md` + schemas + tests together
- Do not invent nugget ids absent from `nuggets.json` / `nuggets_extension.json`
- Do not parse CLI text to produce workflow output variables (GSE on scan graphs only)
- Do not implement Langium, Monaco, workflow visualisation, or AST↔diagram sync in this SPEC
- Do not rewrite legacy `sfp_*` EVENT listeners (future SPEC)
- Do not invent Nexus
- Do not violate structured-first / graph-mandatory laws (proj-06)

## Agent instructions
1. Read `.governance/project/SPEC007_AGENT_PLAN.md` for this story's epic section
2. Read `.seed/12B_Workflow_DSL_Description.md` and `.seed/12C_Graph_Select_Language.md`
3. Read `.governance/specs/SPEC-007-cli-workflow-dsl.md` requirement IDs on this issue
4. One issue → one PR; comment verification commands on the issue
5. Prefer extending `.seed/scripts/cli_workflow/` foundation already on `develop` rather than forking a second package
"""


def gh_create(title: str, body: str, labels: list[str]) -> int:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as fh:
        fh.write(body.strip() + "\n")
        path = fh.name
    cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body-file", path]
    for lab in labels:
        cmd.extend(["--label", lab])
    try:
        out = subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError:
        # retry without labels if label missing
        cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body-file", path]
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
) -> int:
    blocked = f"\n## Blocked by\n{blocked_by}\n" if blocked_by else ""
    body = f"""## Problem
See parent epic #{parent}. Bounded unit: **{code}**.

## Desired outcome
Lesser agent completes this unit with evidence; workflow YAML + GSE runtime foundation advances without redesigning the language.

## Spec binding
{specs} · Parent epic #{parent} · Spec `.governance/specs/SPEC-007-cli-workflow-dsl.md`

## Scope
{scope}
{blocked}
## Acceptance criteria
- [ ] Scope completed with evidence (paths + commands in PR/issue comment)
- [ ] Forbidden list respected
- [ ] PR to `develop` links this issue
- [ ] Playbook section for this code followed (`SPEC007_AGENT_PLAN.md`)

## Verification
{verify}
{FOOTER}
"""
    n = gh_create(f"[SPEC-007] {code} - {title}", body, ["enhancement"])
    print(f"{code} = #{n}")
    return n


def main() -> None:
    epic_p = gh_create(
        "[SPEC-007] Epic P - Workflow DSL schema + seed freeze",
        f"""## Problem
Need a frozen YAML workflow contract and GSE schema so agents do not re-litigate language design while building runtime.

## Spec binding
SPEC-007 R7-01-*, R7-02-04, R7-06-01

## Children
- P0 Sketch gap notes
- P1 workflow_v1.schema.json
- P2 gse_v1.schema.json

## Success
12A validates; informal sketch forms rejected; gap notes explain design deltas.
{FOOTER}
""",
        ["enhancement"],
    )
    print(f"Epic P = #{epic_p}")

    epic_q = gh_create(
        "[SPEC-007] Epic Q - Graph Select Language engine",
        f"""## Problem
Output variables must walk scan graphs with cascade/product semantics. Informal concat templates are insufficient.

## Spec binding
SPEC-007 R7-02-*

## Children
- Q1 graph_index
- Q2 simple select + where
- Q3 for_each product

## Success
GSE evaluates nmap + subfinder corpus fixtures correctly.
{FOOTER}
""",
        ["enhancement"],
    )
    print(f"Epic Q = #{epic_q}")

    epic_r = gh_create(
        "[SPEC-007] Epic R - Workflow loader + variables",
        f"""## Problem
Workflow YAML must load, validate DAG, and resolve `$workflow` / `$steps` references.

## Spec binding
SPEC-007 R7-01-*, R7-03-02, R7-03-03

## Children
- R1 models + loader
- R2 DAG validation
- R3 variables + normalize

## Success
12A loads; cycles rejected; hostname_from_url works.
{FOOTER}
""",
        ["enhancement"],
    )
    print(f"Epic R = #{epic_r}")

    epic_s = gh_create(
        "[SPEC-007] Epic S - Runtime + context export",
        f"""## Problem
Need execution foundation: temp files, DAG executor, context merge of full nodes/edges, dry-run without live CLI.

## Spec binding
SPEC-007 R7-03-*

## Children
- S1 tempfile manager
- S2 context merge
- S3 executor skeleton
- S4 dry-run CLI

## Success
Dry-run fills vars from fixture graphs; context only includes export steps.
{FOOTER}
""",
        ["enhancement"],
    )
    print(f"Epic S = #{epic_s}")

    epic_t = gh_create(
        "[SPEC-007] Epic T - Tool drivers + dry E2E",
        f"""## Problem
Map `tool.<adapter>` to CLI drivers that reuse SPEC-004 adapters; prove 12A dry E2E.

## Spec binding
SPEC-007 R7-04-*, R7-05-05

## Children
- T1 registry + protocol
- T2 example drivers
- T3 dry E2E of 12A

## Success
CI dry E2E green without network; live CLI optional/skipped-if-missing.
{FOOTER}
""",
        ["enhancement"],
    )
    print(f"Epic T = #{epic_t}")

    epic_u = gh_create(
        "[SPEC-007] Epic U - Docs + continuity handoff",
        f"""## Problem
Lesser agents and operators need package README, AGENTS pointer, and continuity handoff.

## Spec binding
SPEC-007 R7-06-*

## Children
- U1 README + AGENTS
- U2 continuity checklist

## Success
Handoff doc exists; AGENTS.md points at SPEC-007.
{FOOTER}
""",
        ["enhancement"],
    )
    print(f"Epic U = #{epic_u}")

    ids: dict[str, int] = {
        "Epic P": epic_p,
        "Epic Q": epic_q,
        "Epic R": epic_r,
        "Epic S": epic_s,
        "Epic T": epic_t,
        "Epic U": epic_u,
    }

    ids["P0"] = child(
        "P0",
        "Sketch gap notes vs redesigned DSL",
        epic_p,
        "R7-06-01",
        "Ensure `.governance/project/SPEC007_SKETCH_GAP_NOTES.md` is complete and linked from 12B.",
        "File lists concat/SUBDOMAIN/sum/sequence/sfp_*/shell-string gaps.",
    )
    ids["P1"] = child(
        "P1",
        "Freeze workflow_v1.schema.json",
        epic_p,
        "R7-01-*",
        "Harden `.seed/scripts/cli_workflow/schema/workflow_v1.schema.json`; 12A must validate; add negative fixture test.",
        "`poetry run pytest .tests/test_cli_workflow_foundation.py -q` (schema cases) + validate CLI.",
        blocked_by=f"P0 #{ids['P0']}",
    )
    ids["P2"] = child(
        "P2",
        "Freeze gse_v1.schema.json",
        epic_p,
        "R7-02-01, R7-02-04",
        "Harden GSE schema; validate all 12A output.vars bindings; reject informal concat samples.",
        "Schema tests green; invalid concat sample rejected.",
        blocked_by=f"P1 #{ids['P1']}",
    )

    ids["Q1"] = child(
        "Q1",
        "graph_index adjacency + reachable",
        epic_q,
        "R7-02-02",
        "Complete/harden `core/graph_index.py` with unit tests for transitive contains.",
        "Unit tests on handmade 5-node graph.",
        blocked_by=f"P2 #{ids['P2']}",
    )
    ids["Q2"] = child(
        "Q2",
        "GSE simple select + where/related",
        epic_q,
        "R7-02-02, R7-02-03",
        "Harden select/where against subfinder corpus fixture (apex vs child domains).",
        "subfinder fixture test: subs non-empty; disjoint from apex.",
        blocked_by=f"Q1 #{ids['Q1']}",
    )
    ids["Q3"] = child(
        "Q3",
        "GSE for_each product join (ip:port)",
        epic_q,
        "R7-02-02, R7-02-03",
        "Harden for_each/collect/emit.product against nmap corpus fixture.",
        "nmap fixture yields `ip:port` strings; spot-check same-endpoint pairing.",
        blocked_by=f"Q2 #{ids['Q2']}",
    )

    ids["R1"] = child(
        "R1",
        "Workflow models + loader",
        epic_r,
        "R7-03-02",
        "Harden `core/loader.py` (typed models optional); load 12A.",
        "12A loads; missing id fails.",
        blocked_by=f"P2 #{ids['P2']}",
    )
    ids["R2"] = child(
        "R2",
        "DAG validation + topological waves",
        epic_r,
        "R7-01-02, R7-03-02",
        "Cycle detection + wave computation tests for 12A fan-out.",
        "Cycle fixture fails; wave0=subfinder_enum; wave1 includes nmap+httpx.",
        blocked_by=f"R1 #{ids['R1']}",
    )
    ids["R3"] = child(
        "R3",
        "Variable resolver + normalize",
        epic_r,
        "R7-03-03",
        "Implement `core/variables.py`; harden `normalize.py` hostname_from_url.",
        "Resolver unit tests; hostname_from_url cases.",
        blocked_by=f"R2 #{ids['R2']}",
    )

    ids["S1"] = child(
        "S1",
        "Auto tempfile manager for list inputs",
        epic_s,
        "R7-03-04",
        "Implement `runtime/tempfile_mgr.py` writing line_text lists; document cleanup.",
        "Temp line count == list length.",
        blocked_by=f"R3 #{ids['R3']}",
    )
    ids["S2"] = child(
        "S2",
        "Context graph merge export",
        epic_s,
        "R7-03-06",
        "Harden `core/context_export.py`; export none vs scan_graph policy tests.",
        "Double-merge does not duplicate nodes; export none no-op.",
        blocked_by=f"S1 #{ids['S1']}",
    )
    ids["S3"] = child(
        "S3",
        "Executor skeleton with injected runner",
        epic_s,
        "R7-03-05",
        "Implement `runtime/executor.py` + result bundle; mock runner for unit tests.",
        "Mocked 12A path fills step vars.",
        blocked_by=f"S2 #{ids['S2']} + Q3 #{ids['Q3']}",
    )
    ids["S4"] = child(
        "S4",
        "dry-run CLI with fixture map",
        epic_s,
        "R7-03-07",
        "Extend `cli.py` with dry-run; map step id → corpus graph JSON.",
        "Context excludes httpx/katana when export=none.",
        blocked_by=f"S3 #{ids['S3']}",
    )

    ids["T1"] = child(
        "T1",
        "Tool registry + driver protocol",
        epic_t,
        "R7-04-01",
        "Implement `tools/registry.py` + `tools/base.py`.",
        "Registry unit test; unknown tool errors clearly.",
        blocked_by=f"S3 #{ids['S3']}",
    )
    ids["T2"] = child(
        "T2",
        "Drivers for 12A tools (adapter reuse)",
        epic_t,
        "R7-04-02",
        "Thin drivers for subfinder/nmap/nerva/httpx/katana/nuclei calling SPEC-004 adapters; live CLI optional.",
        "Adapter call unit-tested; live binary tests skip-if-missing.",
        blocked_by=f"T1 #{ids['T1']}",
    )
    ids["T3"] = child(
        "T3",
        "Dry E2E of 12A example workflow",
        epic_t,
        "R7-05-05",
        "Fixture-mapped dry E2E pytest for full 12A; assert vars + context policy.",
        "CI green without network.",
        blocked_by=f"S4 #{ids['S4']} + T1 #{ids['T1']}",
    )

    ids["U1"] = child(
        "U1",
        "Package README + AGENTS.md pointer",
        epic_u,
        "R7-06-01, R7-06-02",
        "Complete README; add SPEC-007 row to AGENTS.md.",
        "Links resolve; README documents validate/gse-eval/dry-run.",
        blocked_by=f"T3 #{ids['T3']}",
    )
    ids["U2"] = child(
        "U2",
        "Continuity handoff + operator checklist",
        epic_u,
        "R7-06-03",
        "Write `.governance/project/continuity/SPEC007_FOUNDATION.md` with verify commands.",
        "Handoff lists green commands and residual gaps.",
        blocked_by=f"U1 #{ids['U1']}",
    )

    lines = [
        "# SPEC-007 issue index",
        "",
        "**Plan:** `.governance/project/SPEC007_AGENT_PLAN.md`",
        "**Spec:** `.governance/specs/SPEC-007-cli-workflow-dsl.md`",
        "**Seed:** `.seed/12A_Workflow_YAML_Example.yaml`, `.seed/12B_Workflow_DSL_Description.md`, `.seed/12C_Graph_Select_Language.md`",
        "",
        "| Code | Issue |",
        "|------|-------|",
    ]
    order = [
        "Epic P",
        "Epic Q",
        "Epic R",
        "Epic S",
        "Epic T",
        "Epic U",
        "P0",
        "P1",
        "P2",
        "Q1",
        "Q2",
        "Q3",
        "R1",
        "R2",
        "R3",
        "S1",
        "S2",
        "S3",
        "S4",
        "T1",
        "T2",
        "T3",
        "U1",
        "U2",
    ]
    for code in order:
        n = ids[code]
        lines.append(f"| {code} | [#{n}](https://github.com/brettforbes/spiderfeet/issues/{n}) |")

    lines.extend(
        [
            "",
            "## Execution order",
            "",
            "```text",
            "P0 → P1 → P2",
            "  → Q1 → Q2 → Q3",
            "  → R1 → R2 → R3",
            "  → S1 → S2 → S3 → S4",
            "  → T1 → T2 → T3",
            "  → U1 → U2",
            "```",
            "",
            "Foundation stubs already exist under `.seed/scripts/cli_workflow/` — harden and complete per plan; do not redesign GSE.",
            "",
        ]
    )
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {INDEX}")


if __name__ == "__main__":
    main()
