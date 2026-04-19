import { useState, KeyboardEvent } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Compass, BarChart3, LogOut, X, Search,
  BookOpen, Code, Database, Server, GitBranch, Globe, Zap, Layout
} from "lucide-react";
import RadialOrbitalTimeline, { type TimelineItem } from "@/components/ui/radial-orbital-timeline";
import { API_BASE } from "@/lib/api";

/* ── types ────────────────────────────────── */

interface SkillMatch {
  name: string;
  proficiency: number;
}

interface MissingSkill {
  name: string;
  priority: "HIGH" | "LOW";
  estimatedTime: string;
  resources?: { title: string; link: string }[];
}

interface LearningResource {
  skill: string;
  title: string;
  description: string;
  link: string;
}

interface AnalysisResult {
  projectName: string;
  level: string;
  readinessScore: number;
  totalRequired: number;
  matchedCount: number;
  missingCount: number;
  skillsYouHave: SkillMatch[];
  missingSkills: MissingSkill[];
  learningPath: LearningResource[];
  categoryBreakdown: { category: string; percentage: number }[];
}


/* ── styles ────────────────────────────────── */

const glass =
  "rounded-2xl backdrop-blur-xl bg-white/[0.06] border border-white/[0.12] shadow-[0_8px_60px_rgba(0,0,0,0.6),0_0_15px_rgba(255,255,255,0.03)]";

function priorityColor(p: string) {
  return p === "HIGH"
    ? "bg-red-500/20 text-red-300 border-red-500/30"
    : "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
}

/* ════════════════════════════════════════════ */

