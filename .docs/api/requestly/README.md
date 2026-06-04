# Requestly local workspace — SpiderFeet API v1

This folder **is** the Requestly workspace root. It contains `requestly.json` and `environments/` as required by the desktop app.

## Open in Requestly

1. Start the API: `.\start.ps1 -Mode api` (from repo root).
2. In Requestly → workspace menu → **Join or Create Project** → **Create Project** → **Local project**.
3. **Folder:** select this directory exactly:

   `C:\projects\spiderfeet\.docs\api\requestly`

4. **Project name:** `spiderfeet` (or any label you prefer; the folder name does not have to match).
5. In the API client, choose environment **SpiderFeet Local**.
6. Open collection **SpiderFeet API v1** and follow [WALKTHROUGH.md](WALKTHROUGH.md).

## Layout

```
requestly/
  requestly.json          # workspace manifest (version 0.0.2)
  environments/
    global.json
    e5f6a7b8-....json     # SpiderFeet Local (base_url, scan_id)
  SpiderFeet API v1/      # one JSON file per request
  WALKTHROUGH.md
  import/                 # optional Postman import backup
```

## If the workspace looks empty

- Confirm you selected **`...\spiderfeet\.docs\api\requestly`**, not the parent `.docs\api` folder.
- Restart Requestly after pointing at the folder.
- Ensure `feature/26-stage2-scan-ui-close` is checked out (or `develop` after PR #651 merge) so these files exist on disk.

## Related

- [../api_reference.md](../api_reference.md)
- [../README.md](../README.md)
