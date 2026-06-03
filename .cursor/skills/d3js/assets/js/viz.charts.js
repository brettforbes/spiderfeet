/**
 * Viz.Charts — non-force chart helpers (vanilla JS).
 */
(function (global) {
  'use strict';

  global.Viz = global.Viz || {};
  const Core = global.Viz.Core;

  const Charts = {
  /**
   * @param {SVGElement|string} svgElement
   * @param {Array<{label:string,value:number}>} data
   * @param {object} [options]
   */
    bar(svgElement, data, options = {}) {
      if (!data?.length) return;

      const svg = Core.selectSvg(svgElement);
      Core.clear(svg);

      const dims = Core.dimensions(svgElement, options);
      svg.attr('width', dims.width).attr('height', dims.height);

      const g = svg
        .append('g')
        .attr('transform', `translate(${dims.margin.left},${dims.margin.top})`);

      const xScale = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, dims.innerWidth])
        .padding(0.1);

      const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .range([dims.innerHeight, 0])
        .nice();

      g.append('g')
        .attr('transform', `translate(0,${dims.innerHeight})`)
        .call(d3.axisBottom(xScale));

      g.append('g').call(d3.axisLeft(yScale));

      g.selectAll('rect')
        .data(data)
        .join('rect')
        .attr('x', d => xScale(d.label))
        .attr('y', d => yScale(d.value))
        .attr('width', xScale.bandwidth())
        .attr('height', d => dims.innerHeight - yScale(d.value))
        .attr('fill', options.colour || '#4A90E2');
    },
  };

  global.Viz.Charts = Charts;
})(typeof window !== 'undefined' ? window : globalThis);
