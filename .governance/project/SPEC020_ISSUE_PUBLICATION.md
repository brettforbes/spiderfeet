# SPEC-020 GitHub issue publication checklist

**Source of truth:** `.governance/project/SPEC020_ISSUE_INDEX.md`
**Bodies:** `.governance/project/spec020_issue_bodies/`

**Publication status:** Complete — 46 issues, 8 epic/sub-issue trees, cross-repo dependency links, and board fields verified on 2026-10-21.

## Required labels

Create/reuse consistently in each repository:

- `spec-020`
- `epic`
- `feature`
- `infrastructure`
- `backend`
- `frontend`
- `integration`
- `testing`
- `documentation`
- `blocked`
- `operator-gate`

Use the canonical project board fields:

- Priority: `P0`, `P1`, `P2`
- Size: `XS`, `S`, `M`, `L`, `XL`
- Status: `Backlog`, `Ready`, `In progress`, `In review`, `Done`, `Blocked`

## Publication order

1. Publish parent epics A–E and I in `brettforbes/spiderfeet`.
2. Publish Epic W and W0 in `brettforbes/widget-context-gorules`.
3. Publish Epic H in `brettforbes/spiderfeet-widget`.
4. Publish all child stories with actual parent-epic links.
5. Replace every `TBD` in `SPEC020_ISSUE_INDEX.md` with a Markdown issue link.
6. Add cross-repo dependency links to affected issue bodies/comments.
7. Add all issues to the canonical board with fields below.
8. Move W0, A1, B1, and C1 to `Ready`; leave dependent work in `Backlog`.
9. Add a program-start comment to each epic linking the spec, agent plan, and issue index.

## Suggested planning fields

### `brettforbes/spiderfeet`

| Code | Priority | Size | Labels |
|---|---|---|---|
| G0 | P0 | S | `spec-020`, `story`, `documentation` |
| Epic A | P0 | L | `spec-020`, `epic`, `infrastructure` |
| A1 | P0 | M | `spec-020`, `infrastructure` |
| A2 | P0 | M | `spec-020`, `backend` |
| A3 | P0 | M | `spec-020`, `backend` |
| Epic B | P0 | XL | `spec-020`, `epic`, `backend` |
| B1 | P0 | M | `spec-020`, `backend` |
| B2 | P0 | L | `spec-020`, `backend` |
| B3 | P0 | L | `spec-020`, `backend` |
| B4 | P0 | L | `spec-020`, `backend`, `testing` |
| B5 | P0 | M | `spec-020`, `backend` |
| Epic C | P0 | XL | `spec-020`, `epic`, `backend` |
| C1 | P0 | L | `spec-020`, `backend` |
| C2 | P1 | M | `spec-020`, `backend` |
| C3 | P0 | L | `spec-020`, `backend` |
| C4 | P0 | L | `spec-020`, `backend` |
| Epic D | P0 | XL | `spec-020`, `epic`, `backend` |
| D1 | P0 | M | `spec-020`, `backend` |
| D2 | P0 | XL | `spec-020`, `backend` |
| D3 | P0 | L | `spec-020`, `backend` |
| D4 | P0 | L | `spec-020`, `backend` |
| D5 | P0 | L | `spec-020`, `backend` |
| D6 | P0 | L | `spec-020`, `backend` |
| Epic E | P0 | L | `spec-020`, `epic`, `testing` |
| E1 | P0 | M | `spec-020`, `testing` |
| E2 | P0 | L | `spec-020`, `testing` |
| E3 | P0 | L | `spec-020`, `testing` |
| E4 | P1 | S | `spec-020`, `documentation` |
| Epic I | P0 | L | `spec-020`, `epic`, `integration` |
| I1 | P0 | M | `spec-020`, `integration`, `testing` |
| I2 | P0 | L | `spec-020`, `integration`, `testing` |
| I3 | P0 | M | `spec-020`, `operator-gate`, `testing` |

### `brettforbes/widget-context-gorules`

| Code | Priority | Size | Labels |
|---|---|---|---|
| Epic W | P0 | XL | `spec-020`, `epic`, `frontend` |
| W0 | P0 | M | `spec-020`, `infrastructure`, `documentation` |
| W1 | P0 | L | `spec-020`, `frontend` |
| W2 | P0 | M | `spec-020`, `frontend`, `integration` |
| W3 | P0 | L | `spec-020`, `frontend` |
| W4 | P0 | L | `spec-020`, `frontend` |
| W5 | P0 | L | `spec-020`, `frontend` |
| W6 | P0 | L | `spec-020`, `frontend` |
| W7 | P0 | M | `spec-020`, `frontend`, `testing` |

### `brettforbes/spiderfeet-widget`

| Code | Priority | Size | Labels |
|---|---|---|---|
| Epic H | P0 | L | `spec-020`, `epic`, `frontend`, `integration` |
| H1 | P0 | M | `spec-020`, `frontend`, `integration` |
| H2 | P0 | M | `spec-020`, `frontend` |
| H3 | P0 | L | `spec-020`, `frontend`, `integration` |
| H4 | P0 | M | `spec-020`, `frontend`, `testing` |

## License blocker handling

- A1 may proceed through Compose/static validation without a license.
- Live A1 health, A2 live contract, A3 live lifecycle, B5 live activation, and I2 are `Blocked` until `LICENSE_KEY` is supplied.
- Do not mark those acceptance criteria verified from mocks.
- The blocker comment must link the official GoRules BRMS deployment requirement and state that Docker Desktop availability alone is insufficient.

## Assignment gate

The program is ready for lesser agents only when:

- every story exists as a GitHub issue;
- every `TBD` link is replaced;
- parent and dependency links resolve;
- W0, A1, B1, and C1 are `Ready`;
- all other stories are `Backlog`;
- the license-dependent proof boundary is visible;
- no issue describes filesystem exports as production input.
