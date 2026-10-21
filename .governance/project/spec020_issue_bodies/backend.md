# SPEC-020 GitHub issue bodies — `brettforbes/spiderfeet`

Copy each section into one GitHub issue. After publication, add its URL to `SPEC020_ISSUE_INDEX.md`.

Every story follows `.governance/project/SPEC020_AGENT_PLAN.md`: branch from `develop`, PR to `develop`, issue comments at start/blocker/verification/final, and direct evidence in the PR.

---

## G0 — Land canonical planning and issue package

**Spec:** Governance prerequisite
**Depends on:** none

### Problem

The canonical SPEC-020 specification, lesser-agent plan, issue index, publication metadata, issue bodies, and continuity checkpoint must be available from `develop` before clean worktrees can resolve issue links.

### Scope

- Land only SPEC-020 planning/governance artifacts and the idempotent issue publisher.
- Reconcile all published issue URLs, parent/dependency links, and board state.
- Exclude every pre-existing product, seed, test, temporary export, and widget change.

### Acceptance criteria

- Canonical SPEC-020 links resolve from `develop`.
- Exactly the documented SPEC-020 artifacts are committed.
- Issue/index counts and statuses match live GitHub state.
- Markdown/lint and publisher syntax checks pass.

### Verification

- `python -m py_compile .tasks/publish_spec020_issues.py`
- No `TBD` or `planned` issue rows in the index.
- Diff review proves no unrelated files are included.

---

## Epic A — Local GoRules platform

**Spec:** R20-07, R20-08
**Outcome:** A reproducible local GoRules BRMS/PostgreSQL platform and a backend-only client supporting reviewed rule authoring, release, and traced evaluation.

### Acceptance criteria

- A1–A3 are complete with linked PR and verification evidence.
- No secret or license value is committed.
- Live validation is explicitly blocked until a self-hosted license is supplied.
- Browser clients never receive BRMS credentials.

---

## A1 — Provision Docker Desktop + GoRules BRMS/PostgreSQL

**Spec:** R20-08.1..4
**Depends on:** none

### Problem

Docker Desktop is installed, but the project has no reproducible BRMS/PostgreSQL stack or Windows startup workflow. GoRules requires PostgreSQL 12+, persistent state, a license, secrets, and outbound license validation.

### Scope

- Add `deploy/gorules/compose.yaml` with `gorules/brms` and a dedicated PostgreSQL service.
- Add persistent named volumes, database and BRMS health checks, dependency ordering, restart policy, and a non-conflicting host port.
- Add a committed redacted `.env.example`; ignore the real local environment file.
- Add a PowerShell entry point that starts Docker Desktop if the engine is unavailable, polls engine readiness, starts the stack, and verifies BRMS `/api/health`.
- Document license acquisition as a blocker; never invent or embed a key.

### Non-goals

- SpiderFeet application integration.
- Rule/document creation.
- Production deployment topology.

### Acceptance criteria

- `docker compose config` validates without secret material.
- PostgreSQL data survives stack restart.
- Startup script is idempotent and reports Docker, PostgreSQL, BRMS, and license/readiness failures distinctly.
- No existing SpiderFeet Compose service/port is broken.
- Without a license, the exact blocked health/startup state is documented honestly.

### Verification

- Compose config validation.
- PowerShell syntax/static check.
- Live startup/health when a license becomes available; otherwise classify live BRMS proof `Blocked`.
- Secret scan over changed files.

---

## A2 — Add typed backend BRMS client

**Spec:** R20-08.5, R20-09.3
**Depends on:** A1

### Problem

The backend needs a narrow, testable client for the BRMS API described by `.temp/brms.json`; generic raw HTTP calls would scatter authentication and error semantics.

### Scope

- Define configuration for base URL, project/environment/release identifiers, token source, timeouts, retries, and TLS behavior.
- Implement only required operations: health, documents, branches/commits, simulation, releases/environments, evaluate with trace, runs/cancel, and token metadata where required.
- Model request/response contracts with typed validation.
- Centralize `X-Access-Token`/bearer handling in the backend.
- Normalize network, auth, timeout, invalid-contract, and BRMS decision errors into explicit service exceptions.
- Use deterministic fake-server contract tests generated/checked against `.temp/brms.json`.

### Non-goals

- Exposing tokens to browser clients.
- Wrapping every endpoint in the 1 MB OpenAPI document.
- Merge orchestration.

### Acceptance criteria

