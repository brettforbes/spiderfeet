#!/usr/bin/env python3
"""Create SPEC-006 GitHub epics and child stories via gh CLI.

Run once from repo root:
  poetry run python .seed/scripts/cli_corpus/create_spec006_issues.py

Writes `.governance/project/SPEC006_ISSUE_INDEX.md`.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

REPO = "brettforbes/spiderfeet"
INDEX = Path(__file__).resolve().parents[3] / ".governance" / "project" / "SPEC006_ISSUE_INDEX.md"

FOOTER = """
## Branch
`feature/<issue>-<slug>` from `develop` · PR into `develop`

## Forbidden (all SPEC-006 stories)
- Do not invent Nexus or create nexus adapters
- Do not put IP/host/URL/CVE **values** into Structure Mermaid diagrams (types + relations only)
- Do not invent graph structures the live `proposed_nuggets_edges.json` graphs do not emit
- Do not rewrite production `sfp_*` modules
- Do not add divergent UUID helpers (use `core.graph_builder.nugget_instance_id` only)
- Do not invent relations outside `contains` / `had` / `listens-to` without seed+SPEC update
- Do not hand-maintain Structure MD after the engine lands — edit `rules/<tool>/structure.yaml` and regenerate
- Do not violate structured-first / graph-mandatory laws (proj-06)

## Agent instructions
1. Read `.governance/project/SPEC006_AGENT_PLAN.md` for this story's epic section
2. Read `.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md` and the Nmap gold Structure doc
3. Read `.governance/specs/SPEC-006-tool-structure-docs-ontology.md` requirement IDs on this issue
4. Follow `.cursor/rules/proj-07-cli-graph-rules-engine.mdc`
5. One issue → one PR; comment verification commands on the issue
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
) -> int:
    blocked = f"\n## Blocked by\n{blocked_by}\n" if blocked_by else ""
    body = f"""## Problem
See parent epic #{parent}. Bounded unit: **{code}**.

## Desired outcome
Lesser agent can complete this unit with evidence; Tools-page Structure docs move toward Nmap gold quality via centralized YAML/engine.

## Spec binding
{specs} · Parent epic #{parent} · Related #826 · Spec `.governance/specs/SPEC-006-tool-structure-docs-ontology.md`

## Scope
{scope}
{blocked}
## Acceptance criteria
- [ ] Scope completed with evidence (paths + commands in PR/issue comment)
- [ ] Forbidden list respected
- [ ] PR to `develop` links this issue
- [ ] Lesser-agent playbook section for this code followed (`SPEC006_AGENT_PLAN.md`)
- [ ] Structure Mermaid diagrams are type-relation only (no values)

## Verification
{verify}
{FOOTER}
"""
    n = gh_create(f"[SPEC-006] {code} - {title}", body, ["enhancement"])
    print(f"{code} = #{n}")
    return n


