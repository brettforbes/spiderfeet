# CLI capability matrix — SpiderFeet Stage 2

**Spec:** R2-02-01 (SPEC-002)  
**Issue:** SF-02-01 (#27)  
**Status:** Approved for implementation 2026-06-03

This document maps today’s `sf.py` / `sfcli.py` / CherryPy web UI behaviour to the planned **FastAPI** surface (`/api/v1/...`). The widget and Requestly tests target FastAPI, not CherryPy.

## Operational modes (`sf.py`)

| Mode | Trigger | Behaviour | FastAPI scope |
|------|---------|-----------|---------------|
| **Web UI server** | `-l IP:port` (required if no other mode) | CherryPy `SpiderFeetWebUi` on port 5001 default | **Deferred** — legacy UI stays on CherryPy until main UI epic (stage 8). Widget uses FastAPI only. |
| **One-shot CLI scan** | `-s TARGET` (+ module/type options) | Foreground scan, stdout via `sfp__stor_stdout`, exit when finished | **SF-02-04** — `POST /api/v1/scans` |
| **Module catalogue** | `-M` / `--modules` | Print module list to stdout | **SF-02-05** — `GET /api/v1/modules` |
| **Event type catalogue** | `-T` / `--types` | Print event types to stdout | **SF-02-06** — `GET /api/v1/event-types` |
| **Correlation run** | `-C scanID` | Run correlation rules on existing scan | **SF-02-07+** — `POST /api/v1/scans/{id}/correlations` (planned) |
| **Version** | `-V` / `--version` | Print version and exit | **SF-02-02** — `GET /api/v1/health` includes version |

## `sf.py` flags → scan / output semantics

| Flag | Purpose | Maps to scan request field | FastAPI notes |
|------|---------|---------------------------|---------------|
| `-s` | Scan target (required for scan mode) | `target` | Required on `POST /api/v1/scans` |
| `-m` | Comma-separated modules | `modules[]` | Mutually exclusive with strict `-x` path |
| `-t` | Comma-separated event types (auto module selection) | `event_types[]` | Expands module list like web UI |
| `-u` | Use case: `all`, `footprint`, `investigate`, `passive` | `use_case` | Same grouping as `sf.py` / `startscan` |
| `-x` | Strict mode (requires `-t`) | `strict: true` + `event_types[]` | |
| `-d` | Debug | `debug: true` | Stored in scan config |
| `-max-threads` | Concurrency | `max_threads` | Config key `_maxthreads` |
| `-q` | Disable logging | `logging: false` | |
| `-o` | Output format `tab`/`csv`/`json` | CLI-only (stdout module) | API returns JSON; export via results endpoints |
| `-H`, `-n`, `-r`, `-S`, `-D`, `-f`, `-F` | Stdout formatting / filtering | CLI-only | **Out of scope** for REST v1 (use `GET .../results`) |

## `sfcli.py` → legacy CherryPy JSON endpoints

`sfcli` talks to the **web UI server** (`cli.server_baseurl`, default `http://127.0.0.1:5001`), not FastAPI.

| sfcli command | HTTP (CherryPy) | FastAPI v1 replacement |
|---------------|-----------------|------------------------|
| `ping` | `GET /ping` | `GET /api/v1/health` |
| `modules` | `GET /modules` | `GET /api/v1/modules` |
| `types` | `GET /eventtypes` | `GET /api/v1/event-types` |
| `correlationrules` | `GET /correlationrules` | `GET /api/v1/correlation-rules` (planned) |
| `start` | `POST /startscan` | `POST /api/v1/scans` |
| `stop` | `GET /stopscan?id=` | `POST /api/v1/scans/{id}/abort` (planned) |
| `scans` | `GET /scanlist` | `GET /api/v1/scans` |
| `scaninfo` | `GET /scanstatus?id=` | `GET /api/v1/scans/{id}` |
| `data` | `GET /scaneventresults?...` | `GET /api/v1/scans/{id}/results` (planned) |
| `summary` | `GET /scansummary?...` | `GET /api/v1/scans/{id}/summary` (planned) |
| `logs` | `GET /scanlog?...` | `GET /api/v1/scans/{id}/logs` (planned) |
| `correlations` | `GET /scancorrelations?...` | `GET /api/v1/scans/{id}/correlations` (planned) |
| `query` | `GET /query?query=` | **Not ported** — raw SQL unsafe for public API |
| `export`, `find`, `delete`, … | various `/scan*` exports | Later stories / widget stage 4 |

## Planned FastAPI v1 resource map (Stage 2 epic)

Base URL: `http://127.0.0.1:8000` (default; override via `start.ps1 -Mode api`).

| Method | Path | SF-02 story | CLI / legacy parity |
|--------|------|-------------|---------------------|
| `GET` | `/api/v1/health` | SF-02-02 | `ping`, `-V` |
| `GET` | `/api/v1/modules` | SF-02-05 | `-M`, `/modules` |
| `GET` | `/api/v1/event-types` | SF-02-06 | `-T`, `/eventtypes` |
| `POST` | `/api/v1/scans` | SF-02-04 | `-s` + `-m`/`-t`/`-u`, `/startscan` |
| `GET` | `/api/v1/scans` | SF-02-07 | `/scanlist` |
| `GET` | `/api/v1/scans/{scan_id}` | SF-02-07 | `/scanstatus` |
| `GET` | `/api/v1/scans/{scan_id}/results` | SF-02-07 | `/scaneventresults` |
| `GET` | `/docs`, `/openapi.json` | SF-02-08 | New |

## Explicitly out of Stage 2 REST v1

- CherryPy HTML pages (`/newscan`, `/scaninfo`, templates)
- Raw SQL `query` endpoint
- TypeDB map APIs (Stage 3 — separate epic)
- Stdout-only CLI formatting flags (`-o`, `-H`, …)

## Implementation order

1. SF-02-02 skeleton + health + CORS  
2. SF-02-03 `start.ps1 -Mode api`  
3. SF-02-04 → SF-02-07 endpoints (reuse `SpiderFeetDb`, `startSpiderFeetScanner`, module loader from `sf.py`)  
4. SF-02-08 OpenAPI polish  
5. SF-02-09–13 docs, pytest, Requestly  

## References

- Entry: `sf.py`, `sfcli.py`, `sfwebui.py`
- Scanner: `sfscan.startSpiderFeetScanner`
- Config bootstrap: `sf.py` `main()` (modules, correlations, DB)
