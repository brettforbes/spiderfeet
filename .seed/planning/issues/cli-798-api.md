**Epic:** #723 · **Phase:** 2c · **Depends:** #796, #797 · **Blocks:** spiderfeet-widget #67

## Problem

Custom CLI manifests need persistence, catalogue merge, and install probing for the Add Service UI.

## Desired outcome

FastAPI routes under `/api/v1/custom-services` (or `/cli-tools`):

| Method | Purpose |
|--------|---------|
| `GET /` | List registered custom CLI services |
| `POST /` | Create manifest + catalogue entry |
| `PUT /{id}` | Update manifest |
| `DELETE /{id}` | Remove (soft-delete or archive) |
| `POST /{id}/probe` | Check binary exists + optional `--version` |
| `POST /{id}/smoke` | Run `scan_ui` with stored seed |

Storage: `.docs/analysis/custom_cli_services.json` (v1) or TypeDB (follow-up). Merge into `osint_services.json` / map bootstrap on save.

## Acceptance criteria

- [ ] OpenAPI documented; CORS compatible with widget
- [ ] Created service appears in Tests module list + Maps after bootstrap
- [ ] `service_origin: custom`, `access_tier: none`, `data_source.model: LOCAL_CLI`
- [ ] Invalid manifest rejected with schema errors from #796

## Verification

- API integration tests
- Widget #67 can call all endpoints

## Spec

R3-05-08, R3-05-02

## Security

- Operator-only (no public registration without auth — document as SPEC_GAP if auth not ready)
- Path allowlist / no parent traversal in `tool_path`
