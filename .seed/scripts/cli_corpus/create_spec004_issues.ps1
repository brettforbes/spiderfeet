# SPEC-004 GitHub issue creation script
# Creates epics A-E then child stories with parent links.
# Run from repo root: powershell -File .seed/scripts/cli_corpus/create_spec004_issues.ps1

$ErrorActionPreference = "Stop"
$Repo = "brettforbes/spiderfeet"
$Org = "brettforbes"
$Name = "spiderfeet"

function New-Issue {
  param(
    [string]$Title,
    [string]$Body,
    [string[]]$Labels = @("enhancement")
  )
  $labelArgs = @()
  foreach ($l in $Labels) { $labelArgs += @("--label", $l) }
  $tmp = New-TemporaryFile
  # gh on Windows: use --body-file
  Set-Content -Path $tmp -Value $Body -Encoding utf8
  $url = gh issue create --repo $Repo --title $Title --body-file $tmp @labelArgs
  Remove-Item $tmp -Force
  if ($url -match '/issues/(\d+)') { return [int]$Matches[1] }
  throw "Failed to parse issue number from: $url"
}

$commonFooter = @"

## Branch
``feature/<issue>-<slug>`` from ``develop`` · PR into ``develop``

## Forbidden (all SPEC-004 stories)
- Do not invent Nexus or create nexus adapters
- Do not lock golden graph/narrative byte fixtures before visual-review story D7
- Do not rewrite production ``sfp_*`` modules unless under Epic E
- Do not add divergent UUID helpers (use shared ``graph_builder.nugget_instance_id`` only)
- Do not invent relations outside ``contains`` / ``had`` / ``listens-to`` without seed+SPEC update

## Agent rule
``.cursor/rules/proj-07-cli-graph-rules-engine.mdc`` · Spec ``.governance/specs/SPEC-004-cli-graph-rules-engine.md``
"@

Write-Host "Creating Epic A..."
$epicA = New-Issue -Title "[SPEC-004] Epic A — Foundations (identity, core/, governance)" -Labels @("epic","enhancement") -Body @"
## Problem
CLI structured→graph conversion embeds rules in per-tool Python with divergent identity helpers. Foundations must land before the rule engine and adapters.

## Spec binding
SPEC-004 R4-01-01, R4-01-02, R4-01-07 · Related #826 #723

## Children (execute in order)
- A1 SPEC-004 file (may already be landed — verify)
- A2 Canonical identity; remove ``_uid`` divergence
- A3 Create ``core/`` package; move ``graph_builder``
- A4 Catalogue extensions (SYSTEM, MAC_VENDOR, CDN/correlation descriptors)
- A5 ``proj-07`` rule + ONBOARDING + ``_template`` (may already be landed — verify)
- A6 Cleanup doc 14 §1.8 seed list

## Success criteria
All child stories closed; lesser agents can start Epic B without foundation blockers.
$commonFooter
"@

Write-Host "Epic A = #$epicA"

$epicB = New-Issue -Title "[SPEC-004] Epic B — Rule engine + Nmap/Netdiscover pilots" -Labels @("epic","enhancement") -Body @"
## Problem
Mapping/topology rules are hardcoded in converters. Need shared ``rule_engine`` + YAML packs, proven on both capture families.

## Spec binding
R4-01-02, R4-01-03, R4-01-06 · Parent coordination Epic A #$epicA · Related #826

## Children
- B1 ``rule_engine.py`` + ``_shared`` YAML schemas
- B2 Topology templates (scan_head, host stack, system_l2, trace)
- B3 Netdiscover adapter — **text_native** + TextFSM
- B4 Nmap adapter — **structured_native** + 06B hooks
- B5 Harvest dispatch via adapters only; always emit four artifacts

## Depends on
Epic A foundations (A2–A3 especially).
$commonFooter
"@
Write-Host "Epic B = #$epicB"

$epicC = New-Issue -Title "[SPEC-004] Epic C — Correlation + Nerva (07 + 07B)" -Labels @("epic","enhancement") -Body @"
## Problem
Nerva correlation A/B/C and ontology rules N0–N5 exist only as markdown. Minimal ``nerva_to_graph`` ignores them.

