# Naabu References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | All flags grouped by INPUT, PORT, OUTPUT, CONFIGURATION, HOST-DISCOVERY, etc. |
| [json-output-schema.md](json-output-schema.md) | `-json` JSON Lines record shapes from live v2.6.1 |
| [workflows-and-phases.md](workflows-and-phases.md) | Discovery → port scan → verify → enrich pipelines |
| [tactics.md](tactics.md) | Rate tuning, CDN exclusion, passive mode, Windows CONNECT |
| [nugget-mapping.md](nugget-mapping.md) | JSONL → SpiderFeet ports/hosts + `nodes[]`/`edges[]` |
| [nmap-integration.md](nmap-integration.md) | `-nmap-cli`, `-sV`, `-sD` (flags present in live help only) |
| [sources.md](sources.md) | ProjectDiscovery docs, GitHub, articles |

**Read order for new agents**

1. `workflows-and-phases.md` — SYN vs CONNECT, when to use passive/host discovery.
2. `cli-options.md` — flags for targets, ports, output (live help only).
3. `json-output-schema.md` — always `-json` for automation.
4. `nugget-mapping.md` — emit port nuggets for downstream Nerva/Julius/httpx.
5. `tactics.md` — adapt when filtered, CDN, Windows, or rate-limited.
6. `nmap-integration.md` — when to chain Nmap vs built-in `-sV`/`-sD`.

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Naabu-Zero-to-Hero.md` | Install → scan → JSONL → nuggets → pipelines |
| `.docs/docs-for-cli-tools/Naabu-CLI-Options.md` | Full CLI reference + captured help |

**Help captures:** `.tmp_naabu_help/` — **2026-08-10**, binary `C:\projects\spiderfeet\.tools\naabu\naabu.exe` **v2.6.1**.

**Upstream skills:** [`../../dnsx/SKILL.md`](../../dnsx/SKILL.md), [`../../subfinder/SKILL.md`](../../subfinder/SKILL.md)

**Downstream skills:** [`../../httpx/SKILL.md`](../../httpx/SKILL.md), [`../../nerva/SKILL.md`](../../nerva/SKILL.md), [`../../nmap/SKILL.md`](../../nmap/SKILL.md), [`../../julius/SKILL.md`](../../julius/SKILL.md)

**Ontology:** `.docs/docs-for-cli-tools/_Current_Ontology.md` — naabu feeds NETWORKS / APPLICATIONS (open ports) before service fingerprinting.
