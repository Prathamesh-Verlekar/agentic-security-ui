import { useCallback, useMemo, useState } from "react";
import { Link } from "react-router-dom";
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

/* ─── Difficulty config ──────────────────────────────────────────────────── */
const DIFF_COLORS: Record<string, { color: string; bg: string; label: string }> = {
  easy:     { color: "#34d399", bg: "rgba(52,211,153,0.12)", label: "Easy" },
  moderate: { color: "#fbbf24", bg: "rgba(251,191,36,0.12)", label: "Moderate" },
  hard:     { color: "#f87171", bg: "rgba(248,113,113,0.12)", label: "Hard" },
};

/* ─── Node color palette (by index, wraps) ───────────────────────────────── */
const NODE_PALETTE = [
  { bg: "#0f2847", border: "#3b82f6", glow: "rgba(59,130,246,0.25)" },
  { bg: "#1a1040", border: "#8b5cf6", glow: "rgba(139,92,246,0.25)" },
  { bg: "#0d3331", border: "#10b981", glow: "rgba(16,185,129,0.25)" },
  { bg: "#2d1b0e", border: "#f59e0b", glow: "rgba(245,158,11,0.25)" },
  { bg: "#2d0e1b", border: "#ec4899", glow: "rgba(236,72,153,0.25)" },
  { bg: "#0e2d2d", border: "#06b6d4", glow: "rgba(6,182,212,0.25)" },
  { bg: "#1e1433", border: "#a78bfa", glow: "rgba(167,139,250,0.25)" },
  { bg: "#2d2d0e", border: "#84cc16", glow: "rgba(132,204,22,0.25)" },
];

/* ─── Ellipse layout for N nodes ─────────────────────────────────────────── */
function computePositions(count: number, cx: number, cy: number, rx: number, ry: number) {
  return Array.from({ length: count }, (_, i) => {
    const angle = (2 * Math.PI * i) / count - Math.PI / 2;
    return { x: cx + rx * Math.cos(angle), y: cy + ry * Math.sin(angle) };
  });
}