- No caller handles raw auth headers.
- Invalid BRMS JSON fails validation and cannot be treated as a valid decision.
- Evaluation supports `trace: true` and preserves matched-row trace fields.
- Retry behavior is bounded and excludes unsafe mutation retries unless idempotency is proven.
- Unit/contract tests cover success, auth denial, timeout, invalid response, and health failure.

### Verification

- Targeted client unit/contract suite.
- Type/lint checks.
- Live `/api/health` and one safe simulation when licensed; otherwise live proof remains `Blocked`.

---

## A3 — Implement branch/simulate/release/evaluate lifecycle service

**Spec:** R20-07.4..7, R20-08.5
**Depends on:** A2

### Problem

Rule edits must not alter runtime policy until simulator cases pass and a release is explicitly activated.

### Scope

- Add backend services for loading repository JDM seeds, creating/updating a draft BRMS branch, simulating cases, committing, creating/publishing a release, and selecting the active environment/release.
- Record document path, branch/commit/release/environment IDs and hashes.
- Reject activation unless all required simulator classes pass.
- Keep release activation explicit and auditable.
- Expose application-facing methods; HTTP routes belong to the relevant API story.

### Non-goals

- Automatic publication from ontology Markdown.
- UI implementation.
- Merge execution.

### Acceptance criteria

- Draft save cannot change active runtime release.
- Required cases are `match`, `boundary`, `clean_miss`, and `invalid_input`.
- Release pin is stable and usable by evaluation/replay.
- Repository seed drift versus released JDM is detectable.
- Tests cover failed simulation, partial suite, publish failure, and successful activation.

### Verification

- Service tests with fake BRMS.
- Live branch → simulate → release → traced evaluate when licensed.
- Audit record inspection.

---

## Epic B — Semantic identity + JDM rules

**Spec:** R20-02..07
**Outcome:** A deterministic candidate layer plus reviewed GoRules policy that produces MECE, convergent merge actions for the first five tools.

### Acceptance criteria

- B1–B5 complete.
- Policy decisions never depend on filesystem paths or canvas layout.
- httpx/Katana remain documented extension targets, not validated mappings.

---

## B1 — Define semantic records, normalizers, and identity strategies

**Spec:** R20-02, R20-03, R20-05
**Depends on:** none

### Scope

- Define normalized merge-event and decision schemas.
- Implement IPv4/IPv6, MAC, FQDN/IDNA, company-name/alias, relation, and source normalization.
- Define identity strategies by nugget semantics: global normalized, parent-scoped compound, observation-unique, evidence-resolved.
- Define parent-scoped keys for categories, transport, port, service, and equivalent contained entities.
- Define source occurrence IDs distinct from graph instance IDs.
- Document address evidence thresholds and workflow-execution boundary.

### Non-goals

- Deciding policy outcomes.
- Mutating graphs.
- Global literal-value dedupe.

### Acceptance criteria

- Same host/TCP/443 yields one port key; different hosts/TCP/443 yield two.
- Hostname-only input yields a domain record, not a system candidate.
- IPv4 and IPv6 normalize deterministically.
- Equivalent FQDN/IDNA forms normalize consistently.
- Every identity strategy has unit tests for match and non-match.

### Verification

- Pure unit tests with traceability to R20-02/03/05.
- Property tests for normalization idempotence where practical.

---

## B2 — Build candidate index and MECE occurrence accounting

**Spec:** R20-02, R20-03, R20-06
**Depends on:** B1

### Scope

- Index normalized nodes, edges, ancestry, sources, addresses, MACs, domains, and parent-scoped keys.
- Generate compact candidate events for GoRules; never send complete graphs or canvas payloads.
- Track every source occurrence through candidate generation.
- Implement confidence inputs for same-address, same-MAC, explicit same-system, contradictory MAC, shared CDN/anycast, and missing anchor evidence.
- Add invariant checks that each occurrence has one terminal disposition: retained mapping or hold.

### Non-goals

- Applying graph mutations.
- Embedding policy thresholds in Python.

### Acceptance criteria

- Candidate generation is deterministic under input ordering.
- Same address is candidate evidence, not forced fusion.
- Different addresses require strong-link evidence to share a candidate group.
- No occurrence is duplicated or lost.
- Candidate batches exclude `canvas` and remain bounded/configurable.

### Verification

- Unit/property tests for ordering and occurrence conservation.
- Fixture-scale payload-size assertion.

