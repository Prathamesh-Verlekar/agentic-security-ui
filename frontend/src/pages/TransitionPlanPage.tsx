import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchTransitionPlan } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { ErrorDetail, Region, TransitionPlan, TransitionStep } from "../types";

/* ─── Category config ──────────────────────────────────────────────────────── */
const CATEGORY_ICONS: Record<string, string> = {
  Education: "🎓",
  Certification: "📜",
  Course: "📚",
  Skill: "🛠️",
  Experience: "💼",
  Networking: "🤝",
  Portfolio: "📂",
};

const CATEGORY_COLORS: Record<string, { bg: string; border: string; text: string; glow: string }> = {
  Education:     { bg: "rgba(99,102,241,0.12)",  border: "#6366f1", text: "#a5b4fc", glow: "rgba(99,102,241,0.3)" },
  Certification: { bg: "rgba(245,158,11,0.12)",  border: "#f59e0b", text: "#fcd34d", glow: "rgba(245,158,11,0.3)" },
  Course:        { bg: "rgba(59,130,246,0.12)",   border: "#3b82f6", text: "#93c5fd", glow: "rgba(59,130,246,0.3)" },
  Skill:         { bg: "rgba(16,185,129,0.12)",   border: "#10b981", text: "#6ee7b7", glow: "rgba(16,185,129,0.3)" },
  Experience:    { bg: "rgba(236,72,153,0.12)",   border: "#ec4899", text: "#f9a8d4", glow: "rgba(236,72,153,0.3)" },
  Networking:    { bg: "rgba(139,92,246,0.12)",   border: "#8b5cf6", text: "#c4b5fd", glow: "rgba(139,92,246,0.3)" },
  Portfolio:     { bg: "rgba(6,182,212,0.12)",    border: "#06b6d4", text: "#67e8f9", glow: "rgba(6,182,212,0.3)" },
};

const PRIORITY_LABELS: Record<string, { label: string; color: string; bg: string }> = {
  required:    { label: "Required",    color: "#f87171", bg: "rgba(248,113,113,0.1)" },
  recommended: { label: "Recommended", color: "#fbbf24", bg: "rgba(251,191,36,0.1)" },
  optional:    { label: "Optional",    color: "#94a3b8", bg: "rgba(148,163,184,0.1)" },
};

const DIFFICULTY_LABELS: Record<string, { label: string; color: string }> = {
  easy:     { label: "Easy",     color: "#34d399" },
  moderate: { label: "Moderate", color: "#fbbf24" },
  hard:     { label: "Hard",     color: "#f87171" },
};

/* ─── Component ────────────────────────────────────────────────────────────── */

