## Problem

Nerva (priority 3) needs Windows binary install, semantic JSON-lines output exploration, formal examination, and nugget graph proposals.

## Mandatory skill

Read **before any work:** `.cursor/skills/nerva/SKILL.md`

## Desired outcome

- Binary in `.tools/bin/nerva.exe` or PATH
- Manifest `manifests/nerva.yaml`
- Evidence bundles with `--json` NDJSON
- Scenarios: single TCP target, multi-target file, `--fast`, UDP (`-U`), clean miss on closed port

## Targets

Permissive: `scanme.nmap.org:22,80` · Corporate filtered behaviour optional

## Spec binding

Parent #856 · #826

## Verification

`poetry run python .seed/scripts/cli_corpus/harvest.py --tool nerva`