---

## B3 — Author core identity, hierarchy, and classification JDM

**Spec:** R20-03..07
**Depends on:** B1

### Scope

- Add repository JDM seeds for identity confidence/action, hierarchy placement/inference, SYSTEM classification/retyping, descriptor attachment, edge handling, and hold outcomes.
- Use decision tables and ZEN expressions; avoid function nodes unless documented as unavoidable.
- Emit strict typed actions such as `merge`, `insert`, `attach`, `infer`, `retype`, `separate`, and `hold`.
- Handle conflicting specific classifications with `hold`.
- Include company alias ambiguity and missing-anchor behavior.

### Non-goals

- Tool-specific evidence extraction.
- Whole-graph traversal in JDM.
- Automatic release.

### Acceptance criteria

- Every table has a final explicit catch-all.
- No unknown action can pass output validation.
- Rules are independent of left/right operand order.
- Retyping returns target type and reason/evidence but not backend-generated IDs.
- Four simulator classes exist per decision document.

### Verification

- Local JDM structural validation.
- Simulator fixtures with expected action and matched row.
- Live BRMS simulation when licensed.

---

## B4 — Add five-tool evidence mappings and exceptional overrides

**Spec:** R20-07.1..3, R20-07.7
**Depends on:** B3

### Scope

- Map NetDiscover, Nmap, Nerva, Subfinder, and Nuclei ontology output into normalized evidence used by B3.
- Derive mappings from each `modules_v2/content/<tool>/graph_structure.md`.
- Add pair-specific override documents only where generic policy cannot represent a proven semantic difference.
- Cover minimal NetDiscover SYSTEM, Nmap/Nerva endpoint/service overlap, Subfinder hierarchy, and Nuclei attachment.
- Record httpx/Katana extension contracts without claiming mappings validated.

### Acceptance criteria

- Tool source changes evidence, not core traversal.
- NetDiscover IP/MAC-only observations remain SYSTEM.
- Nmap/Nerva evidence can promote with explicit matched rule evidence.
- Subfinder domains do not synthesize hosts without endpoint evidence.
- Nuclei findings attach without creating duplicate endpoint entities.
- Every mapping has four simulator classes.

### Verification

- Tool-level mapping tests.
- Cross-tool simulator matrix.
- Review against all five graph-structure docs.

---

## B5 — Enforce repository seed to BRMS release gate

**Spec:** R20-07.4..7
**Depends on:** A3, B4

### Scope

- Validate repository JDM seeds/exports before sync.
- Compare seed hash, BRMS document/commit, release, and active environment.
- Prevent activation with missing simulator evidence, uncommitted drift, or invalid output schema.
- Persist release metadata needed by merge jobs and replay.
- Provide an operator command/report for draft sync and release activation.

### Acceptance criteria

- A merge job can pin exactly one immutable rule release.
- Active release cannot change through editor autosave.
- Drift is visible and blocks release.
- Activation report lists documents, simulator outcomes, commit, release, and environment.

### Verification

- Fake-BRMS release gate tests.
- Live release activation/retrieval when licensed.

---

## Epic C — Revisions + provenance persistence

**Spec:** R20-08..11
**Outcome:** Immutable context history, durable job state, canonical materialization, and a complete source-to-result ledger.

---

## C1 — Add revision, merge-job, hold, and active-pointer schema

**Spec:** R20-09, R20-10
**Depends on:** none

### Scope

- Extend TypeDB schema and CRUD contracts for merge jobs, immutable context revisions, parent links, source references/hashes, rule pins, status, holds, corrective links, and active pointer.
- Define statuses for queued/running/cancelling/cancelled/failed/discarded/draft/active/superseded.
- Provide idempotent schema delta/migration and compatibility reads for existing single project-context rows.

### Acceptance criteria

- Immutability is enforced by service contract/tests.
- One project has at most one active revision pointer.
- Existing projects without revisions still return an empty/legacy-compatible context.
- Stale/discarded jobs are representable without a revision.

### Verification

- Schema delta tests.
- CRUD round-trip and uniqueness tests.
- Migration compatibility test.

---

## C2 — Add content-addressed snapshot and trace storage

**Spec:** R20-01.3, R20-10, R20-11
**Depends on:** C1

### Scope

- Define a storage interface for immutable operand snapshots, result graphs, BRMS traces, and ledgers.
- Implement content-addressed hashing, atomic write, verified read, deduplication, and corruption detection.
- Store hash/reference/size/media metadata in TypeDB.
- Keep test storage isolated and deterministic.

