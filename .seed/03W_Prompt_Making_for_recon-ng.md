# Creating a Skill and Documentation for Recon-ng, Scanning Networks and Systems

I want you to help me author an AI Agent Skill for my library.

## Goal

Create a SKILL.md file and a precise trigger description for **Recon-ng** when we are conducting **web-based OSINT reconnaissance** and need to chain modular gathering workflows into SpiderFeet nugget graphs.

Recon-ng is **not** a single-purpose CLI like `nmap` or `dnsx`. It is an **interactive Python framework** (Metasploit-style console) with **workspaces**, a **SQLite database**, a **module marketplace**, and optional headless automation via **`recon-cli`** and **resource files** (`recon-ng -r script.rc`). The skill must teach the agent how to:

- install and bootstrap the framework and marketplace modules,
- isolate engagements with workspaces and API keys,
- select modules by **input/output table path** (e.g. `recon/domains-hosts/*`, `recon/hosts-ports/*`),
- chain modules so database rows become seeds for the next module,
- export or query structured results for **nugget graph** construction,
- automate repeatable recon sequences for SpiderFeet module execution.

More importantly, the skill should teach **how to adapt technique and module sequencing** to maximise harvested OSINT data while respecting rate limits, API key requirements, module dependencies, and stealth options.

You will use this skill to exercise Recon-ng in different scenarios, and over time you will update it with your learnings and insights.

## Source Material

Collect and consolidate all high-signal source material from official docs, code, marketplace modules, releases, training, and strong practitioner references. Recon-ng's wiki and marketplace are canonical; blogs and cheat sheets help with workflow patterns but must not override official behaviour.

### Official repository and releases

