# Titus Output and Parsing

## Structured-first (SpiderFeet)

Titus can emit **`json`**, **`sarif`**, or **`human`** (`scan` / `report`). For corpus, automation, and nugget graphs:

1. Prefer **`--format json`**.
2. Persist an engagement datastore (`--output` on scan; `--datastore` on report).
3. Derive human-readable review text from JSON — do not harvest human-only console as the structured artifact.

SARIF is appropriate for CI (e.g. GitHub Advanced Security), not as the primary SpiderFeet Structured pane when JSON is available.

## Datastores

| Mode | Default path | Flag |
|------|--------------|------|
| `scan` | `titus.ds` | `--output` (`:memory:`, `:auto:` supported) |
| `enum` | `titus.db` | `--output` |
| `report` / `explore` | `titus.ds` | `--datastore` |

Keep one datastore per engagement. Do not mix clients.

## Preferred capture pattern

```bash
titus scan ./target --format json --output ./engagement.ds > ./scan_console.json
# or re-read later:
titus report --datastore ./engagement.ds --format json > ./findings.json
titus report summary --datastore ./engagement.ds --format json > ./summary.json
```

If scan already printed JSON, still keep the datastore for `explore` triage and re-export.

## Parsing workflow

1. Load JSON root (array or object — inspect live output; do not assume Nosey Parker JSONL shape).
2. For each finding: capture **rule id/name**, **score/severity**, **validation status** (if `--validate`), **provenance** (path, repo, commit, URL host) — **not** raw secret bytes.
3. Redact capture groups / matched strings before logging or writing examination text.
4. De-duplicate by rule + redacted fingerprint + provenance root.
5. Bundle for harvest as a **single JSON document** with `schema`, scan metadata, and `records[]` (not raw multi-root dumps) when integrating with SpiderFeet harvest.

## NDJSON / serve

`titus serve` speaks **NDJSON** on stdin/stdout for Burp. That is a streaming integration path — not the default formal examination capture. If ever harvested, wrap lines into a single JSON bundle with `records[]` (same pattern as nerva/pius).

## Error / empty shapes

- Clean miss: empty findings list + successful exit is a valid sparse artifact (still produce graph head + empty tree).
- Auth / rate-limit failures on `enum` or remote `scan`: capture exit status + stderr in structured metadata.
- Never invent fields; map only keys present in the live JSON.

## Normalization sketch (redacted)

```json
{
  "finding_id": "titus-<stable-hash>",
  "rule_id": "…",
  "rule_name": "…",
  "score": 0,
  "severity": "info|low|medium|high|critical",
  "path": "repo/config/example.env",
  "validation": "confirmed|denied|unknown|null",
  "evidence_redacted": true
}
```
