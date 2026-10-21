# Local GoRules BRMS

This stack is for SPEC-020 development. It runs `gorules/brms` with a dedicated PostgreSQL 16 database and a persistent volume.

## License blocker

A self-hosted GoRules license is required. Docker Desktop and PostgreSQL can start without it, but BRMS `/api/health` remains blocked until `LICENSE_KEY` is present in the untracked `deploy/gorules/.env`. Do not invent or commit a key.

Official requirements: https://docs.gorules.io/developers/deployment/brms/overview

## Start

```powershell
./deploy/gorules/start-brms.ps1
```

The script starts Docker Desktop when the engine is unavailable, waits for it, starts this Compose project, and checks `http://localhost:8088/api/health`.

SpiderFeet's existing application Compose file publishes port `5001`. This stack publishes `8088` and uses separate container and volume names.

## Persistence

`gorules-postgres-data` retains database state across `docker compose stop` and `start`. Removing the volume deletes local BRMS data.
