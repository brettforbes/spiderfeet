---
name: bootstrap
description: Bootstrap 5.3 layout and components for spiderfeet-widget iframe embeds. Use when building HTML5 UI in content.html, structuring containers/controls, wiring window.Widgets modules, or placing D3/canvas visualisation panels. Not for ASP.NET Core or Razor.
---

# Bootstrap 5 — spiderfeet-widget iframe UI

## Mission

Build responsive UI inside the **webpack iframe widget** (`spiderfeet-widget`), not server-rendered .NET pages.

| Use | Avoid |
|-----|--------|
| HTML5 in `src/html/content.html` | Razor, tag helpers, `_Layout.cshtml` |
| Bootstrap from **vendor.css / vendor.js** (webpack bundle) | LibMan, `~/lib/bootstrap`, CDN in production unless dev-only |
| `window.Widgets.*` namespaced IIFEs | React/Vue in widget shell |
| `Widgets.Events` for parent messaging | Ad-hoc string `postMessage` in new code |
| SVG/canvas slots for D3 (`Viz.ForceGraph`) | Filling entire iframe with raw `<svg>` without layout |

Pair with **`d3js`** skill for graph logic; this skill covers **layout chrome** around the viz.

## Stack in spiderfeet-widget

```text
src/html/_index.html     → shell (vendor + widget.css + body inject + widget.js)
src/html/content.html    → Bootstrap markup (injected body)
src/js/_namespace.js     → window.Widgets
src/js/#events.js        → window.Widgets.Events
src/js/<feature>.js      → window.Widgets.<Feature> (IIFE)
webpack → dist/index.html (iframe src)
```

Bootstrap 5.3 and D3 7 are already in **vendor** bundles. Do not add a second Bootstrap copy unless intentionally replacing webpack vendor config.

## HTML shell constraints (iframe)

- `body { overflow: hidden; }` in widget CSS — design for **internal scroll regions**, not full-page body scroll.
- Prefer **`container-fluid`** + fixed header/toolbar + flex column main area.
- Keep embed height predictable: use `min-vh-100` inside the iframe document, not on the parent page.
- Semantic regions: `<header>`, `<main>`, `<aside>`, `<footer>` with Bootstrap utilities.

### Canonical page skeleton

```html
<div class="container-fluid vh-100 d-flex flex-column p-0" data-bs-theme="light">
  <header class="border-bottom bg-body-tertiary px-3 py-2">
    <div class="d-flex align-items-center justify-content-between">
      <h1 class="h5 mb-0">Spiderfeet map</h1>
      <div id="map-toolbar" class="btn-toolbar gap-2" role="toolbar" aria-label="Map controls"></div>
    </div>
  </header>

  <div class="row g-0 flex-grow-1 overflow-hidden">
    <aside class="col-12 col-md-3 border-end overflow-auto p-3" id="map-sidebar">
      <!-- filters, route list, sequence picker -->
    </aside>
    <main class="col-12 col-md-9 d-flex flex-column overflow-hidden position-relative p-0">
      <div id="viz-stage" class="flex-grow-1 position-relative bg-body-secondary">
        <svg id="graph" class="viz-layer" role="img" aria-label="Force graph"></svg>
        <canvas id="graph-canvas" class="viz-layer d-none" aria-hidden="true"></canvas>
        <div id="tooltip" class="viz-tooltip position-absolute" hidden></div>
      </div>
      <footer class="border-top px-3 py-2 small text-body-secondary" id="map-status">
        Ready
      </footer>
    </main>
  </div>
</div>
```

## Namespace pattern for UI modules

Add features under `window.Widgets`, one file per concern, IIFE + explicit deps:

```javascript
window.Widgets = window.Widgets || {};
window.Widgets.Map = window.Widgets.Map || {};

(function ($, Map, Widgets, Events, document, window) {
  Map.selectorToolbar = '[data-widget="map-toolbar"]';

  Map.init = function ($root) {
    // Bootstrap components via JS when needed:
    // const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById('routeModal'));
  };

  Widgets.watchDOMForComponent(Map.selectorToolbar, Map.init);
})(window.jQuery, window.Widgets.Map, window.Widgets, window.Widgets.Events, document, window);
```

