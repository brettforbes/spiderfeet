# SpiderFeet HTTP API (Stage 2)

| Document | Purpose |
|----------|---------|
| [cli_capability_matrix.md](cli_capability_matrix.md) | `sf.py` / `sfcli` / CherryPy → FastAPI mapping (SF-02-01) |

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

Example scan start (Swagger **POST /api/v1/scans**):

```json
{
  "target": "sbs.com.au",
  "use_case": "passive"
}
```

Legacy web UI (CherryPy) remains `.\start.ps1` or `.\start.ps1 -Mode web`.

## Verify

```bash
poetry run pytest .tests/api -q
```
