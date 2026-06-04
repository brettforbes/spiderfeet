# Requestly walkthrough — SpiderFeet Stage 2 (Epic #26)

**Operator:** Brett  
**Goal:** Prove every Stage 2 endpoint with Requestly, then sign off epic #26.  
**Spec:** R2-02-01 · Stories SF-02-11 through SF-02-13

---

## Step 1 — Start the API

```powershell
cd C:\projects\spiderfeet
git checkout feature/26-stage2-scan-ui-close   # or develop after PR #651 merges
.\start.ps1 -Mode api
```

Browser check: http://127.0.0.1:8000/api/v1/health → `"status": "ok"`

---

## Step 2 — Open the local workspace (not Postman import)

Requestly needs a **folder on disk** with `requestly.json` and `environments/`. That folder is:

```
C:\projects\spiderfeet\.docs\api\requestly
```

1. Requestly desktop → workspace menu (top-left) → **Join or Create Project**.
2. **Create Project** → type **Local project**.
3. **Folder:** browse to `C:\projects\spiderfeet\.docs\api\requestly` (this directory, not `.docs\api` parent).
4. **Project name:** e.g. `spiderfeet` → **Create**.
5. In the API client, select environment **SpiderFeet Local** (`base_url` = `http://127.0.0.1:8000`).
6. Open collection **SpiderFeet API v1** (11 requests, numbered 01–11).

If the collection is empty, you opened the wrong folder — it must contain `requestly.json` at the root you selected.

**Optional:** Postman backup under `import/` if your Requestly build supports Postman import instead.

---

## Step 3 — Run requests in order

| # | Request | Expected |
|---|---------|----------|
| 01 | GET health | 200, tests green |
| 02 | GET modules | 200, includes `sfp_dnsresolve` |
| 03 | GET event-types | 200, includes `INTERNET_NAME` |
| 04 | POST scans (start) | 201, sets `scan_id` env var |
| 05 | GET scans (list) | 200 |
| 06 | GET scan status | 200 — **repeat until** `status` = `FINISHED` |
| 07 | GET scan results | 200, non-empty array |
| 08 | GET scan not found | 404 |
| 09 | POST scan_ui (wait FINISHED) | 200, ~2–30 s |
| 10 | POST scan_ui (no wait) | 200, `STARTING` |
| 11 | POST scan_ui invalid module | 400 |

After **04**, `scan_id` is saved automatically (post-response script). **06** must run after **04** and may need several sends.

---

## Step 4 — Sign-off (SF-02-13)

When all 11 pass, comment on epic #26 or reply in chat:

`Stage 2 Requestly sign-off: PASS` + date

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Cannot find workspace files | Open `...\spiderfeet\.docs\api\requestly` exactly |
| Collection empty | Same as above; restart Requestly |
| Connection refused | Run `.\start.ps1 -Mode api` |
| 404 on scan_ui | Checkout branch with scan_ui or merge PR #651 |
| `scan_id` empty on 06/07 | Run **04** first |
| Tests use `pm.*` | Same as Postman; enable Scripts → Post-response in UI |

See [README.md](README.md) and [../api_reference.md](../api_reference.md).
