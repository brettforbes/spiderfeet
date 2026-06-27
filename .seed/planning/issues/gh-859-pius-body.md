## Problem

Pius (priority 7) needs Go install on WSL, API key inventory synced from Subscriptions UI / SpiderFeet DB, exploration of passive NDJSON output, and formal examination.

## Mandatory skill

Read **before any work:** `.cursor/skills/pius/SKILL.md`

## Desired outcome

- `pius` binary on WSL (`go install`)
- `.tools/pius.env` (gitignored) synced from subscription keys where modules exist
- `.tools/pius.env.example` + `.docs/docs-for-cli-tools/pius_api_key_mapping.md`
- Manifest with passive no-key plugins, Shodan-key scenarios, corporate target
- Evidence NDJSON bundles

## API keys

Map from Subscriptions: `sfp_shodan` → `SHODAN_API_KEY`, etc. Document missing paid keys; run scenarios that work without them plus keyed plugin scenarios when keys exist.

## Spec binding

Parent #856 · #826

## Verification

`poetry run python .seed/scripts/cli_corpus/harvest.py --tool pius`
