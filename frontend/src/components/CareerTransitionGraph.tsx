import { useCallback, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
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
import type { CareerTransitionEdge, Profession } from "../types";

/* ─── Difficulty colors ──────────────────────────────────────────────────── */
const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "#22c55e",
  moderate: "#f59e0b",
  hard: "#ef4444",
};

/* ─── Circular layout positions for 10 professions ───────────────────────── */
function computePositions(count: number, cx: number, cy: number, rx: number, ry: number) {
  return Array.from({ length: count }, (_, i) => {
    const angle = (2 * Math.PI * i) / count - Math.PI / 2;
    return { x: cx + rx * Math.cos(angle), y: cy + ry * Math.sin(angle) };
  });
}

/* ─── Profession Node ────────────────────────────────────────────────────── */
function ProfessionNode({ data }: NodeProps) {
  const highlighted = data.highlighted as boolean;
  const emoji = (data.emoji as string) || "";
  const label = (data.label as string) || "";

  return (
    <div
      className={`transition-node ${highlighted ? "highlighted" : ""}`}
      style={{
        border: highlighted ? "2px solid #10b981" : "2px solid #334155",
        boxShadow: highlighted
          ? "0 0 24px rgba(16,185,129,0.35), 0 4px 12px rgba(0,0,0,0.4)"
          : "0 2px 8px rgba(0,0,0,0.3)",
      }}
    >
      <Handle type="target" position={Position.Top} style={{ opacity: 0, width: 1, height: 1 }} />
      <Handle type="target" position={Position.Left} id="left-in" style={{ opacity: 0, width: 1, height: 1 }} />
      <Handle type="target" position={Position.Right} id="right-in" style={{ opacity: 0, width: 1, height: 1 }} />
      <Handle type="target" position={Position.Bottom} id="bottom-in" style={{ opacity: 0, width: 1, height: 1 }} />

      <div className="transition-node-emoji">{emoji}</div>
      <div className="transition-node-label">{label}</div>

      <Handle type="source" position={Position.Bottom} style={{ opacity: 0, width: 1, height: 1 }} />
      <Handle type="source" position={Position.Left} id="left-out" style={{ opacity: 0, width: 1, height: 1 }} />
      <Handle type="source" position={Position.Right} id="right-out" style={{ opacity: 0, width: 1, height: 1 }} />
      <Handle type="source" position={Position.Top} id="top-out" style={{ opacity: 0, width: 1, height: 1 }} />
    </div>
  );
}

const nodeTypes = { profession: ProfessionNode };

/* ─── Props ──────────────────────────────────────────────────────────────── */
interface Props {
  professions: Profession[];
  transitions: CareerTransitionEdge[];
}

export default function CareerTransitionGraphView({ professions, transitions }: Props) {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const navigate = useNavigate();

  const positions = useMemo(
    () => computePositions(professions.length, 450, 350, 380, 300),
    [professions.length]
  );

  // Determine which edges are connected to the selected node
  const connectedEdgeIds = useMemo(() => {
    if (!selectedNode) return new Set<string>();
    return new Set(
      transitions
        .filter((e) => e.source === selectedNode || e.target === selectedNode)
        .map((e) => e.id)
    );
  }, [selectedNode, transitions]);

  const connectedNodeIds = useMemo(() => {
    if (!selectedNode) return new Set<string>();
    const ids = new Set<string>([selectedNode]);
    transitions.forEach((e) => {
      if (e.source === selectedNode) ids.add(e.target);
      if (e.target === selectedNode) ids.add(e.source);
    });
    return ids;
  }, [selectedNode, transitions]);

  const rfNodes: Node[] = professions.map((p, i) => ({
    id: p.id,
    type: "profession",
    position: positions[i],
    data: {
      label: p.title,
      emoji: p.icon_emoji,
      highlighted: selectedNode ? connectedNodeIds.has(p.id) : false,
    },
  }));

  const rfEdges: Edge[] = transitions.map((e) => {
    const isActive = selectedNode ? connectedEdgeIds.has(e.id) : true;
    const color = DIFFICULTY_COLORS[e.difficulty] ?? DIFFICULTY_COLORS.moderate;

    return {
      id: e.id,
      source: e.source,
      target: e.target,
      type: "default",
      animated: isActive && (selectedNode !== null),
      label: isActive ? `${e.label} (${e.stage})` : "",
      style: {
        stroke: isActive ? color : "#1e2740",
        strokeWidth: isActive ? 2 : 0.8,
        opacity: isActive ? 1 : 0.25,
      },
      labelStyle: {
        fill: isActive ? "#e2e8f0" : "transparent",
        fontSize: 9.5,
        fontWeight: 500,
      },
      labelBgStyle: {
        fill: "#0b0f19",
        fillOpacity: isActive ? 0.92 : 0,
        rx: 4,
        ry: 4,
      },
      labelBgPadding: [5, 3] as [number, number],
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 14,
        height: 14,
        color: isActive ? color : "#1e2740",
      },
    };
  });

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      setSelectedNode((prev) => (prev === node.id ? null : node.id));
    },
    []
  );

  const onNodeDoubleClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      navigate(`/careers/${node.id}`);
    },
    [navigate]
  );

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
  }, []);

  const onInit = useCallback((instance: { fitView: () => void }) => {
    setTimeout(() => instance.fitView(), 100);
  }, []);

  return (
    <div className="transition-graph-wrapper">
      <div className="transition-graph-container">
        <ReactFlow
          nodes={rfNodes}
          edges={rfEdges}
          nodeTypes={nodeTypes}
          onNodeClick={onNodeClick}
          onNodeDoubleClick={onNodeDoubleClick}
          onPaneClick={onPaneClick}
          onInit={onInit}
          fitView
          fitViewOptions={{ padding: 0.15 }}
          attributionPosition="bottom-left"
          proOptions={{ hideAttribution: true }}
          minZoom={0.3}
          maxZoom={2}
        >
          <Background variant={BackgroundVariant.Dots} color="#1e2740" gap={24} size={1.5} />
          <Controls
            style={{
              background: "#131825",
              border: "1px solid #1e2740",
              borderRadius: "8px",
            }}
          />
          <MiniMap
            nodeColor={() => "#10b981"}
            maskColor="rgba(11, 15, 25, 0.85)"
            style={{
              background: "#131825",
              border: "1px solid #1e2740",
              borderRadius: "8px",
            }}
          />
        </ReactFlow>
      </div>

      <div className="transition-legend">
        <span className="transition-legend-item">
          <span className="transition-legend-dot" style={{ background: "#22c55e" }} />
          Easy Transition
        </span>
        <span className="transition-legend-item">
          <span className="transition-legend-dot" style={{ background: "#f59e0b" }} />
          Moderate Transition
        </span>
        <span className="transition-legend-item">
          <span className="transition-legend-dot" style={{ background: "#ef4444" }} />
          Hard Transition
        </span>
      </div>

      <p className="transition-hint">
        Click a profession to highlight its transition paths. Double-click to view full details.
      </p>
    </div>
  );
}