## Spec binding
R4-01-04, R4-01-05, R4-01-06 · Seeds:
- ``.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md``
- ``.seed/07B_Nerva_Ontology_Rules.md``

## Children
- C1 CDN signatures + ASN YAML (from 07)
- C2 ``correlation_engine.py`` A→C→B
- C3 Nerva adapter + ``rules/nerva/`` from 07B (calls C2)
- C4 Nerva narrative + four-output harvest

## Depends on
Epic B engine + shared identity.
$commonFooter
"@
Write-Host "Epic C = #$epicC"

$epicD = New-Issue -Title "[SPEC-004] Epic D — Remaining tools + narratives + visual review" -Labels @("epic","enhancement") -Body @"
## Problem
Pius, Subfinder, Httpx, Katana, Nuclei lack full four-output pipelines under the shared engine. Narratives and operator visual review must complete before goldens.

## Spec binding
R4-01-05, R4-01-06, R4-01-08

## Children
- D1 Pius (seed 08)
- D2 Subfinder (seed 09)
- D3 Httpx (seed 10)
- D4 Katana
- D5 Nuclei (seeds 11 + 11B)
- D6 Narrative YAML + harvest MD for D1–D5
- D7 Operator visual-review checklist + refinement tracking

## Depends on
Epic B (engine); Epic C patterns helpful for CDN-ish tools.
$commonFooter
"@
Write-Host "Epic D = #$epicD"

$epicE = New-Issue -Title "[SPEC-004] Epic E — Second push: thin sfp_<app> modules (placeholder)" -Labels @("epic","enhancement") -Body @"
## Problem
After goldens, production modules should call shared adapters (abuse.ch-shaped thin wrappers) instead of embedding mapping logic.

## Spec binding
R4-01-09

## Status
**Placeholder only.** Do not create child coding stories until Phase 4 goldens (after D7 visual review).

## Future children (deferred)
- Design note: graph→event flatten vs dual-emit
- Pilot ``sfp_nmap`` / ``sfp_tool_nmap`` on shared adapter
- Pattern doc + one issue per remaining tool module

## Related
#723 #796 #797 · Example shape: ``modules/sfp_abusech.py``
$commonFooter
"@
Write-Host "Epic E = #$epicE"

# --- Child stories ---
function Child($code, $title, $parent, $spec, $bodyExtra, $labels = @("enhancement")) {
  $body = @"
## Problem
See parent epic #$parent. This story is the bounded unit: **$code**.

## Spec binding
$spec · Parent epic #$parent · Related #826

$bodyExtra

## Acceptance criteria
- [ ] Scope below completed with evidence (paths + commands)
- [ ] Forbidden list in parent epic respected
- [ ] PR to ``develop`` links this issue

## Verification
Document exact commands run (pytest / harvest) in the PR or issue comment.
$commonFooter
"@
  $n = New-Issue -Title "[SPEC-004] $code — $title" -Body $body -Labels $labels
  Write-Host "$code = #$n"
  return $n
}

Child "A1" "Verify/land SPEC-004 + BACKLOG link" $epicA "R4-01-*" @"
## Scope
- Ensure ``.governance/specs/SPEC-004-cli-graph-rules-engine.md`` exists and matches program
- Ensure ``.governance/project/BACKLOG.md`` links SPEC-004
- If already landed in setup PR, verify and close with comment

## Files
``.governance/specs/SPEC-004-cli-graph-rules-engine.md``, ``.governance/project/BACKLOG.md``
"@

Child "A2" "Canonical identity; remove cli_tool_to_graph _uid divergence" $epicA "R4-01-01" @"
## Scope
- All converters import ``graph_builder.nugget_instance_id`` / shared GraphBuilder
- Delete divergent ``_uid`` in ``cli_tool_to_graph.py``
- Add test that fails if alternate UUID namespace schemes are introduced

## Files
``.seed/scripts/cli_corpus/cli_tool_to_graph.py``, ``graph_builder.py``, ``nmap_xml_to_graph.py``, ``.tests/``
"@

