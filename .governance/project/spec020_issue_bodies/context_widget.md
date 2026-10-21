# SPEC-020 GitHub issue bodies — `brettforbes/widget-context-gorules`

Canonical spec: `brettforbes/spiderfeet/.governance/specs/SPEC-020-gorules-project-context.md`.

After W0, every story branches from `develop`, targets `develop`, and follows the issue visibility/evidence rules installed by W0.

---

## Epic W — React Context GoRules iframe

**Spec:** R20-12
**Outcome:** A standalone and embeddable React iframe with Rules, Combined Graph, and Provenance panes, backed only by FastAPI application APIs.

### Guardrails

- Never call GoRules directly from the browser or store BRMS tokens.
- Never accept filesystem paths as operands.
- Never treat client graph payloads as authoritative.
- One active pane; two icon-summary panes; Combined Graph initially active.

---

## W0 — Bootstrap governance and integration branch

**Spec:** Governance prerequisite
**Depends on:** none

### Problem

The repository is an ungoverned template on `main`, while all later SPEC-020 work requires issue-scoped branches, `develop`, tests, and durable project intent.

### Scope

- Add VibeGov-compatible `AGENTS.md`, project intent, SPEC-020 binding, git workflow, issue pickup, PR template, test expectations, continuity scaffolding, and mirrored rules appropriate to this repo.
- Establish `develop` from `main` through the governed path and document branch protection expectations.
- Update package/repository identity from template naming without rebuilding product UI yet.
- Record current prototype deficiencies as superseded baseline, not product bugs to fix independently.

### Acceptance criteria

- New agents can locate canonical cross-repo spec and issue index.
- Normal work flow is `issue branch from develop → PR to develop`.
- Commit policy remains operator-controlled.
- Governance bootstrap verification is documented.

### Verification

- Markdown/link/structure checks.
- Git branch and PR workflow review.

---

## W1 — Rebuild shell in React and spike official JDM editor

**Spec:** R20-12.1, R20-12.7
**Depends on:** W0

### Scope

- Replace the broken vanilla prototype entry with a React application shell while retaining useful Bootstrap/D3 assets only where justified.
- Integrate `@gorules/jdm-editor` in an isolated Rules pane.
- Test editor CSS, resize, iframe focus, keyboard interaction, and WASM initialization.
- Test required COOP/COEP/CORP/CORS headers both standalone and inside the Composer origin/port arrangement.
- Make backend simulation authoritative even if WASM enhancement is disabled.
- Resolve the existing port collision with `spiderfeet-widget`.

### Acceptance criteria

- Production build renders the React shell and editor.
- Compatibility decision is evidence-backed: full WASM enabled safely or explicitly deferred with basic editor functional.
- No missing sample JSON or nonexistent DOM mount remains in startup path.
- No Composer-wide header change is made without a documented compatibility result.

### Verification

- Build/lint.
- Standalone browser smoke.
- Embedded compatibility evidence.

---

## W2 — Define versioned embed protocol and standalone API shell

**Spec:** R20-12.5..6, R20-13.4
**Depends on:** W1

### Scope

- Define protocol version, origin allowlist, handshake, request IDs, acknowledgements, errors, and capability negotiation.
- Host messages: set project/workflow scope, selected temporary-subgraph IDs, theme, active pane, expansion acknowledgement, refresh.
- Child messages: ready, request combine pair/all, cancel, request expansion, selection/cross-highlight, revision/hold state.
- Carry IDs/scope only; forbid graph bodies, local paths, and credentials.
- Add standalone configuration that uses the same FastAPI endpoints and contracts.

### Acceptance criteria

- Wrong origin/version is rejected visibly.
- Duplicate request IDs are idempotent or rejected deterministically.
- Standalone and embedded modes share application state/actions.
- Message schemas have unit tests and written examples.

### Verification

- Protocol unit/contract tests.
- Host harness handshake smoke.

---

## W3 — Implement BRMS Rules pane and release workflow

**Spec:** R20-07, R20-12.2..4
**Depends on:** W2, backend A3

### Scope

