import { useState } from "react";
import { FloatingPaths } from "@/components/ui/background-paths";
import { motion } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { API_BASE } from "@/lib/api";

const Register = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    fullname: "",
    email: "",
    username: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.fullname || !formData.email || !formData.username || !formData.password) {
      toast.error("All fields are required");
      return;
    }
    if (formData.password.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }
    setIsSubmitting(true);
    try {
      const res = await fetch(`${API_BASE}/api/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          fullname: formData.fullname,
          username: formData.username,
          email: formData.email,
          password: formData.password,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        toast.error(data.error || "Registration failed");
        return;
      }
      toast.success("Account created! Please log in.");
      navigate("/login");
    } catch {
      toast.error("Connection error. Please check your internet and try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-black">
      <div className="absolute inset-0 bg-black" />
      <div className="absolute inset-0">
        <FloatingPaths position={1} />
        <FloatingPaths position={-1} />
      </div>

      <div className="relative z-10 container mx-auto px-4 md:px-6 text-center">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 2 }}
          className="max-w-md mx-auto"
        >
          <h1 className="text-2xl sm:text-3xl font-bold mb-8 tracking-tighter">
            <motion.span
              initial={{ y: 100, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ type: "spring", stiffness: 150, damping: 25 }}
              className="inline-block text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70"
            >
              Create Account
            </motion.span>
          </h1>

          <div className="inline-block group relative bg-gradient-to-b from-white/10 to-white/5 p-px rounded-2xl backdrop-blur-lg overflow-hidden shadow-[0_0_40px_rgba(120,80,255,0.08)]">
            <div className="rounded-[1.15rem] px-8 py-8 backdrop-blur-md bg-white/[0.05] border border-white/10">
              <form onSubmit={handleSubmit} className="space-y-4 text-left">
                <div className="space-y-2">
                  <label htmlFor="fullname" className="text-sm text-white/90">Full Name</label>
                  <input
                    id="fullname"
                    name="fullname"
                    type="text"
                    placeholder="Enter your full name"
                    required
                    value={formData.fullname}
                    onChange={handleChange}
                    className="w-full rounded-lg bg-white/[0.04] border border-white/10 text-white placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 px-4 py-2.5 text-sm transition-all"
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="email" className="text-sm text-white/90">Email</label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="Enter your email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full rounded-lg bg-white/[0.04] border border-white/10 text-white placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 px-4 py-2.5 text-sm transition-all"
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="username" className="text-sm text-white/90">Username</label>
                  <input
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Choose a username"
                    required
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full rounded-lg bg-white/[0.04] border border-white/10 text-white placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 px-4 py-2.5 text-sm transition-all"
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="password" className="text-sm text-white/90">Password</label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Create a password"
                    required
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full rounded-lg bg-white/[0.04] border border-white/10 text-white placeholder:text-white/30 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-white/20 px-4 py-2.5 text-sm transition-all"
                  />
                </div>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full rounded-xl py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-primary to-accent hover:opacity-90 shadow-[0_0_20px_rgba(120,80,255,0.3)] transition-all disabled:opacity-50"
                >
                  {isSubmitting ? "Creating Account..." : "Register"}
                </button>
                <div className="text-center pt-2">
                  <Link
                    to="/login"
                    className="text-sm text-white/40 hover:text-white/80 hover:drop-shadow-[0_0_8px_rgba(255,255,255,0.3)] transition-all"
                  >
                    Already have an account? Login
                  </Link>
                </div>
              </form>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Register;
