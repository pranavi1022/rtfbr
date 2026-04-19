import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Compass, ArrowLeft, Clock, Code, BookOpen,
  Layers, AlertCircle, CheckCircle2, Loader2
} from "lucide-react";
import { API_BASE } from "@/lib/api";

/* ── types ──────────────────────────────────────────────────── */

interface RequiredSkill {
  name: string;
  category: string;
  priority: "HIGH" | "LOW";
  estimatedTime: string;
}

interface ProjectDetailsData {
  title: string;
  description: string;
  difficulty: string;
  technologies: string[];
  required_skills: RequiredSkill[];
  estimated_time: string;
  project_type: string;
  match_source: string;
}

/* ── helpers ─────────────────────────────────────────────────── */

const glass =
  "rounded-2xl backdrop-blur-xl bg-white/[0.06] border border-white/[0.12] shadow-[0_8px_60px_rgba(0,0,0,0.6),0_0_15px_rgba(255,255,255,0.03)]";

function levelColor(l: string) {
  if (l === "Beginner")     return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
  if (l === "Intermediate") return "bg-amber-500/20 text-amber-300 border-amber-500/30";
  return "bg-red-500/20 text-red-300 border-red-500/30";
}

function priorityBadge(p: string) {
  return p === "HIGH"
    ? "bg-red-500/20 text-red-300 border-red-500/30"
    : "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
}

/* ════════════════════════════════════════════════════════════ */

