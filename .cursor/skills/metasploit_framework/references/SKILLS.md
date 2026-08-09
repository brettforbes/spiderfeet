# Metasploit Framework References Index

| File | Contents |
|------|----------|
| [cli-options.md](cli-options.md) | Package CLI flags (msfconsole / msfvenom / msfdb) + companion bins |
| [msfconsole-commands.md](msfconsole-commands.md) | Interactive console command families |
| [module-types-and-datastore.md](module-types-and-datastore.md) | Module classes, datastore, check vs exploit |
| [msfvenom-workflows.md](msfvenom-workflows.md) | Payload generation and handler pairing |
| [msfdb-workspaces-and-db-exports.md](msfdb-workspaces-and-db-exports.md) | Database lifecycle, workspaces, exports |
| [auxiliary-scanner-workflows.md](auxiliary-scanner-workflows.md) | Auxiliary-first discovery pipelines |
| [resource-scripts-and-automation.md](resource-scripts-and-automation.md) | `-r`, `-x`, and repeatable scripts |
| [sessions-and-handler-patterns.md](sessions-and-handler-patterns.md) | Session lifecycle and `multi/handler` |
| [development-metadata-and-stability.md](development-metadata-and-stability.md) | Metadata reliability and module safety |
| [nugget-mapping.md](nugget-mapping.md) | DB/console evidence → SpiderFeet graph |
| [tactics.md](tactics.md) | Search heuristics, empty workspace, tool handoffs |
| [sources.md](sources.md) | Canonical source URLs |

**Read order for new agents**

1. `../SKILL.md` — purpose, decision rules, Windows package caveats.
2. `cli-options.md` + operator `Metasploit-Framework-CLI-Options.md` — authoritative flags for **6.5.2-20260809060523-1rapid7**.
3. `auxiliary-scanner-workflows.md` + `msfconsole-commands.md` — discovery loop.
4. `msfdb-workspaces-and-db-exports.md` — persistence and export.
5. `nugget-mapping.md` — SpiderFeet graph emission.
6. `tactics.md` — adapt when search is thin, workspace empty, or GemNotFound blocks runtime.
7. `msfvenom-workflows.md` + `sessions-and-handler-patterns.md` — lab-only payload path.

**Operator docs (repo)**

| File | Contents |
|------|----------|
| `.docs/docs-for-cli-tools/Metasploit-Framework-Zero-to-Hero.md` | Install → DB → aux scan → optional handler → export |
| `.docs/docs-for-cli-tools/Metasploit-Framework-CLI-Options.md` | Combined CLI capture (failure + reconstructed OptionParser) |

**Related skills:** [`../../nmap/SKILL.md`](../../nmap/SKILL.md), [`../../naabu/SKILL.md`](../../naabu/SKILL.md), [`../../nuclei/SKILL.md`](../../nuclei/SKILL.md), [`../../nerva/SKILL.md`](../../nerva/SKILL.md), [`../../httpx/SKILL.md`](../../httpx/SKILL.md)

**Ontology:** `.docs/docs-for-cli-tools/_Current_Ontology.md` — MSF discovery typically extends HOST / APPLICATIONS / VULNERABILITY layers.
