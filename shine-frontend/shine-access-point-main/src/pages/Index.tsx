import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FloatingPaths } from "@/components/ui/background-paths";
import { Eye, EyeOff, Lock, Mail, User } from "lucide-react";
import { toast } from "sonner";
import { Link, useNavigate } from "react-router-dom";
import { API_BASE } from "@/lib/api";

const Index = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isLogin && formData.password !== formData.confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }
    setIsSubmitting(true);
    try {
      if (isLogin) {
        // ── Login ──────────────────────────────────────────────────
        const res = await fetch(`${API_BASE}/api/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            username: formData.username,
            password: formData.password,
          }),
        });
        const data = await res.json();
        if (!res.ok) {
          toast.error(data.error || "Login failed");
          return;
        }
        toast.success("Login successful!");
        navigate("/dashboard");
      } else {
        // ── Register ───────────────────────────────────────────────
        const res = await fetch(`${API_BASE}/api/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            fullname: formData.username,   // using username as fullname for this form
            username: formData.username,
            email:    formData.email,
            password: formData.password,
          }),
        });
        const data = await res.json();
        if (!res.ok) {
          toast.error(data.error || "Registration failed");
          return;
        }
        toast.success("Account created! Please log in.");
        setIsLogin(true);
      }
    } catch {
      toast.error("Connection error. Make sure the backend is running on port 5000.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-black">
      <div className="absolute inset-0 bg-black" />
      <div className="absolute inset-0">
        <FloatingPaths position={1} />
        <FloatingPaths position={-1} />
      </div>

      <div className="relative z-10 w-full max-w-md mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="rounded-2xl p-8 backdrop-blur-xl bg-white/[0.04] border border-white/[0.08] shadow-[0_8px_60px_rgba(0,0,0,0.6)]">
            {/* Header */}
            <AnimatePresence mode="wait">
              <motion.div
                key={isLogin ? "login" : "register"}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className="text-center mb-6"
              >
                <div className="flex justify-center mb-4">
                  <div className="w-14 h-14 rounded-full border border-white/20 flex items-center justify-center bg-white/[0.05]">
                    <Lock className="w-6 h-6 text-white/70" />
                  </div>
                </div>

                <h1 className="text-2xl font-bold text-foreground">
                  {isLogin ? "Login" : "Register"}
                </h1>

                <p className="text-sm text-muted-foreground mt-1">
                  {isLogin
                    ? "Enter your credentials to continue"
                    : "Create your account to get started"}
                </p>
              </motion.div>
            </AnimatePresence>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-3">
                {/* Username */}
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                  <input
                    name="username"
                    type="text"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    className="w-full pl-12 pr-4 h-12 rounded-full bg-white/[0.04] border border-white/[0.08] text-foreground placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 text-sm transition-all"
                  />
                </div>

                {/* Email — register only */}
                <AnimatePresence>
                  {!isLogin && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.3 }}
                      className="relative overflow-hidden"
                    >
                      <div className="relative">
                        <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                        <input
                          name="email"
                          type="email"
                          placeholder="Email"
                          value={formData.email}
                          onChange={handleChange}
                          required={!isLogin}
                          className="w-full pl-12 pr-4 h-12 rounded-full bg-white/[0.04] border border-white/[0.08] text-foreground placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 text-sm transition-all"
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Password */}
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                  <input
                    name="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    className="w-full pl-12 pr-12 h-12 rounded-full bg-white/[0.04] border border-white/[0.08] text-foreground placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 text-sm transition-all"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors"
                  >
                    {showPassword ? (
                      <EyeOff className="w-5 h-5" />
                    ) : (
                      <Eye className="w-5 h-5" />
                    )}
                  </button>
                </div>

                {/* Confirm Password — register only */}
                <AnimatePresence>
                  {!isLogin && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.3 }}
                      className="relative overflow-hidden"
                    >
                      <div className="relative">
                        <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
                        <input
                          name="confirmPassword"
                          type="password"
                          placeholder="Confirm Password"
                          value={formData.confirmPassword}
                          onChange={handleChange}
                          required={!isLogin}
                          className="w-full pl-12 pr-4 h-12 rounded-full bg-white/[0.04] border border-white/[0.08] text-foreground placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 text-sm transition-all"
                        />
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full h-12 rounded-full bg-white/[0.08] hover:bg-white/[0.14] text-foreground font-semibold text-base border border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.3)] mt-2 transition-colors disabled:opacity-50"
              >
                {isSubmitting
                  ? "Processing..."
                  : isLogin
                  ? "Login"
                  : "Register"}
              </button>
            </form>

            {/* Footer links */}
            <div className="flex items-center justify-between pt-5">
              {isLogin && (
                <Link
                  to="/forgot-password"
                  className="text-sm text-white/40 hover:text-white/70 transition-colors"
                >
                  Forgot Password?
                </Link>
              )}
              <button
                type="button"
                onClick={() => setIsLogin(!isLogin)}
                className="text-sm text-white/40 hover:text-white/70 transition-colors ml-auto"
              >
                {isLogin ? "Register" : "Back to Login"}
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Index;
