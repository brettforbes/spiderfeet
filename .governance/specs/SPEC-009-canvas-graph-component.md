# SPEC-009 — CanvasGraph: canvas-rendered, worker-offloaded nugget graph component

**Status:** Active
**Parent coordination:** follow-on to SPEC-008 (`Viz.ForceGraph` consumers: CLI Scan App Graph tab, Maps tab)
**Plan / agent playbook:** `@spiderfeet-widget/.governance/project/SPEC009_AGENT_PLAN.md`
**Issue index:** `@spiderfeet-widget/.governance/project/SPEC009_ISSUE_INDEX.md`
**Repo scope:** `spiderfeet-widget` only — no backend/`spiderfeet` changes required

## Objective

Replace the SVG-based D3 force graph (`window.Viz.ForceGraph`, `src/js/viz.force.js`) with a
canvas-rendered, Web Worker-offloaded engine, **`window.Viz.CanvasGraph`**, that scales to the
node/edge counts real CLI examination scenarios produce (thousands of nodes), and cut over both
existing consumers to it.

### Diagnosis this SPEC fixes

Investigating why the Katana `from_httpx_upside_com` CLI Profiling scenario made the browser tab
unresponsive found two stacked causes:

1. `GraphShadows.apply()` (`src/js/graph-shadows.js`) runs an O(shadowPairs × edges) nested loop
   that, for that scenario's 3,426 nodes / 11,199 edges, iterated ~50M times, blocked the main
   thread ~0.5-0.9s, and produced ~4,400 near-duplicate shadow nodes — nearly doubling total node
   count before rendering even starts.
2. `Viz.ForceGraph` then builds ~30k+ individual SVG DOM elements for that node/edge count (one
   `<g>` per node with 2-4 children, one `<line>` **and** one `<text>` per edge because
   `linkLabels: true` is hardcoded) and rewrites 6+ attributes per element on every one of D3's
   ~300 default simulation ticks — tens of millions of synchronous main-thread attribute writes.
   This is the direct cause of the "page not responding" freeze.

## Non-goals

- Suppressing or capping shadow-node duplication for extreme fan-in scenarios. The operator has
  explicitly accepted that a small number of scenarios will remain visually dense ("hairball")
  after this SPEC — the objective is *no freeze*, not *fewer shadow nodes*. R9-08 fixes the
  algorithmic complexity of `GraphShadows.apply`, not its shadow-count behavior.
- Composer, Tests, Subscriptions, or Settings panes.
- A general-purpose charting library — this stays a purpose-built graph engine for nugget graphs.
- Backend/API changes — the `graph_proposal` JSON contract from `/cli-corpus` is unchanged.

## Requirements

