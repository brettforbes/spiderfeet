# Naabu References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | All flags grouped by INPUT, PORT, OUTPUT, SCAN, HOST-DISCOVERY, etc. |
| [json-output-schema.md](json-output-schema.md) | `-json` JSON Lines record shape and extended fields |
| [workflows-and-phases.md](workflows-and-phases.md) | Discovery → port scan → verify → enrich pipelines |
| [tactics.md](tactics.md) | Rate tuning, CDN exclusion, passive mode, hostile networks |
| [nugget-mapping.md](nugget-mapping.md) | JSONL → SpiderFeet `TCP_PORT_OPEN`, `UDP_PORT_OPEN`, host nodes |
| [nmap-integration.md](nmap-integration.md) | `-nmap-cli`, `-sV`, UDP probes, service discovery |
| [sources.md](sources.md) | ProjectDiscovery docs, GitHub README, articles |

**Read order for new agents**

1. `workflows-and-phases.md` — SYN vs CONNECT, when to use passive/host discovery.
2. `cli-options.md` — flags for targets, ports, output.
3. `json-output-schema.md` — always `-json` for automation.
4. `nugget-mapping.md` — emit port nuggets for downstream Nerva/Julius/httpx.
5. `tactics.md` — adapt when filtered, CDN, or rate-limited.
6. `nmap-integration.md` — when to chain Nmap vs built-in `-sV`.

**Operator docs (repo root)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Naabu-Zero-to-Hero.md` | Install → scan → JSON → nuggets → pipelines |
| `.docs/docs-for-cli-tools/Naabu-CLI-Options.md` | Full CLI reference |

**Downstream skills:** [`../../nerva/SKILL.md`](../../nerva/SKILL.md), [`../../nmap/SKILL.md`](../../nmap/SKILL.md), [`../../julius/SKILL.md`](../../julius/SKILL.md), [`../../dnsx/SKILL.md`](../../dnsx/SKILL.md)
