# SPEC-020 GitHub issue bodies — `brettforbes/spiderfeet-widget`

Canonical spec: `@spiderfeet/.governance/specs/SPEC-020-gorules-project-context.md`.

Every story branches from `develop`, targets `develop`, and preserves the existing Temporary Subgraph Viewer as the production source-selection surface.

---

## Epic H — Composer host integration

**Spec:** R20-13
**Outcome:** Composer embeds the context iframe, lets users select live backend-owned temporary subgraphs, and invokes pairwise/combine-all through stable IDs only.

### Guardrails

- Do not load `.temp/gorules_temp_exports`.
- Do not send graph payloads or filesystem paths to the iframe/backend.
- Do not duplicate merge logic in the host.
- Do not trigger automatic merging on step completion.

---

## H1 — Add context iframe host and configuration

**Spec:** R20-12.5..6, R20-13.5
**Depends on:** context-widget W2

### Scope

- Replace/nest the empty `#composer-project-context-stage` canvas with a context iframe slot while retaining stage sizing and existing project-context expansion controls.
- Add configurable context-widget URL on `#widget-root`, with a non-conflicting local default.
- Implement the W2 versioned handshake, origin checks, request IDs, acknowledgements, theme/project/workflow scope, ready/error states, and clean unmount.
- Preserve host control over expansion and project navigation.

### Acceptance criteria

- Composer loads without the context widget available and shows a bounded error/retry state.
- Wrong protocol/origin fails visibly.
- No BRMS credentials or graph payloads enter host messages.
- Existing Temporary Subgraph Viewer still loads independently.

### Verification

- Host module unit/contract tests.
- Composer smoke with widget available/unavailable/wrong version.

---

## H2 — Add Temporary Subgraph Viewer selection and combine actions

**Spec:** R20-01, R20-13.1..4
**Depends on:** H1, backend D1/D2/D3

### Scope

- Add accessible selection controls to the existing Temporary Subgraph Viewer using `temporary_subgraph_id`.
- Enable Pairwise Combine only when exactly two eligible subgraphs are selected.
- Add explicit Combine All over the visible/eligible project set with a confirmation summary of IDs/count.
- Send project/workflow scope and IDs through the agreed application path; do not duplicate nodes/edges.
- Handle subgraph refresh/removal by clearing stale selections.

### Acceptance criteria

- Pairwise cannot submit zero, one, duplicate, or more than two IDs.
- Combine All is explicit and never runs on workflow completion or subgraph arrival.
- Selection cannot cross projects.
- `target` and scan chips retain stable labels while IDs remain the contract.
- Error responses identify invalid selection without leaking other-project data.

### Verification

- Selection reducer/unit tests.
- API/message contract tests proving IDs-only payloads.
- Keyboard and refresh behavior.

---

## H3 — Wire async state, cross-highlighting, and host expansion

**Spec:** R20-12.5, R20-13.5..6
**Depends on:** H1, H2, context-widget W4/W5/W6

### Scope

- Surface job queued/running/progress/cancel/failure/draft/active status in Composer without duplicating iframe details.
- Keep selection/action state coherent during reload, project switch, cancellation, stale discard, and activation.
- Route graph/provenance selection events to relevant Temporary Subgraph Viewer chips and vice versa.
- Implement iframe request → host expansion decision → acknowledgement using existing Composer pane expansion mechanics.
- Preserve active context after refresh by asking backend/iframe source of truth.

### Acceptance criteria

- Host never reports success from a toast alone; active revision acknowledgement/source-of-truth refresh is required.
- Expansion/collapse does not remount and lose active job/revision state unnecessarily.
- Project switch cannot leak selection or context from the prior project.
- Cross-highlighting degrades safely when a source chip is no longer present.

### Verification

- State transition tests.
- Composer integration tests for refresh/project switch/cancel/expand.
- Backend-source-of-truth assertion after activation.

---

## H4 — Add host protocol and Composer regression coverage

**Spec:** R20-13, R20-14.6
**Depends on:** H1..H3, context-widget W7

### Scope

- Add end-to-end host harness/Composer tests for handshake, selection, Pairwise, Combine All, progress, cancel, held draft, active result, cross-highlight, theme, refresh, and expansion.
- Cover loading, empty, error, invalid selection, keyboard, and unavailable iframe.
- Verify existing workflow and Temporary Subgraph Viewer behavior is not regressed.
- Document host configuration and protocol troubleshooting.

### Acceptance criteria

- Tests inspect payloads and prove no filesystem path, graph body, or BRMS credential is sent.
- Persistence is checked after refresh against backend active revision.
- Unsupported protocol versions and origins have explicit states.
- Build/lint and relevant Composer regressions pass.

### Verification

- Unit/contract/build/browser suites.
- Static payload/secret/path scan.
