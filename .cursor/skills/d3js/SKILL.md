---
name: d3js
description: Build interactive D3 visualisations with HTML5 and vanilla JavaScript using namespaced modules. Prioritises force-directed graph variants (OSINT maps, route networks, scan graphs). Use when creating custom charts, force graphs, network diagrams, or SVG visualisations without React/Vue frameworks.
---

# D3.js — HTML5 + Vanilla JS

## Stack defaults

- **HTML5** shell (`<svg>`, optional `<canvas>`, tooltip `<div>`)
- **Vanilla ES modules** or script tags; **no React/Vue/Svelte** in templates
- **Namespaced code** under `window.Viz` (or project-specific root, e.g. `window.SpiderFeetViz`)
- **D3 v7** via CDN or npm `import * as d3 from 'd3'`

## Namespace layout

```text
Viz/
├── Core      — SVG setup, margins, resize, teardown, colours
├── Charts    — bar, line, scatter (non-force)
└── ForceGraph — simulation factory + variants + interactions
```

Bootstrap once:

```javascript
window.Viz = window.Viz || {};
```

Load order in HTML: `viz.core.js` → `viz.charts.js` → `viz.force.js` → page init.

## HTML5 page pattern

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Force graph</title>
  <link rel="stylesheet" href="css/viz.css" />
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script src="js/viz.core.js" defer></script>
  <script src="js/viz.force.js" defer></script>
  <script src="js/app.js" defer></script>
</head>
<body>
  <main class="viz-shell">
    <div id="controls"></div>
    <svg id="graph" role="img" aria-label="Force-directed network"></svg>
    <div id="tooltip" class="viz-tooltip" hidden></div>
  </main>
</body>
</html>
```

Page init (`app.js`):

```javascript
document.addEventListener('DOMContentLoaded', async () => {
  const data = await fetch('sample-data.json').then(r => r.json());
  const graph = Viz.ForceGraph.create({
    svg: '#graph',
    tooltip: '#tooltip',
    variant: 'grouped',
    nodes: data.network.nodes,
    links: data.network.links,
  });
  window.addEventListener('beforeunload', () => graph.destroy());
});
```

## Core workflow

1. **Prepare data** — validate nodes/links; ensure `links` use `id` strings or resolve to node objects after `forceLink`.
2. **Create chart** — `Viz.ForceGraph.create(options)` returns `{ destroy, restart, simulation }`.
3. **Wire resize** — `Viz.Core.observeResize(container, callback)` returns disconnect fn.
4. **Teardown** — call `destroy()` to stop simulation and remove listeners.

### Standard draw function shape

```javascript
Viz.Charts.bar = function barChart(svgElement, data, options) {
  if (!data?.length) return;
  const svg = Viz.Core.selectSvg(svgElement);
  Viz.Core.clear(svg);
  const { width, height, margin, innerWidth, innerHeight } = Viz.Core.dimensions(svgElement, options);
  const g = Viz.Core.rootGroup(svg, margin);
  // scales, axes, join data...
};
```

## Force graphs (primary focus)

Use **`references/force-graphs.md`** for full variant catalogue, tuning notes, and copy-paste snippets.

### Variant picker

| Variant | When to use |
|--------|-------------|
| `default` | General OSINT / module graphs |
| `sparse` | Few nodes, long link distance |
| `dense` | Many nodes, stronger repulsion + collision |
| `radial` | Hub-and-spoke or root-centric expansion |
| `grouped` | Cluster by `group` / nugget type |
| `hierarchical` | Tree-like link distances from depth |
| `constrained` | Keep nodes inside viewport bounds |
| `canvas` | 1k+ nodes — draw on canvas, not SVG circles |

```javascript
Viz.ForceGraph.create({
  svg: '#graph',
  variant: 'dense',
  nodes, links,
  onNodeClick: (event, node) => { /* expand route, RMB menu, etc. */ },
  onNodeHover: (event, node) => { /* highlight neighbourhood */ },
});
```

### Simulation checklist

- `forceLink` — `.id(d => d.id)`, `.distance()`, optional `.strength()`
- `forceManyBody` — repulsion; tune `.strength()` (negative)
- `forceCenter` — keeps graph centred
- `forceCollide` — overlap reduction (dense graphs)
- `forceRadial` / `forceX` / `forceY` — layout bias
- `simulation.on('tick')` — update link paths and node positions
- `simulation.alphaDecay()` / `.restart()` — control settle vs reheat

### Interactions (force graphs)

- **Drag** — `d3.drag()` with `fx`/`fy` pin; clear on `dragend` for float
- **Zoom/pan** — `d3.zoom()` on root `<g>`, not on individual nodes
- **Highlight** — on hover, dim non-neighbours; thicken incident links
- **Curved links** — `d3.linkHorizontal` / `linkRadial` or quadratic beziers
- **Labels** — `text` bound to nodes, update x/y on tick

## Other chart types

Keep bar/line/scatter/chord/heatmap patterns in `references/d3-patterns.md` and `Viz.Charts` — use the same `Viz.Core` helpers. Force work stays in `Viz.ForceGraph`.

## Best practices

- **One simulation per graph** — stop previous simulation on variant switch (`destroy()` first).
- **Copy data** — `structuredClone` or `nodes.map(n => ({...n}))` before forces mutate positions.
- **Id keys** — stable `id` on nodes for join and link resolution.
- **Accessibility** — `role="img"`, `<title>`/`<desc>` on SVG, keyboard focus where interactive.
- **Performance** — SVG &lt; ~500 nodes; switch to `canvas` variant above that.

## Resources

| Path | Purpose |
|------|---------|
| `references/force-graphs.md` | **Start here** for force variants and tuning |
| `references/d3-patterns.md` | Other chart types (vanilla `renderFn(svg, data)`) |
| `references/scale-reference.md` | Scales |
| `references/colour-schemes.md` | Palettes |
| `assets/index.html` | Minimal bar chart demo |
| `assets/force-graph.html` | Force variant switcher demo |
| `assets/js/viz.core.js` | `Viz.Core` namespace |
| `assets/js/viz.charts.js` | `Viz.Charts` namespace |
| `assets/js/viz.force.js` | `Viz.ForceGraph` + variants |
| `assets/sample-data.json` | Includes `network` graph sample |

When implementing spiderfeet map UI, read `force-graphs.md` and extend `Viz.ForceGraph.variants` rather than inlining one-off simulations.
