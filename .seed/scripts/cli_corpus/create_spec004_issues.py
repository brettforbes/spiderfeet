#!/usr/bin/env python3
"""Create SPEC-004 GitHub epics and child stories via gh CLI."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

REPO = "brettforbes/spiderfeet"
INDEX = Path(__file__).resolve().parents[3] / ".governance" / "project" / "SPEC004_ISSUE_INDEX.md"

FOOTER = """
## Branch
`feature/<issue>-<slug>` from `develop` · PR into `develop`

## Forbidden (all SPEC-004 stories)
- Do not invent Nexus or create nexus adapters
- Do not lock golden graph/narrative byte fixtures before visual-review story D7
- Do not rewrite production `sfp_*` modules unless under Epic E
- Do not add divergent UUID helpers (use shared `graph_builder.nugget_instance_id` only)
- Do not invent relations outside `contains` / `had` / `listens-to` without seed+SPEC update

## Agent rule
`.cursor/rules/proj-07-cli-graph-rules-engine.mdc` · Spec `.governance/specs/SPEC-004-cli-graph-rules-engine.md`
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


def child(code: str, title: str, parent: int, spec: str, extra: str) -> int:
    body = f"""## Problem
See parent epic #{parent}. This story is the bounded unit: **{code}**.

## Spec binding
{spec} · Parent epic #{parent} · Related #826

{extra}

## Acceptance criteria
- [ ] Scope below completed with evidence (paths + commands)
- [ ] Forbidden list in parent epic respected
- [ ] PR to `develop` links this issue

## Verification
Document exact commands run (pytest / harvest) in the PR or issue comment.
{FOOTER}
"""
    n = gh_create(f"[SPEC-004] {code} - {title}", body, ["enhancement"])
    print(f"{code} = #{n}")
    return n