### Non-goals

- Using golden fixture files as runtime operands.
- Making local paths part of public APIs.

### Acceptance criteria

- Same content produces one artifact hash.
- Partial writes cannot become visible.
- Hash mismatch is a hard integrity error.
- Deleting/altering an operand after job start cannot alter the pinned snapshot.

### Verification

- Unit tests for dedupe, corruption, atomicity, and reload.
- Integration round-trip through TypeDB metadata.

---

## C3 — Implement append-only provenance ledger

**Spec:** R20-04.3..6, R20-05.5..7, R20-11.1..3
**Depends on:** B1, C1, C2

### Scope

- Define ledger events for source intake, normalization, candidate creation, BRMS decision/row/trace, mutation, inference, ID remap, hold, operator resolution, final mapping, and activation.
- Link final nodes/edges to all source node/edge occurrences.
- Record old/new typed IDs for SYSTEM retyping.
- Record inferred hierarchy evidence.
- Support indexed queries in both directions.

### Acceptance criteria

- Ledger is append-only and hashable.
- Every source occurrence has a terminal final mapping or hold.
- Every final node/edge can enumerate all sources and decisions.
- Operator one-off resolution is distinguishable from a reusable released rule.

### Verification

- Ledger invariant tests.
- Bidirectional query tests.
- Retype and inference provenance examples.

---

## C4 — Implement canonical materialization, activation, and rollback

**Spec:** R20-06, R20-09.4..6, R20-10
**Depends on:** C3

### Scope

- Canonically normalize/sort semantic graph content and compute layout-independent hashes.
- Persist immutable revisions and update current project-context materialization atomically.
- Auto-activate valid non-stale hold-free revisions.
- Keep held revisions draft and prior current unchanged.
- Support rollback by active-pointer change without rewriting revisions.
- Record discarded stale jobs without creating a revision.

### Acceptance criteria

- Equivalent graph ordering/layout produces one hash.
- Failed activation cannot leave pointer/materialization split.
- Rollback survives reload.
- Revision ancestry remains immutable.

### Verification

- Transaction/failure-injection tests.
- Hash normalization tests.
- Persistence reload and rollback integration tests.

---

## Epic D — Merge jobs + context APIs

**Spec:** R20-01, R20-06, R20-09..11
**Outcome:** Secure ID-only pairwise/combine-all jobs and APIs for status, provenance, holds, and replay.

---

## D1 — Resolve authoritative project-scoped operands by ID

**Spec:** R20-01, R20-13.4
**Depends on:** B1, C1

### Scope

- Add service/API request schemas containing project/workflow scope and temporary-subgraph IDs only.
- Resolve IDs using the existing temporary-subgraph persistence seam/listing.
- Validate membership, distinctness, eligibility, and current stored state.
- Snapshot canonical stored payload and hash at job creation.
- Reject graph bodies, file paths, cross-project IDs, duplicates, and missing IDs.

### Acceptance criteria

- Pairwise requires exactly two distinct eligible IDs.
- Combine All uses an explicit ID set.
- Browser-supplied graph data cannot become authoritative.
- Errors identify invalid IDs without leaking other-project data.

### Verification

- Route/service tests for valid, missing, duplicate, stale, and cross-project IDs.
- Test proving fixture paths are not accepted.

---

## D2 — Implement async pairwise merge orchestrator

**Spec:** R20-02..06, R20-09
**Depends on:** A2, B2, B3, C4, D1

### Scope

- Build deterministic phase order: normalize → index → candidate events → BRMS batches → validate actions → apply mutations → validate MECE/graph → persist revision/ledger.
- Batch compact events; never send full graphs/canvas to BRMS.
- Preserve all scan heads and observations.
- Apply parent-scoped identity, inference, retyping, and hold actions.
- Pin source hashes, code/normalizer version, and rule release.

### Acceptance criteria

- Left/right operand reversal produces the same graph hash.
- Every occurrence terminates in mapping or hold.
- Unknown/invalid BRMS actions fail closed.
- No append-unique fallback occurs.

### Verification

- Phase-level unit tests.
- Pairwise integration tests with fake BRMS.
- Direct MECE and commutativity assertions.

---

## D3 — Implement explicit Combine All with convergence proof

**Spec:** R20-06, R20-13.3
**Depends on:** D2

### Scope

