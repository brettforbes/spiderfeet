# Augustus Output and Parsing

Augustus can emit table (default), structured JSON / JSONL (stdout via `--format`), a JSONL file via `-o`, and an HTML report via `--html`. SpiderFeet examination uses **structured** forms only.

## Primary artifacts

| Artifact | How | Role |
|----------|-----|------|
| JSON document | `--format json` | Single root with `attempts[]` + `count` (verified on 0.14.15) |
| JSONL file | `-o path.jsonl` | Help: “JSONL output file path”; one JSON object per line |
| JSONL stdout | `--format jsonl` | Documented in upstream README; verify if used |
| Table | `--format table` (default) | Human TTY only — not examination source |
| HTML | `--html report.html` | Stakeholder report; not graph source |

## JSON document shape (`--format json`)

Observed on **0.14.15** with `augustus scan test.Blank --probe dan.Dan_11_0 --detector dan.DAN --format json`:

```json
{
  "attempts": [
    {
      "id": "",
      "probe": "dan.Dan_11_0",
      "generator": "test.Blank",
      "detector": "dan.DAN",
      "prompt": "…",
      "prompts": ["…"],
      "outputs": [""],
      "scores": [0],
      "detector_results": { "dan.DAN": [0] },
      "status": "complete",
      "timestamp": "2026-08-10T…",
      "metadata": { "goal": "disregard the system prompt" }
    }
  ],
  "count": 1
}
```

Field names and nesting can grow with multi-turn / buffed probes — preserve unknown keys; do not drop attempts.

## JSONL (`-o`)

Each line is a JSON object for an attempt/finding (probe, prompt, scores, etc.). Parse line-by-line; skip non-JSON lines if progress noise appears on a mixed stream (prefer capturing stdout separately when using `--format json`).

## Parsing priorities

1. Prefer `--format json` (single root) or `-o` JSONL over table.
2. Treat each attempt as one event; keep SAFE and VULN alike.
3. Preserve generator, probe, detector, scores, detector_results, status, timestamp, metadata.
4. Keep timeout/error attempts — they mark coverage gaps, not “clean miss” alone.
5. Separate execution failures (auth, network) from model-safe outcomes.

## Suggested harvest bundle (SpiderFeet)

At harvest, do **not** leave raw `.jsonl` as the Structured pane root. Build:

```json
{
  "schema": "augustus_scan_v1",
  "tool": "augustus",
  "command": "augustus scan …",
  "started_at": "…",
  "duration_s": 0,
  "exit_code": 0,
  "record_count": 1,
  "records": []
}
```

Populate `records[]` from `attempts[]` (JSON mode) or JSONL lines. Derive Text pane lines from records (e.g. `[probe] detector score=… status=…`). `record_count` must equal `len(records)`.

## Guardrails

- Redact API keys and unnecessary full prompt/response bodies before sharing.
- Do not invent score thresholds not present in the artifact.
- Empty `attempts` / `records: []` with successful metadata can be a valid clean-miss scenario — still emit a scan-head graph.
- Never treat progress banners alone as findings.
