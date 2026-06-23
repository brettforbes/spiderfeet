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

- API base: http://127.0.0.1:8001/api/v1/
- Swagger UI: http://127.0.0.1:8001/docs
- Health: http://127.0.0.1:8001/api/v1/health
- Modules: `GET /api/v1/modules`
- Event types: `GET /api/v1/event-types`
- Scans: `POST /api/v1/scans`, `GET /api/v1/scans`, `GET /api/v1/scans/{id}`, `GET /api/v1/scans/{id}/results`
- **Widget scan UI**: `POST /api/v1/scan_ui` — one consumed nugget + module → `scan_record` + produced nuggets (TypeDB map shape)

## Map API (Stage 3b)

Requires `.config/typedb.connection.json` and a bootstrapped `spiderfeet-map` database (see [`.docs/typedb/README.md`](../typedb/README.md)).

## CLI corpus API (profiling review UI)

Serves examination bundles from `.docs/docs-for-cli-tools/` for the widget **CLI Profiling** tab (`.seed/04_Driving and Integrating_CLI_Apps.md` §2.1.3).

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/cli-corpus/config` | Data Viewer embed URL |
| `GET /api/v1/cli-corpus/tools` | Tools from `corpus_index.json` |
| `GET /api/v1/cli-corpus/tools/{id}/examinations` | Exam list |
| `GET /api/v1/cli-corpus/tools/{id}/examinations/{n}` | Full bundle (text, structured, graph proposal, markdown) |
| `POST /api/v1/cli-corpus/tools/{id}/examinations/{n}/review` | Set `pending` / `approved` / `rejected` |

Structured tab embed: start [json-yaml-xml-csv-widget](https://github.com/brettforbes/json-yaml-xml-csv-widget) (`.\start.ps1` → `http://localhost:3000/widget`). Override with `SPIDERFEET_DATA_VIEWER_URL`.

### Map endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/map/connection` | Redacted TypeDB connection info |
| `POST /api/v1/map/connection/ping` | Test TypeDB reachability |
| `GET /api/v1/map/status` | Nugget/service/link counts |
| `POST /api/v1/map/bootstrap` | Idempotent seed (`?reset=true` dev only) |
| `GET /api/v1/map/graph` | Force-graph `{ nodes[], links[] }` for the widget |

Example: `GET http://127.0.0.1:8001/api/v1/map/graph`

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
$r = Invoke-RestMethod -Uri http://127.0.0.1:8001/api/v1/scans -Method POST -ContentType application/json -Body $body
$r
Invoke-RestMethod "http://127.0.0.1:8001$($r.poll)"
Invoke-RestMethod "http://127.0.0.1:8001$($r.results)"
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
Invoke-RestMethod -Uri http://127.0.0.1:8001/api/v1/scan_ui -Method POST -ContentType application/json -Body $body
```

Set `"wait": false` to return immediately after starting the scan (status `STARTING`, empty `produced` until polled via `/scans/{id}/results`).

Legacy web UI (CherryPy) remains `.\start.ps1` or `.\start.ps1 -Mode web`.

## Verify

```bash
poetry run pytest .tests/api -q -m "not slow"
poetry run pytest .tests/api -q -m slow
```

Requestly: import [requestly/spiderfeet-api.postman_collection.json](requestly/spiderfeet-api.postman_collection.json) and follow [requestly/WALKTHROUGH.md](requestly/WALKTHROUGH.md).
