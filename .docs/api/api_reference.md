# SpiderFeet API reference (v1)

**Spec:** R2-02-01 (SPEC-002) · **Epic:** [#26](https://github.com/brettforbes/spiderfeet/issues/26)  
**Base URL:** `http://127.0.0.1:8001` (default from `.\start.ps1 -Mode api`)  
**Prefix:** `/api/v1`  
**OpenAPI:** http://127.0.0.1:8001/openapi.json · **Swagger:** http://127.0.0.1:8001/docs

---

## Health

### `GET /api/v1/health`

Liveness and version check (sfcli `ping` / startup preflight).

| | |
|---|---|
| **Auth** | None |
| **Body** | None |

**200 response**

```json
{
  "status": "ok",
  "service": "spiderfeet-api",
  "version": "0.1.0"
}
```

---

## Catalogue

### `GET /api/v1/modules`

OSINT module list (`sf.py -M`, CherryPy `/modules`). Internal storage modules (`sfp__stor_*`) are excluded.

**200:** array of `{ "name": "sfp_dnsresolve", "description": "DNS Resolver" }`

### `GET /api/v1/event-types`

Event type catalogue (`sf.py -T`, CherryPy `/eventtypes`).

**200:** array of `{ "name": "INTERNET_NAME", "description": "..." }`

---

## Scans (async)

### `POST /api/v1/scans`

Start a scan in a background process. Returns immediately (non-blocking).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `target` | string | yes | Domain, IP, email, etc. |
| `modules` | string[] | one of* | e.g. `["sfp_dnsresolve"]` |
| `event_types` | string[] | one of* | Expands module list |
| `use_case` | enum | one of* | `all`, `footprint`, `investigate`, `passive` |
| `scan_name` | string | no | Defaults to `target` |
| `debug` | bool | no | Default `false` |

\*At least one of `modules`, `event_types`, or `use_case` is required.

**Example**

```json
{
  "target": "sbs.com.au",
  "modules": ["sfp_dnsresolve"]
}
```

**201 response**

```json
{
  "scan_id": "A1B2C3D4",
  "status": "STARTING",
  "poll": "/api/v1/scans/A1B2C3D4",
  "results": "/api/v1/scans/A1B2C3D4/results"
}
```

| Status | Meaning |
|--------|---------|
| 422 | Validation (missing module selection) |
| 400 | Invalid target or scan start failure |

### `GET /api/v1/scans`

List scan instances (CherryPy `/scanlist`).

**200:** array of `ScanSummary` — `scan_id`, `name`, `target`, `created`, `started`, `ended`, `status`, `result_count`

### `GET /api/v1/scans/{scan_id}`

Scan status (CherryPy `/scanstatus`).

**200:** `scan_id`, `name`, `target`, `created`, `started`, `ended`, `status`  
**404:** unknown `scan_id`

**Terminal statuses:** `FINISHED`, `ERROR-FAILED`, `ABORTED`, `ABORT-REQUESTED`

### `GET /api/v1/scans/{scan_id}/results`

Raw scan events (CherryPy `/scaneventresults`).

| Query | Default | Description |
|-------|---------|-------------|
| `event_type` | `ALL` | Filter by event type |
| `filter_fp` | `false` | Hide false positives |

**200:** array of result items:

```json
{
  "generated": 1717481077,
  "data": "203.0.113.1",
  "source_data": "sbs.com.au",
  "module": "sfp_dnsresolve",
  "type": "IP_ADDRESS",
  "confidence": 100,
  "visibility": 100,
  "risk": 0,
  "event_description": null,
  "false_positive": false
}
```

---

## Widget scan UI (sync)

### `POST /api/v1/scan_ui`

Run **one module** from a **consumed nugget**; intended for the spiderfeet-widget iframe. By default **waits** until the scan finishes.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `module_id` | string | yes | e.g. `sfp_dnsresolve` |
| `consumed.nugget_id` | string | yes | Catalogue id, e.g. `INTERNET_NAME` |
| `consumed.nugget_data` | string | yes | Target value, e.g. `sbs.com.au` |
| `wait` | bool | no | Default `true` |
| `timeout_seconds` | int | no | 5–600, default `120` when `wait` is true |
| `scan_name` | string | no | Defaults to `nugget_data` |
| `scan_notes` | string | no | Stored on `scan_record` |
| `debug` | bool | no | Default `false` |

**Example**

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

**200 response**

```json
{
  "scan_record": {
    "scan_instance_id": "CFA30507",
    "status": "FINISHED",
    "scan_event_count": 9,
    "scan_results_by_type": {
      "IP_ADDRESS": 2,
      "INTERNET_NAME": 3
    },
    "scan_results": {
      "status": "FINISHED",
      "event_count": 9,
      "by_type": { }
    },
    "scan_duration": 2.0,
    "scan_timestamp": "2026-06-04T05:24:37+00:00",
    "scan_notes": "",
    "service": {
      "module_id": "sfp_dnsresolve",
      "name": "DNS Resolver"
    },
    "route": {
      "route_name": "INTERNET_NAME-to-IP_ADDRESS-via-sfp_dnsresolve",
      "route_state": "in-test"
    }
  },
  "consumed": [ { "nugget_id": "INTERNET_NAME", "nugget_data": "sbs.com.au", ... } ],
  "produced": [ { "nugget_id": "IP_ADDRESS", "nugget_data": "...", ... } ]
}
```

| Status | Meaning |
|--------|---------|
| 400 | Unknown module/nugget, invalid target, scan start error |
| 504 | `wait: true` and scan did not finish in time |
| 422 | Request validation |

With `"wait": false`, `status` is typically `STARTING`, `produced` is empty; poll via `GET /scans/{scan_id}` and `/results`.

**TypeDB map:** fields align with `.seed/spiderfeet_map.tql` relation `scan-record` (persistence in Stage 3).

---

## Errors

FastAPI returns `{ "detail": "..." }` for HTTP errors (string or validation array).

---

## CORS

Default origins include local widget dev hosts. Override:

```powershell
$env:SPIDERFEET_CORS_ORIGINS = "http://localhost:3000,https://my-widget.example"
.\start.ps1 -Mode api
```

---

## Map (Stage 3b)

Requires `.config/typedb.connection.json` and bootstrapped `spiderfeet-map`. See [typedb/README.md](../typedb/README.md).

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/map/connection` | Redacted TypeDB connection info |
| POST | `/api/v1/map/connection/ping` | Test TypeDB reachability |
| GET | `/api/v1/map/status` | Nugget / service / link counts |
| POST | `/api/v1/map/bootstrap` | Idempotent seed (`?reset=true` dev only) |
| GET | `/api/v1/map/graph` | Force-graph `{ nodes[], links[] }` |

---

## Testing

| Layer | Command |
|-------|---------|
| Unit / fast API | `poetry run pytest .tests/api -q` |
| Excludes slow scan | `poetry run pytest .tests/api -q -m "not slow"` |
| Full + integration | `poetry run pytest .tests/api -q -m slow` |
| Requestly | See [requestly/WALKTHROUGH.md](requestly/WALKTHROUGH.md) |

---

## Related docs

- [README.md](README.md) — quick start
- [cli_capability_matrix.md](cli_capability_matrix.md) — CLI → REST mapping
- [requestly/spiderfeet-api.postman_collection.json](requestly/spiderfeet-api.postman_collection.json) — import into Requestly
