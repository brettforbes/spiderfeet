# Examination Checklist (per CLI tool)

## Exploration (before saving evidence)

- [ ] Confirm binary on PATH (Windows and/or WSL per manifest)
- [ ] Capture `--help` / `-h` / manual text → `cli_help_text/<tool>_cli_help_text.md`
- [ ] Identify output path type (1=structured+text, 2=structured only, 3=text only)
- [ ] List command families that change **semantic data types** (not just formatting)
- [ ] Compare permissive vs corporate target behaviour
- [ ] Write formal examination plan with scenario ids
- [ ] Write `.strategy/<tool>_strategy.skill`

## Formal examination

- [ ] Add/update `.seed/scripts/cli_corpus/manifests/<tool>.yaml`
- [ ] Run `harvest.py` for each scenario (structured + text per rules)
- [ ] Verify `*_manifest.json` and outputs exist
- [ ] Draft `nugget_structure/<tool>_nugget_graph_structure.md`
- [ ] Set `*_review.status.json` to `pending`

## Operator gate

- [ ] Operator reviews text, data, graph proposal
- [ ] Operator sets review status `approved` or `rejected`
- [ ] On approval: update ontology / `nuggets.json` extensions as needed

## Do not

- Brute-force every flag permutation
- Skip corporate-target scenarios
- Promote nugget types without evidence bundle
- Run Aircrack-ng until hardware available
