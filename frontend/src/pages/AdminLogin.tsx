import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { adminLogin } from "../api/client";

export default function AdminLogin() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await adminLogin(password);
      if (res.success && res.data) {
        sessionStorage.setItem("admin_token", res.data.token);
        navigate("/admin");
      } else {
        setError(res.error?.message ?? "Login failed");
      }
    } catch {
      setError("Failed to connect to server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-login">
      <form className="admin-login-form" onSubmit={handleSubmit}>
        <h1 className="admin-login-title">Admin Access</h1>
        <p className="admin-login-subtitle">
          Enter the admin password to continue.
        </p>

        <input
          type="password"
          className="admin-input"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoFocus
        />

        {error && <p className="admin-error">{error}</p>}

        <button
          type="submit"
          className="admin-btn"
          disabled={loading || !password}
        >
          {loading ? "Verifying…" : "Unlock"}
        </button>
      </form>
    </div>
  );
}
