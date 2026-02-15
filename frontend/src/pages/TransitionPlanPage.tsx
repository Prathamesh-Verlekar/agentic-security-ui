import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchTransitionPlan } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { ErrorDetail, TransitionPlan } from "../types";

/* ─── Category icon map ────────────────────────────────────────────────────── */
const CATEGORY_ICONS: Record<string, string> = {
  Education: "🎓",
  Certification: "📜",
  Course: "📚",
  Skill: "🛠️",
  Experience: "💼",
  Networking: "🤝",
  Portfolio: "📂",
};

const CATEGORY_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  Education:     { bg: "rgba(99,102,241,0.10)",  border: "#6366f1", text: "#a5b4fc" },
  Certification: { bg: "rgba(245,158,11,0.10)",  border: "#f59e0b", text: "#fcd34d" },
  Course:        { bg: "rgba(59,130,246,0.10)",   border: "#3b82f6", text: "#93c5fd" },
  Skill:         { bg: "rgba(16,185,129,0.10)",   border: "#10b981", text: "#6ee7b7" },
  Experience:    { bg: "rgba(236,72,153,0.10)",   border: "#ec4899", text: "#f9a8d4" },
  Networking:    { bg: "rgba(139,92,246,0.10)",   border: "#8b5cf6", text: "#c4b5fd" },
  Portfolio:     { bg: "rgba(6,182,212,0.10)",    border: "#06b6d4", text: "#67e8f9" },
};

const PRIORITY_BADGES: Record<string, { label: string; className: string }> = {
  required:    { label: "Required",    className: "tp-badge-required" },
  recommended: { label: "Recommended", className: "tp-badge-recommended" },
  optional:    { label: "Optional",    className: "tp-badge-optional" },
};

const DIFFICULTY_LABELS: Record<string, { label: string; color: string }> = {
  easy:     { label: "Easy",     color: "#34d399" },
  moderate: { label: "Moderate", color: "#fbbf24" },
  hard:     { label: "Hard",     color: "#f87171" },
};

export default function TransitionPlanPage() {
  const [searchParams] = useSearchParams();
  const sourceId = searchParams.get("from") ?? "";
  const targetId = searchParams.get("to") ?? "";

  const [plan, setPlan] = useState<TransitionPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  useEffect(() => {
    if (!sourceId || !targetId) {
      setError({ message: "Both source and target professions are required." });
      setLoading(false);
      return;
    }

    setLoading(true);
    fetchTransitionPlan(sourceId, targetId)
      .then((res) => {
        if (res.success && res.data) {
          setPlan(res.data);
        } else {
          setError(res.error ?? { message: "Failed to generate transition plan" });
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, [sourceId, targetId]);

  if (loading) {
    return (
      <Loader message="Generating your personalized career roadmap… This may take a moment." />
    );
  }
  if (error) return <ErrorBanner error={error} />;
  if (!plan) return null;

  const diff = DIFFICULTY_LABELS[plan.difficulty] ?? DIFFICULTY_LABELS.moderate;

  return (
    <div className="tp-page">
      <Link to="/careers" className="back-link">
        &larr; Back to Careers
      </Link>

      {/* ── Hero ──────────────────────────────────────────────────────── */}
      <div className="tp-hero">
        <div className="tp-hero-route">
          <Link to={`/careers/${plan.source_id}`} className="tp-hero-profession">
            {plan.source_title}
          </Link>
          <span className="tp-hero-arrow">→</span>
          <Link to={`/careers/${plan.target_id}`} className="tp-hero-profession">
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

      {/* ── Timeline ──────────────────────────────────────────────────── */}
      <div className="tp-timeline">
        {plan.steps.map((step, idx) => {
          const catColor = CATEGORY_COLORS[step.category] ?? CATEGORY_COLORS.Skill;
          const catIcon = CATEGORY_ICONS[step.category] ?? "📌";
          const priority = PRIORITY_BADGES[step.priority] ?? PRIORITY_BADGES.required;
          const isLast = idx === plan.steps.length - 1;

          return (
            <div key={step.order} className="tp-step">
              {/* Timeline spine */}
              <div className="tp-step-spine">
                <div
                  className="tp-step-dot"
                  style={{ borderColor: catColor.border, background: catColor.bg }}
                >
                  <span className="tp-step-number">{step.order}</span>
                </div>
                {!isLast && (
                  <div className="tp-step-line" style={{ background: `linear-gradient(to bottom, ${catColor.border}66, #1a203544)` }} />
                )}
              </div>

              {/* Step content card */}
              <div
                className="tp-step-card"
                style={{ borderLeftColor: catColor.border }}
              >
                <div className="tp-step-card-header">
                  <span className="tp-step-icon">{catIcon}</span>
                  <div className="tp-step-header-text">
                    <h3 className="tp-step-title">{step.title}</h3>
                    <div className="tp-step-pills">
                      <span
                        className="tp-step-category"
                        style={{ color: catColor.text, background: catColor.bg }}
                      >
                        {step.category}
                      </span>
                      <span className="tp-step-duration">⏱ {step.duration}</span>
                      <span className={`tp-step-priority ${priority.className}`}>
                        {priority.label}
                      </span>
                    </div>
                  </div>
                </div>

                <p className="tp-step-desc">{step.description}</p>

                {step.resources.length > 0 && (
                  <div className="tp-step-resources">
                    <span className="tp-step-resources-label">Resources:</span>
                    {step.resources.map((r, ri) => (
                      <span key={ri} className="tp-step-resource">{r}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Finish marker */}
        <div className="tp-step tp-step-finish">
          <div className="tp-step-spine">
            <div className="tp-step-dot tp-step-dot-finish">
              <span className="tp-step-number">🎉</span>
            </div>
          </div>
          <div className="tp-step-card tp-finish-card">
            <h3 className="tp-step-title">Ready for {plan.target_title}!</h3>
            <p className="tp-step-desc">
              You've completed all the steps. Time to update your resume, start
              applying, and land your dream role.
            </p>
          </div>
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

      {/* ── Footer CTA ────────────────────────────────────────────────── */}
      <div className="tp-footer-cta">
        <Link to={`/careers/${plan.target_id}`} className="tp-footer-link primary">
          Learn more about {plan.target_title} →
        </Link>
        <Link to="/careers" className="tp-footer-link secondary">
          ← Plan a different transition
        </Link>
      </div>
    </div>
  );
}
