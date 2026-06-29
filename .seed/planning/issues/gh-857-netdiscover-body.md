## Problem

Netdiscover (priority 2) needs WSL-root installation verification, semantic output exploration, formal examination scenarios, and nugget graph proposals per the Nmap pilot.

## Mandatory skill

Read **before any work:** `.cursor/skills/netdiscover/SKILL.md`

## Desired outcome

- CLI help captured
- Manifest `.seed/scripts/cli_corpus/manifests/netdiscover.yaml`
- Evidence bundles under `app_examination_docs/netdiscover/`
- `nugget_structure/netdiscover_nugget_graph_structure.md` + scenario graph JSON
- TextFSM template for `-P` parseable output

## Scenarios (minimum)

- Active `-P -N -r` on local L2 CIDR (`192.168.1.0/24` or WSL-attached subnet)
- Fast mode `-f`
- Passive `-p` (bounded timeout / partial capture noted)
- Clean miss / sparse subnet if applicable

## Spec binding

Parent #856 · #826 · `.seed/04_Driving and Integrating_CLI_Apps.md`

## Verification

`poetry run python .seed/scripts/cli_corpus/harvest.py --tool netdiscover`
