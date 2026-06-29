# Examination Checklist (per CLI tool)

## Exploration (before saving evidence)

- [ ] Confirm binary on PATH (Windows and/or WSL per manifest)
- [ ] Capture `--help` / `-h` / manual text → `cli_help_text/<tool>_cli_help_text.md`
- [ ] Identify output path type (1=structured+text, 2=structured only, 3=text only)
- [ ] **Draft semantic outcome matrix** — every distinct output shape with planned scenario id (rich, sparse, empty, error, clean miss, mode/format variants)
- [ ] List command families that change **semantic data types** (not just formatting)
- [ ] Compare permissive vs corporate target behaviour; tune inputs until each matrix row is demonstrated or documented as impossible
- [ ] Search the web for practitioner example commands when local trials under-deliver
- [ ] Write formal examination plan with scenario ids
- [ ] Write `.strategy/<tool>_strategy.skill`

## Formal examination

- [ ] Add/update `.seed/scripts/cli_corpus/manifests/<tool>.yaml`
- [ ] Run `harvest.py` for each scenario (structured + text per rules; `cls` before text-only runs)
- [ ] Verify structured JSON includes command, timestamp, scan metadata, and `exit_status` (text-only tools)
- [ ] Confirm structured counts match text (`scan_tries`, `empty_scans`, row counts)
- [ ] Confirm no `head`/`tail` truncation in manifest commands or captured text
- [ ] Verify `*_manifest.json` and outputs exist
- [ ] Graph via `graph_builder.py` pattern; `validate_graph()` passes (no orphans/duplicates)
- [ ] Load nugget templates from `nuggets.json` + `nuggets_extension.json`; new types only in extension
- [ ] Draft `nugget_structure/<tool>_nugget_graph_structure.md`
- [ ] Draft per-scenario `*_proposed_nuggets_edges_description.md` (§4.3 narrative)
- [ ] Set `*_review.status.json` to `pending`

## Operator gate

- [ ] Operator reviews text, data, graph proposal, narrative report
- [ ] Operator sets review status `approved` or `rejected` (all legacy bundles for a scenario key update together)
- [ ] On approval: record sign-off doc under `.docs/docs-for-cli-tools/<tool>_pilot_signoff.md`
- [ ] On approval: set `corpus_index.json` tool phase to `complete` when pilot criteria met
- [ ] On approval: update `nuggets_extension.json` / TypeQL as needed (not `nuggets.json` for new tool types)

## Do not

- Brute-force every flag permutation
- Skip corporate-target scenarios
- Promote nugget types without evidence bundle
- Run Aircrack-ng until hardware available
