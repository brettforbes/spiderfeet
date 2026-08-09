# SPEC-014 BD1 — nmap / netdiscover match-or-beat criteria

**Issue:** #1185 · **Requirement:** R14-06 · **Consumed by:** BD2 (#1186)

These Markdown files are a frozen snapshot of bespoke `NarrativeReportBuilder` /
`NetdiscoverNarrativeReportBuilder` output **before** unification onto the shared
meta-concept engine. BD2 must regenerate narratives through `render_narrative` and
**match or beat** this baseline before deleting the bespoke builders.

Snapshot taken from `.docs/docs-for-cli-tools/nugget_structure/` on the BD1 branch
(post-BC2 develop). Count: see `MANIFEST.json`.

## Gate (all must pass)

### G1 — Coverage (match)

For every snapshotted scenario, load the sibling `*_proposed_nuggets_edges.json`
from the live nugget_structure tree and the **new** Markdown from
`render_narrative`. `validate_narrative_coverage(graph, new_md)` must pass with
an empty missing list.

### G2 — Prior section families present (match)

When the graph contains the supporting nugget types, the new Markdown must retain
these **section families** (heading text may modernize to registry headings such
as `## Scan`, `## Host`, `## System`, `## Trace`):

| Tool | Required when present |
|------|------------------------|
| nmap | Introduction; Scan; one Host (or Hosts) section per host entity; Conclusion; Appendix |
| nmap | Networks / Applications subsections (or category subsections) when those category nodes exist |
| nmap | Trace (or hop chain) when TRACE / hop nodes exist |
| nmap | Environment / OS prose or category section when OPERATING_SYSTEM (or ENVIRONMENT) exists |
| netdiscover | Introduction; Scan; one System section family per SYSTEM; Networks inventory; Conclusion; Appendix |

Use `extract_h2_headings` / family mapping in `match_or_beat.py` — do not require
byte-identical titles from the bespoke builder.

### G3 — Progressive disclosure (beat)

New Markdown must add (when concepts are present):

1. Per meta-concept: a `### Structure overview` (or equivalent) **type-only** Mermaid.
2. Per category with instances: capped **example** Mermaid (`example_cap`, `+N more`) **and** a full value table.
3. Exactly one appendix edge inventory (no duplicated `### Edges` / repeated edge rows after every category).

### G4 — Diagram hygiene (beat)

- Each Mermaid block ≤ registry `max_shapes` (default 12).
- Overview Mermaid blocks remain type-only (no IP / URL / CVE literals as node labels).
- Category example diagrams may show capped values (R14-05).

### G5 — No value loss vs snapshot (match)

Every distinct `nugget_data` string that appears in the reference Markdown appendix
(or body) must still appear somewhere in the new Markdown. Prefer proving this via
G1 (`validate_narrative_coverage`) against the live graph; treat the snapshot as
the human-readable baseline for operator diff review.

### G6 — Bespoke retirement (BD2 only)

Only after G1–G5 pass for **all** snapshotted scenarios:

- Remove hard-branch to `build_nmap_narrative_report` / `build_netdiscover_narrative_report` in `narrative_engine.py`.
- Delete `NarrativeReportBuilder` / `NetdiscoverNarrativeReportBuilder` (and thin wrappers) from `narrative_report.py` (+ modules_v2 mirror).
- Keep `validate_narrative_coverage` and any non-narrative helpers that other tools need.

## How to run the gate (BD2)

```bash
poetry run python .seed/scripts/cli_corpus/match_or_beat.py --reference \
  .seed/scripts/cli_corpus/fixtures/spec014_bd1_narrative_reference
```

Exit 0 = all scenarios pass G1–G5. Exit 1 = print failing scenario keys.

## Out of scope for the gate

- Byte-identical prose vs the bespoke story tone.
- Preserving value-labelled Mermaid in netdiscover “Scan topology” / per-system
  diagrams that exceed the shape cap — BD2 may replace those with capped
  overview + example + table progressive disclosure (that is a **beat**).
