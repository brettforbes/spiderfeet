# Automation and Scripting

## Automation modes

Recon-ng supports both interactive and headless automation styles for repeatable OSINT chains.

### `recon-ng -r <script.rc>`

Resource script execution for deterministic command playback.

Use when:
- workflow is stable and ordered,
- you want easy versioning of command sequences,
- same pipeline runs across multiple engagements with minor variable changes.

### `recon-cli`

Headless/non-interactive execution interface.

Use when:
- integrating into larger orchestration systems,
- running scheduled jobs,
- embedding Recon-ng in SpiderFeet external-tool pipelines.

### Script recording and replay

- `script record` captures interactive command sessions.
- `script execute` replays known-good sequences.

Use when converting exploratory manual sessions into repeatable runbooks.

### Spooling

`spool` captures output streams for:
- audit/evidence retention,
- troubleshooting,
- parser ingestion into text/data output tabs.

## Recommended automation template

1. Select/create workspace.
2. Configure keys and global options.
3. Refresh/install/load required modules.
4. Set module options + SOURCE.
5. Execute module.
6. Run `db query` checks for row deltas.
7. Branch to next module path based on results.
8. Export reporting artifacts.

## Adaptive automation logic

Automation should not be purely linear. Add decision gates:
- If prerequisite table empty -> skip dependent module.
- If row delta below threshold -> pivot to alternate module family.
- If API quota warning/failure -> pause expensive modules and continue passive collection.

## Error handling and diagnostics

- Increase verbosity when diagnosing module failures.
- Route framework bugs vs marketplace module bugs to correct issue tracker.
- Keep captured logs with workspace IDs for reproducibility.
