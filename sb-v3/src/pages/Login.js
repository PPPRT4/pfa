import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

/* ── Icons ── */
const IconArrow = () => (
  <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
    <path d="M2 7.5h11M9 4l4 3.5L9 11" stroke="currentColor" strokeWidth="1.5"
      strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const IconUser = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <circle cx="7" cy="4.5" r="2.5" stroke="currentColor" strokeWidth="1.25" />
    <path d="M1.5 12.5c0-3.04 2.46-5.5 5.5-5.5s5.5 2.46 5.5 5.5" stroke="currentColor"
      strokeWidth="1.25" strokeLinecap="round" />
  </svg>
);

const IconEyeOff = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M1 7S3.5 2.5 7 2.5 13 7 13 7 10.5 11.5 7 11.5 1 7 1 7z"
      stroke="currentColor" strokeWidth="1.25" />
    <circle cx="7" cy="7" r="1.75" stroke="currentColor" strokeWidth="1.25" />
  </svg>
);

const IconEyeOn = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M1 1l12 12M5.6 5.1A2.25 2.25 0 009 8.5M1 7S3.5 2.5 7 2.5c.9 0 1.75.22 2.5.6M13 7c-.7 1.5-2.2 3-4 3.9"
      stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
  </svg>
);

const IconCheck = () => (
  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
    <path d="M2.5 6.5l3 3 5-5" stroke="currentColor" strokeWidth="1.5"
      strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const FEATURES = [
  "AI auto-classification & summaries",
  "Smart keyword extraction",
  "Filter & search your notes",
  "Backend API sync",
];

/* ── FieldGroup ── */
function FieldGroup({ label, id, rightSlot, children, error }) {
  return (
    <div className="mb-5">
      <div className="flex items-center justify-between mb-1.5">
        <label htmlFor={id}
          className="text-xs font-semibold uppercase tracking-widest text-ink-400">
          {label}
        </label>
        {rightSlot}
      </div>
      {children}
      {error && (
        <p className="mt-1.5 text-xs text-red-400 flex items-center gap-1 animate-fade-up">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <circle cx="6" cy="6" r="5" stroke="currentColor" strokeWidth="1.25" />
            <path d="M6 4v2.5M6 8v.5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
          </svg>
          {error}
        </p>
      )}
    </div>
  );
}

/* ── Login Page ── */
export default function Login() {
  const [username,  setUsername]  = useState("");
  const [password,  setPassword]  = useState("");
  const [showPw,    setShowPw]    = useState(false);
  const [errors,    setErrors]    = useState({});
  const [loading,   setLoading]   = useState(false);
  const navigate = useNavigate();

  const validate = () => {
    const e = {};
    if (!username.trim())   e.username = "Please enter your username.";
    if (password.length < 4) e.password = "Password must be at least 4 characters.";
    return e;
  };

  const handleSubmit = async (ev) => {
    ev.preventDefault();
    const e = validate();
    if (Object.keys(e).length) { setErrors(e); return; }
    setErrors({});
    setLoading(true);
    await new Promise((r) => setTimeout(r, 700)); // simulate auth
    sessionStorage.setItem("sb_user", username.trim());
    navigate("/notes");
  };

  return (
    <div className="min-h-screen flex bg-ink-900">

      {/* ── Left panel ── */}
      <div className="hidden lg:flex flex-col justify-center items-center flex-1
                      bg-ink-900 border-r border-ink-700 px-16 relative overflow-hidden">
        {/* Grid bg */}
        <div className="absolute inset-0 pointer-events-none opacity-20"
          style={{
            backgroundImage:
              "radial-gradient(circle, rgba(255,255,255,.07) 1px, transparent 1px)",
            backgroundSize: "28px 28px",
          }} />
        {/* Glow */}
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[500px] h-64
                        rounded-full pointer-events-none"
          style={{
            background: "radial-gradient(ellipse at center, rgba(240,169,59,.12), transparent 70%)",
          }} />

        <div className="relative z-10 max-w-xs text-center">
          {/* Logo */}
          <div className="w-16 h-16 bg-gradient-to-br from-gold-400 to-gold-600
                          rounded-2xl flex items-center justify-center mx-auto mb-8
                          shadow-[0_8px_32px_rgba(240,169,59,.35)]">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <path d="M8 11c0-4.42 3.58-8 8-8s8 3.58 8 8c0 .45-.04.9-.11 1.32C25.72 13.1 27 14.9 27 17c0 2.48-1.7 4.55-4 5.17V27H9v-4.83C6.7 21.55 5 19.48 5 17c0-.45.04-.9.11-1.32A7.96 7.96 0 018 11z"
                stroke="#1c2233" strokeWidth="1.6" strokeLinecap="round" />
              <line x1="16" y1="10" x2="16" y2="20" stroke="#1c2233" strokeWidth="1.6" strokeLinecap="round" />
              <line x1="20" y1="13" x2="20" y2="20" stroke="#1c2233" strokeWidth="1.6"
                strokeDasharray="2.5 2" strokeLinecap="round" />
            </svg>
          </div>

          <h1 className="text-3xl font-semibold text-white tracking-tight mb-3">
            Second Brain
          </h1>
          <p className="text-ink-400 text-sm leading-relaxed mb-10">
            Your AI-powered knowledge base. Capture, classify and recall anything.
          </p>

          <ul className="space-y-3 text-left">
            {FEATURES.map((f) => (
              <li key={f} className="flex items-center gap-3 text-sm text-ink-400">
                <span className="w-6 h-6 rounded-lg bg-gold-400/15 border border-gold-400/25
                                 flex items-center justify-center text-gold-400 flex-shrink-0">
                  <IconCheck />
                </span>
                {f}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* ── Right panel ── */}
      <div className="flex-1 lg:max-w-[460px] flex items-center justify-center p-8 bg-ink-900">
        <div className="w-full max-w-sm">

          {/* Header */}
          <div className="mb-8">
            <p className="text-xs font-semibold uppercase tracking-widest text-ink-500
                          flex items-center gap-2 mb-4">
              <span className="w-5 h-px bg-ink-600" />
              Secure access
            </p>
            <h2 className="text-2xl font-semibold text-white tracking-tight mb-1.5">
              Sign in to your brain
            </h2>
            <p className="text-sm text-ink-400">
              Enter your credentials to access your knowledge base.
            </p>
          </div>

          <form onSubmit={handleSubmit} noValidate>

            {/* Username */}
            <FieldGroup label="Username" id="username" error={errors.username}>
              <div className="relative">
                <input
                  id="username"
                  type="text"
                  autoComplete="username"
                  autoFocus
                  value={username}
                  onChange={(e) => { setUsername(e.target.value); setErrors((p) => ({ ...p, username: "" })); }}
                  placeholder="your_username"
                  className={`field pr-10 ${errors.username ? "error" : ""}`}
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-500">
                  <IconUser />
                </span>
              </div>
            </FieldGroup>

            {/* Password */}
            <FieldGroup
              label="Password"
              id="password"
              error={errors.password}
              rightSlot={
                <button type="button" onClick={() => {}}
                  className="text-xs text-ink-500 hover:text-gold-400 transition-colors">
                  Forgot password?
                </button>
              }
            >
              <div className="relative">
                <input
                  id="password"
                  type={showPw ? "text" : "password"}
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); setErrors((p) => ({ ...p, password: "" })); }}
                  placeholder="••••••••"
                  className={`field pr-10 ${errors.password ? "error" : ""}`}
                />
                <button
                  type="button"
                  onClick={() => setShowPw((v) => !v)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-500
                             hover:text-ink-300 transition-colors"
                >
                  {showPw ? <IconEyeOn /> : <IconEyeOff />}
                </button>
              </div>
            </FieldGroup>

            {/* Remember me */}
            <div className="flex items-center gap-2.5 mb-6">
              <input type="checkbox" id="remember"
                className="w-4 h-4 rounded border-ink-600 accent-gold-400 cursor-pointer" />
              <label htmlFor="remember" className="text-sm text-ink-400 cursor-pointer select-none">
                Remember me for 30 days
              </label>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3 text-base"
            >
              {loading ? (
                <>
                  <svg className="w-4 h-4 animate-spin-slow" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2"
                      strokeDasharray="28" strokeDashoffset="10" />
                  </svg>
                  Signing in…
                </>
              ) : (
                <>
                  Sign in
                  <IconArrow />
                </>
              )}
            </button>
          </form>

          {/* Demo hint */}
          <p className="text-center text-xs text-ink-600 mt-6">
            Demo: any username + password&nbsp;
            <span className="text-ink-500 font-medium">≥ 4 characters</span>
          </p>
        </div>
      </div>

    </div>
  );
}