const SkillGap = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [projectName, setProjectName] = useState("");
  const [projectType, setProjectType] = useState("website");
  const [skillInput, setSkillInput] = useState("");
  const [skills, setSkills] = useState<string[]>([]);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const projectTypes = ["Website", "App", "Other"];

  const addSkill = (value: string) => {
    const trimmed = value.trim();
    if (trimmed && !skills.map((s) => s.toLowerCase()).includes(trimmed.toLowerCase())) {
      setSkills([...skills, trimmed]);
    }
    setSkillInput("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      addSkill(skillInput);
    }
  };

  const removeSkill = (index: number) => {
    setSkills(skills.filter((_, i) => i !== index));
  };

  const handleAnalyze = async () => {
    if (!projectName || skills.length === 0) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/skill-gap`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          projectName,
          projectType,
          skills,
        }),
      });
      if (!response.ok) throw new Error("Analysis failed");
      const data = await response.json();
      setResult(data);

      // Save activity for dashboard history (fire-and-forget)
      fetch(`${API_BASE}/api/save-activity`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          project: projectName,
          level: data.level || projectType,
          missing_skills: data.missingCount || 0,
          action: "skill_gap",
        }),
      }).catch(() => {});
    } catch (err) {
      console.error("Skill gap analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  /* build orbital data from learning path (backend returns {skill, title, description, link}) */
  const orbitalData: TimelineItem[] = result
    ? result.learningPath.map((resource, i) => ({
        id: i + 1,
        title: resource.title,
        date: `Step ${i + 1}`,
        content: resource.description,
        category: "Learning",
        icon: BookOpen,
        relatedIds: i < result.learningPath.length - 1 ? [i + 2] : [],
        status: ("pending" as const),
        energy: Math.max(30, 100 - i * 15),
        link: resource.link,
      }))
    : [];

  const navLinks = [
    { label: "Project Guidance", path: "/project-guidance" },
    { label: "Skill Gap Analysis", path: "/skill-gap" },
  ];

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-black">
      {/* ── subtle white beams ─────────────────────── */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div
          className="absolute -top-32 left-[15%] w-[1px] h-[140%] rotate-[25deg] opacity-[0.04]"
          style={{ background: "linear-gradient(to bottom, transparent 0%, white 30%, white 70%, transparent 100%)" }}
        />
        <div
          className="absolute -top-32 left-[45%] w-[1px] h-[140%] rotate-[-15deg] opacity-[0.06]"
          style={{ background: "linear-gradient(to bottom, transparent 0%, white 40%, white 60%, transparent 100%)" }}
        />
        <div
          className="absolute -top-32 right-[20%] w-[1px] h-[140%] rotate-[18deg] opacity-[0.035]"
          style={{ background: "linear-gradient(to bottom, transparent 0%, white 35%, white 65%, transparent 100%)" }}
        />
        <div
          className="absolute -top-32 right-[40%] w-[1px] h-[140%] rotate-[-30deg] opacity-[0.045]"
          style={{ background: "linear-gradient(to bottom, transparent 0%, white 25%, white 75%, transparent 100%)" }}
        />
      </div>

      {/* ── content ────────────────────────────────── */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* ── navbar ─────────────────────────────── */}
        <nav className="flex items-center justify-between px-8 py-4 border-b border-white/[0.08]">
          <div className="flex items-center gap-2">
            <Compass className="w-6 h-6 text-white drop-shadow-[0_0_6px_rgba(255,255,255,0.5)]" />
            <span className="text-white font-semibold text-lg tracking-wide">Guidance System</span>
          </div>
          <div className="flex items-center gap-6">
            {navLinks.map((l) => (
              <button
                key={l.path}
                onClick={() => navigate(l.path)}
                className={`text-sm font-medium transition-colors ${
                  location.pathname === l.path
                    ? "text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.6)]"
                    : "text-white/50 hover:text-white/80"
                }`}
              >
                {l.label}
              </button>
            ))}
            <button
              onClick={() => navigate("/dashboard")}
              className="flex items-center gap-1.5 text-sm text-white/50 hover:text-white/80 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Dashboard
            </button>
          </div>
        </nav>

        {/* ── header ─────────────────────────────── */}
        <div className="px-8 pt-10 pb-6">
          <div className="flex items-center gap-3 mb-2">
            <BarChart3 className="w-7 h-7 text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.6)]" />
            <h1 className="text-3xl font-bold text-white tracking-tight">Skill Gap Analysis</h1>
          </div>
          <p className="text-white/60 text-base max-w-2xl">
            Enter the project you want to build and the skills you already have. We'll show what's missing and how to fill the gap.
          </p>
        </div>

        {/* ── two-column layout ──────────────────── */}
        <div className="flex-1 px-8 pb-12 grid grid-cols-1 lg:grid-cols-[420px_1fr] gap-8">
          {/* LEFT – form */}
          <div className={`${glass} p-6 h-fit`}>
            <div className="flex items-center gap-2 mb-5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.7)]" />
              <span className="text-white font-semibold text-base">Analyse My Skills</span>
            </div>

            {/* project name */}
            <label className="block mb-1.5 text-xs font-medium text-white/60 uppercase tracking-wider">Project Name</label>
            <input
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="e.g. attendance website, e-commerce app"
              className="w-full rounded-xl bg-white/[0.06] border border-white/[0.1] px-4 py-2.5 text-sm text-white placeholder:text-white/30 outline-none focus:border-white/30 focus:shadow-[0_0_12px_rgba(255,255,255,0.08)] transition-all mb-5"
            />

            {/* project type */}
            <label className="block mb-2 text-xs font-medium text-white/60 uppercase tracking-wider">Project Type</label>
            <div className="flex gap-3 mb-5">
              {projectTypes.map((t) => (
                <button
                  key={t}
                  onClick={() => setProjectType(t.toLowerCase())}
                  className={`flex-1 rounded-full py-2 text-sm font-medium border transition-all ${
                    projectType === t.toLowerCase()
                      ? "bg-white/[0.12] border-white/30 text-white shadow-[0_0_14px_rgba(255,255,255,0.1)]"
                      : "bg-white/[0.04] border-white/[0.08] text-white/50 hover:bg-white/[0.08] hover:text-white/70"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>

            {/* skills */}
            <label className="block mb-1.5 text-xs font-medium text-white/60 uppercase tracking-wider">Skills I Already Have</label>
            <div className="rounded-xl bg-white/[0.06] border border-white/[0.1] p-3 mb-1">
              <div className="flex flex-wrap gap-2 mb-2">
                {skills.map((skill, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1 text-xs px-3 py-1 rounded-full bg-white/[0.1] border border-white/[0.15] text-white/80"
                  >
                    {skill}
                    <button onClick={() => removeSkill(i)} className="hover:text-white transition-colors">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
              <input
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a skill and press Enter..."
                className="w-full bg-transparent text-sm text-white placeholder:text-white/30 outline-none"
              />
            </div>
            <p className="text-white/30 text-xs mb-5">
              e.g. Python, HTML, SQL — press <kbd className="px-1.5 py-0.5 rounded bg-white/[0.1] border border-white/[0.15] text-white/50">Enter</kbd> after each skill
            </p>

            {/* submit */}
            <button
              onClick={handleAnalyze}
              disabled={!projectName || skills.length === 0 || loading}
              className="w-full rounded-full py-3 text-sm font-semibold text-white bg-gradient-to-r from-white/[0.12] to-white/[0.06] border border-white/[0.2] hover:from-white/[0.18] hover:to-white/[0.1] shadow-[0_0_20px_rgba(255,255,255,0.08)] hover:shadow-[0_0_30px_rgba(255,255,255,0.15)] transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              <BarChart3 className="w-4 h-4" />
              {loading ? "Analysing…" : "Analyse Skill Gap"}
            </button>
          </div>

          {/* RIGHT – results */}
          <div className="space-y-6">
            {!result && !loading && (
              <div className={`${glass} p-10 flex flex-col items-center justify-center text-center min-h-[320px]`}>
                <Search className="w-10 h-10 text-white/20 mb-4" />
                <p className="text-white/40 text-base">Enter your project details and skills to analyse the gap</p>
              </div>
            )}

            {loading && (
              <div className={`${glass} p-10 flex items-center justify-center min-h-[320px]`}>
                <div className="w-8 h-8 border-2 border-white/20 border-t-white rounded-full animate-spin" />
              </div>
            )}

            {result && !loading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                {/* ── readiness card ──────────────── */}
                <div className={`${glass} p-6`}>
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h2 className="text-xl font-bold text-white">{result.projectName} — {result.level}</h2>
                      <p className="text-white/50 text-sm mt-1">
                        You have {result.matchedCount} of {result.totalRequired} required skills. {result.missingCount} skills to learn.
                      </p>
                    </div>
                    <div className="relative w-20 h-20">
                      <svg className="w-20 h-20 -rotate-90" viewBox="0 0 80 80">
                        <circle cx="40" cy="40" r="34" stroke="rgba(255,255,255,0.1)" strokeWidth="6" fill="none" />
                        <circle
                          cx="40" cy="40" r="34"
                          stroke="white"
                          strokeWidth="6"
                          fill="none"
                          strokeDasharray={`${(result.readinessScore / 100) * 213.6} 213.6`}
                          strokeLinecap="round"
                          className="drop-shadow-[0_0_6px_rgba(255,255,255,0.5)]"
                        />
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-lg font-bold text-white">{result.readinessScore}%</span>
                        <span className="text-[10px] text-white/50 uppercase tracking-wider">Ready</span>
                      </div>
                    </div>
                  </div>
                  <span className={`text-xs font-medium px-3 py-1 rounded-full border ${
                    result.readinessScore >= 70
                      ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"
                      : result.readinessScore >= 40
                      ? "bg-amber-500/20 text-amber-300 border-amber-500/30"
                      : "bg-red-500/20 text-red-300 border-red-500/30"
                  }`}>
                    {result.readinessScore >= 70 ? "READY" : result.readinessScore >= 40 ? "NEEDS WORK" : "NEEDS WORK"}
                  </span>
                </div>

                {/* ── skills you have ────────────── */}
                {result.skillsYouHave.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-3 flex items-center gap-2">
                      <span className="text-emerald-400">✅</span> Skills You Have
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {result.skillsYouHave.map((skill) => (
                        <div key={skill.name} className={`${glass} p-4`}>
                          <div className="flex justify-between items-center mb-2">
                            <div className="flex items-center gap-2">
                              <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.6)]" />
                              <span className="text-sm font-medium text-white">{skill.name}</span>
                            </div>
                            <span className="text-xs text-white/50">{skill.proficiency}%</span>
                          </div>
                          <div className="w-full h-1.5 bg-white/[0.08] rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${skill.proficiency}%` }}
                              transition={{ duration: 0.8, delay: 0.2 }}
                              className="h-full rounded-full bg-emerald-400/60 shadow-[0_0_8px_rgba(52,211,153,0.4)]"
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* ── missing skills ─────────────── */}
                {result.missingSkills.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-3 flex items-center gap-2">
                      <span className="text-red-400">✕</span> Missing Skills
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                      {result.missingSkills.map((skill) => (
                        <div key={skill.name} className={`${glass} p-4`}>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-semibold text-white">{skill.name}</span>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${priorityColor(skill.priority)}`}>
                              {skill.priority}
                            </span>
                          </div>
                          <p className="text-xs text-white/40 flex items-center gap-1 mb-2">
                            {skill.estimatedTime}
                          </p>

                          {/* ── Learning Resources (DB-driven) ── */}
                          {skill.resources && skill.resources.length > 0 ? (
                            <div className="mt-2 pt-2 border-t border-white/[0.06] space-y-1.5">
                              <p className="text-[10px] font-medium text-white/30 uppercase tracking-wider">Resources</p>
                              {skill.resources.map((res, ri) => (
                                <a
                                  key={ri}
                                  href={res.link}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="flex items-center gap-1.5 text-xs text-blue-300/80 hover:text-blue-200 transition-colors group"
                                >
                                  <BookOpen className="w-3 h-3 flex-shrink-0 opacity-50 group-hover:opacity-100 transition-opacity" />
                                  <span className="truncate underline underline-offset-2 decoration-white/10 group-hover:decoration-blue-300/40">
                                    {res.title}
                                  </span>
                                </a>
                              ))}
                            </div>
                          ) : (
                            <p className="text-[10px] text-white/20 mt-2 pt-2 border-t border-white/[0.06] italic">
                              No resources available
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* ── category breakdown ─────────── */}
                <div>
                  <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-3">
                    Category Readiness Breakdown
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {result.categoryBreakdown.map((cat) => (
                      <div key={cat.category} className={`${glass} p-4`}>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-white">{cat.category}</span>
                          <span className="text-xs text-white/50">{cat.percentage}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-white/[0.08] rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${cat.percentage}%` }}
                            transition={{ duration: 0.8 }}
                            className="h-full rounded-full bg-white/40 shadow-[0_0_8px_rgba(255,255,255,0.3)]"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* ── learning path orbital ──────── */}
                {orbitalData.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-white/70 uppercase tracking-wider mb-3 flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-white/50" />
                      Learning Path
                    </h3>
                    <div
                      className="relative rounded-xl p-2 overflow-hidden"
                      style={{
                        background: 'rgba(192,192,192,0.08)',
                        backdropFilter: 'blur(12px)',
                        WebkitBackdropFilter: 'blur(12px)',
                        border: '1px solid rgba(255,255,255,0.15)',
                        boxShadow: '0 0 25px rgba(255,255,255,0.05), inset 0 0 20px rgba(255,255,255,0.03)',
                      }}
                    >
                      <RadialOrbitalTimeline timelineData={orbitalData} />
                    </div>
                  </div>
                )}

                {/* ── footer ────────────────────── */}
                <p className="text-center text-white/20 text-xs pb-4">
                  Academic Portal 2024–25 · Student Project Guidance System
                </p>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkillGap;
