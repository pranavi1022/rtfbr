/**
 * ForgotPassword.tsx
 *
 * Feature 5 — Full OTP-based password reset flow
 *
 * Steps:
 *   1. Enter email  → POST /api/forgot-password
 *   2. Enter OTP    → POST /api/verify-otp
 *   3. New password → POST /api/reset-password
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { FloatingPaths } from "@/components/ui/background-paths";
import { Mail, KeyRound, Lock, ArrowLeft, CheckCircle2, Loader2, AlertCircle } from "lucide-react";
import { API_BASE } from "@/lib/api";

/* ── types ─────────────────────────────────── */

type Step = "email" | "otp" | "password" | "done";

/* ── helpers ────────────────────────────────── */

const BASE = API_BASE;

async function postJSON(endpoint: string, body: object) {
  const res = await fetch(`${BASE}${endpoint}`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

/* ── component ──────────────────────────────── */

const ForgotPassword = () => {
  const navigate = useNavigate();

  /* state */
  const [step,        setStep]        = useState<Step>("email");
  const [email,       setEmail]       = useState("");
  const [otp,         setOtp]         = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPwd,  setConfirmPwd]  = useState("");
  const [loading,     setLoading]     = useState(false);
  const [error,       setError]       = useState<string | null>(null);
  const [info,        setInfo]        = useState<string | null>(null);

  /* ── Step 1: send OTP ── */
  const handleSendOtp = async () => {
    if (!email.trim()) { setError("Please enter your email address."); return; }
    setLoading(true);
    setError(null);
    setInfo(null);
    try {
      const res = await postJSON("/api/forgot-password", { email });
      setInfo(res.message);
      setStep("otp");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /* ── Step 2: verify OTP ── */
  const handleVerifyOtp = async () => {
    if (!otp.trim()) { setError("Please enter the OTP."); return; }
    setLoading(true);
    setError(null);
    setInfo(null);
    try {
      const res = await postJSON("/api/verify-otp", { email, otp });
      setInfo(res.message);
      setStep("password");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /* ── Step 3: reset password ── */
  const handleResetPassword = async () => {
    if (!newPassword.trim()) { setError("Please enter a new password."); return; }
    if (newPassword.length < 6) { setError("Password must be at least 6 characters."); return; }
    if (newPassword !== confirmPwd) { setError("Passwords do not match."); return; }
    setLoading(true);
    setError(null);
    setInfo(null);
    try {
      await postJSON("/api/reset-password", { email, new_password: newPassword });
      setStep("done");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /* ── step metadata ── */
  const stepMeta: Record<Step, { title: string; subtitle: string; icon: React.ReactNode }> = {
    email: {
      title:    "Forgot Password",
      subtitle: "Enter your registered email address to receive an OTP.",
      icon:     <Mail className="w-8 h-8 text-white/50" />,
    },
    otp: {
      title:    "Enter OTP",
      subtitle: `An OTP has been sent to ${email}. Check your email inbox (or server console in demo mode).`,
      icon:     <KeyRound className="w-8 h-8 text-white/50" />,
    },
    password: {
      title:    "Reset Password",
      subtitle: "Choose a strong new password for your account.",
      icon:     <Lock className="w-8 h-8 text-white/50" />,
    },
    done: {
      title:    "Password Reset!",
      subtitle: "Your password has been updated successfully.",
      icon:     <CheckCircle2 className="w-8 h-8 text-emerald-400" />,
    },
  };

  const meta = stepMeta[step];

  /* ── step indicator ── */
  const steps = ["email", "otp", "password"];
  const currentStepIndex = steps.indexOf(step === "done" ? "password" : step);

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-[#050510]">
      <div className="absolute inset-0 bg-gradient-to-br from-[#050510] via-[#0a0a1a] to-[#0f0f24]" />
      <div className="absolute inset-0">
        <FloatingPaths position={1} />
        <FloatingPaths position={-1} />
      </div>

      <div className="relative z-10 w-full max-w-md px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* ── step progress indicator ── */}
          {step !== "done" && (
            <div className="flex items-center justify-center gap-2 mb-8">
              {steps.map((s, i) => (
                <div key={s} className="flex items-center gap-2">
                  <div
                    className={`w-2.5 h-2.5 rounded-full transition-all ${
                      i <= currentStepIndex
                        ? "bg-white shadow-[0_0_8px_rgba(255,255,255,0.6)]"
                        : "bg-white/20"
                    }`}
                  />
                  {i < steps.length - 1 && (
                    <div className={`h-px w-10 transition-all ${i < currentStepIndex ? "bg-white/50" : "bg-white/10"}`} />
                  )}
                </div>
              ))}
            </div>
          )}

          {/* ── card ── */}
          <div className="bg-gradient-to-b from-white/10 to-white/5 p-px rounded-2xl backdrop-blur-lg overflow-hidden shadow-[0_0_40px_rgba(120,80,255,0.08)]">
            <div className="rounded-[1.1rem] px-8 py-8 backdrop-blur-md bg-white/[0.05] border border-white/10">

              {/* icon + title */}
              <div className="flex flex-col items-center text-center mb-6">
                <div className="mb-3">{meta.icon}</div>
                <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70 mb-1">
                  {meta.title}
                </h1>
                <p className="text-sm text-white/40">{meta.subtitle}</p>
              </div>

              {/* error / info banners */}
              <AnimatePresence mode="wait">
                {error && (
                  <motion.div
                    key="error"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="overflow-hidden mb-4"
                  >
                    <div className="flex items-center gap-2 rounded-xl bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
                      <AlertCircle className="w-4 h-4 shrink-0" />
                      {error}
                    </div>
                  </motion.div>
                )}
                {info && !error && (
                  <motion.div
                    key="info"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="overflow-hidden mb-4"
                  >
                    <div className="flex items-center gap-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 px-4 py-3 text-sm text-emerald-400">
                      <CheckCircle2 className="w-4 h-4 shrink-0" />
                      {info}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* ── Step 1: Email ── */}
              {step === "email" && (
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-sm text-white/70">Email Address</label>
                    <input
                      id="forgot-email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleSendOtp()}
                      placeholder="you@example.com"
                      className="w-full rounded-xl bg-white/[0.04] border border-white/10 px-4 py-2.5 text-sm text-white placeholder:text-white/30 outline-none focus:border-white/30 transition-all"
                    />
                  </div>
                  <button
                    id="send-otp-btn"
                    onClick={handleSendOtp}
                    disabled={loading}
                    className="w-full rounded-xl py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-[0_0_20px_rgba(120,80,255,0.3)] transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Mail className="w-4 h-4" />}
                    {loading ? "Sending…" : "Send OTP"}
                  </button>
                </div>
              )}

              {/* ── Step 2: OTP ── */}
              {step === "otp" && (
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-sm text-white/70">One-Time Password (OTP)</label>
                    <input
                      id="otp-input"
                      type="text"
                      inputMode="numeric"
                      maxLength={6}
                      value={otp}
                      onChange={(e) => setOtp(e.target.value.replace(/\D/, ""))}
                      onKeyDown={(e) => e.key === "Enter" && handleVerifyOtp()}
                      placeholder="6-digit code"
                      className="w-full rounded-xl bg-white/[0.04] border border-white/10 px-4 py-2.5 text-sm text-white placeholder:text-white/30 outline-none focus:border-white/30 transition-all tracking-[0.4em] text-center font-mono"
                    />
                    <p className="text-xs text-white/30 text-center">
                      📋 Check your email inbox. If not received, check the server console (demo mode).
                    </p>
                  </div>
                  <button
                    id="verify-otp-btn"
                    onClick={handleVerifyOtp}
                    disabled={loading || otp.length < 6}
                    className="w-full rounded-xl py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-[0_0_20px_rgba(120,80,255,0.3)] transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <KeyRound className="w-4 h-4" />}
                    {loading ? "Verifying…" : "Verify OTP"}
                  </button>
                  <button
                    onClick={() => { setStep("email"); setError(null); setInfo(null); setOtp(""); }}
                    className="w-full text-sm text-white/30 hover:text-white/60 transition-colors"
                  >
                    ← Use a different email
                  </button>
                </div>
              )}

              {/* ── Step 3: New Password ── */}
              {step === "password" && (
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-sm text-white/70">New Password</label>
                    <input
                      id="new-password-input"
                      type="password"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      placeholder="Minimum 6 characters"
                      className="w-full rounded-xl bg-white/[0.04] border border-white/10 px-4 py-2.5 text-sm text-white placeholder:text-white/30 outline-none focus:border-white/30 transition-all"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-sm text-white/70">Confirm Password</label>
                    <input
                      id="confirm-password-input"
                      type="password"
                      value={confirmPwd}
                      onChange={(e) => setConfirmPwd(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleResetPassword()}
                      placeholder="Repeat your new password"
                      className="w-full rounded-xl bg-white/[0.04] border border-white/10 px-4 py-2.5 text-sm text-white placeholder:text-white/30 outline-none focus:border-white/30 transition-all"
                    />
                  </div>
                  <button
                    id="reset-password-btn"
                    onClick={handleResetPassword}
                    disabled={loading}
                    className="w-full rounded-xl py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-[0_0_20px_rgba(120,80,255,0.3)] transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                  >
                    {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Lock className="w-4 h-4" />}
                    {loading ? "Updating…" : "Reset Password"}
                  </button>
                </div>
              )}

              {/* ── Step 4: Done ── */}
              {step === "done" && (
                <div className="space-y-4 text-center">
                  <p className="text-white/60 text-sm">
                    You can now log in with your new password.
                  </p>
                  <button
                    id="go-to-login-btn"
                    onClick={() => navigate("/login")}
                    className="w-full rounded-xl py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-[0_0_20px_rgba(120,80,255,0.3)] transition-all flex items-center justify-center gap-2"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    Go to Login
                  </button>
                </div>
              )}

              {/* back to login link */}
              {step !== "done" && (
                <div className="text-center pt-4">
                  <button
                    id="back-to-login-link"
                    onClick={() => navigate("/login")}
                    className="text-sm text-white/30 hover:text-white/60 transition-colors"
                  >
                    Back to Login
                  </button>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ForgotPassword;