def main() -> None:
    epic_l = gh_create(
        "[SPEC-006] Epic L - Structure doc quality bar + pattern inventory",
        f"""## Problem
Tool Structure docs on the CLI Profiling Tools page are inconsistent. Nmap is excellent; several tools are thin or missing. Agents need a frozen quality bar and shared Mermaid pattern library before generating docs.

## Spec binding
SPEC-006 R6-01-01, R6-01-02 · Related #826 · Predecessor SPEC-004/005

## Children (order)
- L0 Gap inventory vs Nmap bar
- L1 Freeze quality bar + `rules/_template/structure.yaml`
- L2 Shared `rules/_shared/structure_v1.yaml` Mermaid patterns

## Success
Quality bar + gap inventory + shared patterns checked in; lesser agents have a clear contract.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic L = #{epic_l}")

    epic_m = gh_create(
        "[SPEC-006] Epic M - Central structure-doc engine",
        f"""## Problem
Structure markdown is hand-authored and drifts from mapping/topology. Need centralized render logic (like narrative v2) so Tools-page Structure docs are generated from YAML packs.

## Spec binding
SPEC-006 R6-01-03, R6-01-04, R6-01-05, R6-01-06 · Related #826

## Children (order)
- M1 `core/structure_doc_engine.py`
- M2 CLI `render_structure_docs.py`
- M3 Governance tests for Structure docs

## Success
Engine + CLI regenerate Structure MD from YAML; tests enforce Nmap-bar sections and Mermaid purity.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic M = #{epic_m}")

    epic_n = gh_create(
        "[SPEC-006] Epic N - Per-tool structure packs (8 adapter tools)",
        f"""## Problem
Eight adapter tools need Nmap-quality `*_nugget_graph_structure.md` files for the Tools page Structure button. Katana and Nuclei are missing; Nerva/Pius/Subfinder/httpx are below bar.

## Spec binding
SPEC-006 R6-01-07, R6-01-10, R6-01-11 · Related #826

## Children (order)
- N1 nmap + netdiscover (freeze gold into YAML)
- N2 nerva + pius
- N3 subfinder + httpx
- N4 katana + nuclei (create)
- N5 ONBOARDING / proj wiring

## Success
All eight Tools → Structure views meet the quality bar; files regenerated from `structure.yaml`.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic N = #{epic_n}")

    epic_o = gh_create(
        "[SPEC-006] Epic O - Compose unified `_Current_Ontology.md`",
        f"""## Problem
`.docs/docs-for-cli-tools/_Current_Ontology.md` still reads as Nmap+Netdiscover only. After tool Structure packs exist, compose all ontology sources into one Mermaid-first living document in the same style.

## Spec binding
SPEC-006 R6-01-08, R6-01-09, R6-01-10 · Related #826

## Children (order)
- O1 Ontology source inventory
- O2 Composer path (engine/script)
- O3 Land composed `_Current_Ontology.md`
- O4 Operator visual review (Tools Structure + ontology)

## Success
`_Current_Ontology.md` lists all eight tools with sub-graph Mermaid sections and composition overview; operator sign-off recorded.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic O = #{epic_o}")

    # L children
    l0 = child(
        "L0",
        "Gap inventory vs Nmap Structure quality bar",
        epic_l,
        "R6-01-01",
        """1. Score each ADAPTER_TOOLS Structure doc against SPEC006_STRUCTURE_QUALITY_BAR.md
2. Note missing files (katana, nuclei)
3. Sample live graphs for topology patterns actually present
4. Write `.governance/project/SPEC006_STRUCTURE_GAP_INVENTORY.md`""",
        "Inventory MD checked in; 8 tools classified; Missing called out for katana/nuclei.",
    )
    l1 = child(
        "L1",
        "Freeze quality bar + rules/_template/structure.yaml",
        epic_l,
        "R6-01-01, R6-01-03",
        """1. Align SPEC006_STRUCTURE_QUALITY_BAR.md to Nmap gold sections
2. Add `rules/_template/structure.yaml` with required keys + comments
3. Do not regenerate all tool MDs yet""",
        "Template path exists; quality bar Q1–Q13 stable.",
        blocked_by=f"#{l0}",
    )
    l2 = child(
        "L2",
        "Shared structure_v1.yaml Mermaid pattern library",
        epic_l,
        "R6-01-02",
        """1. Create `rules/_shared/structure_v1.yaml`
2. Patterns aligned with topology_templates.yaml (scan_head, system_l2, host_networks_port_service, trace_hop_chain) + stubs for domain/org/web/vuln
3. Loadable in a small unit test""",
        "YAML loads; required pattern ids asserted in test.",
        blocked_by=f"#{l1}",
    )

    # M children
    m1 = child(
        "M1",
        "core/structure_doc_engine.py render from YAML",
        epic_m,
        "R6-01-03, R6-01-04",
        """1. Implement structure_doc_engine.render_tool_structure_doc
2. Emit title/header/sections/Mermaid/tables from structure_v1 + per-tool structure.yaml
3. Fixture-based unit tests""",
        "`pytest .tests/test_structure_doc_engine.py` green.",
        blocked_by=f"#{l2}",
    )
    m2 = child(
        "M2",
        "CLI render_structure_docs.py --tool/--all",
        epic_m,
        "R6-01-05",
        """1. Add `.seed/scripts/cli_corpus/render_structure_docs.py`
2. Writes `nugget_structure/<tool>_nugget_graph_structure.md` when structure.yaml exists
3. Document flags in PR""",
        "`--help` works; dry-run or fixture tool succeeds.",
        blocked_by=f"#{m1}",
    )
    m3 = child(
        "M3",
        "Governance tests for Structure docs",
        epic_m,
        "R6-01-06",
        """1. Tests: every ADAPTER_TOOLS tool has Structure MD
2. Required headings + mermaid fence + no IP-like literals in Mermaid
3. Wire pytest module under `.tests/`""",
        "`pytest .tests/test_spec006_structure_docs.py` green (may soft-skip until N packs land — document gate).",
        blocked_by=f"#{m2}",
    )

    # N children
    n1 = child(
        "N1",
        "structure.yaml + regenerate nmap + netdiscover",
        epic_n,
        "R6-01-07",
        """Author structure.yaml for nmap and netdiscover to reproduce gold Structure quality via engine; regenerate MD; diff carefully — prefer fidelity over simplification.""",
        "Both Structure docs still pass quality bar; engine-owned; API graph-structure OK.",
        blocked_by=f"#{m2}",
    )
    n2 = child(
        "N2",
        "structure.yaml + regenerate nerva + pius",
        epic_n,
        "R6-01-07",
        """Full rewrite to Nmap bar. Match live graphs only. Nerva host/port/service (+ CDN if present). Pius org/domain trees as emitted.""",
        "Quality bar Pass; Mermaid type-only; Tools Structure button OK.",
        blocked_by=f"#{n1}",
    )
    n3 = child(
        "N3",
        "structure.yaml + regenerate subfinder + httpx",
        epic_n,
        "R6-01-07",
        """Replace thin bullet docs with Mermaid-first Structure docs. Domain apex, unresolved/resolved names, URL/tech/CDN type patterns.""",
        "Quality bar Pass; no value Mermaid labels.",
        blocked_by=f"#{n2}",
    )
    n4 = child(
        "N4",
        "Create katana + nuclei Structure docs",
        epic_n,
        "R6-01-07",
        """Create missing Structure docs from structure.yaml + live graphs. Katana crawl URL tree; Nuclei findings → VULNERABILITIES patterns as graphs emit.""",
        "Both files exist; quality bar Pass; API returns MD.",
        blocked_by=f"#{n3}",
    )
    n5 = child(
        "N5",
        "ONBOARDING + proj rules require structure.yaml",
        epic_n,
        "R6-01-11",
        """Update ONBOARDING.md and proj-06/07 pointers: formal examination incomplete without Structure doc regenerated from structure.yaml; mention render_structure_docs.py.""",
        "Docs updated; checklist item present.",
        blocked_by=f"#{n4}",
    )

    # O children
    o1 = child(
        "O1",
        "Ontology source inventory for _Current_Ontology",
        epic_o,
        "R6-01-09",
        """Write SPEC006_ONTOLOGY_SOURCE_INVENTORY.md listing seed docs, catalogues, and tool structure packs to compose.""",
        "Inventory MD checked in.",
        blocked_by=f"#{n1}",
    )
    o2 = child(
        "O2",
        "Composer path for _Current_Ontology.md",
        epic_o,
        "R6-01-08, R6-01-09",
        """Implement compose helper (engine method or compose_current_ontology.py) that extends unified ontology sections from tool structure packs without deleting qualification hierarchy.""",
        "Composer runnable; dry output reviewed in PR.",
        blocked_by=f"#{o1} #{n4}",
    )
    o3 = child(
        "O3",
        "Land composed _Current_Ontology.md (all 8 tools)",
        epic_o,
        "R6-01-08",
        """Run composer; land `.docs/docs-for-cli-tools/_Current_Ontology.md` with sub-graph table + per-tool Mermaid sections + composition diagram in Nmap/Netdiscover style.""",
        "Doc updated; 8 tools listed; Mermaid type-only.",
        blocked_by=f"#{o2}",
    )
    o4 = child(
        "O4",
        "Operator visual review — Tools Structure + ontology",
        epic_o,
        "R6-01-10",
        """Operator: ./start.ps1 → Tools → Structure for each of 8 tools; skim _Current_Ontology.md. Comment sign-off on issue. Update SPEC006 visual checklist if present.""",
        "Operator sign-off comment recorded.",
        blocked_by=f"#{o3} #{n5}",
    )

    lines = [
        "# SPEC-006 issue index",
        "",
        "Generated by `.seed/scripts/cli_corpus/create_spec006_issues.py`.",
        "",
        "**Plan:** `.governance/project/SPEC006_AGENT_PLAN.md`",
        "**Spec:** `.governance/specs/SPEC-006-tool-structure-docs-ontology.md`",
        "**Quality bar:** `.governance/project/SPEC006_STRUCTURE_QUALITY_BAR.md`",
        "",
        "| Code | Issue |",
        "|------|-------|",
        f"| Epic L | [#{epic_l}](https://github.com/brettforbes/spiderfeet/issues/{epic_l}) |",
        f"| Epic M | [#{epic_m}](https://github.com/brettforbes/spiderfeet/issues/{epic_m}) |",
        f"| Epic N | [#{epic_n}](https://github.com/brettforbes/spiderfeet/issues/{epic_n}) |",
        f"| Epic O | [#{epic_o}](https://github.com/brettforbes/spiderfeet/issues/{epic_o}) |",
        f"| L0 | [#{l0}](https://github.com/brettforbes/spiderfeet/issues/{l0}) |",
        f"| L1 | [#{l1}](https://github.com/brettforbes/spiderfeet/issues/{l1}) |",
        f"| L2 | [#{l2}](https://github.com/brettforbes/spiderfeet/issues/{l2}) |",
        f"| M1 | [#{m1}](https://github.com/brettforbes/spiderfeet/issues/{m1}) |",
        f"| M2 | [#{m2}](https://github.com/brettforbes/spiderfeet/issues/{m2}) |",
        f"| M3 | [#{m3}](https://github.com/brettforbes/spiderfeet/issues/{m3}) |",
        f"| N1 | [#{n1}](https://github.com/brettforbes/spiderfeet/issues/{n1}) |",
        f"| N2 | [#{n2}](https://github.com/brettforbes/spiderfeet/issues/{n2}) |",
        f"| N3 | [#{n3}](https://github.com/brettforbes/spiderfeet/issues/{n3}) |",
        f"| N4 | [#{n4}](https://github.com/brettforbes/spiderfeet/issues/{n4}) |",
        f"| N5 | [#{n5}](https://github.com/brettforbes/spiderfeet/issues/{n5}) |",
        f"| O1 | [#{o1}](https://github.com/brettforbes/spiderfeet/issues/{o1}) |",
        f"| O2 | [#{o2}](https://github.com/brettforbes/spiderfeet/issues/{o2}) |",
        f"| O3 | [#{o3}](https://github.com/brettforbes/spiderfeet/issues/{o3}) |",
        f"| O4 | [#{o4}](https://github.com/brettforbes/spiderfeet/issues/{o4}) |",
        "",
        "## Execution order",
        "",
        "```",
        "L0 -> L1 -> L2",
        "  -> M1 -> M2 -> M3",
        "    -> N1 -> N2 -> N3 -> N4 -> N5",
        "      -> O1 (after N1) -> O2 (after N4) -> O3 -> O4 (operator)",
        "```",
        "",
        "Lesser agents: pick next unblocked child; read SPEC006_AGENT_PLAN.md epic section first.",
        "Gold Structure doc: `.docs/docs-for-cli-tools/nugget_structure/nmap_nugget_graph_structure.md`",
        "",
    ]
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INDEX}")


if __name__ == "__main__":
    main()