/* ─── Profession Node ────────────────────────────────────────────────────── */
function ProfessionNode({ data }: NodeProps) {
  const selected = data.selected as boolean;
  const dimmed = data.dimmed as boolean;
  const emoji = (data.emoji as string) || "";
  const label = (data.label as string) || "";
  const colorIdx = (data.colorIdx as number) || 0;
  const colors = NODE_PALETTE[colorIdx % NODE_PALETTE.length];

  const borderColor = selected ? "#ffffff" : dimmed ? "#1e2740" : colors.border;
  const opacity = dimmed ? 0.35 : 1;

  return (
    <div
      className="tg-node"
      style={{
        background: colors.bg,
        border: `2px solid ${borderColor}`,
        boxShadow: selected
          ? `0 0 28px ${colors.glow}, 0 0 0 3px ${colors.border}55`
          : dimmed
            ? "none"
            : `0 0 16px ${colors.glow}`,
        opacity,
        transform: selected ? "scale(1.08)" : "scale(1)",
      }}
    >
      <Handle type="target" position={Position.Top} style={{ opacity: 0 }} />
      <Handle type="target" position={Position.Left} id="l-in" style={{ opacity: 0 }} />
      <Handle type="target" position={Position.Right} id="r-in" style={{ opacity: 0 }} />
      <Handle type="target" position={Position.Bottom} id="b-in" style={{ opacity: 0 }} />

      <div className="tg-node-emoji">{emoji}</div>
      <div className="tg-node-label">{label}</div>

      <Handle type="source" position={Position.Bottom} style={{ opacity: 0 }} />
      <Handle type="source" position={Position.Left} id="l-out" style={{ opacity: 0 }} />
      <Handle type="source" position={Position.Right} id="r-out" style={{ opacity: 0 }} />
      <Handle type="source" position={Position.Top} id="t-out" style={{ opacity: 0 }} />
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

  /* ── Layout ──────────────────────────────────────────────────────────── */
  const positions = useMemo(
    () => computePositions(professions.length, 500, 420, 430, 360),
    [professions.length]
  );

  const profMap = useMemo(() => {
    const m = new Map<string, Profession>();
    professions.forEach((p) => m.set(p.id, p));
    return m;
  }, [professions]);

  /* ── Selected node's outgoing transitions ────────────────────────────── */
  const outgoing = useMemo(() => {
    if (!selectedNode) return [];
    return transitions
      .filter((e) => e.source === selectedNode)
      .map((e) => ({ edge: e, target: profMap.get(e.target) }))
      .filter((t) => t.target) as { edge: CareerTransitionEdge; target: Profession }[];
  }, [selectedNode, transitions, profMap]);

  const incoming = useMemo(() => {
    if (!selectedNode) return [];
    return transitions
      .filter((e) => e.target === selectedNode)
      .map((e) => ({ edge: e, source: profMap.get(e.source) }))
      .filter((t) => t.source) as { edge: CareerTransitionEdge; source: Profession }[];
  }, [selectedNode, transitions, profMap]);

  /* ── Connected node IDs ──────────────────────────────────────────────── */
  const connectedIds = useMemo(() => {
    if (!selectedNode) return null;
    const ids = new Set<string>([selectedNode]);
    transitions.forEach((e) => {
      if (e.source === selectedNode) ids.add(e.target);
      if (e.target === selectedNode) ids.add(e.source);
    });
    return ids;
  }, [selectedNode, transitions]);

  const connectedEdgeIds = useMemo(() => {
    if (!selectedNode) return null;
    return new Set(
      transitions
        .filter((e) => e.source === selectedNode || e.target === selectedNode)
        .map((e) => e.id)
    );
  }, [selectedNode, transitions]);

  /* ── Build React Flow nodes ──────────────────────────────────────────── */
  const rfNodes: Node[] = professions.map((p, i) => ({
    id: p.id,
    type: "profession",
    position: positions[i],
    data: {
      label: p.title,
      emoji: p.icon_emoji,
      colorIdx: i,
      selected: selectedNode === p.id,
      dimmed: connectedIds !== null && !connectedIds.has(p.id),
    },
  }));

  /* ── Build React Flow edges ──────────────────────────────────────────── */
  const rfEdges: Edge[] = transitions.map((e) => {
    const isActive = connectedEdgeIds === null || connectedEdgeIds.has(e.id);
    const isOutgoing = selectedNode !== null && e.source === selectedNode;
    const diff = DIFF_COLORS[e.difficulty] ?? DIFF_COLORS.moderate;

    return {
      id: e.id,
      source: e.source,
      target: e.target,
      type: "default",
      animated: isOutgoing,
      label: isActive ? e.label : "",
      style: {
        stroke: isActive ? diff.color : "#111827",
        strokeWidth: isOutgoing ? 3 : isActive ? 1.8 : 0.5,
        opacity: isActive ? 1 : 0.12,
      },
      labelStyle: {
        fill: isActive ? "#e2e8f0" : "transparent",
        fontSize: 9,
        fontWeight: 600,
      },
      labelBgStyle: {
        fill: "#0b0f19",
        fillOpacity: isActive ? 0.95 : 0,
        rx: 4,
        ry: 4,
      },
      labelBgPadding: [5, 3] as [number, number],
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: isOutgoing ? 18 : 12,
        height: isOutgoing ? 18 : 12,
        color: isActive ? diff.color : "#111827",
      },
    };
  });

  /* ── Handlers ────────────────────────────────────────────────────────── */
  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    setSelectedNode((prev) => (prev === node.id ? null : node.id));
  }, []);

  const onPaneClick = useCallback(() => setSelectedNode(null), []);

  const onInit = useCallback((instance: { fitView: () => void }) => {
    setTimeout(() => instance.fitView(), 100);
  }, []);

  const selectedProf = selectedNode ? profMap.get(selectedNode) : null;

  return (
    <div className="tg-wrapper">
      {/* ── Graph ──────────────────────────────────────────────────────── */}
      <div className="tg-graph-area">
        <div className="tg-container">
          <ReactFlow
            nodes={rfNodes}
            edges={rfEdges}
            nodeTypes={nodeTypes}
            onNodeClick={onNodeClick}
            onPaneClick={onPaneClick}
            onInit={onInit}
            fitView
            fitViewOptions={{ padding: 0.12 }}
            proOptions={{ hideAttribution: true }}
            minZoom={0.25}
            maxZoom={2.5}
          >
            <Background variant={BackgroundVariant.Dots} color="#1a2035" gap={22} size={1} />
            <Controls style={{ background: "#0d1117", border: "1px solid #1e2740", borderRadius: "8px" }} />
            <MiniMap
              nodeColor={(n) => {
                const ci = (n.data?.colorIdx as number) ?? 0;
                return NODE_PALETTE[ci % NODE_PALETTE.length].border;
              }}
              maskColor="rgba(11,15,25,0.88)"
              style={{ background: "#0d1117", border: "1px solid #1e2740", borderRadius: "8px" }}
            />
          </ReactFlow>
        </div>

        {/* Legend */}
        <div className="tg-legend">
          {Object.entries(DIFF_COLORS).map(([key, val]) => (
            <span key={key} className="tg-legend-item">
              <span className="tg-legend-dot" style={{ background: val.color }} />
              {val.label}
            </span>
          ))}
          <span className="tg-legend-item tg-legend-sep">|</span>
          <span className="tg-legend-item">Click node to drill down</span>
        </div>
      </div>

      {/* ── Drill-Down Panel ───────────────────────────────────────────── */}
      <div className={`tg-panel ${selectedNode ? "open" : ""}`}>
        {selectedProf ? (
          <>
            <div className="tg-panel-header">
              <span className="tg-panel-emoji">{selectedProf.icon_emoji}</span>
              <div>
                <h3 className="tg-panel-title">{selectedProf.title}</h3>
                <Link to={`/careers/${selectedProf.id}`} className="tg-panel-detail-link">
                  View full profile &rarr;
                </Link>
              </div>
              <button className="tg-panel-close" onClick={() => setSelectedNode(null)}>
                &times;
              </button>
            </div>

            {/* Outgoing */}
            {outgoing.length > 0 && (
              <div className="tg-panel-section">
                <h4 className="tg-panel-section-title">
                  Can transition to <span className="tg-count">{outgoing.length}</span>
                </h4>
                <div className="tg-panel-cards">
                  {outgoing.map((t) => {
                    const d = DIFF_COLORS[t.edge.difficulty];
                    return (
                      <Link
                        key={t.edge.id}
                        to={`/careers/${t.target.id}`}
                        className="tg-panel-card"
                        style={{ borderLeftColor: d.color }}
                      >
                        <div className="tg-panel-card-top">
                          <span className="tg-panel-card-emoji">{t.target.icon_emoji}</span>
                          <span className="tg-panel-card-name">{t.target.title}</span>
                        </div>
                        <div className="tg-panel-card-meta">
                          <span className="tg-panel-card-label">{t.edge.label}</span>
                          <span className="tg-panel-card-pills">
                            <span className="tg-pill stage">{t.edge.stage}</span>
                            <span className="tg-pill diff" style={{ color: d.color, background: d.bg }}>
                              {d.label}
                            </span>
                          </span>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Incoming */}
            {incoming.length > 0 && (
              <div className="tg-panel-section">
                <h4 className="tg-panel-section-title">
                  Can come from <span className="tg-count">{incoming.length}</span>
                </h4>
                <div className="tg-panel-cards">
                  {incoming.map((t) => {
                    const d = DIFF_COLORS[t.edge.difficulty];
                    return (
                      <div
                        key={t.edge.id}
                        className="tg-panel-card incoming"
                        style={{ borderLeftColor: d.color }}
                      >
                        <div className="tg-panel-card-top">
                          <span className="tg-panel-card-emoji">{t.source.icon_emoji}</span>
                          <span className="tg-panel-card-name">{t.source.title}</span>
                        </div>
                        <div className="tg-panel-card-meta">
                          <span className="tg-panel-card-label">{t.edge.label}</span>
                          <span className="tg-panel-card-pills">
                            <span className="tg-pill stage">{t.edge.stage}</span>
                            <span className="tg-pill diff" style={{ color: d.color, background: d.bg }}>
                              {d.label}
                            </span>
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="tg-panel-empty">
            <p>Click any profession on the graph to explore transition paths.</p>
          </div>
        )}
      </div>
    </div>
  );
}