**Rules:**
- Selectors drive init: `data-widget="..."` or `data-type="..."` (match existing template).
- No inline `<script>` in new `content.html` — put behaviour in `src/js/`.
- Use `Events.raiseEvent` / `Events.windowListener` for parent host (see `references/widget-iframe-integration.md`).

## Grid and spacing (iframe-friendly)

```html
<div class="container-fluid px-3 py-2">
  <div class="row g-2">
    <div class="col-12 col-lg-8"><!-- viz --></div>
    <div class="col-12 col-lg-4"><!-- panel --></div>
  </div>
</div>
```

- Always `.row` > `.col-*`; use `.g-*` gutters.
- Side panels: `overflow-auto` + `max-height` or flex `flex-grow-1 overflow-hidden` parent.
- Toolbars: `btn-toolbar`, `btn-group`, `gap-2`; icon buttons need `aria-label`.

## D3 / canvas integration

Use a **stage** wrapper; swap SVG vs canvas by variant (see `references/viz-canvas-layout.md`):

| Layer | Element | Role |
|-------|---------|------|
| Graph (SVG) | `#graph` | Default force graph, zoom on inner `<g>` |
| Graph (canvas) | `#graph-canvas` | Large graphs (`dense`, 1k+ nodes) |
| Tooltip | `#tooltip` | `position-absolute`, Bootstrap-adjacent styling |
| Overlay UI | `.viz-overlay` | Legend, variant buttons (Bootstrap `btn-group`) |

Toggle visibility with utilities: `d-none` / `d-block` on layers; do not stack opaque canvases over SVG.

Wire graph from namespaced module:

```javascript
Map.mountGraph = function (nodes, links, variant) {
  Map.graph?.destroy();
  const useCanvas = variant === 'canvas';
  document.getElementById('graph').classList.toggle('d-none', useCanvas);
  document.getElementById('graph-canvas').classList.toggle('d-none', !useCanvas);
  Map.graph = Viz.ForceGraph.create({
    svg: useCanvas ? null : '#graph',
    canvas: useCanvas ? '#graph-canvas' : null,
    tooltip: '#tooltip',
    variant, nodes, links,
  });
};
```

(Extend `Viz.ForceGraph` in d3js skill assets if canvas selector not yet implemented.)

## Bootstrap JS in widget code

Vendor exposes global `bootstrap` (bundle). Initialise imperatively when markup is injected dynamically:

```javascript
document.querySelectorAll('[data-bs-toggle="tooltip"]')
  .forEach(el => new bootstrap.Tooltip(el));
```

Modals for route detail, offcanvas for filters — prefer `data-bs-*` in HTML when markup is static; use `bootstrap.Modal.getOrCreateInstance` after DOM updates.

## Colour mode

```html
<html lang="en" data-bs-theme="light">
```

Use semantic tokens: `bg-body`, `bg-body-secondary`, `text-body-secondary`, `border-body` — not hardcoded `bg-light` / `bg-dark`.

## References

| File | Contents |
|------|----------|
| `references/widget-iframe-integration.md` | iframe shell, webpack inject, `Widgets.Events`, parent contract |
| `references/viz-canvas-layout.md` | Viz stage, SVG/canvas swap, resize, toolbar patterns |
| `references/components.md` | Modals, offcanvas, tables, dashboard layouts (HTML only) |

## Anti-patterns (this project)

- Razor / `asp-for` / LibMan paths
- Full-page `body` scroll inside iframe
- Inline scripts in `content.html` for product features
- Second copy of Bootstrap or D3 outside vendor bundle
- `postMessage(..., "*")` without structured `Events.compileEventData` for new features
- Placing D3 zoom on `<svg>` while controls live outside `#viz-stage` without shared resize handler

## Checklist before shipping UI

1. Markup lives in `content.html` with Bootstrap grid + semantic regions.
2. Behaviour in `src/js` under `window.Widgets.<Feature>`.
3. Parent events use `Widgets.Events`.
4. Viz has `#viz-stage`, tooltip, and SVG or canvas layer.
5. Toolbar/status regions use `btn-toolbar` + `aria-label` on icon-only controls.
6. Test at iframe width 320px and desktop; panels collapse via `col-12 col-md-*`.