- Browse repository/BRMS decision documents through FastAPI.
- Load/edit a draft branch, save draft, run required simulator cases, display node/row traces, commit, create/publish release, and request explicit activation.
- Display active release/commit/environment and seed-drift status.
- Keep autosave/draft changes non-authoritative.
- Show icon summary counts for documents/rules and fired instances for selected revision.

### Acceptance criteria

- No BRMS URL/token is exposed to the widget.
- Activation is impossible until required simulator cases pass.
- Read-only mode works when user/service capability denies editing.
- Active runtime pin remains unchanged after draft save.

### Verification

- Component and API-contract tests.
- Branch/simulation/release UI smoke with fake backend.
- Live proof when licensed.

---

## W4 — Implement Combined Graph pane and pane modes

**Spec:** R20-12.2..5
**Depends on:** W2, backend D2

### Scope

- Render active/draft context graph from FastAPI with stable selection and efficient large-graph behavior.
- Default Combined Graph active; Rules and Provenance icon sized.
- Implement active-pane switching, normal mode, full-within-widget mode, and host expansion request/acknowledgement.
- Show node/edge counts, revision status, hold count, and inferred/observed distinction.
- Preserve viewport/selection across pane switches and refresh where valid.

### Acceptance criteria

- No graph is constructed from browser-held temporary payloads.
- Large golden Nuclei graph remains interactive within agreed performance budget.
- Inferred elements are visually distinguishable without changing canonical graph data.
- Host denial of expansion leaves a usable widget state.

### Verification

- Component tests.
- Performance fixture smoke.
- Visual/responsive/keyboard checks.

---

## W5 — Implement Provenance and revision pane

**Spec:** R20-11, R20-12.2..4
**Depends on:** W4, backend D6

### Scope

- Display revision DAG, selected revision metadata, source set/hashes, rule pin, decisions, mutations, inferences, remaps, holds, and replay outcomes.
- Implement source → decision → final and final → decision → source navigation.
- Cross-highlight selected final graph elements and provenance paths.
- Lazily request detailed traces to avoid loading all trace content.
- Show icon summary for revisions, decisions fired, changes, and holds.

### Acceptance criteria

- Every displayed final element can request its complete lineage.
- Retyping shows old/new IDs and reason.
- Inferred hierarchy shows evidence and matched rule.
- Missing/corrupt trace artifacts show integrity errors, not empty success.

### Verification

- Component tests with representative ledger fixtures.
- Bidirectional navigation integration tests.
- Accessibility review of graph alternative/detail view.

---

## W6 — Implement async jobs, holds, replay, and correction UI

**Spec:** R20-09, R20-11, R20-12
**Depends on:** W3, W4, W5, backend D4/D5/D6

### Scope

- Show queued/running phase progress, cancellation, failure, stale discard, draft hold, and active result.
- Resume status after reload/reconnect.
- Provide hold inspection and one-off resolution; offer optional draft rule proposal without auto-release.
- Provide exact replay and re-evaluate-under-release as distinct actions.
- Display replay mismatch and corrective revision flow without rewriting original.

### Acceptance criteria

- Cancel never appears as successful context activation.
- Holds cannot replace current context until resolved.
- Replay and re-evaluation labels/actions are unambiguous.
- Retry creates a new job with visible pins.

### Verification

- State-machine component tests.
- Reconnect/cancel/hold/replay integration scenarios.

---

## W7 — Add widget contract, accessibility, and build gates

**Spec:** R20-12, R20-14.6
**Depends on:** W3..W6

### Scope

- Add protocol compatibility suite, API mock integration, production build, lint/type checks, and browser scenarios.
- Cover keyboard pane switching, editor focus, graph alternative details, hold forms, loading/empty/error states, standalone mode, and host expansion acknowledgement.
- Document local startup, environment configuration, embed protocol, and known WASM/header decision.

### Acceptance criteria

- All meaningful controls are keyboard reachable with visible focus.
- Protocol and API incompatibility fail visibly.
- Build artifacts contain no token/secret or local fixture path.
- Evidence distinguishes direct behavior proof from surrogate build proof.

### Verification

- Unit/contract/build/browser suites.
- Bundle secret/path scan.
