# Widget iframe integration (spiderfeet-widget)

HTML5 embed built with webpack; parent application hosts `<iframe src=".../dist/index.html">`.

## File roles

| Path | Role |
|------|------|
| `src/html/_index.html` | Minimal shell: `vendor.js`, `vendor.css`, `widget.css`, injected body, `widget.js` |
| `src/html/content.html` | All visible Bootstrap markup |
| `src/js/_namespace.js` | `window.Widgets` + `watchDOMForComponent` |
| `src/js/#events.js` | `window.Widgets.Events` |
| `src/js/*.js` | Feature modules (IIFE) |
| `webpack.common.js` | Injects `content.html` into `htmlWebpackPlugin.options.body` |
| `dist/index.html` | Built iframe entry |

## Load order

```html
<script src="./vendor.js"></script>   <!-- jQuery, Bootstrap, D3, Popper -->
<link rel="stylesheet" href="./vendor.css" />
<link rel="stylesheet" href="./widget.css" />
<!-- body from content.html -->
<script src="./widget.js" defer></script>
```

Do not add duplicate Bootstrap CDN links in `content.html` unless debugging outside webpack.

## Parent ↔ child messaging

### Preferred: structured events

```javascript
// Compile payload
const data = Widgets.Events.compileEventData(
  { routeId: 'sfp-dnscommonsrv' },  // payload
  'map-route-selected',              // type / event name
  'select',                          // action
  'map-panel',                       // componentId
  { variant: 'grouped' },            // config
  'parent'                           // target
);

Widgets.Events.raiseEvent('map-route-selected', data);
```

Child listens:

```javascript
Widgets.Events.windowListener(function (event, sourceData) {
  if (sourceData.type === 'map-set-variant') {
    Widgets.Map.setVariant(sourceData.payload.variant);
  }
});
```

`windowListener` ignores messages where `sourceData.target === 'parent'` to avoid loops.

### Legacy demo (avoid for new code)

`content.html` includes raw string `postMessage` demos. New features must use `Events.compileEventData` + JSON.stringify path inside `raiseEvent`.

## Module template

```javascript
window.Widgets = window.Widgets || {};
window.Widgets.Sidebar = window.Widgets.Sidebar || {};

(function ($, Sidebar, Widgets, Events, document, window) {
  'use strict';

  Sidebar.selector = '[data-widget="map-sidebar"]';

  Sidebar.init = function ($root) {
    const el = $root[0];
    if (el.dataset.initialized) return;
    el.dataset.initialized = 'true';

    el.querySelector('[data-action="refresh"]')?.addEventListener('click', () => {
      Events.raiseEvent('map-refresh', Events.compileEventData(
        {}, 'map-refresh', 'click', 'sidebar', {}, 'parent'
      ));
    });
  };

  Widgets.watchDOMForComponent(Sidebar.selector, Sidebar.init);
})(window.jQuery, window.Widgets.Sidebar, window.Widgets, window.Widgets.Events, document, window);
```

## Webpack / HTML injection

Body markup is not edited in `dist/` — change `src/html/content.html` and rebuild.

Title/description come from webpack config (`htmlWebpackPlugin.options`).

## Bootstrap forms in iframe

No server round-trip — use `type="button"` for actions; `type="submit"` only when intentionally posting via JS.

Client validation pattern:

```html
<div class="mb-3">
  <label for="seedTarget" class="form-label">Seed target</label>
  <input type="text" class="form-control" id="seedTarget" required>
  <div class="invalid-feedback">Required</div>
</div>
```

```javascript
input.classList.toggle('is-invalid', !input.value.trim());
```

## Security notes

- Replace `postMessage(..., "*")` with explicit parent origin when host URL is known.
- Sanitize any HTML inserted into tooltips or sidebar lists.
- Do not expose secrets in iframe query strings.

## Host responsibilities (parent app)

- Size iframe with explicit width/height or aspect ratio container.
- Listen for `message` events; parse JSON; route by `data.type`.
- Send commands via `iframe.contentWindow.postMessage(JSON.stringify(...), origin)`.

## Related skills

- **d3js** — `Viz.ForceGraph`, force variants, `assets/js/viz.*.js`
- **bootstrap5-ui** (this skill) — layout around `#viz-stage`
