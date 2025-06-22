/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class GoalGraph extends Component {
    setup() {
        this.container = useRef("mapContainer");
        this.rpc = useService("rpc");

        onWillStart(async () => {
            const { nodes, links } = await this.rpc("/goal/graph");
            // this.nodes = nodes;
            // this.links = links;
            this.nodes = Array.isArray(nodes) ? nodes : [];
            this.links = Array.isArray(links) ? links : [];
        });

        onMounted(() => this.renderGraph());
    }

    renderGraph() {
        const container = this.container.el;
        const width = container.clientWidth;
        const height = container.clientHeight;

        const svg = d3.select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height);

        const simulation = d3.forceSimulation(this.nodes)
            .force("link", d3.forceLink(this.links).id(d => d.id).distance(150))
            // .force("link", d3.forceLink(this.links).id(d => String(d.id)).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g")
            .attr("stroke", "#aaa")
            .selectAll("line")
            .data(this.links)
            .join("line");

        // const node = svg.append("g")
        //     .selectAll("circle")
        //     .data(this.nodes)
        //     .join("circle")
        //     .attr("r", 20)
        //     .attr("fill", "#5A9")
        //     .call(d3.drag()
        //         .on("start", dragstarted)
        //         .on("drag", dragged)
        //         .on("end", dragended));
        const node = svg.append("g")
            .selectAll("g")
            .data(this.nodes)
            .join("g")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended))
            .each(function (d) {
                const el = d3.select(this);
                if (d.type === "parent") {
                    el.append("rect")
                        .attr("x", -40)
                        .attr("y", -25)
                        .attr("width", 130)
                        .attr("height", 100)
                        .attr("rx", 10)
                        .attr("fill", "#007bff");
                } else {
                    el.append("rect")
                        .attr("r", 25)
                        .attr("width", 130)
                        .attr("height", 100)
                        .attr("fill", "#28a745");
                }

                // Text wrapping
                // const maxWidth = d.type === "parent" ? 130 : 100;
                // const maxLines = 4;
                // const words = d.label.split(/\s+/);
                // let lines = [], currentLine = [];

                // const temp = el.append("text")
                //     .attr("font-size", 12)
                //     .attr("visibility", "hidden");

                // words.forEach(word => {
                //     currentLine.push(word);
                //     temp.text(currentLine.join(" "));
                //     if (temp.node().getComputedTextLength() > maxWidth) {
                //         currentLine.pop();
                //         lines.push(currentLine.join(" "));
                //         currentLine = [word];
                //     }
                // });
                // if (currentLine.length) lines.push(currentLine.join(" "));
                // temp.remove();

                // if (lines.length > maxLines) {
                //     lines = lines.slice(0, maxLines);
                //     const last = lines[lines.length - 1];
                //     lines[lines.length - 1] = last.slice(0, -3) + "…";
                // }

                // lines.forEach((line, i) => {
                //     el.append("text")
                //         .text(line)
                //         .attr("text-anchor", "middle")
                //         .attr("fill", "white")
                //         .attr("font-size", 12)
                //         .attr("y", (i - (lines.length - 1) / 2) * 14);
                // });
            });



        const label = svg.append("g")
            .selectAll("text")
            .data(this.nodes)
            .join("text")
            .text(d => d.label)
            .attr("font-size", 12)
            .attr("dx", 5)
            .attr("dy", 5);

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("transform", d => `translate(${d.x},${d.y})`);
            label.attr("x", d => d.x).attr("y", d => d.y);
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
