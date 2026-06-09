# Requestly local workspace — SpiderFeet API v1

Open this folder as a **Local project** in Requestly desktop.

**Path:** `C:\projects\spiderfeet\.docs\api\requestly`

Required layout (Requestly 1.2+):

- `requestly.json` / `__requestly.json` — workspace manifest
- `environments/` — **SpiderFeet Local** (`base_url`, `scan_id`)
- `apis/SpiderFeet API v1/` — one folder per request

## Quick start

1. `.\start.ps1 -Mode api` from repo root
2. Requestly → Create **Local project** → select this directory
3. Environment: **SpiderFeet Local**
4. Run requests **01** → **11** per [WALKTHROUGH.md](WALKTHROUGH.md)

Legacy Postman import files remain in this folder for backup; the live workspace uses `apis/`.
