import React, { useState } from "react";
import { Lock, Mail, User, AlertCircle, Loader2, CheckCircle2 } from "lucide-react";
import { Logo } from "./Logo";
import { login, register } from "../api";

export default function Login({ onLoginSuccess }) {
  const [mode, setMode] = useState("signin"); // "signin" | "register"
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError("");
    setSuccessMsg("");
    setLoading(true);

    try {
      const data = await login(email, password);
      onLoginSuccess(data.access_token, data.username, email);
    } catch (err) {
      setError(err.message || "Failed to log in");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setSuccessMsg("");
    setLoading(true);

    try {
      const data = await register(name, email, password);
      setSuccessMsg(data.message);
      // Switch back to signin mode automatically
      setMode("signin");
    } catch (err) {
      setError(err.message || "Failed to register account");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0F172A] p-4 relative overflow-hidden select-none">
      {/* Background Glow Effects */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-[#2563EB]/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md bg-slate-900/90 backdrop-blur-xl border border-slate-800 rounded-2xl shadow-2xl p-8 relative z-10">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center p-2 mb-2">
            <Logo className="w-12 h-14 drop-shadow-lg" />
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Finance Intelligence
          </h2>
          <p className="text-slate-400 text-xs mt-1">
            {mode === "signin"
              ? "Sign in with your verified email account"
              : "Create an account to receive your email verification link"}
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex bg-slate-950/80 p-1 rounded-xl mb-6 border border-slate-800">
          <button
            type="button"
            onClick={() => {
              setMode("signin");
              setError("");
              setSuccessMsg("");
            }}
            className={`flex-1 py-2 text-xs font-semibold rounded-lg transition ${
              mode === "signin"
                ? "bg-[#2563EB] text-white shadow"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => {
              setMode("register");
              setError("");
              setSuccessMsg("");
            }}
            className={`flex-1 py-2 text-xs font-semibold rounded-lg transition ${
              mode === "register"
                ? "bg-[#2563EB] text-white shadow"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Register
          </button>
        </div>

        {error && (
          <div className="mb-5 p-3.5 rounded-xl bg-red-500/10 border border-red-500/20 flex items-start gap-2.5 text-red-400 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {successMsg && (
          <div className="mb-5 p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-start gap-2.5 text-emerald-400 text-xs leading-relaxed">
            <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5 text-emerald-400" />
            <span>{successMsg}</span>
          </div>
        )}

        {mode === "signin" ? (
          <form onSubmit={handleSignIn} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-3 bg-[#2563EB] hover:bg-blue-600 text-white font-medium py-2.5 rounded-xl shadow-lg shadow-blue-600/25 flex items-center justify-center gap-2 transition disabled:opacity-50 disabled:cursor-not-allowed text-xs"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Signing in...
                </>
              ) : (
                "Log in"
              )}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Nupur Sawant"
                  className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Real Email Address (Inbox required)
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="password"
                  required
                  minLength={6}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-3 bg-[#2563EB] hover:bg-blue-600 text-white font-medium py-2.5 rounded-xl shadow-lg shadow-blue-600/25 flex items-center justify-center gap-2 transition disabled:opacity-50 disabled:cursor-not-allowed text-xs"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Sending verification email...
                </>
              ) : (
                "Register & Send Verification Email"
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
