# CLI Profiling batch — netdiscover, nerva, pius

**Epic:** GitHub #853 · **Tasks:** #854 netdiscover, #855 nerva, #856 pius

Formal examination completed 2026-06-27. Each agent run **must read the tool skill** before exploration:

| Tool | Skill |
|------|-------|
| netdiscover | `.cursor/skills/netdiscover/SKILL.md` |
| nerva | `.cursor/skills/nerva/SKILL.md` |
| pius | `.cursor/skills/pius/SKILL.md` |

## Deliverables

- Manifests: `.seed/scripts/cli_corpus/manifests/{netdiscover,nerva,pius}.yaml`
- Evidence: `.docs/docs-for-cli-tools/app_examination_docs/{tool}/`
- Graph structure: `.docs/docs-for-cli-tools/nugget_structure/{tool}_nugget_graph_structure.md`
- PIUS keys: `sync_pius_env.py` + `pius_api_key_mapping.md`

## Verification

```bash
poetry run python .seed/scripts/cli_corpus/harvest.py --tool netdiscover
poetry run python .seed/scripts/cli_corpus/harvest.py --tool nerva
poetry run python .seed/scripts/cli_corpus/harvest.py --tool pius
poetry run python -m pytest .tests/test_cli_tool_to_graph.py .tests/api/test_cli_corpus.py -q
```