| ID | Requirement |
|----|-------------|
| R9-01 | `window.Viz.CanvasGraph.create(options)` canvas scaffold: same option shape as `Viz.ForceGraph.create` except a `canvas` selector (not `svg`); devicePixelRatio-aware sizing via `Viz.Core.dimensions`/`observeResize`; `d3.zoom()` bound to the canvas via a manually-applied transform; a `requestAnimationFrame` draw loop. Added to the webpack `widget.js` bundle list. |
| R9-02 | Node/link drawing parity with `Viz.ForceGraph`: icon/label-fallback rendering (via `drawImage`/`Image` cache and wrapped label text using `Viz.Core.normalizeNuggetLabel`), quarantine service rings, link stroke/dash-by-role, optional link labels — visually equivalent output for the same input graph. |
| R9-03 | Hit-testing and interactivity parity: `d3.quadtree`-backed hover/click/drag/dblclick-unpin, hover-dims-non-neighbours, tooltip — behaviourally equivalent to `Viz.ForceGraph`. |
| R9-04 | Legend and lifecycle parity: existing HTML legend keeps working unchanged; `.destroy()` fully tears down the rAF loop, listeners, Image cache, and the Web Worker. |
| R9-05 | `src/assets/workers/canvas-graph.worker.js`: classic (non-module) Web Worker running `d3.forceSimulation` (all 4 existing `viz.force.js` variants: `default`/`sparse`/`dense`/`grouped`) via `importScripts('/vendor.js')`; documented message protocol (`init`/`pin`/`unpin`/`reheat`/`destroy` in, throttled `tick` position batches out). |
| R9-06 | Main-thread integration: `CanvasGraph`'s draw loop consumes the worker's position stream instead of running physics on the main thread; `.destroy()` terminates the worker; a main-thread fallback runs the same physics-stepping function synchronously when `typeof Worker === 'undefined'`. |
| R9-07 | Performance verification: the Katana `from_httpx_upside_com` proposal graph (3,426 nodes / 11,199 edges pre-shadow-fix) mounts, renders a first frame within ~2s, and stays interactive (pan/zoom responsive) during active layout, with no browser "page unresponsive" prompt. |
| R9-08 | `GraphShadows.apply()` nested-loop fix: replace the O(shadowPairs × edges) scan with a `Map<source, edge[]>` index (O(edges)); identical output node/edge sets before and after for the Katana fixture; before/after timing logged. |
| R9-09 | CLI Scan App Graph tab (`cli-scan-app.js`) cut over from `Viz.ForceGraph.create` to `Viz.CanvasGraph.create` — same options object already built by `transformProposalGraph`/`applyShadowOptions`; fullscreen/stats/legend wiring unchanged. |
| R9-10 | GOV-08 regression matrix for the CLI Scan App Graph tab: gold/capstone scenario per onboarded tool (8) + the Katana stress scenario + one empty/no-graph scenario; classified `Validated`/`Invalidated`/`Blocked`/`Uncovered-spec-gap` with tracked follow-ups for anything not `Validated`. |
| R9-11 | Maps tab (`map.js`) cut over from `Viz.ForceGraph.create` to `Viz.CanvasGraph.create` (`Map._graphInstance`) — `Map.transformGraph`, icon-fallback logic, and the existing `GraphShadows.apply('map-nuggets', ...)` call unchanged. |
| R9-12 | GOV-08 regression check of the Maps tab; classified and tracked follow-ups. |
| R9-13 | Decommission `src/js/viz.force.js` (remove from the webpack bundle list and delete) and `profiling.js`'s orphaned `ForceGraph.create` call (already unreachable dead code — no matching DOM in `content.html`); remove now-unused SVG-only CSS selectors, preserving tooltip/legend rules. Gated on R9-10 and R9-12 both being recorded complete. |
| R9-14 | Documentation pass: update the `d3js` skill and any doc that names `Viz.ForceGraph` as the current graph engine to point at `Viz.CanvasGraph`; add SPEC-009 pointer rows to both repos' `AGENTS.md`. |

## Milestone (what "done" looks like for the operator)

Opening CLI Profiling → any onboarded tool → the Katana `from_httpx_upside_com` scenario (or any
other large-graph scenario) renders the Graph tab without the browser tab becoming unresponsive,
with pan/zoom/hover/click/drag behaving the same as the current SVG engine. The same holds for the
Maps tab. `Viz.ForceGraph`/SVG rendering is fully retired from the codebase once both cutovers are
verified stable.

## Architecture

```text
src/js/canvas-graph.js              → window.Viz.CanvasGraph (new engine, peer of Viz.ForceGraph)
src/assets/workers/canvas-graph.worker.js → copied verbatim to dist/workers/ (static asset, no build config change)
src/js/graph-shadows.js             → GraphShadows.apply() nested-loop fix (O(n), same output)
src/js/cli-scan-app.js              → Graph tab cut over to Viz.CanvasGraph
src/js/map.js                       → Maps tab cut over to Viz.CanvasGraph
src/js/viz.force.js                 → deleted once both cutovers are verified stable
src/js/profiling.js                 → orphaned ForceGraph.create call deleted
```

Physics (the expensive, main-thread-blocking part today) moves entirely into a Web Worker that
loads `d3` via `importScripts('/vendor.js')` — validated safe in a Node `vm` sandbox with no
`window`/`document` present (d3's UMD bundle only touches DOM globals lazily, inside functions
that are never called from the worker). The main thread only ever performs cheap canvas draw calls
and O(log n) quadtree lookups, so it stays responsive regardless of graph size.

## Traceability

Implementation: GitHub epics under `[SPEC-009]` in `brettforbes/spiderfeet-widget` only (no
backend epics — this SPEC has no `spiderfeet`-repo scope). Epic letters `AB`-`AG`, continuing after
SPEC-008's `V`-`AA`.
