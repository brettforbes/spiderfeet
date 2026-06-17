# Module Types and Datastore

Module classes:

- `auxiliary/*` for scanning and gathering
- `exploit/*` for exploitation
- `payload/*`, encoders, nops, post

Datastore guidance:

- Set required options (`RHOSTS`, `RPORT`, auth fields) first.
- Prefer `check` before `exploit` where available.
- Use global options (`setg`) cautiously to avoid cross-module mistakes.
- Start from auxiliary modules in discovery-focused pipelines.
