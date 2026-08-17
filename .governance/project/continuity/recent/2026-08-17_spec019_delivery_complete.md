# SPEC-019 program delivery (2026-08-17)

CP3 complete for lesser-agent scope. All implementation PRs merged to `develop` in both repos.

## spiderfeet (PRs #1334–#1351)

- **Epic A:** uuid4 identity, topology parent_id, host-scoped GSE, docs
- **Epic B:** Nerva `--output` hydrate + `--list` ip:port fixture
- **Epic C:** Nuclei full URL batching, batch i/n, crawl_urls URL-only
- **Epic F:** COMPANY/SUBDOMAIN catalogue, domain tree helper, F3–F7 adapters, F8 validator
- **Epic E:** E1 cross-repo smoke doc (`.docs/docs-for-cli-tools/SPEC019_E1_E2E_SMOKE.md`)

## yaml-workflow-widget (PRs #301–#305)

- **Epic D:** collector deps, port geometry, spec019.smoke.mjs

## Remaining

- **#1331 E2** — operator GOV-08 exploratory review (not agent-automated)

## Verify

See `SPEC019_E1_E2E_SMOKE.md` for pytest + `node src/workflow-dag/spec019.smoke.mjs` commands.
