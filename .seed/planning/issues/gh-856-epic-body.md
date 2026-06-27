## Problem

Three priority CLI tools (priorities 2–4 and 7 in corpus_index) need formal exploration, semantic output mapping, and examination evidence bundles following the Nmap pilot pattern (#850).

## Desired outcome

Each tool: installed (WSL where required), explored, manifest + harvest scenarios run, nugget graph structure drafted, operator review pending.

## Spec binding

- `.seed/04_Driving and Integrating_CLI_Apps.md`
- Parent: #826
- **Mandatory skill read before each tool:**
  - `.cursor/skills/netdiscover/SKILL.md`
  - `.cursor/skills/nerva/SKILL.md`
  - `.cursor/skills/pius/SKILL.md`

## Child tasks

- #857 netdiscover (WSL-root)
- #858 nerva (windows)
- #859 pius (WSL + API keys / Subscriptions UI)

## Verification

`harvest.py` bundles under `app_examination_docs/{netdiscover,nerva,pius}/`; graph structure markdown per tool.
