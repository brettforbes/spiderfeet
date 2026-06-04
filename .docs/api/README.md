# SpiderFeet HTTP API (Stage 2)

| Document | Purpose |
|----------|---------|
| [api_reference.md](api_reference.md) | Full v1 endpoint reference (SF-02-09) |
| [cli_capability_matrix.md](cli_capability_matrix.md) | `sf.py` / `sfcli` / CherryPy → FastAPI mapping (SF-02-01) |
| [requestly/WALKTHROUGH.md](requestly/WALKTHROUGH.md) | Requestly import + operator sign-off (SF-02-11–13) |

## Run locally

```powershell
.\start.ps1 -Mode api
```

- API base: http://127.0.0.1:8000/api/v1/
- Swagger UI: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/v1/health
- Modules: `GET /api/v1/modules`
- Event types: `GET /api/v1/event-types`
- Scans: `POST /api/v1/scans`, `GET /api/v1/scans`, `GET /api/v1/scans/{id}`, `GET /api/v1/scans/{id}/results`
- **Widget scan UI**: `POST /api/v1/scan_ui` — one consumed nugget + module → `scan_record` + produced nuggets (TypeDB map shape)

Example scan start (Swagger **POST /api/v1/scans**):

```json
{
  "target": "sbs.com.au",
  "modules": ["sfp_dnsresolve"]
}
```

The response returns immediately with `scan_id`, `poll`, and `results` paths. Poll status until `FINISHED`, then fetch results.

**PowerShell** (Swagger *curl* often fails — `curl` is an alias for `Invoke-WebRequest`):

```powershell
$body = '{"target":"sbs.com.au","modules":["sfp_dnsresolve"]}'
$r = Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/scans -Method POST -ContentType application/json -Body $body
$r
Invoke-RestMethod "http://127.0.0.1:8000$($r.poll)"
Invoke-RestMethod "http://127.0.0.1:8000$($r.results)"
```

Or use **`curl.exe`** (real curl), not `curl`.

### Widget scan UI (`POST /api/v1/scan_ui`)

Single-call endpoint for the iframe: pass a catalogue **consumed** nugget and **module_id**; response includes a `scan_record` (mirrors TypeDB `scan-record`) plus `consumed` / `produced` nugget instances.

```json
{
  "module_id": "sfp_dnsresolve",
  "consumed": {
    "nugget_id": "INTERNET_NAME",
    "nugget_data": "sbs.com.au"
  },
  "wait": true,
  "timeout_seconds": 120
}
```

```powershell
$body = '{"module_id":"sfp_dnsresolve","consumed":{"nugget_id":"INTERNET_NAME","nugget_data":"sbs.com.au"},"wait":true}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/scan_ui -Method POST -ContentType application/json -Body $body
```

Set `"wait": false` to return immediately after starting the scan (status `STARTING`, empty `produced` until polled via `/scans/{id}/results`).

Legacy web UI (CherryPy) remains `.\start.ps1` or `.\start.ps1 -Mode web`.

## Verify

```bash
poetry run pytest .tests/api -q -m "not slow"
poetry run pytest .tests/api -q -m slow
```

Requestly: import [requestly/spiderfeet-api.postman_collection.json](requestly/spiderfeet-api.postman_collection.json) and follow [requestly/WALKTHROUGH.md](requestly/WALKTHROUGH.md).