def main() -> None:
    epic_a = gh_create(
        "[SPEC-004] Epic A - Foundations (identity, core/, governance)",
        f"""## Problem
CLI structured-to-graph conversion embeds rules in per-tool Python with divergent identity helpers. Foundations must land before the rule engine and adapters.

## Spec binding
SPEC-004 R4-01-01, R4-01-02, R4-01-07 · Related #826 #723

## Children (execute in order)
- A1 SPEC-004 file (may already be landed - verify)
- A2 Canonical identity; remove `_uid` divergence
- A3 Create `core/` package; move `graph_builder`
- A4 Catalogue extensions (SYSTEM, MAC_VENDOR, CDN/correlation descriptors)
- A5 `proj-07` rule + ONBOARDING + `_template` (may already be landed - verify)
- A6 Cleanup doc 14 section 1.8 seed list

## Success criteria
All child stories closed; lesser agents can start Epic B without foundation blockers.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic A = #{epic_a}")

    epic_b = gh_create(
        "[SPEC-004] Epic B - Rule engine + Nmap/Netdiscover pilots",
        f"""## Problem
Mapping/topology rules are hardcoded in converters. Need shared `rule_engine` + YAML packs, proven on both capture families.

## Spec binding
R4-01-02, R4-01-03, R4-01-06 · Parent coordination Epic A #{epic_a} · Related #826

## Children
- B1 `rule_engine.py` + `_shared` YAML schemas
- B2 Topology templates (scan_head, host stack, system_l2, trace)
- B3 Netdiscover adapter - **text_native** + TextFSM
- B4 Nmap adapter - **structured_native** + 06B hooks
- B5 Harvest dispatch via adapters only; always emit four artifacts

## Depends on
Epic A foundations (A2-A3 especially).
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic B = #{epic_b}")

    epic_c = gh_create(
        "[SPEC-004] Epic C - Correlation + Nerva (07 + 07B)",
        f"""## Problem
Nerva correlation A/B/C and ontology rules N0-N5 exist only as markdown. Minimal `nerva_to_graph` ignores them.

## Spec binding
R4-01-04, R4-01-05, R4-01-06 · Seeds:
- `.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md`
- `.seed/07B_Nerva_Ontology_Rules.md`

## Children
- C1 CDN signatures + ASN YAML (from 07)
- C2 `correlation_engine.py` A then C then B
- C3 Nerva adapter + `rules/nerva/` from 07B (calls C2)
- C4 Nerva narrative + four-output harvest

## Depends on
Epic B engine + shared identity. Epic A #{epic_a}. Epic B #{epic_b}.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic C = #{epic_c}")

    epic_d = gh_create(
        "[SPEC-004] Epic D - Remaining tools + narratives + visual review",
        f"""## Problem
Pius, Subfinder, Httpx, Katana, Nuclei lack full four-output pipelines under the shared engine. Narratives and operator visual review must complete before goldens.

## Spec binding
R4-01-05, R4-01-06, R4-01-08 · Epic B #{epic_b} · Epic C #{epic_c}

## Children
- D1 Pius (seed 08)
- D2 Subfinder (seed 09)
- D3 Httpx (seed 10)
- D4 Katana
- D5 Nuclei (seeds 11 + 11B)
- D6 Narrative YAML + harvest MD for D1-D5
- D7 Operator visual-review checklist + refinement tracking

## Depends on
Epic B (engine); Epic C patterns helpful for CDN-ish tools.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic D = #{epic_d}")

    epic_e = gh_create(
        "[SPEC-004] Epic E - Second push: thin sfp_<app> modules (placeholder)",
        f"""## Problem
After goldens, production modules should call shared adapters (abuse.ch-shaped thin wrappers) instead of embedding mapping logic.

## Spec binding
R4-01-09

## Status
**Placeholder only.** Do not create child coding stories until Phase 4 goldens (after D7 visual review).

## Future children (deferred)
- Design note: graph-to-event flatten vs dual-emit
- Pilot `sfp_nmap` / `sfp_tool_nmap` on shared adapter
- Pattern doc + one issue per remaining tool module

## Related
#723 #796 #797 · Example shape: `modules/sfp_abusech.py`
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic E = #{epic_e}")

    rows: list[tuple[str, int]] = [
        ("Epic A", epic_a),
        ("Epic B", epic_b),
        ("Epic C", epic_c),
        ("Epic D", epic_d),
        ("Epic E", epic_e),
    ]

    stories = [
        (
            "A1",
            "Verify/land SPEC-004 + BACKLOG link",
            epic_a,
            "R4-01-*",
            """## Scope
- Ensure `.governance/specs/SPEC-004-cli-graph-rules-engine.md` exists and matches program
- Ensure `.governance/project/BACKLOG.md` links SPEC-004
- If already landed in setup PR, verify and close with comment

## Files
`.governance/specs/SPEC-004-cli-graph-rules-engine.md`, `.governance/project/BACKLOG.md`""",
        ),
        (
            "A2",
            "Canonical identity; remove cli_tool_to_graph _uid divergence",
            epic_a,
            "R4-01-01",
            """## Scope
- All converters import `graph_builder.nugget_instance_id` / shared GraphBuilder
- Delete divergent `_uid` in `cli_tool_to_graph.py`
- Add test that fails if alternate UUID namespace schemes are introduced

## Files
`.seed/scripts/cli_corpus/cli_tool_to_graph.py`, `graph_builder.py`, `nmap_xml_to_graph.py`, `.tests/`""",
        ),
        (
            "A3",
            "Create core/ package; move graph_builder",
            epic_a,
            "R4-01-02",
            """## Scope
- Introduce `.seed/scripts/cli_corpus/core/` with `graph_builder.py` (move or re-export shim)
- Keep old imports green during migration
- Add `types.py` stubs for RulePack / CaptureFamily if needed for later stories

## Files
`.seed/scripts/cli_corpus/core/**`, shims at old paths""",
        ),
        (
            "A4",
            "Catalogue extensions for SYSTEM, MAC_VENDOR, CDN/correlation descriptors",
            epic_a,
            "R4-01-01",
            """## Scope
- Add missing nugget types used by netdiscover/nerva seeds to `nuggets_extension.json`
- Document any TypeQL follow-up (do not block if TypeQL is separate issue)
- Prefer reuse before invent (proj-05)

## Seeds
`.seed/07B_Nerva_Ontology_Rules.md` vocabulary tables · netdiscover structure docs""",
        ),
        (
            "A5",
            "Verify/land proj-07 rule + ONBOARDING + _template dirs",
            epic_a,
            "R4-01-07",
            """## Scope
- Ensure `.cursor/rules/proj-07-cli-graph-rules-engine.mdc` exists
- Add `.seed/scripts/cli_corpus/ONBOARDING.md` checklist for new tools
- Add `rules/_template/` and `adapters/_template/` skeletons
- Cross-links from proj-05/06 if missing""",
        ),
        (
            "A6",
            "Cleanup doc 14 seed list (no Nexus; include 07B + Nuclei 11)",
            epic_a,
            "R4-01-06",
            """## Scope
- `.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md` section 1.8 lists: 06B, 07, 07B, 08, 09, 10, 11, 11B + SPEC-004/proj-07 pointers
- Confirm no Nexus file remains under `.seed/`
- If already fixed in setup, verify and close""",
        ),
        (
            "B1",
            "rule_engine.py + _shared YAML schemas",
            epic_b,
            "R4-01-02",
            """## Scope
- Implement `core/rule_engine.py` that loads YAML packs and emits via GraphBuilder
- `rules/_shared/`: relations, scan_head, categories, identity, validation, four_outputs
- Unit tests: load invalid pack fails; minimal pack creates SCAN_RECORD

## Depends on
A3""",
        ),
        (
            "B2",
            "Shared topology templates",
            epic_b,
            "R4-01-02",
            """## Scope
- Templates: scan_head, host_networks_port_service, system_l2, trace_hop_chain
- Fixture tests prove expected edges/relations

## Depends on
B1""",
        ),
        (
            "B3",
            "Netdiscover adapter - text_native + TextFSM",
            epic_b,
            "R4-01-03 R4-01-06",
            """## Capture family
`text_native`

## Scope
- `adapters/netdiscover/`: text to structured (existing TextFSM path), to_graph via rules, to_text, to_narrative
- `rules/netdiscover/` mapping + narrative YAML
- Harvest writes **four** artifacts
- Structural tests only (no golden lock)

## Seeds
Existing netdiscover structure docs + converters""",
        ),
        (
            "B4",
            "Nmap adapter - structured_native + 06B hooks",
            epic_b,
            "R4-01-03 R4-01-06",
            """## Capture family
`structured_native`

## Scope
- `adapters/nmap/`: XML to intermediate to rule_engine; hooks cite `06B` rule ids
- `rules/nmap/` from `.seed/06B_NMAP_Ontology_Update_Ruleset.md`
- Four artifacts; structural tests; regenerate proposed graphs for visual review

## Depends on
B1 B2; prefer after B3 pattern exists""",
        ),
        (
            "B5",
            "Harvest dispatch via adapters only; four artifacts always",
            epic_b,
            "R4-01-01 R4-01-06",
            """## Scope
- `harvest.py` imports only `adapters.<tool>`
- Remove dead direct converter imports for migrated tools
- Contract: Text, Structured, Graph, Markdown written for each formal scenario

## Depends on
B3 B4""",
        ),
        (
            "C1",
            "CDN signatures + ASN YAML from seed 07",
            epic_c,
            "R4-01-04",
            """## Scope
- `rules/_shared/cdn_signatures.yaml` and `edge_asns.yaml` versioned from seed 07
- Document update process in ONBOARDING or README

## Seed
`.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md` Ruleset C""",
        ),
        (
            "C2",
            "correlation_engine.py A-C-B with fired-rule evidence",
            epic_c,
            "R4-01-04",
            """## Scope
- Implement chaining: per hostname -> A -> C first -> B if not fronted
- Outputs: same_system_*, host_classification, classification_rule_fired, confidence
- Unit tests: scanme dual-stack same system; praetorian Cloudflare fronted (fixtures from seed 07 appendix)

## Depends on
C1 · Seeds 07""",
        ),
        (
            "C3",
            "Nerva adapter + rules from 07B (calls correlation)",
            epic_c,
            "R4-01-04 R4-01-06",
            """## Capture family
`structured_native`

## Scope
- `adapters/nerva/` + `rules/nerva/` implementing Rules **N0-N5** from `.seed/07B_Nerva_Ontology_Rules.md`
- N1 must invoke correlation_engine (C2) before creating HOST/CDN nodes
- Replace minimal `cli_tool_to_graph.nerva_to_graph`
- Four outputs; structural tests

## Seeds
07 + 07B · Watch #880 if fixtures invalid""",
        ),
        (
            "C4",
            "Nerva narrative profile + four-output harvest",
            epic_c,
            "R4-01-05",
            """## Scope
- `rules/nerva/narrative.yaml` + harvest writes `*_description.md`
- Run narrative coverage validator where applicable
- Document CDN / indeterminate origin phrasing per 07/07B

## Depends on
C3""",
        ),
        (
            "D1",
            "Pius adapter + rules + four outputs",
            epic_d,
            "R4-01-06",
            """## Capture family
`structured_native` (NDJSON bundle)

## Seed
`.seed/08_Rules_for_Pius.md`""",
        ),
        (
            "D2",
            "Subfinder adapter + rules + four outputs",
            epic_d,
            "R4-01-06",
            """## Capture family
`structured_native`

## Seed
`.seed/09_Ontology_For_Subfinder.md`""",
        ),
        (
            "D3",
            "Httpx adapter + rules + four outputs",
            epic_d,
            "R4-01-06",
            """## Capture family
`structured_native`

## Seed
`.seed/10_Rules_For_Httpx.md`""",
        ),
        (
            "D4",
            "Katana adapter + rules + four outputs",
            epic_d,
            "R4-01-06",
            """## Capture family
`structured_native`

## Scope
Migrate existing `katana_json_to_graph.py` onto adapter + YAML; align hierarchy with proj-05""",
        ),
        (
            "D5",
            "Nuclei adapter + rules + four outputs",
            epic_d,
            "R4-01-06",
            """## Capture family
`structured_native`

## Seeds
`.seed/11_Ontology_for_Nuclei.md` · `.seed/11B_Rules_for_Nuclei.md`""",
        ),
        (
            "D6",
            "Narrative YAML + harvest MD for D1-D5",
            epic_d,
            "R4-01-05",
            """## Scope
- Narrative profiles for pius, subfinder, httpx, katana, nuclei
- Harvest writes Markdown Report for each
- Coverage validator smoke tests

## Depends on
D1-D5""",
        ),
        (
            "D7",
            "Operator visual-review checklist + refinement tracking",
            epic_d,
            "R4-01-08",
            """## Scope
- Checklist doc for reviewing Text/Structured/Graph/Markdown panes per tool
- Tracking issue or section for refinement follow-ups (engine/YAML/phrasing/ids)
- Explicit gate: **no golden locks until this review is signed off by operator**

## Depends on
D6 · C4 · B3/B4 narratives""",
        ),
    ]

    for code, title, parent, spec, extra in stories:
        n = child(code, title, parent, spec, extra)
        rows.append((code, n))

    lines = [
        "# SPEC-004 issue index",
        "",
        "Generated by `.seed/scripts/cli_corpus/create_spec004_issues.py`.",
        "",
        "| Code | Issue |",
        "|------|-------|",
    ]
    for code, n in rows:
        lines.append(f"| {code} | [#{n}](https://github.com/brettforbes/spiderfeet/issues/{n}) |")
    lines.extend(
        [
            "",
            "## Execution order",
            "",
            "```",
            "A1 -> A2 -> A3 -> A4 -> A5 -> A6",
            "         \\-> B1 -> B2 -> B3 -> B4 -> B5",
            "                \\-> C1 -> C2 -> C3 -> C4",
            "                       \\-> D1-D5 -> D6 -> D7 (visual review)",
            "                              \\-> Phase 4 goldens -> Epic E children",
            "```",
            "",
            "Lesser agents: pick next open child in order; read proj-07 + parent epic + seed docs listed in the issue.",
            "",
        ]
    )
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INDEX}")
    print(json.dumps({k: v for k, v in rows}, indent=2))


if __name__ == "__main__":
    main()
