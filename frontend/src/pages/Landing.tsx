import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="landing">
      <div className="landing-hero">
        <h1 className="landing-title">Agentic Security</h1>
        <p className="landing-subtitle">
          Explore the essential building blocks for securing autonomous AI
          agents — from runtime guardrails to comprehensive evaluation suites.
        </p>
      </div>

      <div className="landing-cards">
        <Link to="/guardrails" className="landing-card guardrails-card">
          <div className="landing-card-icon">&#x1F6E1;</div>
          <h2>LLM Guardrails</h2>
          <p>
            Runtime defenses that validate, filter, and constrain every
            interaction between your agent and the outside world.
          </p>
          <span className="landing-card-cta">Explore Guardrails &rarr;</span>
        </Link>

        <Link to="/evals" className="landing-card evals-card">
          <div className="landing-card-icon">&#x1F4CA;</div>
          <h2>Evals</h2>
          <p>
            Systematic evaluations that measure correctness, safety, and
            robustness of your agent's behavior.
          </p>
          <span className="landing-card-cta">Explore Evals &rarr;</span>
        </Link>
      </div>
    </div>
  );
}
