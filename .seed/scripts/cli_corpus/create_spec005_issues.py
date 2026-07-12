#!/usr/bin/env python3
"""Create SPEC-005 GitHub epics and child stories via gh CLI.

Run once from repo root:
  python .seed/scripts/cli_corpus/create_spec005_issues.py

Writes `.governance/project/SPEC005_ISSUE_INDEX.md`.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

REPO = "brettforbes/spiderfeet"
INDEX = Path(__file__).resolve().parents[3] / ".governance" / "project" / "SPEC005_ISSUE_INDEX.md"

FOOTER = """
## Branch
`feature/<issue>-<slug>` from `develop` · PR into `develop`

## Forbidden (all SPEC-005 stories)
- Do not invent Nexus or create nexus adapters
- Do not lock golden graph/narrative byte fixtures before story K1 operator sign-off
- Do not rewrite production `sfp_*` modules (tracked under #723 / SPEC-004 Epic E)
- Do not add divergent UUID helpers (use `core.graph_builder.nugget_instance_id` only)
- Do not invent relations outside `contains` / `had` / `listens-to` without seed+SPEC update
- Do not put IP literal values into section Mermaid diagrams (types + relations only)
- Do not hardcode IPv4/IPv6 regexes outside `rules/_shared/ip_patterns.yaml`

## Agent instructions
1. Read `.governance/project/SPEC005_AGENT_PLAN.md` for this story's epic section
2. Read `.governance/specs/SPEC-005-narrative-v2-ip-classify.md` requirement IDs on this issue
3. Follow `.cursor/rules/proj-07-cli-graph-rules-engine.mdc`
4. One issue → one PR; comment verification commands on the issue
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


def child(code: str, title: str, parent: int, specs: str, scope: str, verify: str, blocked_by: str = "") -> int:
    blocked = f"\n## Blocked by\n{blocked_by}\n" if blocked_by else ""
    body = f"""## Problem
See parent epic #{parent}. Bounded unit: **{code}**.

## Spec binding
{specs} · Parent epic #{parent} · Related #826 · Visual gate #932

## Scope
{scope}
{blocked}
## Acceptance criteria
- [ ] Scope completed with evidence (paths + commands in PR/issue comment)
- [ ] Forbidden list respected
- [ ] PR to `develop` links this issue
- [ ] Lesser-agent playbook section for this code followed (SPEC005_AGENT_PLAN.md)

## Verification
{verify}
{FOOTER}
"""
    n = gh_create(f"[SPEC-005] {code} - {title}", body, ["enhancement"])
    print(f"{code} = #{n}")
    return n


def main() -> None:
    epic_g = gh_create(
        "[SPEC-005] Epic G - Artifact trust + UI graph/markdown resolution",
        f"""## Problem
Operator review shows missing graph descriptions (and some graphs) for scenarios that may already have files on disk, or that are truly text-only. The CLI Profiling UI must resolve artifacts correctly before narrative quality work is judged.

## Spec binding
SPEC-005 R5-01-10, R5-01-11 · Related #826 #932 · Predecessor SPEC-004

## Children (order)
- G0 Inventory + naming/resolution contract
- G1 Fix `cli_corpus` path resolution for format-suffixed scenario ids
- G2 Text-only scenarios: derive graph or explicit `graph_deferred`

## Success
Every non-deferred examination scenario shows Graph + Markdown in the UI when files exist; deferred scenarios show an explicit reason.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic G = #{epic_g}")

    epic_h = gh_create(
        "[SPEC-005] Epic H - Shared IPv4/IPv6 nugget classification",
        f"""## Problem
Many IP_ADDRESS entity nuggets are incorrectly applied to IPv6 literals. Classification must be central (YAML regex + core helper) and used by all adapters/topology.

## Spec binding
SPEC-005 R5-01-01, R5-01-02, R5-01-03 · Related #826

## Children (order)
- H1 `ip_patterns.yaml` + `core/ip_classify.py` + unit tests
- H2 Wire `core/topology.py`
- H3 Wire all adapter hooks
- H4 Regenerate graphs / add fixture covering IPv6

## Nugget mapping
- IPv4 → `IP_ADDRESS` | `INTERNAL_IP_ADDRESS` | `AFFILIATE_IPADDR`
- IPv6 → `IPV6_ADDRESS` | `AFFILIATE_IPV6_ADDRESS`
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic H = #{epic_h}")

    epic_i = gh_create(
        "[SPEC-005] Epic I - Central narrative engine v2",
        f"""## Problem
Rich §4.3 narratives exist only for nmap/netdiscover (`narrative_report.py`). Other tools emit stub markdown. Need one YAML-driven engine: meta-concepts, category subsections, type-relation Mermaid, prose, tables, appendix.

## Spec binding
SPEC-005 R5-01-04 … R5-01-09 · Ontology `.seed/05_Onotology_for_Nuggets.md` §4.3 · Related #826

## Children (order)
- I1 Shared `narrative_v2.yaml` meta-concept schema
- I2 Promote/refactor engine into `core/narrative_engine.py`
- I3 Factual introduction builder
- I4 Type-only Mermaid projector
- I5 Consume per-tool `narrative.yaml` sections (no dead YAML)

## Quality bar
Match nmap/netdiscover structure; improve Introduction to be factual about types/hierarchies.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic I = #{epic_i}")

    epic_j = gh_create(
        "[SPEC-005] Epic J - Adapter cutover + regenerate all narratives",
        f"""## Problem
Adapters still call divergent `to_narrative` stubs. Cut every tool over to the v2 engine and regenerate on-disk graph description markdown.

## Spec binding
SPEC-005 R5-01-12 · Depends on Epic I · Related #826

## Children (order)
- J1 nmap + netdiscover cutover (preserve quality; better intro)
- J2 nerva + pius + subfinder cutover
- J3 httpx + katana + nuclei cutover
- J4 Full corpus backfill/regenerate + inventory update

## Success
All eight tools produce equivalent narrative shape from shared machinery.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic J = #{epic_j}")

    epic_k = gh_create(
        "[SPEC-005] Epic K - Operator visual re-review gate",
        f"""## Problem
Byte-locked goldens must not land until operator confirms v2 narratives + IP classification in the live CLI Profiling UI.

## Spec binding
SPEC-005 R5-01-12 · SPEC-004 R4-01-08 · #932

## Children
- K1 Visual re-review checklist update + sign-off

## Success
Checklist signed; refinement table links closed SPEC-005 issues.
{FOOTER}
""",
        ["epic", "enhancement"],
    )
    print(f"Epic K = #{epic_k}")

    # --- children ---
    g0 = child(
        "G0",
        "Artifact inventory + resolution contract",
        epic_g,
        "R5-01-10",
        """Write `.governance/project/SPEC005_ARTIFACT_INVENTORY.md` listing every examination scenario for the eight adapter tools with: scenario_id, has_structured, has_graph, has_markdown, resolved paths tried, UI visible?, notes.

Document the accepted path resolution order for G1.

Confirm which of the operator-reported misses are (a) UI resolution bugs vs (b) truly missing files:
- netdiscover active text / passive snippet
- nerva JSON scenarios missing descriptions
- nerva `tcp_http_human_text`
- pius `corporate_bbc_terminal`
""",
        "Inventory doc committed; table complete; G1 contract section filled.",
    )

    g1 = child(
        "G1",
        "Fix cli_corpus graph/markdown path resolution",
        epic_g,
        "R5-01-10",
        """Update `spiderfeet/api/services/cli_corpus.py` so graph + markdown resolve for format-suffixed scenario ids (`_text`, `_json`, `_xml`, …).

Add/extend `.tests/api/test_cli_corpus.py` covering:
- netdiscover `local_subnet_active_text` / `passive_snippet_text`
- nerva `tcp_http_rich_json` (or equivalent existing file)

Do not rename all corpus files unless inventory proves necessary; prefer multi-candidate lookup.
""",
        "pytest `.tests/api/test_cli_corpus.py -q` green; manual API/UI check optional.",
        blocked_by=f"G0 #{g0}",
    )

    g2 = child(
        "G2",
        "Text-only scenarios: derive outputs or graph_deferred",
        epic_g,
        "R5-01-11",
        """For `nerva/tcp_http_human_text` and `pius/corporate_bbc_terminal`:
1. Prefer derive structured → graph → narrative via adapter/TextFSM from captured text, OR
2. Mark manifest `graph_deferred: true` with explicit reason and ensure UI surfaces the reason.

Update harvest/backfill + corpus inventory. No silent missing panes.
""",
        "Both scenarios either have graph+md or deferred flag visible in API/UI; inventory updated.",
        blocked_by=f"G1 #{g1}",
    )

    h1 = child(
        "H1",
        "ip_patterns.yaml + core/ip_classify + unit tests",
        epic_h,
        "R5-01-01, R5-01-03",
        """Create `rules/_shared/ip_patterns.yaml` with the operator-provided IPv4/IPv6 regexes and role→nugget_id map.

Implement `core/ip_classify.py` with `classify_ip(value, role=\"host\")`.

Add `.tests/test_ip_classify.py` (v4, compressed v6, full v6, hostname reject, bracketed v6).

Follow schema in SPEC005_AGENT_PLAN.md Epic H.
""",
        "pytest `.tests/test_ip_classify.py -q`",
    )

    h2 = child(
        "H2",
        "Wire topology.py to classify_ip",
        epic_h,
        "R5-01-02",
        """Replace hard-coded `IP_ADDRESS` in `core/topology.py` with `classify_ip`. Support optional role kwarg for callers.

Add/adjust unit tests for topology helpers if present.
""",
        "pytest targeted topology/adapter tests; no IPv6 literals classified as IP_ADDRESS in unit fixtures.",
        blocked_by=f"H1 #{h1}",
    )

    h3 = child(
        "H3",
        "Wire all adapter hooks to classify_ip",
        epic_h,
        "R5-01-02",
        """Update every adapter path that creates IP nodes (nmap, netdiscover, nerva, httpx, subfinder, and any others) to call `classify_ip`.

Affiliate/internal roles when the seed/mapping already implies them.

Governance: no new hardcoded IP regex in adapters.
""",
        "Adapter unit tests green; grep adapters for raw `IP_ADDRESS` string usage reviewed in PR.",
        blocked_by=f"H2 #{h2}",
    )

    h4 = child(
        "H4",
        "Regenerate graphs / IPv6 fixture evidence",
        epic_h,
        "R5-01-02, R5-01-12",
        """Backfill graphs for IP-emitting tools. If no examination contains IPv6, add a unit-test structured fixture proving `IPV6_ADDRESS` emission.

Update inventory notes.
""",
        "Evidence of IPV6_ADDRESS in a fixture or regenerated graph; backfill command documented.",
        blocked_by=f"H3 #{h3}",
    )

    i1 = child(
        "I1",
        "Shared narrative_v2.yaml meta-concept schema",
        epic_i,
        "R5-01-05",
        """Create `rules/_shared/narrative_v2.yaml` defining meta-concepts (scan, host, system, cdn, trace), category order, appendix/footer defaults, and Mermaid type-relation policy.

Update `rules/_template/narrative.yaml` to v2 shape.

Document keys in SPEC005_AGENT_PLAN / ONBOARDING if needed.
""",
        "YAML loads; schema documented; template updated.",
        blocked_by=f"Prefer after H1 #{h1} (can draft in parallel with H2–H4)",
    )

    i2 = child(
        "I2",
        "core/narrative_engine.py (promote narrative_report)",
        epic_i,
        "R5-01-04",
        """Refactor `narrative_report.py` into `core/narrative_engine.py` with `render_narrative(...)`.

Keep shim re-exports so nmap/netdiscover keep working until J1.

Add `.tests/test_narrative_engine_v2.py` skeleton asserting section headers + appendix coverage for a small fixture graph.
""",
        "pytest narrative engine tests + existing nmap/netdiscover narrative tests still green.",
        blocked_by=f"I1 #{i1}",
    )

    i3 = child(
        "I3",
        "Factual introduction builder",
        epic_i,
        "R5-01-08",
        """Implement centralized intro that explains tool + ontology hierarchy (types/containment) as a guide to report layout. Use shared YAML + per-tool `intro_facts` / phrasing.

Example tone: factual Nuclei/SECURITY category style from operator notes — improve wording, keep facts.
""",
        "Unit test: intro mentions tool and at least one meta-concept/category hierarchy phrase.",
        blocked_by=f"I2 #{i2}",
    )

    i4 = child(
        "I4",
        "Type-only Mermaid projector",
        epic_i,
        "R5-01-07",
        """Implement `type_relation_mermaid(graph, ...)` that emits nugget_id nodes and relations only (no nugget_data labels) for section diagrams.

Integrate into each meta-concept and category subsection renderer.

Test that sample Mermaid output does not contain dotted IPv4 or colon IPv6 literals.
""",
        "pytest asserts Mermaid type-only; fixture coverage.",
        blocked_by=f"I2 #{i2}",
    )

    i5 = child(
        "I5",
        "Consume per-tool narrative.yaml sections",
        epic_i,
        "R5-01-06",
        """Engine must read and honor `sections` / `meta_concepts` / `host_nugget_id` / `include_trace` / `include_appendix` / `phrasing` from `rules/<tool>/narrative.yaml`.

Update all eight tool narrative YAML files to v2 schema (can be minimal toggles; phrasing retained).

Kill dead config: if a key exists in YAML, the engine uses it or the key is removed.
""",
        "Tests prove two different profiles change section presence; YAML keys documented.",
        blocked_by=f"I2 #{i2}, I3 #{i3}, I4 #{i4}",
    )

    j1 = child(
        "J1",
        "Cutover nmap + netdiscover to narrative v2",
        epic_j,
        "R5-01-04, R5-01-08, R5-01-12",
        """Replace dedicated narrative builders with `render_narrative`. Preserve section/Mermaid/table/appendix quality; improve Introduction only.

Regenerate nmap + netdiscover description MD files in the same PR if content changes.
""",
        "Adapter tests + spot-check one nmap and one netdiscover MD against quality bar.",
        blocked_by=f"I5 #{i5}",
    )

    j2 = child(
        "J2",
        "Cutover nerva + pius + subfinder to narrative v2",
        epic_j,
        "R5-01-04, R5-01-12",
        """Delete inline stub `to_narrative` implementations; call engine. Expand YAML for CDN/org meta-concepts as needed.

Regenerate affected `nugget_structure/*_description.md`.
""",
        "Adapter tests + narrative coverage tests; sample MD has meta-concept sections + type Mermaid.",
        blocked_by=f"J1 #{j1}",
    )

    j3 = child(
        "J3",
        "Cutover httpx + katana + nuclei to narrative v2",
        epic_j,
        "R5-01-04, R5-01-12",
        """Same as J2 for httpx/katana/nuclei. Nuclei intro must factually describe findings under host security/vuln category containment.
""",
        "Adapter tests + sample nuclei MD reviewed against quality bar.",
        blocked_by=f"J2 #{j2}",
    )

    j4 = child(
        "J4",
        "Full corpus regenerate + inventory refresh",
        epic_j,
        "R5-01-12",
        """Run `backfill_adapter_four_outputs.py --force` (or harvest) for all adapter tools.

Refresh `SPEC005_ARTIFACT_INVENTORY.md`. Ensure G2 deferred cases remain correctly flagged.
""",
        "Inventory shows complete or deferred for every scenario; PR includes regenerated artifacts.",
        blocked_by=f"J3 #{j3}, G2 #{g2}",
    )

    k1 = child(
        "K1",
        "Operator visual re-review + sign-off",
        epic_k,
        "R5-01-12 · R4-01-08",
        """Update visual review checklist with SPEC-005 outcomes. Operator marks pass/fail in CLI Profiling UI for all eight tools.

Link closed child issues in refinement table. Sign off only when satisfied — then Phase 4 byte goldens may proceed under a separate issue.
""",
        "Checklist signed in-repo; no byte golden lock inside this story unless operator explicitly requests.",
        blocked_by=f"J4 #{j4}",
    )

    # index
    rows = [
        ("Epic G", epic_g),
        ("Epic H", epic_h),
        ("Epic I", epic_i),
        ("Epic J", epic_j),
        ("Epic K", epic_k),
        ("G0", g0),
        ("G1", g1),
        ("G2", g2),
        ("H1", h1),
        ("H2", h2),
        ("H3", h3),
        ("H4", h4),
        ("I1", i1),
        ("I2", i2),
        ("I3", i3),
        ("I4", i4),
        ("I5", i5),
        ("J1", j1),
        ("J2", j2),
        ("J3", j3),
        ("J4", j4),
        ("K1", k1),
    ]
    lines = [
        "# SPEC-005 issue index",
        "",
        "Generated by `.seed/scripts/cli_corpus/create_spec005_issues.py`.",
        "",
        "**Plan:** `.governance/project/SPEC005_AGENT_PLAN.md`  ",
        "**Spec:** `.governance/specs/SPEC-005-narrative-v2-ip-classify.md`",
        "",
        "| Code | Issue |",
        "|------|-------|",
    ]
    for code, num in rows:
        lines.append(f"| {code} | [#{num}](https://github.com/brettforbes/spiderfeet/issues/{num}) |")
    lines.extend(
        [
            "",
            "## Execution order",
            "",
            "```",
            "G0 -> G1 -> G2",
            "  -> H1 -> H2 -> H3 -> H4",
            "    -> I1 -> I2 -> I3 -> I4 -> I5",
            "      -> J1 -> J2 -> J3 -> J4",
            "        -> K1 (operator)",
            "```",
            "",
            "H1 may start in parallel with G1 after G0. I1 may draft in parallel with H2–H4.",
            "",
            "Lesser agents: pick next unblocked child; read SPEC005_AGENT_PLAN.md epic section first.",
            "",
        ]
    )
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {INDEX}")


if __name__ == "__main__":
    main()
