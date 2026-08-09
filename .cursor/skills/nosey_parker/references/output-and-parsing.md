# nosey_parker Output and Parsing

## Structured-first law (SpiderFeet)

For CLI profiling and graph derivation, use **`noseyparker report -f jsonl`** or **`-f json`**. Do **not** parse human `summarize` tables or coloured `report -f human` text as the primary artifact.

| Command | Structured? | SpiderFeet role |
|---------|-------------|-----------------|
| `scan` | No (writes datastore) | Capture command + stderr/summary in text pane; graph from report export |
| `summarize -f json/jsonl` | Yes | Scan-level aggregates only — not per-finding detail |
| `report -f json/jsonl/sarif` | Yes | **Primary** structured source for nugget mapping |
| `report -f human` | No | Operator review / Text pane derivative |

## Report formats

| `-f` value | Description |
|------------|-------------|
| `human` | Terminal-friendly detail (default) |
| `json` | Pretty-printed JSON document |
| `jsonl` | One JSON object per line — preferred for streaming pipelines |
| `sarif` | SARIF (experimental) |

JSON schema: release `share/noseyparker/report-schema.json`, or `noseyparker generate json-schema`.

## Report filtering (noise control)

| Flag | Default | Effect |
|------|---------|--------|
| `--min-score` | `0.05` | Mean score threshold [0,1]; `0` disables |
| `--finding-status` | (none) | Filter: `accept`, `reject`, `mixed`, `null` |
| `--max-matches` | `3` | Cap matches shown per finding |
| `--max-provenance` | `3` | Cap provenance entries per match |
| `--suppress-redundant` | `true` | Collapse overlapping matches in same blob |

## Normalized record shape (for adapters)

Redact secret values before persistence outside the engagement vault:

```json
{
  "finding_id": "np-finding-uuid",
  "rule_name": "AWS Access Key ID",
  "rule_id": "aws-access-key-id",
  "status": "null",
  "mean_score": 0.87,
  "matches_count": 4,
  "provenance": [
    {
      "kind": "git_commit",
      "repo": "https://github.com/example/app.git",
      "commit": "abc123",
      "path": "config/settings.yml"
    }
  ],
  "snippet_redacted": "[REDACTED]",
  "classification": "high_confidence_secret"
}
```

Field names in live JSONL follow the release schema — map via `report-schema.json`, do not hard-code stale keys.

## Parsing workflow

1. Run `scan` with captured command line and timestamp.
2. Export: `noseyparker report -d <ds> -f jsonl -o findings.jsonl` (or `-f json`).
3. Parse JSONL line by line (or load the JSON document); skip blank lines.
4. For harvest bundles, fold into a single JSON root with `schema`, `records[]`, and scan metadata (proj-06 JSONL bundle pattern) so Data Viewer gets one parseable root.
5. Redact capture-group values and snippets in any exported narrative.
6. De-duplicate by `(rule_id, normalized_secret_fingerprint)` before graph promotion.
7. Assign confidence from `mean_score`, annotation status, and manual validation.

## Empty / clean miss

Valid scenario: scan completes, `summarize` shows zero findings, `report -f jsonl` emits no records (or empty array for `json`). Still produce a scan-head graph with an empty finding tree.

## Errors

Capture non-zero exit status and stderr in structured metadata. Auth failures on GitHub typically surface during `scan` clone/enumerate, not in report output.
