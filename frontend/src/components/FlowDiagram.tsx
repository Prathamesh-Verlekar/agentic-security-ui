import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import type { DiagramEdge, DiagramNode } from "../types";

interface Props {
  nodes: DiagramNode[];
  edges: DiagramEdge[];
}

export default function FlowDiagram({ nodes, edges }: Props) {
  const rfNodes: Node[] = nodes.map((n) => ({
    id: n.id,
    type: n.node_type === "input" ? "input" : n.node_type === "output" ? "output" : "default",
    position: { x: n.x, y: n.y },
    data: { label: n.label },
    style: {
      background: n.node_type === "input"
        ? "#3b82f6"
        : n.node_type === "output"
          ? "#8b5cf6"
          : "#1e293b",
      color: "#e2e8f0",
      border: "1px solid #334155",
      borderRadius: "8px",
      padding: "10px 16px",
      fontSize: "13px",
      fontWeight: 600,
    },
  }));

  const rfEdges: Edge[] = edges.map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
    label: e.label,
    animated: e.animated,
    style: { stroke: "#6366f1", strokeWidth: 2 },
    labelStyle: { fill: "#a5b4fc", fontSize: 11, fontWeight: 500 },
    labelBgStyle: { fill: "#0b0f19", fillOpacity: 0.85 },
  }));

  return (
    <div className="flow-diagram-container">
      <ReactFlow
        nodes={rfNodes}
        edges={rfEdges}
        fitView
        attributionPosition="bottom-left"
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#1e2740" gap={20} />
        <Controls
          style={{ background: "#131825", border: "1px solid #1e2740", borderRadius: "8px" }}
        />
        <MiniMap
          nodeColor={() => "#6366f1"}
          maskColor="rgba(11, 15, 25, 0.8)"
          style={{ background: "#131825", border: "1px solid #1e2740", borderRadius: "8px" }}
        />
      </ReactFlow>
    </div>
  );
}
