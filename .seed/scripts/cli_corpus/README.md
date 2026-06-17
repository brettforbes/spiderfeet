# CLI Corpus Harvest

Runs formal CLI examinations per `.seed/04_Driving and Integrating_CLI_Apps.md`.

## Quick start

```bash
# Probe + dry run
python .seed/scripts/cli_corpus/harvest.py --tool nmap --dry-run

# One scenario
python .seed/scripts/cli_corpus/harvest.py --tool nmap --scenario tcp_top_ports_permissive_xml

# All scenarios in manifest
python .seed/scripts/cli_corpus/harvest.py --tool nmap
```

## Layout

- `harvest.py` — runner (Windows / WSL)
- `manifests/<tool>.yaml` — scenario definitions
- Outputs → `.docs/docs-for-cli-tools/app_examination_docs/<tool>/`

## Agent skill

`.cursor/skills/cli_app_profiling/SKILL.md`

## Corpus index

`.docs/docs-for-cli-tools/corpus_index.json`
