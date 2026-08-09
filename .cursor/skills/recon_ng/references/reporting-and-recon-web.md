# Reporting and Recon-web

## Reporting modules

`reporting/*` converts workspace tables into exportable artifacts for review and SpiderFeet ingestion.

Workflow:

1. Validate tables (`domains`, `hosts`, `contacts`, `ports`, vulnerabilities as present)
2. `modules load reporting/<module>`
3. Configure output options
4. Run; verify artifact integrity
5. Ingest structured exports into text/data/graph paths

Prefer machine-readable reporting outputs when the module offers them; derive human text for review.

## recon-web

Launcher (captured **2026-08-10**):

```text
recon-web [-h] [--host HOST] [--port PORT]
```

Banner states:

- Web UI for analytics/reporting
- Recon-API under `/api/`

```powershell
$env:PYTHONPATH = "C:\projects\spiderfeet\.tools\recon-ng"
& C:\projects\spiderfeet\.venv\Scripts\python.exe C:\projects\spiderfeet\.tools\recon-ng\recon-web --host 127.0.0.1 --port 5000
```

Use for collaborative review. Still validate with `db query` before declaring completeness. Bind `--host` carefully (prefer localhost for local review).

## Export naming

`<workspace>-<module-family>-<timestamp>.<ext>` — keep workspace identity in filenames.

## Pitfalls

- Exporting before table validation
- Assuming report success equals data quality
- Using recon-web as the only evidence without structured extracts
