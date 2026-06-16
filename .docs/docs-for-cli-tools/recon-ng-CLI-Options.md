# Recon-ng CLI and Console Options

This document covers launcher flags and interactive command families for both framework operation and repeatable OSINT module chaining.

## 1) Launcher binaries and help surfaces

## `recon-ng -h`

Primary interactive framework launcher. Use for:
- direct console-driven operations,
- running resource scripts with `-r`,
- maintaining workspaces and module workflows.

## `recon-cli -h`

Headless command interface. Use for:
- non-interactive automation,
- CI/pipeline integration,
- batch execution where no TTY interaction is required.

## Common launcher usage patterns

- Interactive startup: `recon-ng`
- Scripted run: `recon-ng -r <script.rc>`
- Headless operation entrypoint: `recon-cli ...`

## 2) Console command families

## `workspaces`

Purpose:
- Create, select, list, and manage isolated engagement contexts.

Example flow:
1. create workspace
2. select workspace
3. run modules scoped to that workspace only

## `marketplace`

Purpose:
- Discover/install/remove/update module packages.

Example flow:
1. refresh index
2. search by category or keyword
3. install module
4. inspect info/update as needed

## `modules`

Purpose:
- Load modules by path (`recon/<input>-<output>/...` and `reporting/*`).

Example flow:
1. load module
2. inspect info/options
3. set SOURCE and module options
4. run

## `options`

Purpose:
- Set module-specific and global options.

Key option:
- `SOURCE` controls seed model:
  - literal/default value
  - file-backed list
  - SQL-derived in-workspace seed set

## `keys`

Purpose:
- Manage provider API credentials for key-dependent modules.

Typical operations:
- list configured keys
- add/update keys
- validate before key-required module execution

## `db`

Purpose:
- Query workspace SQLite data to validate pipeline output and drive adaptive sequencing.

Usage patterns:
- row count checks between module runs
- dedup/filter checks for API spend control
- selecting SQL SOURCE subsets

## `show`

Purpose:
- Inspect module metadata, options, and table visibility before/after runs.

Minimum expected usage:
- `show info`
- `show options`
- table/state inspections relevant to chaining decisions

## `dashboard`

Purpose:
- High-level workspace status and activity visibility.

Use as quick orientation before deep `db query` validation.

## `snapshots`

Purpose:
- Manage point-in-time workspace state capture for rollback/comparison workflows.

Use around high-impact module sequences or before destructive cleanup.

## `spool`

Purpose:
- Capture console output to file for evidence, auditing, and parser ingestion.

Recommended:
- enable spool per major run and name output with workspace/timestamp.

## `script`

Purpose:
- Record and replay command sequences.

Sub-workflow:
- `script record` during a validated manual run
- `script execute` to replay deterministic sequence

## Global options

Purpose:
- Set framework-wide execution posture (verbosity/debugging/network/runtime behavior as available in install).

Use cases:
- stealth-sensitive runs,
- troubleshooting failures,
- output verbosity tuning for automation logs.

## 3) Module category worked examples

## `recon/domains-hosts/*`

Goal:
- Convert domain seeds into discovered host assets.

Source strategy:
- start literal/file, then pivot to SQL if chaining from prior domain rows.

## `recon/hosts-ports/*`

Goal:
- Enrich host rows with observed service/port data.

Source strategy:
- SQL-filter hosts to new/priority targets to reduce redundant scans/calls.

## `recon/domains-contacts/*`

Goal:
- Expand domain scope into people/contact artifacts.

Source strategy:
- domain literal or SQL subset for business-unit segmentation.

## `reporting/*`

Goal:
- Export workspace data for operator review and downstream systems.

Output strategy:
- keep both narrative and structured artifacts for SpiderFeet text/data/graph tabs.

## 4) Tactical usage rules

- Choose modules by current table state, not by static favorite list.
- Treat empty prerequisite tables as sequencing blockers, not module failures.
- Run low-cost/passive modules before quota-heavy API modules.
- Stop repeated zero-delta modules to control spend and noise.
- Reuse workspace data through SQL SOURCE rather than re-querying identical inputs.
