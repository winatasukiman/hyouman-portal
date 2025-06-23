/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class GoalGraph extends Component {
    setup() {
        this.container = useRef("mapContainer");
        this.rpc = useService("rpc");
        this.teamSelect = useRef("teamSelect");

        this.teams = [];
        this.nodes = [];
        this.links = [];
        this.defaultTeam = null;

        onWillStart(async () => {
            // Get list of teams
            this.teams = await this.rpc("/goal/team_list");
            this.defaultTeam = this.teams[0].name;
        });

        onMounted(async () => {
            if (this.defaultTeam) {
                await this.loadGraph(this.defaultTeam);  // this will call renderGraph()
            }
        });
    }

    async loadGraph(team_name) {
        const { nodes, links } = await this.rpc("/goal/graph", { team_name });
        this.nodes = Array.isArray(nodes) ? nodes : [];
        this.links = Array.isArray(links) ? links : [];
        this.renderGraph(); // re-render with new data
    }
    
    onTeamChange(ev) {
        const team_name = ev.target.value;
        this.loadGraph(team_name);
    }

    renderGraph() {
        const container = this.container.el;
        container.innerHTML = ""; // ← clear old SVG content
        const width = container.clientWidth;
        const height = container.clientHeight;

        const svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("preserveAspectRatio", "xMidYMid meet")
            ; 
        
        const defs = svg.append("defs");
            defs.append("filter")
                .attr("id", "drop-shadow")
                .append("feDropShadow")
                .attr("dx", 1)
                .attr("dy", 1)
                .attr("stdDeviation", 2);

        const zoom = d3.zoom()
            .scaleExtent([0.3, 2])
            .on("zoom", (event) => {
                svgGroup.attr("transform", event.transform);
            });

        const svgGroup = svg.append("g"); // group all elements here
        svg.call(zoom);


        const simulation = d3.forceSimulation(this.nodes)
            .force("link", d3.forceLink(this.links).id(d => d.id).distance(200))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svgGroup.append("g")
            .attr("stroke", "#aaa")
            .selectAll("line")
            .data(this.links)
            .join("line");

        const tooltip = d3.select(container)
            .append("div")
            .style("position", "absolute")
            .style("visibility", "hidden")
            .style("padding", "4px 8px")
            .style("background", "#333")
            .style("color", "#fff")
            .style("border-radius", "4px")
            .style("font-size", "12px");

        const node = svgGroup.append("g")
            .selectAll("g")
            .data(this.nodes)
            .join("g")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended))
            .each(function (d) {
                const el = d3.select(this);
                el.append("rect")
                    .attr("x", -65)
                    .attr("y", -50)
                    .attr("width", 130)
                    .attr("height", 100)
                    .attr("rx", 12)
                    .attr("fill", d.type === "parent" ? "#007bff" : "#28a745")
                    .attr("stroke", "#fff")
                    .attr("stroke-width", 1)
                    .attr("filter", "url(#drop-shadow)");
                el.style("cursor", "pointer");
                el.append("text")
                    .text(d.label)
                    .attr("text-anchor", "middle")
                    .attr("fill", "white")
                    .attr("font-size", 14)
                    .attr("y", 5)
                    .attr("pointer-events", "none");
                el.on("mouseover", (event, d) => {
                    tooltip.text(d.label).style("visibility", "visible");
                }).on("mousemove", (event) => {
                    tooltip
                        .style("top", (event.offsetY + 10) + "px")
                        .style("left", (event.offsetX + 10) + "px");
                }).on("mouseout", () => {
                    tooltip.style("visibility", "hidden");
                });
            });

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("transform", d => `translate(${d.x},${d.y})`);
        });

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    }
}

GoalGraph.template = "hyouman_goal.GoalGraph";
registry.category("actions").add("hyouman_goal.tag", GoalGraph);