const ProjectDetails = () => {
  const navigate  = useNavigate();
  const location  = useLocation();

  // The basic project data passed via navigate state (title, description,
  // technologies, level) from the ProjectGuidance page
  const passed = location.state as {
    title: string;
    description: string;
    technologies: string[];
    level: string;
  } | null;

  const [details, setDetails] = useState<ProjectDetailsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState<string | null>(null);

  useEffect(() => {
    if (!passed?.title) {
      setError("No project selected. Please go back and choose a project.");
      setLoading(false);
      return;
    }

    // Fetch enriched details from backend
    const fetchDetails = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/project-details`, {
          method:  "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({
            title:        passed.title,
            difficulty:   passed.level,
            technologies: passed.technologies,
            description:  passed.description,
          }),
        });
        if (!res.ok) throw new Error("Failed to fetch project details");
        const data: ProjectDetailsData = await res.json();
        setDetails(data);
      } catch (err) {
        console.error(err);
        // Graceful degradation: build details from passed data locally
        setDetails({
          title:       passed.title,
          description: passed.description,
          difficulty:  passed.level,
          technologies: passed.technologies,
          required_skills: passed.technologies.map((t) => ({
            name:          t,
            category:      "Technology",
            priority:      "LOW" as const,
            estimatedTime: "Est. ~1-2 weeks",
          })),
          estimated_time: passed.level === "Beginner"     ? "2–4 weeks"
                        : passed.level === "Intermediate" ? "4–8 weeks"
                        : "8–16 weeks",
          project_type:   "website",
          match_source:   "client",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, []);   // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-black">
      {/* ── background beams ─── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute -top-32 left-[15%] w-[1px] h-[140%] rotate-[25deg] opacity-[0.04]"
          style={{ background: "linear-gradient(to bottom, transparent 0%, white 30%, white 70%, transparent 100%)" }}
        />
        <div
          className="absolute -top-32 left-[55%] w-[1px] h-[140%] rotate-[-18deg] opacity-[0.05]"
          style={{ background: "linear-gradient(to bottom, transparent 0%, white 40%, white 60%, transparent 100%)" }}
        />
        <div
          className="absolute -top-32 right-[20%] w-[1px] h-[140%] rotate-[15deg] opacity-[0.035]"
          style={{ background: "linear-gradient(to bottom, transparent 0%, white 35%, white 65%, transparent 100%)" }}
        />
      </div>

      {/* ── content ─── */}
      <div className="relative z-10 min-h-screen flex flex-col">

        {/* ── navbar ─── */}
        <nav className="flex items-center justify-between px-8 py-4 border-b border-white/[0.08]">
          <div className="flex items-center gap-2">
            <Compass className="w-6 h-6 text-white drop-shadow-[0_0_6px_rgba(255,255,255,0.5)]" />
            <span className="text-white font-semibold text-lg tracking-wide">Guidance System</span>
          </div>
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-sm text-white/50 hover:text-white/90 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Projects
          </button>
        </nav>

        {/* ── body ─── */}
        <div className="flex-1 px-8 py-10 max-w-4xl mx-auto w-full">

          {/* Loading state */}
          {loading && (
            <div className={`${glass} p-16 flex flex-col items-center justify-center gap-4`}>
              <Loader2 className="w-8 h-8 text-white/40 animate-spin" />
              <p className="text-white/40 text-sm">Loading project details…</p>
            </div>
          )}

          {/* Error state */}
          {!loading && error && (
            <div className={`${glass} p-12 flex flex-col items-center justify-center gap-4 text-center`}>
              <AlertCircle className="w-10 h-10 text-red-400/60" />
              <p className="text-white/60">{error}</p>
              <button
                onClick={() => navigate("/project-guidance")}
                className="mt-2 text-sm text-white/40 hover:text-white/80 underline underline-offset-4 transition-colors"
              >
                Go to Project Guidance
              </button>
            </div>
          )}

          {/* Details */}
          {!loading && details && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className="space-y-6"
            >
              {/* ── title + badges ─── */}
              <div className={`${glass} p-7`}>
                <div className="flex items-start justify-between gap-4 mb-4">
                  <h1 className="text-2xl font-bold text-white leading-tight">{details.title}</h1>
                  <span className={`shrink-0 text-xs font-medium px-3 py-1 rounded-full border ${levelColor(details.difficulty)}`}>
                    {details.difficulty}
                  </span>
                </div>

                {/* Description */}
                <p className="text-white/70 text-sm leading-relaxed mb-6">{details.description}</p>

                {/* Meta row */}
                <div className="flex flex-wrap gap-4 text-sm text-white/50">
                  <span className="flex items-center gap-1.5">
                    <Clock className="w-4 h-4" />
                    Estimated: <span className="text-white/80 font-medium">{details.estimated_time}</span>
                  </span>
                  <span className="flex items-center gap-1.5">
                    <Layers className="w-4 h-4" />
                    Type: <span className="text-white/80 font-medium capitalize">{details.project_type}</span>
                  </span>
                </div>
              </div>

              {/* ── technologies ─── */}
              {details.technologies.length > 0 && (
                <div className={`${glass} p-6`}>
                  <h2 className="text-sm font-semibold text-white/60 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <Code className="w-4 h-4" />
                    Technologies Required
                  </h2>
                  <div className="flex flex-wrap gap-2">
                    {details.technologies.map((t) => (
                      <span
                        key={t}
                        className="text-sm px-3 py-1 rounded-full bg-white/[0.08] border border-white/[0.12] text-white/80"
                      >
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* ── required skills ─── */}
              {details.required_skills.length > 0 && (
                <div className={`${glass} p-6`}>
                  <h2 className="text-sm font-semibold text-white/60 uppercase tracking-wider mb-4 flex items-center gap-2">
                    <BookOpen className="w-4 h-4" />
                    Required Skills
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {details.required_skills.map((skill, i) => (
                      <motion.div
                        key={`${skill.name}-${i}`}
                        initial={{ opacity: 0, y: 8 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.05 }}
                        className="rounded-xl bg-white/[0.04] border border-white/[0.08] p-4"
                      >
                        <div className="flex items-center justify-between mb-1.5">
                          <span className="text-sm font-semibold text-white">{skill.name}</span>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${priorityBadge(skill.priority)}`}>
                            {skill.priority}
                          </span>
                        </div>
                        <p className="text-xs text-white/40">{skill.category}</p>
                        <p className="text-xs text-white/30 mt-1 flex items-center gap-1">
                          🕐 {skill.estimatedTime}
                        </p>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {/* ── action buttons ─── */}
              <div className="flex gap-4">
                <button
                  onClick={() => navigate("/skill-gap")}
                  className="flex-1 rounded-full py-3 text-sm font-semibold text-white bg-gradient-to-r from-white/[0.12] to-white/[0.06] border border-white/[0.2] hover:from-white/[0.18] hover:to-white/[0.1] shadow-[0_0_20px_rgba(255,255,255,0.08)] hover:shadow-[0_0_30px_rgba(255,255,255,0.15)] transition-all flex items-center justify-center gap-2"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  Check My Skill Gap
                </button>
                <button
                  onClick={() => navigate(-1)}
                  className="flex-1 rounded-full py-3 text-sm font-semibold text-white/60 bg-white/[0.04] border border-white/[0.1] hover:bg-white/[0.08] hover:text-white/80 transition-all"
                >
                  ← Back to Results
                </button>
              </div>

              {/* source badge (for viva transparency) */}
              <p className="text-center text-white/20 text-xs">
                Data source: <span className="font-mono">{details.match_source}</span> ·
                SHINE Academic Portal 2024–25
              </p>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectDetails;
