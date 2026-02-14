import { useCallback } from "react";
import {
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  ReactFlow,
  MarkerType,
  type Edge,
  type Node,
  type NodeProps,
  Handle,
  Position,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import type { DiagramEdge, DiagramNode } from "../types";

/* ─── Color palette per node type ─────────────────────────────────────────── */
const NODE_COLORS: Record<string, { bg: string; border: string; accent: string }> = {
  input:    { bg: "#0c2d6b", border: "#3b82f6", accent: "#60a5fa" },
  output:   { bg: "#3b1a6b", border: "#8b5cf6", accent: "#a78bfa" },
  decision: { bg: "#4a1d1d", border: "#ef4444", accent: "#f87171" },
  default:  { bg: "#111827", border: "#334155", accent: "#94a3b8" },
};

/* ─── Custom Node Component ───────────────────────────────────────────────── */
function CustomNode({ data }: NodeProps) {
  const nodeType = (data.nodeType as string) || "default";
  const colors = NODE_COLORS[nodeType] || NODE_COLORS.default;
  const description = (data.description as string) || "";
  const label = (data.label as string) || "";

  const icon =
    nodeType === "input" ? "▶" :
    nodeType === "output" ? "✓" :
    nodeType === "decision" ? "◆" : "●";

  return (
    <div
      style={{
        background: colors.bg,
        border: `2px solid ${colors.border}`,
        borderRadius: nodeType === "decision" ? "12px" : "10px",
        padding: "12px 18px",
        minWidth: "160px",
        maxWidth: "220px",
        boxShadow: `0 0 20px ${colors.border}33, 0 4px 12px rgba(0,0,0,0.4)`,
      }}
    >
      <Handle type="target" position={Position.Top} style={{ background: colors.border, width: 8, height: 8, border: "2px solid #0b0f19" }} />

      <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: description ? "6px" : 0 }}>
        <span style={{ fontSize: "10px", color: colors.accent }}>{icon}</span>
        <span style={{ fontSize: "13px", fontWeight: 700, color: "#e2e8f0", lineHeight: 1.3 }}>
          {label}
        </span>
      </div>

      {description && (
        <div style={{ fontSize: "10.5px", color: "#8b95a9", lineHeight: 1.45 }}>
          {description}
        </div>
      )}

      <Handle type="source" position={Position.Bottom} style={{ background: colors.border, width: 8, height: 8, border: "2px solid #0b0f19" }} />
    </div>
  );
}

const nodeTypes = { custom: CustomNode };

/* ─── Edge color by type ──────────────────────────────────────────────────── */
function edgeColor(animated: boolean): string {
  return animated ? "#6366f1" : "#475569";
}

/* ─── Props ───────────────────────────────────────────────────────────────── */
interface Props {
  nodes: DiagramNode[];
  edges: DiagramEdge[];
}

export default function FlowDiagram({ nodes, edges }: Props) {
  const rfNodes: Node[] = nodes.map((n) => ({
    id: n.id,
    type: "custom",
    position: { x: n.x, y: n.y },
    data: {
      label: n.label,
      description: n.description || "",
      nodeType: n.node_type,
    },
  }));

  const rfEdges: Edge[] = edges.map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
    type: e.edge_type === "bezier" ? "default" : e.edge_type === "straight" ? "straight" : "smoothstep",
    animated: e.animated,
    label: e.label,
    style: {
      stroke: edgeColor(e.animated),
      strokeWidth: e.animated ? 2.5 : 1.5,
      strokeDasharray: e.animated ? undefined : "6 3",
    },
    labelStyle: {
      fill: e.animated ? "#c7d2fe" : "#64748b",
      fontSize: 10.5,
      fontWeight: 600,
      letterSpacing: "0.02em",
    },
    labelBgStyle: {
      fill: "#0b0f19",
      fillOpacity: 0.92,
      rx: 4,
      ry: 4,
    },
    labelBgPadding: [6, 4] as [number, number],
    markerEnd: {
      type: MarkerType.ArrowClosed,
      width: 16,
      height: 16,
      color: edgeColor(e.animated),
    },
  }));

  const onInit = useCallback((instance: { fitView: () => void }) => {
    setTimeout(() => instance.fitView(), 100);
  }, []);

  return (
    <div className="flow-diagram-container">
      <ReactFlow
        nodes={rfNodes}
        edges={rfEdges}
        nodeTypes={nodeTypes}
        onInit={onInit}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        attributionPosition="bottom-left"
        proOptions={{ hideAttribution: true }}
        minZoom={0.3}
        maxZoom={2}
        defaultEdgeOptions={{
          type: "smoothstep",
        }}
      >
        <Background
          variant={BackgroundVariant.Dots}
          color="#1e2740"
          gap={24}
          size={1.5}
        />
        <Controls
          style={{
            background: "#131825",
            border: "1px solid #1e2740",
            borderRadius: "8px",
          }}
        />
        <MiniMap
          nodeColor={() => "#6366f1"}
          maskColor="rgba(11, 15, 25, 0.85)"
          style={{
            background: "#131825",
            border: "1px solid #1e2740",
            borderRadius: "8px",
          }}
        />
      </ReactFlow>
    </div>
  );
}
