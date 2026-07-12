# Examination Checklist (per CLI tool)

## Exploration (before saving evidence)

- [ ] Confirm binary on PATH (Windows and/or WSL per manifest)
- [ ] Capture `--help` / `-h` / manual text → `cli_help_text/<tool>_cli_help_text.md`
- [ ] Identify output path: structured-available (use structured only) vs true text-only (TextFSM required)
- [ ] **Draft semantic outcome matrix** — every distinct output shape with planned scenario id (rich, sparse, empty, error, clean miss, mode/format variants)
- [ ] List command families that change **semantic data types** (not just formatting)
- [ ] Compare permissive vs corporate target behaviour; tune inputs until each matrix row is demonstrated or documented as impossible
- [ ] Add intentional vuln-lab and/or smaller-org rows when the tool's value is CVE/app-class or org enrichment (not only CDN corporate)
- [ ] Validate CLI argument forms produce output before locking manifest commands (hostname vs URL, protocol family, API keys)
- [ ] For multi-mode scanners: draft one-batch-one-goal passes; write tool strategy skill before formal plan
- [ ] Search the web for practitioner example commands when local trials under-deliver
- [ ] Write formal examination plan with scenario ids
- [ ] Write `.strategy/<tool>_strategy.skill`

## Formal examination

- [ ] Follow `.seed/scripts/cli_corpus/ONBOARDING.md` (adapter + YAML path — no new `*_to_graph.py`)
- [ ] Add/update `.seed/scripts/cli_corpus/manifests/<tool>.yaml`
- [ ] Scaffold `adapters/<tool>/` + `rules/<tool>/mapping.yaml` + `narrative.yaml` from `_template/`
- [ ] Wire tool into `harvest.py` `ADAPTER_TOOLS`; implement `build_outputs`
- [ ] Run `harvest.py` for each scenario (structured flags when available; derive Text; `cls` before true text-native runs only)
- [ ] For WSL tools: do not run `wsl --shutdown` before harvest; confirm DNS resolves in the same WSL session
- [ ] For deferred targets: `harvest_deferred` + placeholder bundle; schedule re-harvest
- [ ] Verify structured JSON includes command, timestamp, scan metadata, and `exit_status` (text-only tools)
- [ ] Confirm structured counts match text (`scan_tries`, `empty_scans`, row counts)
- [ ] Confirm no `head`/`tail` truncation in manifest commands or captured text
- [ ] Verify `*_manifest.json` and outputs exist
- [ ] Graph via adapter + `core.graph_builder` / topology; `classify_ip` for addresses; `validate_graph()` passes
- [ ] Load nugget templates from `nuggets.json` + `nuggets_extension.json`; new types only in extension
- [ ] Draft `nugget_structure/<tool>_nugget_graph_structure.md`
- [ ] Narrative via shared engine → `*_proposed_nuggets_edges_description.md` (§4.3: meta-concepts, type Mermaid, appendix)
- [ ] CLI Profiling shows T / S / G / MD for **every** scenario — no graph = incomplete
- [ ] Set `*_review.status.json` to `pending`

## Operator gate

- [ ] Operator reviews text, data, graph proposal, narrative report in CLI Profiling
- [ ] Operator sets review status `approved` or `rejected` (all legacy bundles for a scenario key update together)
- [ ] On approval: record sign-off doc under `.docs/docs-for-cli-tools/<tool>_pilot_signoff.md`
- [ ] On approval: set `corpus_index.json` tool phase to `complete` when pilot criteria met
- [ ] On approval: update `nuggets_extension.json` / TypeQL as needed (not `nuggets.json` for new tool types)
- [ ] Byte-lock golden narratives only after visual sign-off (SPEC-004 R4-01-08 / SPEC-005 K1)

## Do not

- Brute-force every flag permutation
- Skip corporate-target scenarios
- Promote nugget types without evidence bundle
- Run Aircrack-ng until hardware available
- Treat empty export files as completed exploration batches
- Lock examinations that only capture info noise when the matrix row needs critical/CVE/org signal
- Ship a scenario without graph + narrative Markdown
- Use `graph_deferred` for any reason
