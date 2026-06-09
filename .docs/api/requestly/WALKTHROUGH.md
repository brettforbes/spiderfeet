# Requestly walkthrough — SpiderFeet Stage 2 (Epic #26)

**Operator:** Brett  
**Goal:** Prove every Stage 2 endpoint with Requestly, then sign off epic #26.  
**Spec:** R2-02-01 · Stories SF-02-11 through SF-02-13

---

## Before you start

1. **Start the API** (leave this terminal open):

   ```powershell
   cd C:\projects\spiderfeet
   .\start.ps1 -Mode api
   ```

2. Confirm in a browser: http://127.0.0.1:8001/api/v1/health → `"status": "ok"`

3. Open **Requestly** → **API Client** workspace.

---

## Step 2 — Open local workspace

Folder (must contain `requestly.json` and `environments/`):

```
C:\projects\spiderfeet\.docs\api\requestly
```

1. Requestly → **Join or Create Project** → **Local project**.
2. Select the folder above → project name e.g. `spiderfeet` → **Create**.
3. Environment: **SpiderFeet Local** (`base_url`, `scan_id`).
4. Collection: **SpiderFeet API v1** under `apis/` (requests **01**–**11**).

---

## Step 3 — Run folder **01 Health**

| Request | Expected |
|---------|----------|
| GET health | **200**, `status: ok`, `service: spiderfeet-api` |

All tests should show green in Requestly’s test panel.

---

## Step 4 — Run folder **02 Catalogue**

| Request | Expected |
|---------|----------|
| GET modules | **200**, list contains `sfp_dnsresolve` |
| GET event-types | **200**, list contains `INTERNET_NAME` |

---

## Step 5 — Run folder **03 Scans async**

Run in order:

| # | Request | Expected | Notes |
|---|---------|----------|-------|
| 1 | POST scans (start) | **201**, sets `scan_id` variable | Body: `sbs.com.au` + `sfp_dnsresolve` |
| 2 | GET scans (list) | **200** | Array |
| 3 | GET scan status | **200** | Re-run until `status` is **FINISHED** (1–30 s) |
| 4 | GET scan results | **200** | Non-empty array after FINISHED |
| 5 | GET scan not found | **404** | Negative test |

**If step 3 still shows STARTING:** wait a few seconds and send **GET scan status** again.

**Manual check (PowerShell):**

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/v1/scans/YOUR_SCAN_ID
```

---

## Step 6 — Run folder **04 Scan UI (widget)**

| Request | Expected | Duration |
|---------|----------|----------|
| POST scan_ui (wait FINISHED) | **200**, `scan_record.status` = FINISHED, `produced` length ≥ 1 | ~2–30 s |
| POST scan_ui (no wait) | **200**, `scan_record.status` = STARTING | Immediate |
| POST scan_ui invalid module | **400** | Immediate |

Inspect **POST scan_ui (wait FINISHED)** response:

- `scan_record.scan_instance_id`
- `scan_record.scan_event_count` / `scan_results_by_type`
- `scan_record.service` → `module_id`, `name`
- `scan_record.route` → `route_name`, `route_state`
- `consumed[]` and `produced[]` nugget objects with `nugget_icon`, `nugget_colour`

---

## Step 7 — Sign-off checklist (SF-02-13)

Record results (copy into GitHub issue #39 or epic #26 comment):

| # | Endpoint | Pass? |
|---|----------|-------|
| 1 | GET /api/v1/health | ☐ |
| 2 | GET /api/v1/modules | ☐ |
| 3 | GET /api/v1/event-types | ☐ |
| 4 | POST /api/v1/scans | ☐ |
| 5 | GET /api/v1/scans | ☐ |
| 6 | GET /api/v1/scans/{id} | ☐ |
| 7 | GET /api/v1/scans/{id}/results | ☐ |
| 8 | GET /api/v1/scans/{id} 404 | ☐ |
| 9 | POST /api/v1/scan_ui (wait) | ☐ |
| 10 | POST /api/v1/scan_ui (no wait) | ☐ |
| 11 | POST /api/v1/scan_ui 400 | ☐ |

**Operator sign-off:** When all boxes are checked, reply in chat or on #26:  
`Stage 2 Requestly sign-off: PASS` with date.

Agent will then close epic #26 (or you close via GitHub).

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Connection refused | API not running — `.\start.ps1 -Mode api` |
| POST scans 422 | Body missing `modules`, `event_types`, or `use_case` |
| scan_ui 504 | Scan slow; increase `timeout_seconds` or retry |
| scan_ui 400 invalid target | Use valid domain `sbs.com.au`, not strings with `@` unless email |
| Tests fail on scan_id empty | Run **POST scans (start)** before status/results |
| PowerShell curl fails | Use `curl.exe` or `Invoke-RestMethod`, not `curl` alias |

---

## Files in this folder

| File | Purpose |
|------|---------|
| `spiderfeet-api.postman_collection.json` | Import via Postman |
| `spiderfeet-local.environment.json` | `base_url` + `scan_id` variables |
| `WALKTHROUGH.md` | This guide |

Full field reference: [../api_reference.md](../api_reference.md)
