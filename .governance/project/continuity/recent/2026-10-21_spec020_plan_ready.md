# SPEC-020 planning checkpoint — GoRules Project Context

**Date:** 2026-10-21
**Mode:** Planning
**Status:** Architecture published; GitHub epics/stories linked and first wave ready.

## Decisions fixed

- FastAPI orchestrates; GoRules is the pinned policy authority.
- Production operands come only from project-scoped temporary-subgraph IDs selected in Composer’s Temporary Subgraph Viewer.
- `.temp/gorules_temp_exports` is development/test golden corpus only.
- Golden tests seed authoritative temporary-subgraph persistence and exercise the same ID-only path as production.
- Semantic merge is MECE, commutative, and associative.
- Identity uses global, parent-scoped, observation, and evidence-resolved strategies.
- Same address is strong candidate evidence within one workflow execution, not unconditional identity.
- IPv4 and IPv6 are supported.
- SYSTEM may be retyped to HOST/DEVICE/CDN by released GoRules policy; specific conflicts hold.
- Retyping adopts a new typed instance ID and records the remap; no stable context entity ID is added.
- Context hierarchy is a multi-parent DAG; inferred nodes/edges require provenance.
- Revisions are immutable; valid hold-free results auto-activate; holds remain non-current drafts.
- Exact replay and newer-release re-evaluation are distinct; mismatch uses corrective revision.
- Context iframe is rebuilt in React with Rules, Combined Graph, and Provenance panes.
- Docker Desktop hosts GoRules BRMS plus dedicated PostgreSQL.
- A self-hosted GoRules license is not yet available and blocks live BRMS proof.

## Durable artifacts

- Spec: `.governance/specs/SPEC-020-gorules-project-context.md`
- Agent plan: `.governance/project/SPEC020_AGENT_PLAN.md`
- Issue index: `.governance/project/SPEC020_ISSUE_INDEX.md`
- Publication checklist: `.governance/project/SPEC020_ISSUE_PUBLICATION.md`
- Issue bodies:
  - `.governance/project/spec020_issue_bodies/backend.md`
  - `.governance/project/spec020_issue_bodies/context_widget.md`
  - `.governance/project/spec020_issue_bodies/host_widget.md`
- Cursor plan: `C:\Users\brett\.cursor\plans\gorules_context_graph_7164ac16.plan.md`

## GitHub publication

- 46 issues published: 8 epics and 38 stories.
- `brettforbes/spiderfeet`: #1353–#1384.
- `brettforbes/widget-context-gorules`: #1–#9.
- `brettforbes/spiderfeet-widget`: #278–#282.
- Parent/child issue relationships and cross-repo dependency links are populated.
- All issues are on the canonical project board with Priority, Size, and VibeGov Status.
- W0, A1, B1, and C1 are `Ready`; all dependent issues remain `Backlog`.

## Next action

Land G0 (#1384), then start the first bounded lesser-agent wave:

1. W0 — governance/integration branch bootstrap.
2. A1 — Docker Desktop + BRMS/PostgreSQL stack (live BRMS proof remains license-blocked).
3. B1 — semantic records, normalizers, and identity strategies.
4. C1 — revision/job/hold schema.

Each agent owns one issue/branch/evidence bundle and must follow `.governance/project/SPEC020_AGENT_PLAN.md`.