Child "A3" "Create core/ package; move graph_builder" $epicA "R4-01-02" @"
## Scope
- Introduce ``.seed/scripts/cli_corpus/core/`` with ``graph_builder.py`` (move or re-export shim)
- Keep old imports green during migration
- Add ``types.py`` stubs for RulePack / CaptureFamily if needed for later stories

## Files
``.seed/scripts/cli_corpus/core/**``, shims at old paths
"@

Child "A4" "Catalogue extensions for SYSTEM, MAC_VENDOR, CDN/correlation descriptors" $epicA "R4-01-01" @"
## Scope
- Add missing nugget types used by netdiscover/nerva seeds to ``nuggets_extension.json``
- Document any TypeQL follow-up (do not block if TypeQL is separate issue)
- Prefer reuse before invent (proj-05)

## Seeds
``.seed/07B_Nerva_Ontology_Rules.md`` vocabulary tables · netdiscover structure docs
"@

Child "A5" "Verify/land proj-07 rule + ONBOARDING + _template dirs" $epicA "R4-01-07" @"
## Scope
- Ensure ``.cursor/rules/proj-07-cli-graph-rules-engine.mdc`` exists
- Add ``.seed/scripts/cli_corpus/ONBOARDING.md`` checklist for new tools
- Add ``rules/_template/`` and ``adapters/_template/`` skeletons
- Cross-links from proj-05/06 if missing
"@

Child "A6" "Cleanup doc 14 seed list (no Nexus; include 07B + Nuclei 11)" $epicA "R4-01-06" @"
## Scope
- ``.seed/14_Business_Rules_for_Converting_Structured_Data_to_Graph.md`` §1.8 lists: 06B, 07, 07B, 08, 09, 10, 11, 11B + SPEC-004/proj-07 pointers
- Confirm no Nexus file remains under ``.seed/``
- If already fixed in setup, verify and close
"@

Child "B1" "rule_engine.py + _shared YAML schemas" $epicB "R4-01-02" @"
## Scope
- Implement ``core/rule_engine.py`` that loads YAML packs and emits via GraphBuilder
- ``rules/_shared/``: relations, scan_head, categories, identity, validation, four_outputs
- Unit tests: load invalid pack fails; minimal pack creates SCAN_RECORD

## Depends on
A3
"@

Child "B2" "Shared topology templates" $epicB "R4-01-02" @"
## Scope
- Templates: scan_head, host_networks_port_service, system_l2, trace_hop_chain
- Fixture tests prove expected edges/relations

## Depends on
B1
"@

Child "B3" "Netdiscover adapter — text_native + TextFSM" $epicB "R4-01-03 R4-01-06" @"
## Capture family
``text_native``

## Scope
- ``adapters/netdiscover/``: text→structured (existing TextFSM path), to_graph via rules, to_text, to_narrative
- ``rules/netdiscover/`` mapping + narrative YAML
- Harvest writes **four** artifacts
- Structural tests only (no golden lock)

## Seeds
Existing netdiscover structure docs + converters
"@

Child "B4" "Nmap adapter — structured_native + 06B hooks" $epicB "R4-01-03 R4-01-06" @"
## Capture family
``structured_native``

## Scope
- ``adapters/nmap/``: XML→intermediate→rule_engine; hooks cite ``06B`` rule ids
- ``rules/nmap/`` from ``.seed/06B_NMAP_Ontology_Update_Ruleset.md``
- Four artifacts; structural tests; regenerate proposed graphs for visual review

## Depends on
B1 B2; prefer after B3 pattern exists
"@

Child "B5" "Harvest dispatch via adapters only; four artifacts always" $epicB "R4-01-01 R4-01-06" @"
## Scope
- ``harvest.py`` imports only ``adapters.<tool>``
- Remove dead direct converter imports for migrated tools
- Contract: Text, Structured, Graph, Markdown written for each formal scenario

## Depends on
B3 B4
"@

Child "C1" "CDN signatures + ASN YAML from seed 07" $epicC "R4-01-04" @"
## Scope
- ``rules/_shared/cdn_signatures.yaml`` and ``edge_asns.yaml`` versioned from seed 07
- Document update process in ONBOARDING or README

## Seed
``.seed/07_Nerva_Scan_Record_Host_Correlation_Rulesets.md`` Ruleset C
"@

Child "C2" "correlation_engine.py A→C→B with fired-rule evidence" $epicC "R4-01-04" @"
## Scope
- Implement chaining: per hostname → A → C first → B if not fronted
- Outputs: same_system_*, host_classification, classification_rule_fired, confidence
- Unit tests: scanme dual-stack same system; praetorian Cloudflare fronted (fixtures from seed 07 appendix)

## Depends on
C1 · Seeds 07
"@

Child "C3" "Nerva adapter + rules from 07B (calls correlation)" $epicC "R4-01-04 R4-01-06" @"
## Capture family
``structured_native``

## Scope
- ``adapters/nerva/`` + ``rules/nerva/`` implementing Rules **N0–N5** from ``.seed/07B_Nerva_Ontology_Rules.md``
- N1 must invoke correlation_engine (C2) before creating HOST/CDN nodes
- Replace minimal ``cli_tool_to_graph.nerva_to_graph``
- Four outputs; structural tests

## Seeds
07 + 07B · Watch #880 if fixtures invalid
"@

Child "C4" "Nerva narrative profile + four-output harvest" $epicC "R4-01-05" @"
## Scope
- ``rules/nerva/narrative.yaml`` + harvest writes ``*_description.md``
- Run narrative coverage validator where applicable
- Document CDN / indeterminate origin phrasing per 07/07B

## Depends on
C3
"@

Child "D1" "Pius adapter + rules + four outputs" $epicD "R4-01-06" @"
## Capture family
``structured_native`` (NDJSON bundle)

## Seed
``.seed/08_Rules_for_Pius.md``
"@

Child "D2" "Subfinder adapter + rules + four outputs" $epicD "R4-01-06" @"
## Capture family
``structured_native``

## Seed
``.seed/09_Ontology_For_Subfinder.md``
"@

Child "D3" "Httpx adapter + rules + four outputs" $epicD "R4-01-06" @"
## Capture family
``structured_native``

## Seed
``.seed/10_Rules_For_Httpx.md``
"@

Child "D4" "Katana adapter + rules + four outputs" $epicD "R4-01-06" @"
## Capture family
``structured_native``

## Scope
Migrate existing ``katana_json_to_graph.py`` onto adapter + YAML; align hierarchy with proj-05
"@

Child "D5" "Nuclei adapter + rules + four outputs" $epicD "R4-01-06" @"
## Capture family
``structured_native``

## Seeds
``.seed/11_Ontology_for_Nuclei.md`` · ``.seed/11B_Rules_for_Nuclei.md``
"@

Child "D6" "Narrative YAML + harvest MD for D1–D5" $epicD "R4-01-05" @"
## Scope
- Narrative profiles for pius, subfinder, httpx, katana, nuclei
- Harvest writes Markdown Report for each
- Coverage validator smoke tests

## Depends on
D1–D5
"@

Child "D7" "Operator visual-review checklist + refinement tracking" $epicD "R4-01-08" @"
## Scope
- Checklist doc for reviewing Text/Structured/Graph/Markdown panes per tool
- Tracking issue or section for refinement follow-ups (engine/YAML/phrasing/ids)
- Explicit gate: **no golden locks until this review is signed off by operator**

## Depends on
D6 · C4 · B3/B4 narratives
"@

# Index file for handoff
$index = @"
# SPEC-004 issue index (generated)

| Code | Issue |
|------|-------|
| Epic A | #$epicA |
| Epic B | #$epicB |
| Epic C | #$epicC |
| Epic D | #$epicD |
| Epic E | #$epicE |

See GitHub search: ``[SPEC-004]`` in brettforbes/spiderfeet.

Execution order: A1→A6, then B1→B5, then C1→C4, then D1→D7; Epic E deferred.
"@
Set-Content -Path "C:\projects\spiderfeet\.governance\project\SPEC004_ISSUE_INDEX.md" -Value $index -Encoding utf8
Write-Host "Wrote SPEC004_ISSUE_INDEX.md"
Write-Host "DONE epics A=$epicA B=$epicB C=$epicC D=$epicD E=$epicE"
