# Trajan Output and Parsing

## Formats (`-o` / `--output`)

| Value | Use |
|-------|-----|
| `json` | **SpiderFeet primary** — structured findings for harvest / graphs |
| `sarif` | CI / code-scanning integrations |
| `html` | Human report artifact |
| `console` | Default operator triage — not corpus structured source |

Global default is `console`. Always pass `-o json` for automation.

ADO `enumerate` help also documents local `-o` values `console`, `json`, `csv` for that subtree — prefer `json` when present.

## Parsing priorities

1. Parse **findings** as the primary record set when present.
2. Retain severity, detection/capability name, workflow or pipeline path, repo/project identity, and evidence text.
3. Keep non-fatal errors / skipped detectors as coverage caveats, not hard failure of the whole run.
4. De-duplicate by a stable key such as: `platform + repo/project + workflow_file + detection + evidence_hash`.
5. Mark `--path` (offline) scans as reduced coverage vs API mode.

## Suggested normalized record

```json
{
  "platform": "github",
  "scope": "owner/repo",
  "severity": "high",
  "detection_type": "artifact-poisoning",
  "workflow_file": ".github/workflows/release.yml",
  "evidence": "untrusted artifact consumed in privileged job",
  "source": "trajan",
  "mode": "api"
}
```

Field names vary by platform and Trajan version — inspect the live JSON; do not invent schema keys.

## Harvest / SpiderFeet notes

- Prefer a **single JSON root** for the Structured pane (bundle with `schema`, scan metadata, and `records[]` when integrating harvest).
- Derive Text pane from structured finding lines — do not harvest console banners alone.
- Empty finding lists are valid clean-miss / hardened-org scenarios when the command succeeded.
- **Never** treat `attack` / `retrieve` secret payloads as corpus `nugget_data`. Redact or exclude.

## Parser guardrails

- Handle missing optional fields defensively.
- Do not fail entire ingestion on one malformed finding.
- Preserve evidence snippets for analysts; redact secrets.
- Do not invent flags or output fields absent from Captured help / observed JSON.
