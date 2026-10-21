# SPEC-020 — GoRules Project Context

**Status:** Planned
**Mode:** Development
**Primary repo:** `brettforbes/spiderfeet`
**UI repos:** `brettforbes/widget-context-gorules`, `brettforbes/spiderfeet-widget`
**Seed:** `.seed/21_Create_Context_GoRules.md`
**Agent plan:** `.governance/project/SPEC020_AGENT_PLAN.md`
**Issue index:** `.governance/project/SPEC020_ISSUE_INDEX.md`

## 1. Problem

Workflow steps produce temporary semantic subgraphs that are intentionally narrow views of the same project. The current project-context merge is append-unique by instance ID and cannot identify semantically equivalent records, reconcile intrinsic hierarchy, promote a minimally known `SYSTEM`, preserve rule-level provenance, or replay a merge against a pinned policy version.

The production source is the Temporary Subgraph Viewer and its backend-owned temporary-subgraph records. Files under `.temp/gorules_temp_exports` exist only as a development and test golden corpus; they are not a production storage or transport contract.

## 2. Outcome

Users select temporary subgraphs in Composer and explicitly invoke Pairwise Combine or Combine All. FastAPI resolves the selected IDs from the authoritative project-scoped temporary-subgraph store, runs a deterministic merge orchestrator whose policy decisions come from a pinned GoRules release, and persists an immutable context revision plus full provenance. A dedicated React iframe provides Rules, Combined Graph, and Provenance views.

## 3. Architectural boundaries

- FastAPI owns operand loading, normalization, candidate indexing, deterministic traversal, graph mutation, invariant checks, async jobs, persistence, revision activation, and replay.
- GoRules owns versioned, user-editable merge, classification, hierarchy, conflict, and hold policy over normalized events.
- The browser never receives BRMS credentials and never supplies authoritative graph payloads.
- Production merge requests contain project/workflow scope and temporary-subgraph IDs only. Filesystem paths are forbidden.
- TypeDB remains authoritative for temporary subgraphs, project-context metadata/current materialization, and semantic relationships.
- Large immutable snapshots and traces may use a content-addressed artifact store whose hashes and references are authoritative in TypeDB.

## 4. Requirements

### R20-01 — Production operand contract

1. Pairwise merge accepts exactly two distinct `temporary_subgraph_id` values belonging to the selected project.
2. Combine All accepts the explicit selected ID set; it does not discover files or accept client-supplied graph bodies.
3. FastAPI resolves operands through the existing temporary-subgraph persistence seam, snapshots their stored payloads at job start, and records canonical hashes.
4. Missing, stale, duplicated, or cross-project IDs fail before BRMS evaluation.
5. `.temp/gorules_temp_exports` is test/development input only and cannot be referenced by runtime API, iframe messages, merge jobs, or persisted revisions.

### R20-02 — MECE semantic union

1. The result is mutually exclusive and collectively exhaustive over semantic records.
2. Every source occurrence maps to exactly one retained final record or one explicit retained hold.
3. Equivalence is semantic, not raw-literal-only:
   - global normalized values where valid, including IP, MAC, and FQDN;
   - parent-scoped compound keys for categories, transport, ports, services, and similar contained entities;
   - observation identity for scan records and source findings;
   - evidence-resolved grouping for `SYSTEM`, `HOST`, `DEVICE`, and `CDN`.
4. Same host + transport + port fuses; the same port number on different hosts remains separate.
5. No source record or relationship may be silently dropped.

### R20-03 — Address and system correlation

1. IPv4 and IPv6 use one address-family-neutral contract.
2. Same normalized address inside one workflow execution is strong candidate evidence, not unconditional identity.
3. Different addresses group only with strong linking evidence such as an in-scope MAC match or explicit same-system assertion.
4. Address-only or address-plus-MAC evidence remains `SYSTEM`.
5. Hostname-only evidence remains `DOMAIN_NAME`; it does not synthesize a system.
6. Correlation across later workflow executions requires stronger evidence than an address match.

### R20-04 — Classification and retyping

1. GoRules classifies normalized evidence using reviewed ontology-derived tables.
2. Rich evidence may retype `SYSTEM` to `HOST`, `DEVICE`, or `CDN`.
3. Retyping creates the appropriate new typed `nugget_instance_id`; no separate stable context entity ID is introduced.
4. Provenance records every old-to-new ID remap and contributing assertion.
5. Incompatible specific classifications enter `hold`; latest-write and fixed-precedence resolution are forbidden.
6. One-off operator resolution applies only to the revision and may optionally create a draft reusable rule proposal.

### R20-05 — Hierarchy reconciliation

1. Company identity uses canonical company name plus reviewed aliases or stronger identifiers; ambiguous name-only matches enter `hold`.
2. Domain identity uses normalized FQDN/IDNA rules.
3. Company → domain → endpoint is a navigation hierarchy represented as a DAG, not a strict tree.
4. One endpoint may have multiple supported domain/company parents.
5. Rules may synthesize missing hierarchy nodes or edges only when evidence supports them.
6. Every synthesized node/edge is marked inferred in provenance with its supporting evidence and rule decision.
7. Original scan heads and all distinct time-varying observations remain available and connect to fused entities.

### R20-06 — Convergence

1. `A + B` and `B + A` produce the same canonical graph hash.
2. `(A + B) + C` and `A + (B + C)` converge to the same canonical graph hash for the same source set and rule release.
3. Graph hashing excludes layout and non-semantic ordering.
4. Evaluation sequence may differ, but provenance must record it without changing canonical semantics.

### R20-07 — GoRules rule lifecycle

