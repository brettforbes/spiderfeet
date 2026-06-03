# Force-directed graph variants (D3 v7, vanilla JS)

All examples assume `Viz.ForceGraph.create()` or the same simulation API. Nodes need `id`; links use `source`/`target` as ids or objects after `forceLink` runs.

## Shared render loop

```javascript
function tickUpdate(simulation, linkSel, nodeSel) {
  simulation.on('tick', () => {
    linkSel
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);
    nodeSel
      .attr('cx', d => d.x)
      .attr('cy', d => d.y);
  });
}
```

## Variant: default

Balanced link + charge + center. Good starting point for OSINT module graphs.

```javascript
function applyDefault(simulation, width, height, linkDistance = 80) {
  simulation
    .force('link', d3.forceLink().id(d => d.id).distance(linkDistance).strength(0.8))
    .force('charge', d3.forceManyBody().strength(-220))
    .force('center', d3.forceCenter(width / 2, height / 2));
}
```

## Variant: sparse

Few nodes, more spacing, weaker link pull.

```javascript
function applySparse(simulation, width, height) {
  simulation
    .force('link', d3.forceLink().id(d => d.id).distance(140).strength(0.4))
    .force('charge', d3.forceManyBody().strength(-120))
    .force('center', d3.forceCenter(width / 2, height / 2));
}
```

## Variant: dense

Many nodes; stronger repulsion + collision.

```javascript
function applyDense(simulation, width, height) {
  simulation
    .force('link', d3.forceLink().id(d => d.id).distance(35).strength(0.9))
    .force('charge', d3.forceManyBody().strength(-400))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collide', d3.forceCollide().radius(d => (d.r || 8) + 4));
}
```

## Variant: radial

Pull nodes toward rings around a focal hub (e.g. root nugget).

```javascript
function applyRadial(simulation, width, height, rootId) {
  const cx = width / 2;
  const cy = height / 2;
  simulation
    .force('link', d3.forceLink().id(d => d.id).distance(60))
    .force('charge', d3.forceManyBody().strength(-180))
    .force('radial', d3.forceRadial(
      d => (d.id === rootId ? 0 : 120),
      cx, cy
    ).strength(0.8));
}
```

## Variant: grouped

Separate clusters by `group` (nugget type, module family, etc.).

```javascript
function applyGrouped(simulation, width, height, nodes) {
  const groups = [...new Set(nodes.map(n => n.group))];
  const centres = new Map(groups.map((g, i) => {
    const angle = (i / groups.length) * 2 * Math.PI;
    return [g, { x: width / 2 + 120 * Math.cos(angle), y: height / 2 + 120 * Math.sin(angle) }];
  }));

  simulation
    .force('link', d3.forceLink().id(d => d.id).distance(50))
    .force('charge', d3.forceManyBody().strength(-250))
    .force('x', d3.forceX(d => centres.get(d.group).x).strength(0.12))
    .force('y', d3.forceY(d => centres.get(d.group).y).strength(0.12));
}
```

## Variant: hierarchical

Link distance scales with tree depth (after `d3.stratify` or precomputed `depth`).

```javascript
function applyHierarchical(simulation, width, height) {
  simulation
    .force('link', d3.forceLink().id(d => d.id)
      .distance(d => 40 + 25 * (d.target.depth || 0)))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('y', d3.forceY(d => (d.depth || 0) * 60 + 40).strength(0.4))
    .force('x', d3.forceX(width / 2).strength(0.05));
}
```

## Variant: constrained

Keep nodes inside the viewport with a custom force.

```javascript
function forceBounds(width, height, margin = 20) {
  let nodes;
  function force(alpha) {
    for (const n of nodes) {
      n.x = Math.max(margin, Math.min(width - margin, n.x));
      n.y = Math.max(margin, Math.min(height - margin, n.y));
    }
  }
  force.initialize = _ => { nodes = _; };
  return force;
}

function applyConstrained(simulation, width, height) {
  simulation
    .force('link', d3.forceLink().id(d => d.id).distance(70))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('bounds', forceBounds(width, height));
}
```

## Variant: canvas (performance)

Use when node count is large. Same simulation; draw links/nodes on `<canvas>` each tick.

```javascript
function canvasRenderer(context, links, nodes) {
  return () => {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    context.strokeStyle = '#999';
    context.lineWidth = 1;
    for (const l of links) {
      context.beginPath();
      context.moveTo(l.source.x, l.source.y);
      context.lineTo(l.target.x, l.target.y);
      context.stroke();
    }
    for (const n of nodes) {
      context.beginPath();
      context.arc(n.x, n.y, n.r || 5, 0, 2 * Math.PI);
      context.fillStyle = n.colour || '#4A90E2';
      context.fill();
    }
  };
}
```

## Link styling variants

### Straight vs curved

```javascript
// Curved horizontal links (good for L-R trees)
const linkPath = d3.linkHorizontal()
  .x(d => d.x)
  .y(d => d.y);

linkSel.attr('d', d => linkPath({
  source: d.source,
  target: d.target
}));
```

### Width by weight

```javascript
linkSel.attr('stroke-width', d => Math.sqrt(d.value || 1));
```

## Interaction patterns

### Drag (pin while dragging)

```javascript
function drag(simulation) {
  return d3.drag()
    .on('start', (event, d) => {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on('drag', (event, d) => {
      d.fx = event.x;
      d.fy = event.y;
    })
    .on('end', (event, d) => {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    });
}
```

### Zoom on graph layer

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.2, 8])
  .on('zoom', (event) => rootG.attr('transform', event.transform));
svg.call(zoom);
```

### Neighbour highlight

```javascript
function highlightNeighbours(hoveredId, links, nodeSel, linkSel) {
  const adjacent = new Set([hoveredId]);
  links.forEach(l => {
    if (l.source.id === hoveredId) adjacent.add(l.target.id);
    if (l.target.id === hoveredId) adjacent.add(l.source.id);
  });
  nodeSel.attr('opacity', n => adjacent.has(n.id) ? 1 : 0.2);
  linkSel.attr('stroke-opacity', l =>
    (l.source.id === hoveredId || l.target.id === hoveredId) ? 1 : 0.1);
}
```

## Simulation lifecycle

| Goal | API |
|------|-----|
| Reheat after data change | `simulation.nodes(nodes); simulation.force('link').links(links); simulation.alpha(1).restart()` |
| Softer settle | `simulation.alphaDecay(0.02)` |
| Stop when stable | `simulation.on('end', () => { ... })` |
| Cleanup | `simulation.stop()` + remove zoom/drag listeners |

## Choosing a variant (spiderfeet map)

| UI goal | Variant |
|---------|---------|
| Full elemental map | `dense` or `grouped` |
| Expand from root nugget | `radial` |
| Favourites / short paths | `default` or `sparse` |
| Sequence step preview | `hierarchical` |
| Large scan log replay | `canvas` |

## Anti-patterns

- Running two simulations on the same nodes without `stop()`
- Appending new SVG layers on every tick instead of updating attributes
- `forceLink` without `.id()` when links use string endpoints
- Zoom on nodes instead of root `<g>` (breaks drag coordinates)
- Mutating shared node objects across graphs without cloning
