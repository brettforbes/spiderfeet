# SPEC-020 agent plan — lesser-agent execution

**Spec:** `.governance/specs/SPEC-020-gorules-project-context.md`
**Issue index:** `.governance/project/SPEC020_ISSUE_INDEX.md`
**Issue bodies:** `.governance/project/spec020_issue_bodies/`
**Seed:** `.seed/21_Create_Context_GoRules.md`

## Mission

Build the project-context combination system without inventing a file-based production path:

`Temporary Subgraph Viewer selection → ID-only host message/API → authoritative temporary-subgraph load → deterministic FastAPI orchestration → pinned GoRules decisions → immutable context revision + ledger → Context iframe`

The files under `.temp/gorules_temp_exports` are golden fixtures only. Lesser agents must not read them from production code, send their paths through browser messages, or add APIs accepting arbitrary graph payloads.

## Repository ownership

- `brettforbes/spiderfeet`: canonical spec, Docker/BRMS, identity/rules, merge engine, persistence, APIs, golden acceptance, integration gates.
- `brettforbes/widget-context-gorules`: React Rules/Graph/Provenance iframe and standalone shell.
- `brettforbes/spiderfeet-widget`: Composer iframe host, Temporary Subgraph Viewer selection/actions, host protocol and browser integration.

## Execution rules

1. One story per branch and PR; branch from that repo’s canonical integration branch only.
2. `spiderfeet` and `spiderfeet-widget`: branch from `develop`, PR to `develop`.
3. `widget-context-gorules`: W0 establishes governed `develop`; all later stories branch from and PR to `develop`.
4. Read the issue body, its R20 requirement IDs, and direct dependencies before editing.
5. Comment on the GitHub issue at start, blocker, verification, PR, and final result.
6. Do not begin a dependent story until prerequisite PRs are on the target integration branch.
7. Do not broaden scope to httpx/Katana policy, file-backed runtime merge, cross-project merge, or implicit continuous recompute.
8. A passing build is not completion. Each issue must produce the direct evidence named in its verification section.
9. Return the repository to `develop` after each landed normal-work issue.
10. Stop at operator gates; lesser agents do not self-approve GOV-08.

## Critical invariants

- Production operands are project-scoped temporary-subgraph IDs resolved by FastAPI.
- Browser and iframe never send authoritative graph payloads or local paths.
- Every source occurrence maps to one final semantic record or one retained hold.
- Port/service/category identities are parent-scoped where required.
- Same address is candidate evidence, not unconditional same-system identity.
- Pairwise merge is commutative; multi-input folding is associative after canonical normalization.
- GoRules decides policy; it does not walk or mutate whole graphs.
- BRMS errors fail closed.
- Holds do not replace the current context.
- Immutable revisions and replay evidence are never rewritten.
- Retyping adopts a new typed instance ID and records the remap.

## Dependency waves

### Wave 0 — Governance

- W0 bootstraps governance and `develop` in `widget-context-gorules`.
- Epic parent issues and story issues are created/linked in all repositories.
- No product implementation starts before W0 and issue/spec confirmation.

### Wave 1 — Foundations in parallel

- A1 local BRMS/PostgreSQL stack.
- B1 semantic identity contract.
- C1 revision/job schema.
- W1 React shell and JDM editor compatibility spike, after W0.
- H1 context iframe host shell may begin only after W2 protocol is fixed; do not pre-invent messages.

The GoRules self-hosted license is an explicit blocker for live A1/A2/A3/B5 verification. Work that uses mocks/contracts may continue, but no live-BRMS claim is allowed.

### Wave 2 — Backend and iframe contracts

- A2 after A1 contract shape; A3 after A2.
- B2 after B1.
- C2 after C1; C3 after B1+C1+C2.
- D1 after B1+C1.
- W2 after W1.
- B3 can proceed after B1 with simulator fixtures.

### Wave 3 — Merge behavior

- B4 after B3.
- B5 after A3+B4.
- C4 after C3.
- D2 after A2+B2+B3+C4+D1.
- D3 after D2.
- D4 after D2+C4.
- W3 after W2+A3 contract.
- W4 after W2+D2 response contract.
- H1 after W2 protocol.

### Wave 4 — Provenance, replay, and host actions

- D5 after D2+D3+D4+C4.
- D6 after C3+C4+D2.
- W5 after W4+D6.
- W6 after W3+W4+W5+D4+D5+D6.
- H2 after H1+D1+D2+D3.
- H3 after H1+H2+W4+W5+W6.

### Wave 5 — Verification

- E1 after D1+D2.
- E2 after B5+D3+C4+E1.
- E3 after D4+D5+D6+E1.
- W7 after W3–W6.
- H4 after H1–H3+W7.
- I1 after backend API tests + W7 + H4.
- I2 after E2+E3+I1 and a live licensed BRMS.
- E4 after I2.
- I3 is the final operator-only GOV-08 gate.

## Recommended parallel lanes

- Lane 1: A1 → A2 → A3 → B5.
- Lane 2: B1 → B2 and B1 → B3 → B4.
- Lane 3: C1 → C2 → C3 → C4.
- Lane 4: D1 → D2 → D3/D4 → D5/D6.
- Lane 5: W0 → W1 → W2 → W3/W4/W5 → W6 → W7.
- Lane 6: H1 → H2 → H3 → H4, beginning only when its protocol/API dependencies land.
- Lane 7: E1 → E2/E3 → I1 → I2 → E4 → I3.

Parallel work is allowed only across independent lanes and only when every agent owns one issue, one branch, and one evidence bundle.

## Handoff template for every lesser agent

Include in the final issue comment and PR:

- Intent and R20 requirement IDs.
- Exact changed paths.
- Acceptance criteria classification: Verified, Invalidated, Blocked, Deferred, or Not applicable.
- Commands/checks and direct evidence.
- Scenario classes covered, including failure/empty/cancel/persistence where relevant.
- Proof strength: direct, partial, or surrogate-only.
- Residual risk and linked follow-up issue.
- Confirmation that no filesystem production merge path or client graph-payload path was introduced.

## Stop conditions

Stop and mark the issue blocked when:

- the self-hosted GoRules license is required for the next direct proof and remains unavailable;
- an API/protocol dependency is not yet landed;
- a proposed identity rule would violate parent scoping, MECE mapping, or convergence;
- a change requires new nugget/relation semantics outside SPEC-020;
- live behavior contradicts the golden expectation and the intended contract is ambiguous.

Do not improvise around these boundaries. Record evidence and return the issue to the orchestrator.