- Accept an explicit project-scoped ID set.
- Use the pairwise engine/semantic accumulator; do not create a second merge implementation.
- Canonicalize fold/event order for trace reproducibility while requiring grouping-independent output.
- Record source set and evaluation order separately.

### Acceptance criteria

- No implicit run on step arrival or workflow completion.
- Permutations and representative parenthesizations converge to one graph hash.
- Duplicate input IDs fail validation.
- Pairwise result can participate as a revision operand without losing source lineage.

### Verification

- Permutation/property tests.
- Golden multi-subgraph convergence test.

---

## D4 — Add job progress, cancellation, stale handling, and fail-closed errors

**Spec:** R20-09
**Depends on:** D2, C4

### Scope

- Add create/status/progress/cancel/result API behavior.
- Define phase and item-count progress.
- Support cooperative cancellation between safe phase/batch boundaries.
- Detect parent-context staleness before activation.
- Preserve failed/cancelled/discarded job audit details.
- Normalize BRMS auth/network/timeout/invalid-contract errors without fallback.

### Acceptance criteria

- Cancellation never activates a partial graph.
- Stale completion creates no context revision.
- Retry is explicit and uses newly pinned inputs.
- API states are monotonic and resumable after client reconnect.

### Verification

- State-machine unit tests.
- Cancellation and stale-race integration tests.
- BRMS failure matrix.

---

## D5 — Add exact replay, newer-rule re-evaluation, and corrective revisions

**Spec:** R20-10, R20-11.4..6
**Depends on:** D2, D3, D4, C4

### Scope

- Exact replay loads immutable source snapshots and original version/rule pins.
- Compare canonical output and ledger hashes.
- Re-evaluation accepts a different released rule pin and creates a new revision.
- Replay mismatch preserves original history and creates diagnostic evidence.
- Accepted mismatch creates a linked corrective revision, never mutation.

### Acceptance criteria

- Exact replay is impossible if any required immutable artifact/version is unavailable and reports the exact blocker.
- Matching replay proves graph and ledger hash equality.
- Re-evaluation is clearly distinct in API/status/provenance.
- Original revisions remain byte-for-byte immutable.

### Verification

- Exact match, mismatch, missing artifact, newer release, and corrective revision tests.

---

## D6 — Add provenance query and hold-resolution APIs

**Spec:** R20-04.5..6, R20-11.1..3
**Depends on:** C3, C4, D2

### Scope

- Query revision ancestry, summaries, source→final paths, final→source paths, decision details, traces, changes, inferred facts, and holds.
- Resolve a hold with one-off `merge`, `separate`, `attach`, `retype`, or other schema-approved action.
- Optionally emit a draft rule proposal without modifying active rules.
- Re-run validation and create a child draft/active revision as appropriate.

### Acceptance criteria

- Query responses use stable revision/ledger event IDs.
- No raw secrets or unnecessary full traces leak to browser clients.
- Hold resolution is attributed and replayable.
- Draft rule proposal is never auto-released.

### Verification

- Query contract tests.
- Hold resolution integration tests.
- Authorization/data-minimization review.

---

## Epic E — Golden acceptance + operations

**Spec:** R20-14
**Outcome:** Direct proof through the production ID-based path and an operator runbook.

---

## E1 — Seed golden fixtures through temporary-subgraph persistence

**Spec:** R20-01, R20-14.1..3
**Depends on:** D1, D2

### Scope

- Treat `.temp/gorules_temp_exports` as immutable test inputs.
- Build test-only loaders that create isolated projects and authoritative temporary-subgraph records.
- Return IDs used by the same D1/D2 service and route contracts as production.
- Validate manifest completeness and fixture hashes.

### Acceptance criteria

- No production module imports fixture paths.
- Acceptance merges use IDs, not file paths or direct graph arguments.
- Fixture mutation is detected.
- Test teardown cannot affect live projects.

### Verification

- Seeder tests.
- Static search proving no runtime dependency on `.temp/gorules_temp_exports`.
- One seeded pairwise API run with fake/live BRMS as available.

---

## E2 — Verify MECE, classification, hierarchy, and convergence

**Spec:** R20-02..07, R20-14.4..5
**Depends on:** B5, C4, D3, E1

### Scope

