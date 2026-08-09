# nosey_parker Data Model

From upstream README and CLI help (v0.24.0).

## Datastore

A **datastore** is a directory Nosey Parker uses to record findings and internal state (SQLite). The `scan` command creates it if missing. Default path: `datastore.np` (override with `-d` / `NP_DATASTORE`).

Subcommands: `datastore init`, `datastore export`.

## Blob

Each scanned input unit is a **blob** with a unique **blob ID** (SHA-1 digest, Git-compatible).

## Provenance

Metadata describing how a blob was discovered — filesystem path, Git commit, repository URL, etc. A blob may have multiple provenance entries.

## Rule and ruleset

**Rules** are regex patterns with capture groups. **Rulesets** group rules. Built-in default ruleset targets secrets. List with `noseyparker rules list`.

## Match

A rule pattern hit at a byte range in a blob. Uniquely identified by rule + blob ID + start/end offsets.

## Finding

Matches sharing the same rule and capture-group value merge into one **finding** — Nosey Parker's primary reporting unit. Deduplication reduces review volume vs raw matches.

## Workflow objects

| Phase | Command | Output |
|-------|---------|--------|
| Discover | `scan` | Writes to datastore; prints summarize table |
| Overview | `summarize` | Per-rule counts (human/json/jsonl) |
| Detail | `report` | Findings with snippets, provenance, scores (human/json/jsonl/sarif) |

## Environment variables

| Variable | Purpose |
|----------|---------|
| `NP_DATASTORE` | Default datastore path |
| `NP_GITHUB_TOKEN` | GitHub API token for clone/enumerate rate limits and private repo access |
| `NO_COLOR` | Disables colour (same as `--color=never`) |
