**Epic:** #723 · **Phase:** 2a · **Blocks:** #797, #798

## Problem

There is no declarative contract for wrapping a CLI as an OSINT service. Phase 2 runner and Add Service UI need a validated manifest schema.

## Desired outcome

Document and implement a **CLI tool manifest** format (JSON/YAML) describing:

- Service identity (`id`, `name`, `summary`, `service_origin: custom`)
- Executable (`command` argv template, `{tool_path}`, `{target}`, optional `{interpreter}`)
- Input: `consumed_nugget_id`, target extraction rules
- Execution: `timeout_seconds`, `working_dir`, env vars
- Output: `format` (`json` | `jsonlines` | `regex` | `raw`), mapping rules → produced nugget types
- Security: no shell interpolation; argv list only; path validation

## Acceptance criteria

- [ ] Schema file in repo (JSON Schema) + example manifests for dnstwist, wafw00f, snallygaster
- [ ] SPEC-003 updated: R3-05-08 expanded from spike to manifest requirement IDs
- [ ] Validator script or unit tests for schema + 3 examples
- [ ] Security constraints documented (no `shell=True`, max timeout, output size cap)

## Verification

- `pytest` for schema validator
- Manual review: manifest examples round-trip through validator

## Non-goals

- Runtime execution (see #797)
- UI form fields (see spiderfeet-widget #67)

## Spec

R3-05-08
