# Creating a Skill and Documentation for Metasploit Framework, Scanning Networks and Systems

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for the **Metasploit Framework (MSF)** when we are **scanning networks and systems**, generating payloads, or running **auxiliary discovery modules** whose results must be converted into SpiderFeet nugget graphs.

Metasploit is a **modular Ruby penetration-testing platform** centred on **MSFconsole**, with companion tools **`msfvenom`** (payload generation) and **`msfdb`** (PostgreSQL database and REST web service). For SpiderFeet integration, prioritise **legal, authorized** use of:

- **auxiliary/scanner/** and **auxiliary/gather/** modules for enumeration and fingerprinting,
- **exploit/multi/handler** for catching callbacks from generated payloads,
- **database-backed workspaces** for segmented host/service/vuln data,
- **resource scripts** and **`msfconsole -r`** for repeatable automation,
- structured module metadata (`info`, `show options`, `show advanced`, `show evasion`) before execution.

The skill must teach the agent how to adapt technique and module sequencing to maximise **actionable scan data** (hosts, services, vulnerabilities, credentials metadata) while understanding when MSF is the wrong tool versus dedicated scanners (Nmap, Nuclei, Nerva).

You will use this skill to exercise Metasploit in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

Collect and consolidate all high-signal source material from Rapid7 official docs, the GitHub wiki (mirrored at docs.metasploit.com), module documentation in-repo, API references, and strong practitioner guides. Prefer **docs.metasploit.com** and in-repo `documentation/modules/**` over third-party blogs when they conflict.

### Official repository, releases, and in-repo documentation

- [Metasploit Framework GitHub repository](https://github.com/rapid7/metasploit-framework)
- [Metasploit Framework releases](https://github.com/rapid7/metasploit-framework/releases)
- [Repository README](https://github.com/rapid7/metasploit-framework/blob/master/README.md)
- [documentation/README.md](https://github.com/rapid7/metasploit-framework/blob/master/documentation/README.md)
- [Developers guide (PDF)](https://github.com/rapid7/metasploit-framework/blob/master/documentation/developers_guide.pdf)
- [GitHub wiki home (redirects to docs.metasploit.com)](https://github.com/rapid7/metasploit-framework/wiki)
- [Module documentation tree](https://github.com/rapid7/metasploit-framework/tree/master/documentation/modules)
- [Example: auxiliary/scanner/http/brute_dirs module doc](https://github.com/rapid7/metasploit-framework/blob/master/documentation/modules/auxiliary/scanner/http/brute_dirs.md)

### Official Metasploit documentation (docs.metasploit.com)

- [Documentation home](https://docs.metasploit.com/)
- [API documentation (YARD)](https://docs.metasploit.com/api/)
- [Hosted API mirror](https://rapid7.github.io/metasploit-framework/api/)

#### Getting started

- [Nightly installers (Linux, macOS, Windows)](https://docs.metasploit.com/docs/using-metasploit/getting-started/nightly-installers.html)
- [Reporting a bug](https://docs.metasploit.com/docs/using-metasploit/getting-started/reporting-a-bug.html)

#### Using Metasploit — basics

- [How payloads work](https://docs.metasploit.com/docs/using-metasploit/basics/how-payloads-work.html)
- [How to use msfvenom](https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html)
- [How to use a Metasploit module appropriately](https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-a-metasploit-module-appropriately.html)
- [How to use a reverse shell in Metasploit](https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-a-reverse-shell-in-metasploit.html)

#### Using Metasploit — intermediate

- [Metasploit database support (msfdb)](https://docs.metasploit.com/docs/using-metasploit/intermediate/metasploit-database-support.html)
- [Evading antivirus](https://docs.metasploit.com/docs/using-metasploit/intermediate/evading-anti-virus.html)

#### Development and contribution

- [CONTRIBUTING.md (GitHub)](https://github.com/rapid7/metasploit-framework/blob/master/CONTRIBUTING.md)
- [Guidelines for accepting modules and enhancements](https://docs.metasploit.com/docs/development/maintainers/process/guidelines-for-accepting-modules-and-enhancements.html)

#### Module metadata and development guides

- [Module reliability, side effects, and stability definitions](https://docs.metasploit.com/docs/development/developing-modules/module-metadata/definition-of-module-reliability-side-effects-and-stability.html)
- [How to use datastore options](https://docs.metasploit.com/docs/development/developing-modules/module-metadata/how-to-use-datastore-options.html)
- [How to write a check method](https://docs.metasploit.com/docs/development/developing-modules/guides/how-to-write-a-check-method.html)
- [How to get started writing an auxiliary module](https://docs.metasploit.com/docs/development/developing-modules/guides/how-to-get-started-writing-an-auxiliary-module.html)
- [Setting up a Metasploit development environment](https://docs.metasploit.com/docs/development/get-started/setting-up-a-metasploit-development-environment.html)
- [Metasploit stats — framework repository activity](https://docs.metasploit.com/stats/metasploit_repos.html)

### Rapid7 product documentation

- [Metasploit Framework overview (Rapid7 docs)](https://docs.rapid7.com/metasploit/msf-overview/)
- [Managing workspaces](https://docs.rapid7.com/metasploit/managing-workspaces/)
- [Rapid7 module database (example entry)](https://www.rapid7.com/db/modules/auxiliary/scanner/http/dir_scanner/)

### Distribution and environment references

- [Kali Linux — metasploit-framework package context](https://www.kali.org/tools/metasploit-framework/)
- [ArchWiki — Metasploit Framework (msfdb, db_status)](https://wiki.archlinux.org/title/Metasploit_Framework)

### Practitioner guides, training, and blogs

- [Offensive Security — Metasploit Unleashed (free course index)](https://www.offsec.com/metasploit-unleashed/)
- [Metasploit Unleashed — MSFvenom](https://www.offsec.com/metasploit-unleashed/msfvenom/)
- [Metasploit Unleashed — Using the database](https://www.offsec.com/metasploit-unleashed/using-databases/)
- [Hedgehog Security — Metasploit deep dive](https://www.hedgehogsecurity.co.uk/blog/metasploit-deep-dive-exploitation-framework)
- [Jonathan's Blog — Metasploit tutorial for beginners (2026)](https://jonathansblog.co.uk/metasploit-tutorial-for-beginners)
- [Secure Debug — Mastering Metasploit guide](https://securedebug.com/mastering-metasploit-an-in-depth-guide-to-the-penetration-testing-framework/)

## Instructions

Based strictly on the provided source materials, generate the following artifacts:

1. **Skill trigger and description (max 50 words):** A highly specific description of what this skill does and exactly when the AI should trigger it. Include trigger words such as `msfconsole`, `msfvenom`, `use auxiliary/`, `search`, `set RHOSTS`, `exploit/multi/handler`, `db_nmap`, `workspace`, `resource script`, and payload staging.

2. **SKILL.md** (`.cursor\skills\metasploit_framework\SKILL.md`): Deconstruct workflows from source docs into clear, step-by-step instructions. Organize using these headers:

   - **Purpose:** When MSF adds value vs dedicated scanners; scope to authorized assessments.
   - **Step-by-Step Instructions:** Install → `msfdb init` → workspace → `search`/`use` → `info` → `show options` → `set` → `run`/`exploit` → `sessions` → `db_*` export.
   - **If/Then Decision Rules:** Module type selection (auxiliary vs exploit vs payload); staged vs single payloads; handler pairing; `check` vs `exploit`; database present vs absent.
   - **Guardrails & Pitfalls:** Read `info` and references before `exploit`; lab-only payloads; AV/EDR implications; destructive modules; legal authorization.
   - **MSFvenom workflows:** Generation, encoding, badchars, templates, format listing, handler pairing.
   - **Automation:** Resource scripts (`msfconsole -r`), `msfconsole -x` one-liners, workspace switching in scripts.
   - **SpiderFeet nugget mapping:** Map hosts, services, ports, vulnerabilities, and session metadata from DB exports and console output to nugget types and graph edges (per `.seed/04_Driving and Integrating_CLI_Apps.md`); note when TextFSM parsing of console text is required.
   - **References directory** indexed through `SKILLS.md`.

3. **References directory** (`.cursor\skills\metasploit_framework\references\`): Split into focused files (msfconsole commands, module types, datastore options, msfvenom, database/workspaces, sessions/meterpreter, auxiliary scanners, resource scripts, development/metadata). Index through `SKILLS.md`.

4. **Zero to Hero document** (`.docs\docs-for-cli-tools\Metasploit-Framework-Zero-to-Hero.md`): From install through a safe lab workflow: database setup → workspace → host discovery with an auxiliary scanner → service/version module → optional `msfvenom` + `multi/handler` lab callback → export DB results.

5. **CLI and console options documentation** (`.docs\docs-for-cli-tools\Metasploit-Framework-CLI-Options.md`): Document **`msfconsole`**, **`msfvenom`**, and **`msfdb`** flags plus essential console command families (`search`, `use`, `info`, `show`, `set`, `run`, `exploit`, `sessions`, `workspace`, `db_*`, `hosts`, `services`, `vulns`, `loot`, `creds`).

6. **Strategies and tactics:** Module search heuristics; pairing auxiliary scans with downstream tools; when to prefer `db_nmap` import vs native scanners; adapting after `check` failure or empty `hosts` workspace.

## Best Practices for Library Skills

When reviewing the AI output, ensure the final skill file follows these platform-standard rules:

- **Meaning and goals:** Explain module types, datastore, and payload staging — not only command syntax.
- **Workflows over features:** Teach assessment pipelines (discover → enumerate → validate → document), not a module catalogue dump.
- **Comprehensive documentation:** Cover `show advanced`, `show evasion`, `info -d`, and per-module `documentation/modules/**` patterns in `references/`.
- **Distinct trigger description:** Must be distinguishable from Recon-ng, Nmap, Nuclei, and Nerva skills.
- **Comprehensive examples:** Examples for auxiliary scanner setup, handler/listener setup, `msfvenom` generation, and workspace-scoped `db_export`.
- **Strategies and tactics:** Adapt module choice based on `search` results, `check` outcome, and workspace DB state.
- **SpiderFeet alignment:** Document how console output and database exports become text, structured data, and nugget graphs for the three output tabs in `.seed/04_Driving and Integrating_CLI_Apps.md`.
- **Safety default:** Treat exploitation modules as out-of-scope unless explicitly authorized; emphasise auxiliary/discovery paths for OSINT-style graph building.
