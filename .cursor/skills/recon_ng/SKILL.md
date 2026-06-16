---
name: recon_ng
description: Trigger for recon-ng, marketplace install, modules load, workspaces create, options set SOURCE, recon-cli, resource scripts, and OSINT module chaining when modular web OSINT pipelines must persist data in workspaces and feed SpiderFeet text/data/graph nugget outputs with controlled API spend.
---

# Recon-ng Skill

## Purpose

Use this skill when the task needs a modular, database-backed OSINT workflow rather than a one-shot command.

Choose Recon-ng when you need:
- Workspace isolation per engagement.
- Module chaining where one module's output table seeds the next module.
- Marketplace-driven capability expansion.
- Repeatable headless automation with `recon-cli` or resource scripts.
- Structured extraction for SpiderFeet nugget graph mapping.

Prefer standalone tools (for example dnsx or theHarvester) when:
- You only need one narrow data collection step.
- No persistent workspace/database history is required.
- You do not need module-to-module table chaining.

## Step-by-Step Instructions

1. **Bootstrap framework**
   - Install from official package/repo paths.
   - Launch `recon-ng` once to initialize home paths and default workspace assets.
   - Verify core commands (`help`, `workspaces`, `marketplace`, `modules`) are available.

2. **Create or select workspace**
   - Use `workspaces create <name>` for a new engagement.
   - Use `workspaces select <name>` before loading modules.
   - Keep one workspace per client/target scope to avoid data contamination.

3. **Set API keys and global context**
   - Use `keys list` to inspect required providers.
   - Use `keys add <provider> <value>` for required module dependencies.
   - Tune global options (verbosity/user-agent/proxy/threading as available in your install) before expensive module runs.

4. **Prepare marketplace and modules**
   - Refresh/search marketplace index.
   - Install needed modules by category path.
   - Load modules by canonical path such as:
     - `recon/domains-hosts/*`
     - `recon/hosts-ports/*`
     - `recon/domains-contacts/*`
     - `reporting/*`

5. **Configure module options and SOURCE**
   - Run `show info` and `show options` after each `modules load`.
   - Set module options explicitly.
   - Set `SOURCE` based on seed strategy:
     - Single seed value for focused runs.
     - File-backed source for larger target sets.
     - SQL source to pull directly from prior workspace tables.

6. **Execute and validate table growth**
   - Run module.
   - Inspect `show` output and `db query` table counts after each step.
   - Confirm expected table growth before chaining onward.

7. **Chain next module from produced tables**
   - Move from domain to hosts, then hosts to ports or other enrichment modules.
   - Use `SOURCE` set to prior outputs (direct value, file, or SQL).
   - Stop redundant modules when no new rows are being produced.

8. **Query/export for SpiderFeet integration**
   - Use `db query` for structured extraction.
   - Use `reporting/*` modules for export artifacts.
   - Convert rows into SpiderFeet nuggets and graph edges.

## If/Then Decision Rules

- **If module has dependency marker (D), then** verify dependency availability before execution.
- **If module requires API key (K), then** configure key first and test with minimal seed scope.
- **If API spend/rate risk is high, then** run cheap passive modules first and gate expensive modules on new-row yield.
- **If `SOURCE` is large, then** batch inputs and checkpoint row counts between runs.
- **If module output tables are empty, then** pivot to adjacent category modules rather than rerunning unchanged inputs.
- **If module appears stale/disabled/removed in marketplace, then** use maintained alternatives in same input-output path.
- **If stealth is required, then** reduce request intensity, adjust timing/proxy/user-agent settings, and prioritize passive collection.
- **If workspace data looks mixed, then** stop and switch to the correct workspace before continuing.

## Guardrails & Pitfalls

- Authorized targets only. Do not run outside approved scope.
- Do not treat marketplace modules as uniformly maintained; validate metadata and behavior each run.
- Do not mix unrelated clients/engagements in one workspace.
- Do not burn API quota on broad seeds before confirming module utility on small samples.
- Do not assume module success means useful output; verify table delta and row quality.
- Do not proceed from empty prerequisite tables; adjust sequence or source first.

## Automation

Use these modes for repeatability:

- **Resource scripts:** `recon-ng -r <script.rc>`
  - Best for deterministic replay of console commands.
- **Headless CLI:** `recon-cli`
  - Best for non-interactive orchestration in larger pipelines.
- **Script recording/execution:** `script record` / `script execute`
  - Best for capturing a proven interactive workflow and replaying it.
- **Output capture:** `spool`
  - Capture command output for audit trails and parser ingestion.

Automation pattern:
1. Create/select workspace.
2. Add keys.
3. Install/refresh needed modules.
4. Run seed modules.
5. Gate next modules on `db query` delta checks.
6. Export reporting artifacts and table extracts.

## SpiderFeet nugget mapping

Map Recon-ng database/reporting output into SpiderFeet structures aligned with `.seed/04_Driving and Integrating_CLI_Apps.md`.

- `domains` -> `INTERNET_NAME`
- `hosts` -> `IP_ADDRESS` or host-typed nugget as implemented
- `contacts` -> `HUMAN_NAME`, `EMAILADDR`, `PHONE_NUMBER` where available
- `ports` -> `TCP_PORT_OPEN` / `UDP_PORT_OPEN` as applicable
- `vulnerabilities` -> `VULNERABILITY_GENERAL` and CVE-linked types when present
- Reporting artifacts -> text/data tabs; structured rows -> graph tab nodes/edges

Edge guidance:
- Use `contains` for ownership/container relationships (domain contains host, host contains port).
- Use `has` for attribute-style links (contact has email/phone, entity has vulnerability marker).

Pipeline goal:
- Preserve raw evidence for text output.
- Preserve normalized rows for data output.
- Emit nodes/edges for graph output with stable IDs and deduplication.

## Strategies and Tactics

### Module selection by path

- Start with `recon/<input>-<output>/` path that matches current known table.
- Prefer modules whose input table already has non-zero rows.
- Keep a small rotation of alternative modules per path to mitigate staleness.

### SOURCE strategy

- Use default/literal `SOURCE` for quick validation.
- Use file-backed `SOURCE` for curated bulk seed sets.
- Use SQL-backed `SOURCE` for adaptive chaining from workspace truth.

### API spend control

- Run low-cost passive modules first.
- Promote to paid/rate-limited modules only when prior stages yield new high-value seeds.
- Track per-module row delta; stop modules with repeated zero-growth runs.
- Reuse persisted workspace data instead of re-querying providers.

## References

See indexed references in:
- `.cursor/skills/recon_ng/references/SKILLS.md`
- `.cursor/skills/recon_ng/references/sources.md`
