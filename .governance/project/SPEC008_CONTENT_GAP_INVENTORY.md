# SPEC-008 content gap inventory

**Generated:** 2026-07-27 (V0)  
**Contract:** `.governance/project/SPEC008_CONTENT_CONTRACT.md`  
**8 adapter tools** from `corpus_index.json` formal-examination set.

Legend: **Have** = source exists and is copy-ready · **Missing** = not yet in bundle · **Needs regen** = source exists but bundle file must be generated from it

| tool_id | manifest.json | options.md | options_schema.json | zero_to_hero.md | graph_structure.md |
|---------|---------------|------------|---------------------|-----------------|-------------------|
| nmap | Missing | Have (`.docs/docs-for-cli-tools/NMAP-CLI-Options.md`) | Missing (Needs regen via V1) | Have (`NMAP-Zero-to-Hero.md`) | Have (`nugget_structure/nmap_nugget_graph_structure.md`) |
| netdiscover | Missing | Have (`NetDiscover-CLI-Options.md`) | Missing (Needs regen) | Have (`NetDiscover-Zero-to-Hero.md`) | Have (`netdiscover_nugget_graph_structure.md`) |
| nerva | Missing | Have (`Nerva-CLI-Options.md`) | Missing (Needs regen) | Have (`Nerva-Zero-to-Hero.md`) | Have (`nerva_nugget_graph_structure.md`) |
| pius | Missing | Have (`PIUS-CLI-Options.md`) | Missing (Needs regen) | Have (`PIUS-Zero-to-Hero.md`) | Have (`pius_nugget_graph_structure.md`) |
| subfinder | Missing | Have (`SubFinder-CLI-Options.md`) | Missing (Needs regen) | Have (`SubFinder-Zero-to-Hero.md`) | Have (`subfinder_nugget_graph_structure.md`) |
| httpx | Missing | Have (`Httpx-CLI-Options.md`) | Missing (Needs regen) | Have (`Httpx-Zero-to-Hero.md`) | Have (`httpx_nugget_graph_structure.md`) |
| katana | Missing | Have (`katana-CLI-Options.md`) | Missing (Needs regen) | Have (`katana-Zero-to-Hero.md`) | Have (`katana_nugget_graph_structure.md`) |
| nuclei | Missing | Have (`Nuclei-CLI-Options.md`) | Missing (Needs regen) | Have (`Nuclei-Zero-to-Hero.md`) | Have (`nuclei_nugget_graph_structure.md`) |

## Summary

- **options.md / zero_to_hero.md / graph_structure.md:** all 8 tools have source documents under `.docs/docs-for-cli-tools/` — V2 copies them into `modules_v2/content/<tool_id>/`.
- **manifest.json / options_schema.json:** missing for all 8 — V2 creates manifest; V1 generator produces `options_schema.json` (+ `options_schema.review.md` sidecar for human/agent reconciliation per contract §2).

## Next steps (execution order)

1. V1 — run `generate_options_schema.py --tool <id>` for each tool
2. V2 — backfill `modules_v2/content/<id>/` bundles; resolve all `review_log` entries
3. W1 — serve bundles via `/api/v1/content/*`
