# SPEC-004 operator visual review checklist (R4-01-08)

**Issue:** [#932](https://github.com/brettforbes/spiderfeet/issues/932)  
**Spec:** `.governance/specs/SPEC-004-cli-graph-rules-engine.md` (R4-01-08)  
**Gate:** Do **not** lock golden graph/narrative byte fixtures until this checklist is signed off.

## Purpose

Before Phase 4 golden fixtures, an operator reviews live CLI Profiling UI output for each
adapter tool: **Text**, **Structured**, **Graph**, and **Markdown Report**. Structural
pytest coverage (`validate_narrative_coverage`, connectivity) is necessary but not
sufficient for this gate.

## How to review

1. Start the CLI Profiling UI (or open harvested examination bundles under
   `.docs/docs-for-cli-tools/app_examination_docs/<tool>/`).
2. For each tool/scenario row below, open all four panes.
3. Mark pass/fail/notes per scenario.
4. Log refinement follow-ups in the tracking table (engine, YAML, phrasing, nugget ids).
5. Sign off at the bottom when satisfied.

**Harvest command (when re-generating artifacts):**

```bash
python .seed/scripts/cli_corpus/harvest.py --tool <tool> --scenario <scenario_id>
```

**Automated pre-check (does not replace visual review):**

```bash
python -m pytest .tests/test_spec004_narrative_coverage.py .tests/test_harvest_adapter_dispatch.py -q
```

## Per-tool review matrix

| Tool | Capture family | Narrative profile | Example scenario | Text | Structured | Graph | Markdown | Reviewer | Date |
|------|----------------|-------------------|------------------|------|------------|-------|----------|----------|------|
| netdiscover | text_native | `rules/netdiscover/narrative.yaml` | `local_subnet_active_parsable` | ☐ | ☐ | ☐ | ☐ | | |
| nmap | structured_native (XML) | `rules/nmap/narrative.yaml` | `nse_default_permissive` | ☐ | ☐ | ☐ | ☐ | | |
| nerva | structured_native | `rules/nerva/narrative.yaml` | `tcp_list_file_json` | ☐ | ☐ | ☐ | ☐ | | |
| pius | structured_native | `rules/pius/narrative.yaml` | `crt_linode_ndjson` | ☐ | ☐ | ☐ | ☐ | | |
| subfinder | structured_native | `rules/subfinder/narrative.yaml` | `corporate_k2am_passive_cs` | ☐ | ☐ | ☐ | ☐ | | |
| httpx | structured_native | `rules/httpx/narrative.yaml` | `from_subfinder_k2am_passive` | ☐ | ☐ | ☐ | ☐ | | |
| katana | structured_native | `rules/katana/narrative.yaml` | `from_httpx_k2am_passive` | ☐ | ☐ | ☐ | ☐ | | |
| nuclei | structured_native | `rules/nuclei/narrative.yaml` | `pg_dvwa_tech_fingerprint` | ☐ | ☐ | ☐ | ☐ | | |

### Pane expectations

| Pane | Pass criteria |
|------|----------------|
| **Text** | Human-readable; derived or native body matches structured record count; no progress-only banners where findings expected |
| **Structured** | Single-root JSON/XML parses in Data Viewer; `records[]` / scan metadata present |
| **Graph** | Force graph renders; no orphan nodes; hierarchy matches seed ontology intent |
| **Markdown** | Section order matches `narrative.yaml`; appendix lists every node value; tool-specific phrasing (CDN indeterminate, relation deferrals) reads correctly |

## Refinement follow-ups (hydrate before golden lock)

| ID | Tool | Area (engine / YAML / phrasing / nugget_id) | Observation | GitHub issue | Status |
|----|------|---------------------------------------------|-------------|--------------|--------|
| VR-001 | all | UI resolution | Format-suffixed scenario keys may hide existing graph/MD | [#964](https://github.com/brettforbes/spiderfeet/issues/964) (G1) | open |
| VR-002 | all | nugget_id | IPv6 literals incorrectly mapped as `IP_ADDRESS` | [#959](https://github.com/brettforbes/spiderfeet/issues/959) (Epic H) | open |
| VR-003 | all | engine / YAML | Stub narratives for non-nmap/netdiscover tools; need §4.3 v2 | [#960](https://github.com/brettforbes/spiderfeet/issues/960) (Epic I) | open |
| VR-004 | nerva / pius | missing artifacts | Text-only scenarios lack graph/MD | [#965](https://github.com/brettforbes/spiderfeet/issues/965) (G2) | open |

Program plan: `.governance/project/SPEC005_AGENT_PLAN.md` · Index: `.governance/project/SPEC005_ISSUE_INDEX.md`

Add rows as needed. Do not collapse unrelated gaps into one vague item.

## Sign-off

| Field | Value |
|-------|-------|
| Operator | _pending_ |
| Date | _pending_ |
| Tools reviewed | _all eight / subset listed_ |
| Golden lock authorized | **No** until sign-off complete |
| Notes | |

When signed off, update this table and comment on [#932](https://github.com/brettforbes/spiderfeet/issues/932)
with evidence paths. Golden fixture work may then proceed under Phase 4 issues.

## Related artifacts

- Issue index: `.governance/project/SPEC004_ISSUE_INDEX.md`
- **Refinement program:** `.governance/project/SPEC005_ISSUE_INDEX.md` · `.governance/specs/SPEC-005-narrative-v2-ip-classify.md`
- Adapter onboarding: `.seed/scripts/cli_corpus/ONBOARDING.md`
- Narrative coverage tests: `.tests/test_spec004_narrative_coverage.py`
- Harvest adapter dispatch: `.tests/test_harvest_adapter_dispatch.py`
