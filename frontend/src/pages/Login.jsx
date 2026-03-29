import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { getErrorMessage } from "../services/api";
import "../styles/Login.css";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      await login(form);
      navigate("/dashboard", { replace: true });
    } catch (loginError) {
      setError(
        getErrorMessage(loginError, "Não foi possivel autenticar o acesso."),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <div className="logo">BluERP</div>
          <h1>Acessar o sistema</h1>
          <p>
            Entre com suas credenciais para acessar os módulos de gestão da
            plataforma.
          </p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          {error ? <div className="error-message">{error}</div> : null}

          <div className="form-group">
            <label htmlFor="email">E-mail</label>
            <input
              autoComplete="username"
              id="email"
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  email: event.target.value,
                }))
              }
              required
              type="email"
              value={form.email}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Senha</label>
            <input
              autoComplete="current-password"
              id="password"
              onChange={(event) =>
                setForm((current) => ({
                  ...current,
                  password: event.target.value,
                }))
              }
              required
              type="password"
              value={form.password}
            />
          </div>

          <button className="login-btn" disabled={loading} type="submit">
            {loading ? "Entrando..." : "Entrar"}
          </button>
        </form>
      </div>
    </div>
  );
}