- Define expected semantic outcomes/canonical hashes for all five projects.
- Cover parent-scoped ports/services, duplicate fusion, SYSTEM retention/promotion, specific-type conflicts, company/domain DAGs, inferred edges, scan heads, and changing observations.
- Add synthetic IPv6, shared CDN/anycast, conflicting MAC, multi-address system, and company alias cases.
- Exercise pairwise order and Combine All grouping/permutation.

### Acceptance criteria

- Every occurrence is accounted for.
- All expected hashes are stable and documented.
- Holds are expected/explicit, never accidental omissions.
- httpx/Katana are not counted as validated.

### Verification

- Acceptance suite with per-scenario requirement mapping.
- Generated evidence summary committed under project docs.

---

## E3 — Verify failure, persistence, provenance, and replay

**Spec:** R20-09..11, R20-14.4
**Depends on:** D4, D5, D6, E1

### Scope

- Exercise BRMS outage/auth/timeout/invalid action, cancel, stale parent, held draft, atomic activation, reload, rollback, exact replay, mismatch, corrective revision, and newer-release re-evaluation.
- Verify bidirectional ledger completeness and trace references.

### Acceptance criteria

- No failure path activates partial/invalid context.
- Reload preserves active context and ancestry.
- Exact replay is direct proof, not a proxy.
- Every non-verified scenario has a tracked artifact.

### Verification

- Integration suite with fault injection.
- Durable evidence report with proof-strength classification.

---

## E4 — Publish startup, rule-release, and recovery runbook

**Spec:** R20-08, R20-14
**Depends on:** I2

### Scope

- Document Docker Desktop/BRMS/PostgreSQL startup and health diagnosis.
- Document secret/license setup without secret values.
- Document JDM draft/simulate/release/activate workflow.
- Document merge job diagnosis, holds, replay, corrective revision, rollback, backup/restore, and artifact integrity checks.
- State development fixture versus production temporary-subgraph boundary prominently.

### Acceptance criteria

- A new operator can start the licensed stack and execute one seeded merge using only the runbook.
- Recovery steps never prescribe deleting immutable history.
- Every command/path matches final implementation.

### Verification

- Fresh-session runbook walkthrough.
- Link/path check.

---

## Epic I — Cross-repo release gates

**Spec:** R20-14.6
**Outcome:** Contract-complete integration, live acceptance, then operator exploratory classification.

---

## I1 — Verify cross-repo contracts

**Spec:** R20-01, R20-09..13
**Depends on:** D1..D6, W7, H4

### Scope

- Pin backend OpenAPI, iframe protocol version, and host expectations.
- Run contract tests across backend, iframe, and Composer without depending on filesystem operands.
- Verify origin checks, ID-only requests, async states, pane summaries, expansion acknowledgement, and provenance identifiers.

### Acceptance criteria

- Contract versions are compatible and documented.
- No browser message contains a local path, BRMS credential, or authoritative graph payload.
- Incompatible protocol version fails visibly.

### Verification

- Cross-repo contract suite and evidence report.

---

## I2 — Run licensed live seeded end-to-end acceptance

**Spec:** R20-08, R20-14
**Depends on:** E2, E3, I1, valid self-hosted GoRules license

### Scope

- Start Docker Desktop, PostgreSQL, BRMS, FastAPI, context iframe, and Composer.
- Seed golden graphs into temporary persistence.
- Select in Temporary Subgraph Viewer and invoke Pairwise/Combine All buttons.
- Validate active context persistence after refresh and exact replay against the pinned live release.

### Acceptance criteria

- The complete user path uses temporary-subgraph IDs only.
- Combined graph and provenance match backend source of truth after refresh.
- Live traces identify released JDM decisions.
- All failures/non-validated scenarios become tracked follow-up issues.

### Verification

- Browser screenshots/video where useful.
- API/DB source-of-truth checks.
- Live BRMS release and trace IDs in evidence.

---

## I3 — GOV-08 exploratory operator gate

**Spec:** R20-14.6
**Depends on:** I2, E4
**Owner:** Operator only

### Scope

Classify happy, cancel, invalid selection, empty, loading, error, keyboard/accessibility, refresh, persistence, hold resolution, replay, pane modes, host expansion, and rule-release states.

### Acceptance criteria

- Every scenario is `Validated`, `Invalidated`, `Blocked`, or `Uncovered-spec-gap`.
- Every non-validated scenario has a focused backlog artifact.
- Persistence claims are verified against backend source of truth.
- Final completeness label is recorded.

### Lesser-agent instruction

Do not execute or close this issue. Lesser agents may prepare the matrix and evidence hooks only.
