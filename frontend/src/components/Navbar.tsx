import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();

  const linkClass = (path: string) =>
    `nav-link ${pathname.startsWith(path) ? "active" : ""}`;

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <span className="brand-icon">&#x2728;</span> AI Tools
      </Link>
      <div className="nav-links">
        <Link to="/guardrails" className={linkClass("/guardrails")}>
          Guardrails
        </Link>
        <Link to="/evals" className={linkClass("/evals")}>
          Evals
        </Link>
        <Link to="/careers" className={linkClass("/careers")}>
          Careers
        </Link>
      </div>
    </nav>
  );
}
