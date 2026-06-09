# TypeDB map (`spiderfeet-map`)

Stage 3a foundation for [SPEC-002 R2-03-01](.governance/specs/SPEC-002-first-four-stages.md): schema from `.seed/spiderfeet_map.tql`, archetype nuggets from `.docs/analysis/nuggets.json`, and OSINT services from `.docs/analysis/osint_services.json`.

## Prerequisites

- TypeDB **3.x** server reachable (default `127.0.0.1:1729`)
- Python deps: `typedb-driver` (via Poetry)
- **type-bridge** (issue #42) is deferred until **Python 3.13+** is available in the project environment; bootstrap uses `typedb-driver` directly.

## Connection config

1. Copy the example file:

   ```powershell
   Copy-Item .config\typedb.connection.example.json .config\typedb.connection.json
   ```

2. Set `password` (and `addresses` if not local).

3. Optional: point elsewhere with `SPIDERFEET_TYPEDB_CONFIG`.

The real `typedb.connection.json` is gitignored.

## Bootstrap CLI

```powershell
poetry run python -m spiderfeet.map --ping-only
poetry run python -m spiderfeet.map
poetry run python -m spiderfeet.map --reset   # drop & recreate DB (dev only)
```

Idempotent: safe to re-run. Use `--reset` when the schema file (`.seed/spiderfeet_map.tql`) changes.

**Note:** List-valued fields (`flags`, `consumed_nuggets`, etc.) are stored as JSON strings until TypeDB list attributes are enabled on your server build.

**TypeDB relation rules (important):**

- Relation instances **without any role player are deleted on commit**. Bootstrap inserts each OSINT service together with its nugget `links` in the same write transaction.
- Default schema cardinality for `relates` is `@card(0..1)` (one player per role). The map schema sets `relates consumed/produced @card(0..)` on `osint-service`, `route`, and `scan-record` so modules can link many catalogue nuggets.

Creates the database if missing, applies schema once, inserts missing nuggets and OSINT service relations, and links `consumed` / `produced` roles.

## Map FastAPI (Stage 3b)

With the API running (`.\start.ps1 -Mode api`), use `/api/v1/map/*` — see [`.docs/api/README.md`](../api/README.md). The widget Maps tab will consume `GET /api/v1/map/graph`.

## Package layout

| Module | Role |
|--------|------|
| `spiderfeet.map.config` | Load connection JSON |
| `spiderfeet.map.connection` | Open TypeDB driver (TLS on/off) |
| `spiderfeet.map.bootstrap` | Database + seed orchestration |
| `spiderfeet.map.naming` | kebab-case type labels |

## Tests

```powershell
poetry run pytest .tests/map -q
poetry run pytest .tests/map -m typedb -q   # requires running TypeDB + config file
```

## Next (Stage 3b)

- FastAPI connection + init endpoints (#48–#55)
- type-bridge models when Python 3.13 is adopted (#42–#43)
- Widget Maps tab (`spiderfeet-widget` epic #13)
