# SPEC-020 issue index — GoRules Project Context

**Spec:** `.governance/specs/SPEC-020-gorules-project-context.md`
**Agent plan:** `.governance/project/SPEC020_AGENT_PLAN.md`
**Issue bodies:** `.governance/project/spec020_issue_bodies/`

Status legend: `planned` → `open` → `in progress` → `in review` → `done`; use `blocked` only with evidence.

> Publication status: all SPEC-020 epics and stories are published and linked. Board state is authoritative for execution status.

## Repository map

| Repo | Scope | Integration branch |
|---|---|---|
| `brettforbes/spiderfeet` | Spec, BRMS platform/client, identity/rules, persistence, merge APIs, acceptance | `develop` |
| `brettforbes/widget-context-gorules` | React context iframe | W0 creates/normalizes `develop` |
| `brettforbes/spiderfeet-widget` | Composer host and Temporary Subgraph Viewer actions | `develop` |

## Program governance (`spiderfeet`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| G0 — Land canonical planning and issue package | [#1384](https://github.com/brettforbes/spiderfeet/issues/1384) | Governance prerequisite | — | done |

## Epic A — Local GoRules platform (`spiderfeet`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic A | [#1353](https://github.com/brettforbes/spiderfeet/issues/1353) | R20-07, R20-08 | — | open |
| A1 — Docker Desktop + BRMS/PostgreSQL stack | [#1354](https://github.com/brettforbes/spiderfeet/issues/1354) | R20-08.1..4 | — | open |
| A2 — Typed BRMS client + health/auth | [#1355](https://github.com/brettforbes/spiderfeet/issues/1355) | R20-08.5, R20-09.3 | A1 | open |
| A3 — Branch/simulate/release/evaluate lifecycle | [#1356](https://github.com/brettforbes/spiderfeet/issues/1356) | R20-07.4..7, R20-08.5 | A2 | open |

## Epic B — Semantic identity + JDM rules (`spiderfeet`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic B | [#1357](https://github.com/brettforbes/spiderfeet/issues/1357) | R20-02..07 | — | open |
| B1 — Semantic record and normalization contract | [#1358](https://github.com/brettforbes/spiderfeet/issues/1358) | R20-02, R20-03, R20-05 | — | open |
| B2 — Candidate index + MECE mapping | [#1359](https://github.com/brettforbes/spiderfeet/issues/1359) | R20-02, R20-03, R20-06 | B1 | open |
| B3 — Core identity/hierarchy/classification JDM | [#1360](https://github.com/brettforbes/spiderfeet/issues/1360) | R20-03..07 | B1 | open |
| B4 — Five-tool evidence mappings + simulator cases | [#1361](https://github.com/brettforbes/spiderfeet/issues/1361) | R20-07.1..3, R20-07.7 | B3 | open |
| B5 — Repository seed ↔ BRMS release gate | [#1362](https://github.com/brettforbes/spiderfeet/issues/1362) | R20-07.4..7 | A3, B4 | open |

## Epic C — Revisions + provenance persistence (`spiderfeet`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic C | [#1363](https://github.com/brettforbes/spiderfeet/issues/1363) | R20-08..11 | — | open |
| C1 — Revision/job/hold schema | [#1364](https://github.com/brettforbes/spiderfeet/issues/1364) | R20-09, R20-10 | — | open |
| C2 — Content-addressed snapshots and traces | [#1365](https://github.com/brettforbes/spiderfeet/issues/1365) | R20-01.3, R20-10, R20-11 | C1 | open |
| C3 — Provenance ledger + inferred/remap events | [#1366](https://github.com/brettforbes/spiderfeet/issues/1366) | R20-04.3..6, R20-05.5..7, R20-11.1..3 | B1, C1, C2 | open |
| C4 — Canonical materialization, activation, rollback | [#1367](https://github.com/brettforbes/spiderfeet/issues/1367) | R20-06, R20-09.4..6, R20-10 | C3 | open |

## Epic D — Merge jobs + context APIs (`spiderfeet`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic D | [#1368](https://github.com/brettforbes/spiderfeet/issues/1368) | R20-01, R20-06, R20-09..11 | — | open |
| D1 — ID-only authoritative operand resolver | [#1369](https://github.com/brettforbes/spiderfeet/issues/1369) | R20-01, R20-13.4 | B1, C1 | open |
| D2 — Async pairwise merge orchestrator | [#1370](https://github.com/brettforbes/spiderfeet/issues/1370) | R20-02..06, R20-09 | A2, B2, B3, C4, D1 | open |
| D3 — Explicit Combine All + convergence | [#1371](https://github.com/brettforbes/spiderfeet/issues/1371) | R20-06, R20-13.3 | D2 | open |
| D4 — Progress/cancel/stale/fail-closed behavior | [#1372](https://github.com/brettforbes/spiderfeet/issues/1372) | R20-09 | D2, C4 | open |
| D5 — Exact replay, re-evaluation, corrective revision | [#1373](https://github.com/brettforbes/spiderfeet/issues/1373) | R20-10, R20-11.4..6 | D2, D3, D4, C4 | open |
| D6 — Provenance queries + hold resolution | [#1374](https://github.com/brettforbes/spiderfeet/issues/1374) | R20-04.5..6, R20-11.1..3 | C3, C4, D2 | open |

## Epic E — Golden acceptance + operations (`spiderfeet`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic E | [#1375](https://github.com/brettforbes/spiderfeet/issues/1375) | R20-14 | — | open |
| E1 — Golden fixture seeder through temporary persistence | [#1376](https://github.com/brettforbes/spiderfeet/issues/1376) | R20-01, R20-14.1..3 | D1, D2 | open |
| E2 — MECE/classification/convergence acceptance | [#1377](https://github.com/brettforbes/spiderfeet/issues/1377) | R20-02..07, R20-14.4..5 | B5, C4, D3, E1 | open |
| E3 — Failure/persistence/replay acceptance | [#1378](https://github.com/brettforbes/spiderfeet/issues/1378) | R20-09..11, R20-14.4 | D4, D5, D6, E1 | open |
| E4 — Startup, rule-release, recovery runbook | [#1379](https://github.com/brettforbes/spiderfeet/issues/1379) | R20-08, R20-14 | I2 | open |

## Epic W — Context GoRules iframe (`widget-context-gorules`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic W | [#1](https://github.com/brettforbes/widget-context-gorules/issues/1) | R20-12 | — | open |
| W0 — Governance + integration branch bootstrap | [#2](https://github.com/brettforbes/widget-context-gorules/issues/2) | Governance prerequisite | — | open |
| W1 — React shell + JDM editor compatibility spike | [#3](https://github.com/brettforbes/widget-context-gorules/issues/3) | R20-12.1, R20-12.7 | W0 | open |
| W2 — Versioned embed protocol + standalone API shell | [#4](https://github.com/brettforbes/widget-context-gorules/issues/4) | R20-12.5..6, R20-13.4 | W1 | open |
| W3 — Rules branch/simulate/release pane | [#5](https://github.com/brettforbes/widget-context-gorules/issues/5) | R20-07, R20-12.2..4 | W2, A3 | open |
| W4 — Combined graph pane + pane modes | [#6](https://github.com/brettforbes/widget-context-gorules/issues/6) | R20-12.2..5 | W2, D2 | open |
| W5 — Provenance/revision bidirectional pane | [#7](https://github.com/brettforbes/widget-context-gorules/issues/7) | R20-11, R20-12.2..4 | W4, D6 | open |
| W6 — Async jobs, holds, replay UI | [#8](https://github.com/brettforbes/widget-context-gorules/issues/8) | R20-09, R20-11, R20-12 | W3, W4, W5, D4, D5, D6 | open |
| W7 — Widget contract, accessibility, build tests | [#9](https://github.com/brettforbes/widget-context-gorules/issues/9) | R20-12, R20-14.6 | W3..W6 | open |

## Epic H — Composer host (`spiderfeet-widget`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic H | [#278](https://github.com/brettforbes/spiderfeet-widget/issues/278) | R20-13 | — | open |
| H1 — Context iframe host + configuration | [#279](https://github.com/brettforbes/spiderfeet-widget/issues/279) | R20-12.5..6, R20-13.5 | W2 | open |
| H2 — Temporary Viewer selection + combine buttons | [#280](https://github.com/brettforbes/spiderfeet-widget/issues/280) | R20-01, R20-13.1..4 | H1, D1, D2, D3 | open |
| H3 — Async state, cross-highlight, host expansion | [#281](https://github.com/brettforbes/spiderfeet-widget/issues/281) | R20-12.5, R20-13.5..6 | H1, H2, W4, W5, W6 | open |
| H4 — Host protocol + Composer regression tests | [#282](https://github.com/brettforbes/spiderfeet-widget/issues/282) | R20-13, R20-14.6 | H1..H3, W7 | open |

## Epic I — Cross-repo release gates (`spiderfeet`)

| Code | Issue | Requirement | Depends on | Status |
|---|---|---|---|---|
| Epic I | [#1380](https://github.com/brettforbes/spiderfeet/issues/1380) | R20-14.6 | — | open |
| I1 — Cross-repo contract integration | [#1381](https://github.com/brettforbes/spiderfeet/issues/1381) | R20-01, R20-09..13 | D1..D6, W7, H4 | open |
| I2 — Live seeded end-to-end acceptance | [#1382](https://github.com/brettforbes/spiderfeet/issues/1382) | R20-08, R20-14 | E2, E3, I1, licensed BRMS | open |
| I3 — GOV-08 exploratory operator gate | [#1383](https://github.com/brettforbes/spiderfeet/issues/1383) | R20-14.6 | I2, E4 | open |

## Critical path

```text
W0 → W1 → W2 → H1

A1 → A2 → A3 → B5
B1 → B2 ─┐
B1 → B3 → B4 → B5
C1 → C2 → C3 → C4
B2+B3+C4+D1+A2 → D2 → D3/D4 → D5/D6

W2+D2 → W4
W2+A3 → W3
W4+D6 → W5
W3+W4+W5+D4+D5+D6 → W6 → W7

H1+D1+D2+D3 → H2
H2+W4+W5+W6 → H3 → H4

D1+D2 → E1
B5+C4+D3+E1 → E2
D4+D5+D6+E1 → E3
E2+E3+W7+H4 → I1 → I2 → E4 → I3
```

## First lesser-agent assignments after publication

1. W0 in `widget-context-gorules`.
2. A1, B1, and C1 in `spiderfeet` as separate parallel branches.
3. W1 after W0.
4. Do not start host-widget work until W2 defines the protocol.
