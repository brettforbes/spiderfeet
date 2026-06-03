# Viz stage layout — Bootstrap + D3 (SVG / canvas)

Patterns for embedding force graphs and other D3 views inside Bootstrap iframe UI.

## Stage markup

```html
<div id="viz-stage" class="flex-grow-1 position-relative bg-body-secondary overflow-hidden">
  <!-- Toolbar overlay (optional) -->
  <div class="position-absolute top-0 start-0 end-0 p-2 z-3">
    <div class="btn-group btn-group-sm" role="group" aria-label="Force layout variant">
      <button type="button" class="btn btn-outline-secondary" data-variant="default" aria-pressed="true">Default</button>
      <button type="button" class="btn btn-outline-secondary" data-variant="grouped">Grouped</button>
      <button type="button" class="btn btn-outline-secondary" data-variant="dense">Dense</button>
      <button type="button" class="btn btn-outline-secondary" data-variant="canvas">Canvas</button>
    </div>
  </div>

  <svg id="graph" class="viz-layer w-100 h-100" role="img" aria-label="Network graph"></svg>
  <canvas id="graph-canvas" class="viz-layer w-100 h-100 d-none" width="800" height="600"></canvas>

  <div id="tooltip" class="position-absolute border rounded bg-body px-2 py-1 small shadow-sm"
       style="pointer-events:none;" hidden></div>
</div>
```

## CSS (widget.css or content-adjacent)

```css
#viz-stage .viz-layer {
  display: block;
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

#viz-stage .z-3 {
  z-index: 3;
}
```

Bootstrap `d-none` toggles which layer is active.

## Resize handling

Iframe body does not scroll — size the stage from its container:

```javascript
Widgets.Viz = Widgets.Viz || {};

(function (Viz, Widgets) {
  Viz.measureStage = function () {
    const stage = document.getElementById('viz-stage');
    const rect = stage.getBoundingClientRect();
    return { width: rect.width, height: rect.height };
  };

  Viz.onStageResize = function (callback) {
    const stage = document.getElementById('viz-stage');
    if (!stage || typeof ResizeObserver === 'undefined') {
      window.addEventListener('resize', callback);
      return () => window.removeEventListener('resize', callback);
    }
    const ro = new ResizeObserver(() => callback());
    ro.observe(stage);
    return () => ro.disconnect();
  };
})(window.Widgets.Viz = window.Widgets.Viz || {}, window.Widgets);
```

On resize:
1. Read `measureStage()`.
2. Set `svg` width/height attributes (or `viewBox`).
3. Set `canvas.width` / `canvas.height` (device pixels; consider `devicePixelRatio`).
4. `simulation.force('center', d3.forceCenter(w/2, h/2)); simulation.alpha(0.3).restart();`

## SVG vs canvas selection

| Criterion | SVG | Canvas |
|-----------|-----|--------|
| Node count | &lt; ~500 | 500+ |
| DOM events per node | Easy (`mouseover`, drag) | Manual hit-testing |
| Zoom/pan | `d3.zoom` on root `<g>` | Redraw on transform |
| Export / a11y | Better | Add parallel summary table |

```javascript
function mountGraph({ variant, nodes, links }) {
  const useCanvas = variant === 'canvas' || nodes.length > 500;
  document.getElementById('graph').classList.toggle('d-none', useCanvas);
  document.getElementById('graph-canvas').classList.toggle('d-none', !useCanvas);

  if (useCanvas) {
    return Viz.ForceGraph.create({ canvas: '#graph-canvas', variant: 'dense', nodes, links });
  }
  return Viz.ForceGraph.create({ svg: '#graph', variant, nodes, links });
}
```

Align with `d3js` skill `Viz.ForceGraph` API; extend factory to accept `canvas` selector when implementing.

## Bootstrap chrome around graph

### Sidebar + graph (common map layout)

```html
<div class="row g-0 flex-grow-1 overflow-hidden">
  <aside class="col-12 col-md-3 border-end overflow-auto">
  <main class="col-12 col-md-9 d-flex flex-column p-0">
    <div id="viz-stage" class="flex-grow-1">...</div>
  </main>
</div>
```

### Collapsible filter drawer

Use **offcanvas** for mobile filters; keep graph full width on `md+`:

```html
<button class="btn btn-outline-secondary d-md-none" type="button"
        data-bs-toggle="offcanvas" data-bs-target="#filterDrawer" aria-controls="filterDrawer">
  Filters
</button>
<div class="offcanvas offcanvas-start" tabindex="-1" id="filterDrawer">...</div>
```

### Route detail modal

```html
<div class="modal fade" id="routeModal" tabindex="-1" aria-labelledby="routeModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">...</div>
  </div>
</div>
```

Open from graph `onNodeClick` via `bootstrap.Modal.getOrCreateInstance`.

## Toolbar variant state

Sync Bootstrap `aria-pressed` with active variant:

```javascript
function setVariantButtons(active) {
  document.querySelectorAll('[data-variant]').forEach(btn => {
    const on = btn.dataset.variant === active;
    btn.classList.toggle('active', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
}
```

## Loading and empty states

```html
<div id="viz-empty" class="position-absolute top-50 start-50 translate-middle text-center d-none">
  <p class="text-body-secondary mb-2">No routes to display</p>
  <button type="button" class="btn btn-sm btn-primary" data-action="load-sample">Load sample</button>
</div>
<div id="viz-spinner" class="position-absolute top-50 start-50 translate-middle d-none">
  <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading</span></div>
</div>
```

Toggle with `d-none` when graph data arrives.

## Accessibility

- `role="img"` + `aria-label` on active graph layer.
- Provide **sidebar list** or table duplicate of selected node for screen readers.
- Keyboard: focus trap inside modals; do not trap focus in full graph without alternative navigation.

## Event bridge example

```javascript
// Node click → parent + modal
onNodeClick: (event, node) => {
  Widgets.Events.raiseEvent('map-node-selected', Widgets.Events.compileEventData(
    { id: node.id, group: node.group },
    'map-node-selected', 'click', 'force-graph', {}, 'parent'
  ));
  document.getElementById('routeModalLabel').textContent = node.id;
  bootstrap.Modal.getOrCreateInstance(document.getElementById('routeModal')).show();
}
```
