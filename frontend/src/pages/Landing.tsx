import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="landing">
      <div className="landing-hero">
        <h1 className="landing-title">AI-Powered Tools</h1>
        <p className="landing-subtitle">
          A suite of intelligent tools — explore AI security building blocks or
          discover your ideal career path with an AI counselor.
        </p>
      </div>

      <div className="landing-cards">
        <Link to="/guardrails" className="landing-card guardrails-card">
          <div className="landing-card-icon">&#x1F6E1;</div>
          <h2>Agentic Security</h2>
          <p>
            Explore runtime guardrails and evaluation suites that secure
            autonomous AI agents and LLM-powered systems.
          </p>
          <span className="landing-card-cta">Explore Security &rarr;</span>
        </Link>

        <Link to="/careers" className="landing-card careers-card">
          <div className="landing-card-icon">&#x1F680;</div>
          <h2>Career Counselor</h2>
          <p>
            Discover top professions with AI-generated insights, career paths,
            and an interactive counselor to answer your questions.
          </p>
          <span className="landing-card-cta">Explore Careers &rarr;</span>
        </Link>
      </div>
    </div>
  );
}