export default function TransitionPlanPage() {
  const [searchParams] = useSearchParams();
  const sourceId = searchParams.get("from") ?? "";
  const targetId = searchParams.get("to") ?? "";
  const region: Region = (searchParams.get("region") ?? "usa") === "india" ? "india" : "usa";

  const [plan, setPlan] = useState<TransitionPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  // Interactive state
  const [activeIdx, setActiveIdx] = useState(0); // person position
  const [popupIdx, setPopupIdx] = useState<number | null>(null); // open popup
  const trackRef = useRef<HTMLDivElement>(null);
  const popupRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!sourceId || !targetId) {
      setError({ message: "Both source and target professions are required." });
      setLoading(false);
      return;
    }
    setLoading(true);
    fetchTransitionPlan(sourceId, targetId, region)
      .then((res) => {
        if (res.success && res.data) {
          setPlan(res.data);
        } else {
          setError(res.error ?? { message: "Failed to generate transition plan" });
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, [sourceId, targetId, region]);

  // Close popup on click outside
  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (popupRef.current && !popupRef.current.contains(e.target as Node)) {
        setPopupIdx(null);
      }
    }
    if (popupIdx !== null) {
      document.addEventListener("mousedown", handleClick);
      return () => document.removeEventListener("mousedown", handleClick);
    }
  }, [popupIdx]);

  const handleMilestoneClick = useCallback((idx: number) => {
    setActiveIdx(idx);
    setPopupIdx((prev) => (prev === idx ? null : idx));
  }, []);

  if (loading) {
    return (
      <Loader message="Generating your personalized career roadmap… This may take a moment." />
    );
  }
  if (error) return <ErrorBanner error={error} />;
  if (!plan) return null;

  const diff = DIFFICULTY_LABELS[plan.difficulty] ?? DIFFICULTY_LABELS.moderate;
  // Total milestones: steps + finish
  const totalMilestones = plan.steps.length + 1;

  return (
    <div className="tp-page">
      <Link to={`/careers?region=${region}`} className="back-link">
        &larr; Back to Careers
      </Link>

      {/* ── Hero ──────────────────────────────────────────────────────── */}
      <div className="tp-hero">
        <div className="tp-hero-route">
          <Link to={`/careers/${plan.source_id}?region=${region}`} className="tp-hero-profession">
            {plan.source_title}
          </Link>
          <span className="tp-hero-arrow">→</span>
          <Link to={`/careers/${plan.target_id}?region=${region}`} className="tp-hero-profession">
            {plan.target_title}
          </Link>
        </div>
        <h1 className="tp-hero-title">Career Transition Roadmap</h1>
        <p className="tp-hero-summary">{plan.summary}</p>

        <div className="tp-hero-meta">
          <div className="tp-meta-chip">
            <span className="tp-meta-label">Duration</span>
            <span className="tp-meta-value">{plan.estimated_duration}</span>
          </div>
          <div className="tp-meta-chip">
            <span className="tp-meta-label">Difficulty</span>
            <span className="tp-meta-value" style={{ color: diff.color }}>
              {diff.label}
            </span>
          </div>
          <div className="tp-meta-chip">
            <span className="tp-meta-label">Steps</span>
            <span className="tp-meta-value">{plan.steps.length}</span>
          </div>
        </div>
      </div>

      {/* ── Interactive Journey Track ─────────────────────────────────── */}
      <div className="journey-track-container" ref={trackRef}>
        {/* The horizontal rail */}
        <div className="journey-rail">
          {/* Progress fill */}
          <div
            className="journey-rail-fill"
            style={{ width: `${(activeIdx / (totalMilestones - 1)) * 100}%` }}
          />
        </div>

        {/* Person avatar — positioned along the rail */}
        <div
          className="journey-person"
          style={{ left: `${(activeIdx / (totalMilestones - 1)) * 100}%` }}
        >
          <span className="journey-person-icon">🚶</span>
        </div>

        {/* Milestone nodes */}
        <div className="journey-milestones">
          {plan.steps.map((step, idx) => {
            const cat = CATEGORY_COLORS[step.category] ?? CATEGORY_COLORS.Skill;
            const icon = CATEGORY_ICONS[step.category] ?? "📌";
            const isActive = idx === activeIdx;
            const isCompleted = idx < activeIdx;

            return (
              <button
                key={step.order}
                className={`journey-milestone ${isActive ? "active" : ""} ${isCompleted ? "completed" : ""}`}
                style={{
                  left: `${(idx / (totalMilestones - 1)) * 100}%`,
                  borderColor: isActive ? cat.border : isCompleted ? "#34d399" : "#334155",
                  background: isActive ? cat.bg : isCompleted ? "rgba(52,211,153,0.1)" : "#111827",
                  boxShadow: isActive ? `0 0 20px ${cat.glow}` : "none",
                }}
                onClick={() => handleMilestoneClick(idx)}
                title={step.title}
              >
                <span className="journey-milestone-icon">
                  {isCompleted ? "✓" : icon}
                </span>
              </button>
            );
          })}

          {/* Finish milestone */}
          <button
            className={`journey-milestone finish ${activeIdx === plan.steps.length ? "active" : ""} ${activeIdx > plan.steps.length ? "completed" : ""}`}
            style={{
              left: "100%",
              borderColor: activeIdx >= plan.steps.length ? "#34d399" : "#334155",
              background: activeIdx >= plan.steps.length ? "rgba(52,211,153,0.15)" : "#111827",
              boxShadow: activeIdx >= plan.steps.length ? "0 0 20px rgba(52,211,153,0.3)" : "none",
            }}
            onClick={() => handleMilestoneClick(plan.steps.length)}
            title={`Ready for ${plan.target_title}!`}
          >
            <span className="journey-milestone-icon">🎉</span>
          </button>
        </div>

        {/* Labels under milestones */}
        <div className="journey-labels">
          {plan.steps.map((step, idx) => {
            const cat = CATEGORY_COLORS[step.category] ?? CATEGORY_COLORS.Skill;
            return (
              <span
                key={idx}
                className={`journey-label ${idx === activeIdx ? "active" : ""}`}
                style={{
                  left: `${(idx / (totalMilestones - 1)) * 100}%`,
                  color: idx === activeIdx ? cat.text : "#64748b",
                }}
              >
                {step.title.length > 18 ? step.title.slice(0, 16) + "…" : step.title}
              </span>
            );
          })}
          <span
            className={`journey-label ${activeIdx === plan.steps.length ? "active" : ""}`}
            style={{
              left: "100%",
              color: activeIdx === plan.steps.length ? "#34d399" : "#64748b",
            }}
          >
            🎉 Done
          </span>
        </div>
      </div>

      {/* ── Popup Detail ──────────────────────────────────────────────── */}
      {popupIdx !== null && (
        <div className="journey-popup-overlay">
          <div className="journey-popup" ref={popupRef}>
            <button className="journey-popup-close" onClick={() => setPopupIdx(null)}>
              &times;
            </button>
            {popupIdx < plan.steps.length ? (
              <StepPopup step={plan.steps[popupIdx]} />
            ) : (
              <div className="journey-popup-finish">
                <div className="journey-popup-finish-icon">🎉</div>
                <h3>Ready for {plan.target_title}!</h3>
                <p>
                  You've mapped out all the milestones. Time to update your
                  resume, start applying, and land your dream role.
                </p>
                <Link
                  to={`/careers/${plan.target_id}?region=${region}`}
                  className="journey-popup-link"
                  onClick={() => setPopupIdx(null)}
                >
                  Explore {plan.target_title} →
                </Link>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── Step List (scrollable summary below the journey) ──────────── */}
      <div className="journey-steps-list">
        <h2 className="journey-steps-list-title">All Milestones</h2>
        <p className="journey-steps-list-hint">
          Click any milestone on the path above — or tap a card below to see details.
        </p>
        <div className="journey-steps-grid">
          {plan.steps.map((step, idx) => {
            const cat = CATEGORY_COLORS[step.category] ?? CATEGORY_COLORS.Skill;
            const icon = CATEGORY_ICONS[step.category] ?? "📌";
            const isActive = idx === activeIdx;
            const isCompleted = idx < activeIdx;

            return (
              <button
                key={step.order}
                className={`journey-step-card ${isActive ? "active" : ""} ${isCompleted ? "completed" : ""}`}
                style={{ borderTopColor: cat.border }}
                onClick={() => handleMilestoneClick(idx)}
              >
                <div className="journey-step-card-head">
                  <span className="journey-step-card-icon">{isCompleted ? "✓" : icon}</span>
                  <span className="journey-step-card-order">Step {step.order}</span>
                  <span className="journey-step-card-dur">{step.duration}</span>
                </div>
                <h4 className="journey-step-card-title">{step.title}</h4>
                <span
                  className="journey-step-card-cat"
                  style={{ color: cat.text, background: cat.bg }}
                >
                  {step.category}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Tips ──────────────────────────────────────────────────────── */}
      {plan.tips.length > 0 && (
        <div className="tp-tips">
          <h2 className="tp-tips-title">💡 Transition Tips</h2>
          <div className="tp-tips-grid">
            {plan.tips.map((tip, i) => (
              <div key={i} className="tp-tip-card">
                <span className="tp-tip-number">{i + 1}</span>
                <p className="tp-tip-text">{tip}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Footer ────────────────────────────────────────────────────── */}
      <div className="tp-footer-cta">
        <Link to={`/careers/${plan.target_id}?region=${region}`} className="tp-footer-link primary">
          Learn more about {plan.target_title} →
        </Link>
        <Link to={`/careers?region=${region}`} className="tp-footer-link secondary">
          ← Plan a different transition
        </Link>
      </div>
    </div>
  );
}

/* ─── Step Popup Content ───────────────────────────────────────────────────── */

function StepPopup({ step }: { step: TransitionStep }) {
  const cat = CATEGORY_COLORS[step.category] ?? CATEGORY_COLORS.Skill;
  const icon = CATEGORY_ICONS[step.category] ?? "📌";
  const priority = PRIORITY_LABELS[step.priority] ?? PRIORITY_LABELS.required;

  return (
    <div className="journey-popup-content">
      <div className="journey-popup-header">
        <span className="journey-popup-icon" style={{ background: cat.bg, borderColor: cat.border }}>
          {icon}
        </span>
        <div>
          <h3 className="journey-popup-title">{step.title}</h3>
          <div className="journey-popup-pills">
            <span className="journey-popup-pill" style={{ color: cat.text, background: cat.bg }}>
              {step.category}
            </span>
            <span className="journey-popup-pill" style={{ color: "#8892b0", background: "#0d1117" }}>
              ⏱ {step.duration}
            </span>
            <span
              className="journey-popup-pill"
              style={{ color: priority.color, background: priority.bg, border: `1px solid ${priority.color}33` }}
            >
              {priority.label}
            </span>
          </div>
        </div>
      </div>

      <p className="journey-popup-desc">{step.description}</p>

      {step.resources.length > 0 && (
        <div className="journey-popup-resources">
          <h4 className="journey-popup-resources-title">📎 Recommended Resources</h4>
          <ul className="journey-popup-resources-list">
            {step.resources.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="journey-popup-step-badge">
        Step {step.order}
      </div>
    </div>
  );
}