1. Rule packs consist of generic identity/hierarchy/classification decisions, per-tool evidence mappings, and pair-specific overrides only where required.
2. Initial validated tool mappings are NetDiscover, Nmap, Nerva, Subfinder, and Nuclei.
3. httpx and Katana are extension targets and cannot be claimed validated in this release.
4. Ontology documents inform reviewed rules ahead of time; runtime Markdown parsing or automatic rule publication is forbidden.
5. Canonical JDM seeds/exports are version controlled; pinned BRMS releases are runtime authority.
6. Draft rules use branches, simulation, and explicit release activation.
7. Every rule decision has match, boundary, clean-miss, and invalid-input simulator evidence.

### R20-08 — Local BRMS platform

1. Development includes a Docker Compose stack with `gorules/brms`, PostgreSQL 12+, persistent volumes, health checks, and startup ordering.
2. A Windows script starts Docker Desktop when necessary, waits for the engine, starts the stack, and verifies `/api/health`.
3. Secrets and `LICENSE_KEY` use untracked environment configuration; only redacted examples are committed.
4. Lack of a self-hosted GoRules license is a tracked blocker. BRMS validation cannot be claimed without it.
5. A narrow typed backend client is validated against `.temp/brms.json` for health, projects/documents, branches/commits, simulation, releases/environments, trace evaluation, runs/cancellation, and tokens needed by the service.

### R20-09 — Async merge jobs

1. Pairwise and Combine All run as asynchronous backend jobs with status, progress, cancellation, and resumable result retrieval.
2. The job pins operand hashes, normalizer/orchestrator version, and GoRules release before evaluation.
3. BRMS outage, timeout, or invalid output fails closed; append-unique fallback is forbidden.
4. A stale job whose parent context is no longer current creates no context revision, but retains an auditable discarded-job record.
5. A valid, non-stale revision with no holds activates atomically.
6. A revision containing holds is saved as non-current draft and leaves the prior current context unchanged.

### R20-10 — Immutable revisions and persistence

1. Every accepted combine creates an immutable project-context revision with parent links, source set, hashes, rule pin, graph, ledger, status, and timestamps.
2. The active project-context pointer/materialization remains optimized for reads.
3. Prior revisions support rollback without mutation.
4. Persistence reload must reproduce the active graph, revision ancestry, holds, and provenance references.

### R20-11 — Provenance and replay

1. Provenance consists of a clean context graph plus an append-only ledger.
2. The ledger maps source node/edge occurrences through candidate, rule decision/row, mutation, inference, remap, hold, and final node/edge.
3. Users can navigate bidirectionally from source to final result and from final result back to every source and rule trace.
4. Exact replay uses original source snapshots, normalizer/orchestrator version, and pinned rule release and compares canonical hashes.
5. Re-evaluation under another released rule version creates a new revision.
6. Replay mismatch never rewrites history; accepted correction creates a linked corrective revision.

### R20-12 — Context iframe

1. `widget-context-gorules` is rebuilt as a React application around the official `@gorules/jdm-editor`.
2. It provides BRMS Rules, Combined Graph, and Provenance panes.
3. One pane is active at normal/full size; the other two are icon-summary cards. Combined Graph is initially active.
4. Rules summary reports defined and fired counts; graph summary reports node/edge counts; provenance summary reports revisions, decisions, changes, and holds.
5. Full mode requests host expansion and handles acknowledgement; it does not seize browser fullscreen.
6. The widget supports standalone and embedded modes through one versioned, origin-checked protocol.
7. A compatibility spike precedes enabling WASM editor features; backend simulation remains authoritative.

### R20-13 — Composer integration

1. The existing Temporary Subgraph Viewer is the production selection surface.
2. Pairwise Combine is enabled only for exactly two eligible selections.
3. Combine All is an explicit user action over the selected/available project set; no continuous implicit recompute occurs.
4. Host-to-iframe/backend messages carry IDs and scope only, never filesystem paths or graph payload copies.
5. The context iframe replaces the empty Project Context Viewer canvas while preserving Composer expansion, theme, refresh, and project navigation behavior.
6. Host and iframe support request acknowledgement, async state, cancellation, active revision, and cross-highlighting.

### R20-14 — Golden corpus and verification

1. The five exports under `.temp/gorules_temp_exports` are immutable development/test fixtures only.
2. Tests load them through fixture adapters or seeded temporary-subgraph persistence and then exercise the same ID-based service/API path as production.
3. No separate file-based production merge path may exist.
4. Coverage includes pairwise, Combine All, MECE, parent scoping, promotion, conflict holds, inferred DAG edges, scan heads, convergence, BRMS failure, stale jobs, persistence reload, exact replay, corrective revision, and newer-rule re-evaluation.
5. Synthetic cases cover IPv6, shared/anycast CDN addresses, conflicting MACs, multiple addresses for one system, and ambiguous company aliases.
6. Cross-repo browser acceptance verifies selection-button initiation, all pane modes, bidirectional provenance, hold resolution, cancellation, refresh, and host expansion.

## 5. Non-goals

- Runtime merge from `.temp` files or arbitrary browser-supplied graphs.
- Automatic merge after every workflow step or workflow completion.
- Cross-project temporary-subgraph combination.
- Replacing TypeDB with filesystem storage.
- Treating raw `nugget_instance_id` equality as semantic identity.
- Making GoRules traverse or mutate full graphs.
- Validating httpx/Katana policy without fixtures and explicit follow-up requirements.
- Silently resolving incompatible specific classifications.

## 6. Release gates

1. SPEC-020 issues and dependency graph approved.
2. GoRules license supplied and local BRMS health proven, or affected issues remain explicitly blocked.
3. Backend contract/unit/integration suites pass with direct evidence.
4. Golden corpus reaches all expected canonical hashes through seeded temporary-subgraph IDs.
5. All three repository builds and contract tests pass.
6. GOV-08 operator review classifies every UI scenario and tracks every non-validated result.