- [Recon-ng GitHub repository](https://github.com/lanmaster53/recon-ng)
- [Recon-ng releases](https://github.com/lanmaster53/recon-ng/releases)
- [Recon-ng issues (framework)](https://github.com/lanmaster53/recon-ng/issues)
- [Official module marketplace repository](https://github.com/lanmaster53/recon-ng-marketplace)
- [Marketplace issues (modules)](https://github.com/lanmaster53/recon-ng-marketplace/issues)

### Official wiki (read in this order)

- [Wiki home](https://github.com/lanmaster53/recon-ng/wiki)
- [Getting Started](https://github.com/lanmaster53/recon-ng/wiki/Getting-Started) — installation, Docker, v4→v5 migration, key migration, dependencies
- [Features](https://github.com/lanmaster53/recon-ng/wiki/Features) — workspaces, marketplace, module search, SOURCE option, automation, recon-web, global options
- [Troubleshooting](https://github.com/lanmaster53/recon-ng/wiki/Troubleshooting) — VERBOSITY, pdb, issue routing
- [Development Guide](https://github.com/lanmaster53/recon-ng/wiki/Development-Guide) — module meta, Framework API, mixins, marketplace indexing
- [Videos](https://github.com/lanmaster53/recon-ng/wiki/Videos) — Pluralsight training and Intro to Recon-ng v5 screencast

### Distribution, man pages, and packaging

- [Kali Linux — recon-ng tool page](https://www.kali.org/tools/recon-ng/)
- [Ubuntu manpage — recon-ng(1)](https://manpages.ubuntu.com/manpages/jammy/man1/recon-ng.1.html)
- [Linux Command Library — recon-ng man summary](https://linuxcommandlibrary.com/man/recon-ng)

### Practitioner guides, cheat sheets, and workflow write-ups

- [Black Hills InfoSec — What's Changed in Recon-ng 5.x](https://www.blackhillsinfosec.com/whats-changed-in-recon-ng-5x/)
- [Black Hills InfoSec — Recon-ng 5.x cheat sheet (PDF)](https://www.blackhillsinfosec.com/wp-content/uploads/2019/11/recon-ng-5.x-cheat-sheet-Sheet1-1.pdf)
- [HackerTarget — Recon-ng tutorial (marketplace and modules)](https://hackertarget.com/recon-ng-tutorial/)
- [Striker Security — Getting started Recon-ng tutorial](https://strikersecurity.com/blog/getting-started-recon-ng-tutorial/)
- [NativeNode — command list and domain OSINT workflow](https://nativenode.io/an-overview-of-recon-ng-command-list-domain-osint-workflow/)
- [1337skills — Recon-ng cheat sheet](https://1337skills.com/cheatsheets/recon-ng/)
- [Vespersec — Recon-ng modules cheat sheet](https://vespersec.net/docs/osint-reconnaissance/recon-ng-modules-cheat-sheet/)
- [RingSafe — Install, use, optimise](https://ringsafe.in/recon-ng/)
- [OSINTBench — Recon-ng review](https://osintbench.com/tools/recon-ng)
- [DEV Community — Recon-ng tutorial 2026 (workspaces and marketplace)](https://dev.to/lucky_lonerusher/recon-ng-tutorial-2026-modular-osint-framework-for-professional-reconnaissance-tools-day21-4bbf)

### Conference, webcast, and historical context

- [Black Hills InfoSec webcast — Pentester TTPs (Recon-ng section)](https://www.blackhillsinfosec.com/webcast-pentester-tactics-techniques-and-procedures-ttps-w-chris-traynor/)
- [DerbyCon 2013 — Look Ma, No Exploits! (wiki news link)](https://github.com/lanmaster53/recon-ng/wiki/Home#news)

## Instructions

Based strictly on the provided source materials, generate the following artifacts:

1. **Skill trigger and description (max 50 words):** A highly specific description of what this skill does and exactly when the AI should trigger it. Include trigger words such as `recon-ng`, `marketplace install`, `modules load`, `workspaces create`, `options set SOURCE`, `recon-cli`, resource scripts, and OSINT module chaining.

2. **SKILL.md** (`.cursor\skills\recon_ng\SKILL.md`): Deconstruct workflows from source docs into clear, step-by-step instructions. Organize using these headers:

   - **Purpose:** When to use Recon-ng vs standalone CLI tools (dnsx, theHarvester, etc.).
   - **Step-by-Step Instructions:** Bootstrap → workspace → keys → marketplace → load → configure SOURCE → run → query/export.
   - **If/Then Decision Rules:** Dependencies (D), API keys (K), stealth, module staleness, empty tables, rate limits.
   - **Guardrails & Pitfalls:** Authorized targets only; marketplace module risks; conflating workspaces; abandoned modules.
   - **Automation:** `recon-ng -r`, `recon-cli`, `script record` / `script execute`, spooling.
   - **SpiderFeet nugget mapping:** Map `domains`, `hosts`, `contacts`, `ports`, `vulnerabilities`, and reporting exports to nugget types and `contains` / `has` edges (per `.seed/04_Driving and Integrating_CLI_Apps.md`).
   - **References directory** indexed through `SKILLS.md`.

3. **References directory** (`.cursor\skills\recon_ng\references\`): Split source material into focused reference files (workspaces, marketplace, module I/O paths, database schema, keys, global options, automation, reporting/recon-web, development API). Index through `SKILLS.md`.

4. **Zero to Hero document** (`.docs\docs-for-cli-tools\recon-ng-Zero-to-Hero.md`): From first install through a full domain recon pipeline (workspace → subdomain enum → host resolution → port/OSINT modules → export), including API key setup and module chaining.

5. **CLI and console options documentation** (`.docs\docs-for-cli-tools\recon-ng-CLI-Options.md`): Document **both** launcher flags (`recon-ng -h`, `recon-cli -h`) **and** framework console command families (`workspaces`, `marketplace`, `modules`, `options`, `keys`, `db`, `show`, `dashboard`, `snapshots`, `spool`, `script`, global options).

6. **Strategies and tactics:** Module-selection heuristics by `recon/<input>-<output>/` path; when to use `SOURCE` default vs file vs SQL; sequencing to maximise graph breadth without redundant API spend.

## Best Practices for Library Skills

When reviewing the AI output, ensure the final skill file follows these platform-standard rules:

- **Meaning and goals:** Explain *why* workspaces, SOURCE, and module paths exist — not only what commands do.
- **Workflows over features:** Teach end-to-end OSINT pipelines (domain → hosts → ports → contacts → report), not a flat command list.
- **Comprehensive documentation:** Cover marketplace install/remove/refresh/info, disabled modules, and recon-web/reporting export paths in `references/`.
- **Distinct trigger description:** Must be distinguishable from Metasploit, dnsx, uncover, and theHarvester skills.
- **Comprehensive examples:** At least one worked example per major command family and per common module category (`domains-hosts`, `hosts-ports`, `domains-contacts`, `reporting/*`).
- **Strategies and tactics:** Adapt module chains based on prior `db query` / `show` results and empty-table signals.
- **SpiderFeet alignment:** Document how SQLite rows and reporting output become structured data and nugget graphs for the three output tabs (text, data, graph) described in `.seed/04_Driving and Integrating_CLI_Apps.md`.
