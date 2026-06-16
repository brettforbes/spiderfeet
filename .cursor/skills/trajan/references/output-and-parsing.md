# Trajan Output and Parsing

Trajan reports scan results with finding-level details including severity, detection type, workflow context, and evidence text.

## Parsing priorities

1. Parse findings as the primary record.
2. Retain severity, detection name/type, workflow file, and evidence.
3. Keep non-fatal errors as separate records (coverage caveats, not hard failure).
4. De-duplicate by stable key: `platform + repo + workflow_file + detection_type + evidence_hash`.

## Suggested normalized record

```json
{
  "platform": "github",
  "scope": "owner/repo",
  "severity": "high",
  "detection_type": "secret_exposure",
  "workflow_file": ".github/workflows/release.yml",
  "evidence": "Step exposes token to untrusted context",
  "source": "trajan"
}
```

## Parser guardrails

- Handle missing optional fields defensively.
- Do not fail entire ingestion on one malformed finding.
- Preserve raw evidence snippets for analyst review.
- Mark local-path scans with reduced coverage when API-only detections are skipped.
