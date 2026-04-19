import { motion } from "framer-motion";
import { SpiralAnimation } from "@/components/ui/spiral-animation";
import { Lightbulb, BarChart3, Route, GraduationCap } from "lucide-react";
import { Link } from "react-router-dom";

const Introduction = () => {
  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-background">
      {/* Spiral Animation Background */}
      <div className="fixed inset-0 z-0">
        <SpiralAnimation />
      </div>

      {/* Overlay for text readability */}
      <div className="fixed inset-0 z-[1] bg-black/40" />

      {/* Navbar */}
      <nav className="relative z-10 flex items-center justify-between px-6 py-4 md:px-10 backdrop-blur-md bg-white/[0.03] border-b border-white/[0.08]">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-white/[0.08] border border-white/[0.12] flex items-center justify-center">
            <GraduationCap className="w-5 h-5 text-white/90" />
          </div>
          <span className="text-white font-semibold text-lg tracking-tight">Guidance System</span>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/login"
            className="px-5 py-2 rounded-full text-sm font-medium text-white/80 hover:text-white border border-white/[0.1] hover:border-white/[0.2] bg-white/[0.04] hover:bg-white/[0.08] transition-all"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="px-5 py-2 rounded-full text-sm font-medium text-white bg-white/[0.12] hover:bg-white/[0.18] border border-white/[0.15] transition-all"
          >
            Register
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative z-10 flex flex-col items-center justify-center text-center px-6 pt-24 pb-16 md:pt-32 md:pb-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.3 }}
          className="max-w-4xl mx-auto"
        >
          <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold text-white leading-tight tracking-tight mb-8">
            Student-Centric Project Guidance and Skill Gap Analysis System
          </h1>

          <div className="max-w-2xl mx-auto space-y-4">
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="text-base md:text-lg text-white/70 leading-relaxed"
            >
              This system helps students choose the right academic project based on their interests and analyze the skills required to successfully complete it.
            </motion.p>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
              className="text-base md:text-lg text-white/70 leading-relaxed"
            >
              It provides structured guidance, identifies missing skills, and suggests a clear learning path to improve project readiness.
            </motion.p>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="mt-10 flex items-center justify-center gap-4"
          >
            <Link
              to="/login"
              className="px-8 py-3 rounded-full text-sm font-semibold text-white bg-white/[0.1] hover:bg-white/[0.16] border border-white/[0.15] hover:border-white/[0.25] transition-all shadow-[0_0_20px_rgba(255,255,255,0.05)]"
            >
              Get Started
            </Link>
          </motion.div>
        </motion.div>
      </div>

      {/* How It Works Section */}
      <div className="relative z-10 px-6 pb-24 md:pb-32">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.2 }}
          className="max-w-5xl mx-auto"
        >
          <h2 className="text-2xl md:text-3xl font-bold text-white text-center mb-12 tracking-tight">
            How It Works
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Step 1 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.4 }}
              className="rounded-2xl p-6 backdrop-blur-xl bg-white/[0.05] border border-white/[0.1] shadow-[0_4px_30px_rgba(0,0,0,0.4)]"
            >
              <div className="w-12 h-12 rounded-xl bg-white/[0.08] border border-white/[0.12] flex items-center justify-center mb-4">
                <Lightbulb className="w-6 h-6 text-white/80" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Project Guidance</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Enter your interest and get suitable project ideas
              </p>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.6 }}
              className="rounded-2xl p-6 backdrop-blur-xl bg-white/[0.05] border border-white/[0.1] shadow-[0_4px_30px_rgba(0,0,0,0.4)]"
            >
              <div className="w-12 h-12 rounded-xl bg-white/[0.08] border border-white/[0.12] flex items-center justify-center mb-4">
                <BarChart3 className="w-6 h-6 text-white/80" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Skill Gap Analysis</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Analyze required vs existing skills
              </p>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.8 }}
              className="rounded-2xl p-6 backdrop-blur-xl bg-white/[0.05] border border-white/[0.1] shadow-[0_4px_30px_rgba(0,0,0,0.4)]"
            >
              <div className="w-12 h-12 rounded-xl bg-white/[0.08] border border-white/[0.12] flex items-center justify-center mb-4">
                <Route className="w-6 h-6 text-white/80" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Learning Path</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Follow structured steps to complete your project
              </p>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Introduction;
