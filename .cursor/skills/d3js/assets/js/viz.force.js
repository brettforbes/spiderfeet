/**
 * Viz.ForceGraph — force-directed graph factory with layout variants.
 */
(function (global) {
  'use strict';

  global.Viz = global.Viz || {};
  const Core = global.Viz.Core;

  const VARIANTS = {
    default(simulation, width, height) {
      simulation
        .force('link', d3.forceLink().id(d => d.id).distance(80).strength(0.8))
        .force('charge', d3.forceManyBody().strength(-220))
        .force('center', d3.forceCenter(width / 2, height / 2));
    },

    sparse(simulation, width, height) {
      simulation
        .force('link', d3.forceLink().id(d => d.id).distance(140).strength(0.4))
        .force('charge', d3.forceManyBody().strength(-120))
        .force('center', d3.forceCenter(width / 2, height / 2));
    },

    dense(simulation, width, height) {
      simulation
        .force('link', d3.forceLink().id(d => d.id).distance(35).strength(0.9))
        .force('charge', d3.forceManyBody().strength(-400))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collide', d3.forceCollide().radius(d => (d.r || 8) + 4));
    },

    radial(simulation, width, height, nodes, opts) {
      const rootId = opts.rootId || nodes[0]?.id;
      simulation
        .force('link', d3.forceLink().id(d => d.id).distance(60))
        .force('charge', d3.forceManyBody().strength(-180))
        .force('radial', d3.forceRadial(
          d => (d.id === rootId ? 0 : 120),
          width / 2,
          height / 2,
        ).strength(0.8));
    },

    grouped(simulation, width, height, nodes) {
      const groups = [...new Set(nodes.map(n => n.group))];
      const centres = new Map(groups.map((g, i) => {
        const angle = (i / groups.length) * 2 * Math.PI;
        return [g, {
          x: width / 2 + 120 * Math.cos(angle),
          y: height / 2 + 120 * Math.sin(angle),
        }];
      }));
      simulation
        .force('link', d3.forceLink().id(d => d.id).distance(50))
        .force('charge', d3.forceManyBody().strength(-250))
        .force('x', d3.forceX(d => centres.get(d.group).x).strength(0.12))
        .force('y', d3.forceY(d => centres.get(d.group).y).strength(0.12));
    },

    hierarchical(simulation, width, height) {
      simulation
        .force('link', d3.forceLink().id(d => d.id)
          .distance(d => 40 + 25 * (d.target.depth || 0)))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('y', d3.forceY(d => (d.depth || 0) * 60 + 40).strength(0.4))
        .force('x', d3.forceX(width / 2).strength(0.05));
    },

    constrained(simulation, width, height) {
      const margin = 20;
      function forceBounds() {
        let nodes;
        function force() {
          for (const n of nodes) {
            n.x = Math.max(margin, Math.min(width - margin, n.x));
            n.y = Math.max(margin, Math.min(height - margin, n.y));
          }
        }
        force.initialize = _ => { nodes = _; };
        return force;
      }
      simulation
        .force('link', d3.forceLink().id(d => d.id).distance(70))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('bounds', forceBounds());
    },
  };

  function dragBehaviour(simulation) {
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

  function neighbourSet(nodeId, links) {
    const set = new Set([nodeId]);
    links.forEach(l => {
      const sid = l.source.id ?? l.source;
      const tid = l.target.id ?? l.target;
      if (sid === nodeId) set.add(tid);
      if (tid === nodeId) set.add(sid);
    });
    return set;
  }

  const ForceGraph = {
    variants: Object.keys(VARIANTS),

    create(options) {
      const {
        svg: svgSelector,
        tooltip: tooltipSelector,
        nodes: rawNodes,
        links: rawLinks,
        variant = 'default',
        rootId,
        onNodeClick,
        onNodeHover,
      } = options;

      const svgEl = document.querySelector(svgSelector);
      const { width, height } = Core.dimensions(svgEl);
      const svg = Core.selectSvg(svgEl);
      Core.clear(svg);
      svg.attr('width', width).attr('height', height);

      const { nodes, links } = Core.cloneGraph({ nodes: rawNodes, links: rawLinks });
      const groups = [...new Set(nodes.map(n => n.group))];
      const colour = Core.colourByGroup(groups);

      const rootG = svg.append('g').attr('class', 'graph-root');
      const zoom = d3.zoom()
        .scaleExtent([0.2, 8])
        .on('zoom', (event) => rootG.attr('transform', event.transform));
      svg.call(zoom);

      const simulation = d3.forceSimulation(nodes);
      const applyVariant = VARIANTS[variant] || VARIANTS.default;
      applyVariant(simulation, width, height, nodes, { rootId });
      simulation.force('link').links(links);

      const link = rootG.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('class', 'link')
        .attr('stroke-width', d => Math.sqrt(d.value || 1));

      const node = rootG.append('g')
        .attr('class', 'nodes')
        .selectAll('circle')
        .data(nodes)
        .join('circle')
        .attr('class', 'node')
        .attr('r', d => d.r || 8)
        .attr('fill', d => colour(d.group))
        .call(dragBehaviour(simulation));

      const tooltipEl = tooltipSelector
        ? document.querySelector(tooltipSelector)
        : null;

      function resetHighlight() {
        node.classed('dimmed', false);
        link.classed('dimmed', false);
      }

      node
        .on('mouseover', (event, d) => {
          const adj = neighbourSet(d.id, links);
          node.classed('dimmed', n => !adj.has(n.id));
          link.classed('dimmed', l => {
            const sid = l.source.id;
            const tid = l.target.id;
            return !(sid === d.id || tid === d.id);
          });
          if (tooltipEl) {
            tooltipEl.hidden = false;
            tooltipEl.innerHTML = `<strong>${d.id}</strong><br/>group: ${d.group ?? '—'}`;
          }
          onNodeHover?.(event, d);
        })
        .on('mousemove', (event) => {
          if (!tooltipEl) return;
          tooltipEl.style.left = `${event.pageX + 12}px`;
          tooltipEl.style.top = `${event.pageY + 12}px`;
        })
        .on('mouseout', () => {
          resetHighlight();
          if (tooltipEl) tooltipEl.hidden = true;
        })
        .on('click', (event, d) => onNodeClick?.(event, d));

      simulation.on('tick', () => {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);
        node
          .attr('cx', d => d.x)
          .attr('cy', d => d.y);
      });

      const disconnectResize = Core.observeResize(svgEl.parentElement, () => {
        const dims = Core.dimensions(svgEl);
        svg.attr('width', dims.width).attr('height', dims.height);
        simulation.force('center', d3.forceCenter(dims.width / 2, dims.height / 2));
        simulation.alpha(0.3).restart();
      });

      return {
        simulation,
        restart() {
          simulation.alpha(1).restart();
        },
        destroy() {
          simulation.stop();
          disconnectResize();
          svg.on('.zoom', null);
          Core.clear(svg);
        },
      };
    },
  };

  global.Viz.ForceGraph = ForceGraph;
})(typeof window !== 'undefined' ? window : globalThis);
