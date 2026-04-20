import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Compass, Lightbulb, BarChart3, Search, ChevronDown,
  LogOut, ExternalLink, AlertCircle
} from "lucide-react";
import { API_BASE } from "@/lib/api";

/* ── types ─────────────────────────────────────── */

interface ProjectSuggestion {
  title: string;
  description: string;
  level: string;
  technologies: string[];
}

// Domains shown in the dropdown (Feature 4)
const domains = [
  "Education",
  "Medical",
  "Web Development",
  "Artificial Intelligence",
  "Data Science",
  "Cyber Security",
  "IoT",
  "Cloud Computing",
  "Mobile App Development",
  "Blockchain",
  "FinTech",
  "Game Development",
  "Other (Type your own)",
];

const levels = ["Beginner", "Intermediate", "Advanced"];

/* ── API call ─────────────────────────────────── */

async function fetchProjectSuggestions(input: {
  interest: string;
  domain: string;
  level: string;
}): Promise<{ projects: ProjectSuggestion[]; match_source: string; matched_category: string }> {
  const response = await fetch(`${API_BASE}/api/project-guidance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(input),
  });
  if (!response.ok) throw new Error("Failed to fetch project suggestions");

  const data = await response.json();

  // Save activity for dashboard history (fire-and-forget)
  if (data.projects?.length > 0) {
    const localId = localStorage.getItem("shine_user_id");
    fetch(`${API_BASE}/api/save-activity`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        project: data.projects[0].title,
        level: input.level,
        missing_skills: 0,
        action: "search",
        user_id: localId ? parseInt(localId, 10) : undefined,
      }),
    }).catch(() => {}); // ignore errors
  }

  return data;
}

/* ── shared styles ────────────────────────────── */

const glass =
  "rounded-2xl backdrop-blur-xl bg-white/[0.06] border border-white/[0.12] shadow-[0_8px_60px_rgba(0,0,0,0.6),0_0_15px_rgba(255,255,255,0.03)]";

function levelColor(l: string) {
  if (l === "Beginner")     return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
  if (l === "Intermediate") return "bg-amber-500/20 text-amber-300 border-amber-500/30";
  return "bg-red-500/20 text-red-300 border-red-500/30";
}

function levelDot(l: string) {
  if (l === "Beginner")     return "bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.7)]";
  if (l === "Intermediate") return "bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.7)]";
  return "bg-red-400 shadow-[0_0_8px_rgba(248,113,113,0.7)]";
}

/* ════════════════════════════════════════════════ */

const ProjectGuidance = () => {
  const navigate = useNavigate();
  const location = useLocation();

  /* ── form state ── */
  const [interest,      setInterest]      = useState("");
  const [domain,        setDomain]        = useState("");
  const [customDomain,  setCustomDomain]  = useState("");
  const [selectedLevel, setSelectedLevel] = useState("");
  const [domainOpen,    setDomainOpen]    = useState(false);

  // Feature 4: "Other" custom domain
  const isOtherDomain = domain === "Other (Type your own)";
  const finalDomain   = isOtherDomain ? customDomain.trim() : domain;

  /* ── result state ── */
  // null  → no search has been made yet (Feature 0: don't show anything on load)
  // []    → search ran but no results
  // [...]  → results available
  const [results,       setResults]       = useState<ProjectSuggestion[] | null>(null);
  const [matchSource,   setMatchSource]   = useState<string>("");
  const [loading,       setLoading]       = useState(false);
  const [fetchError,    setFetchError]    = useState<string | null>(null);

  /* ── submit handler ── */
  const handleSubmit = async () => {
    if (!interest || !finalDomain || !selectedLevel) return;
    setLoading(true);
    setFetchError(null);
    setResults(null);
    try {
      const data = await fetchProjectSuggestions({
        interest,
        domain: finalDomain,
        level:  selectedLevel,
      });
      // Ensure each project echoes back the user's selected level
      const normalised = data.projects.map((p) => ({ ...p, level: selectedLevel }));
      setResults(normalised);
      setMatchSource(data.match_source || "");
    } catch (err) {
      console.error("Project guidance error:", err);
      setFetchError("Could not connect to the server. Please check your connection or try again later.");
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  /* ── Feature 1: navigate to details page ── */
  const handleViewDetails = (project: ProjectSuggestion) => {
    navigate("/project-details", {
      state: {
        title:        project.title,
        description:  project.description,
        technologies: project.technologies,
        level:        project.level,
      },
    });
  };

  const navLinks = [
    { label: "Project Guidance",  path: "/project-guidance" },
    { label: "Skill Gap Analysis", path: "/skill-gap" },
  ];

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-black">
      {/* ── white diagonal beams ── */}
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
        <div
          className="absolute top-0 left-[30%] w-[2px] h-full opacity-[0.03]"
          style={{ background: "linear-gradient(to bottom, transparent, white, transparent)" }}
        />
        <div
          className="absolute top-0 right-[25%] w-[2px] h-full opacity-[0.025]"
          style={{ background: "linear-gradient(to bottom, transparent, white, transparent)" }}
        />
      </div>

      {/* ── main content ── */}
      <div className="relative z-10 min-h-screen flex flex-col">

        {/* ── navbar ─── */}
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

        {/* ── header ─── */}
        <div className="px-8 pt-10 pb-6">
          <div className="flex items-center gap-3 mb-2">
            <Lightbulb className="w-7 h-7 text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.6)]" />
            <h1 className="text-3xl font-bold text-white tracking-tight">Project Guidance</h1>
          </div>
          <p className="text-white/60 text-base max-w-2xl">
            Tell us your interests and get the best project ideas based on your domain and skill level
          </p>
        </div>

        {/* ── two-column layout ── */}
        <div className="flex-1 px-8 pb-12 grid grid-cols-1 lg:grid-cols-[420px_1fr] gap-8">

          {/* ── LEFT — form ── */}
          <div className={`${glass} p-6 h-fit`}>

            {/* Interest */}
            <label className="block mb-1.5 text-sm font-medium text-white/80">
              Area of Interest
            </label>
            <input
              id="interest-input"
              value={interest}
              onChange={(e) => setInterest(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              placeholder="e.g. artificial intelligence, attendance system, e-commerce"
              className="w-full rounded-full bg-white/[0.06] border border-white/[0.1] px-4 py-2.5 text-sm text-white placeholder:text-white/30 outline-none focus:border-white/30 focus:shadow-[0_0_12px_rgba(255,255,255,0.08)] transition-all mb-5"
            />

            {/* Domain — Feature 4: dropdown + custom text input */}
            <label className="block mb-1.5 text-sm font-medium text-white/80">Domain</label>
            <div className="relative mb-5">
              <button
                id="domain-dropdown"
                onClick={() => setDomainOpen(!domainOpen)}
                className="w-full flex items-center justify-between rounded-full bg-white/[0.06] border border-white/[0.1] px-4 py-2.5 text-sm text-left outline-none focus:border-white/30 transition-all"
              >
                <span className={domain ? "text-white" : "text-white/30"}>
                  {domain || "Select domain"}
                </span>
                <ChevronDown className={`w-4 h-4 text-white/40 transition-transform ${domainOpen ? "rotate-180" : ""}`} />
              </button>

              <AnimatePresence>
                {domainOpen && (
                  <motion.ul
                    initial={{ opacity: 0, y: -4 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -4 }}
                    className="absolute z-20 mt-1 w-full rounded-xl bg-black/90 backdrop-blur-xl border border-white/[0.12] py-1 max-h-52 overflow-auto"
                  >
                    {domains.map((d) => (
                      <li
                        key={d}
                        onClick={() => {
                          setDomain(d);
                          setDomainOpen(false);
                          if (d !== "Other (Type your own)") setCustomDomain("");
                        }}
                        className={`px-4 py-2 text-sm cursor-pointer transition-colors ${
                          d === "Other (Type your own)"
                            ? "text-white/50 hover:bg-white/[0.08] hover:text-white italic border-t border-white/[0.08] mt-0.5"
                            : "text-white/70 hover:bg-white/[0.08] hover:text-white"
                        }`}
                      >
                        {d}
                      </li>
                    ))}
                  </motion.ul>
                )}
              </AnimatePresence>

              {/* Custom domain input — shown when "Other" selected */}
              <AnimatePresence>
                {isOtherDomain && (
                  <motion.div
                    initial={{ opacity: 0, height: 0, marginTop: 0 }}
                    animate={{ opacity: 1, height: "auto", marginTop: 8 }}
                    exit={{ opacity: 0, height: 0, marginTop: 0 }}
                    className="overflow-hidden"
                  >
                    <input
                      id="custom-domain-input"
                      value={customDomain}
                      onChange={(e) => setCustomDomain(e.target.value)}
                      placeholder="e.g. Blockchain, FinTech, Healthcare AI…"
                      className="w-full rounded-full bg-white/[0.06] border border-white/[0.15] px-4 py-2.5 text-sm text-white placeholder:text-white/30 outline-none focus:border-white/30 focus:shadow-[0_0_12px_rgba(255,255,255,0.08)] transition-all"
                      autoFocus
                    />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Difficulty */}
            <label className="block mb-2 text-sm font-medium text-white/80">Difficulty Level</label>
            <div className="flex gap-3 mb-6">
              {levels.map((l) => (
                <button
                  key={l}
                  id={`level-${l.toLowerCase()}`}
                  onClick={() => setSelectedLevel(l)}
                  className={`flex-1 rounded-full py-2 text-sm font-medium border transition-all flex items-center justify-center gap-2 ${
                    selectedLevel === l
                      ? "bg-white/[0.12] border-white/30 text-white shadow-[0_0_14px_rgba(255,255,255,0.1)]"
                      : "bg-white/[0.04] border-white/[0.08] text-white/50 hover:bg-white/[0.08] hover:text-white/70"
                  }`}
                >
                  <span className={`w-2 h-2 rounded-full ${levelDot(l)}`} />
                  {l}
                </button>
              ))}
            </div>

            {/* Submit */}
            <button
              id="find-projects-btn"
              onClick={handleSubmit}
              disabled={!interest || !finalDomain || !selectedLevel || loading}
              className="w-full rounded-full py-3 text-sm font-semibold text-white bg-gradient-to-r from-white/[0.12] to-white/[0.06] border border-white/[0.2] hover:from-white/[0.18] hover:to-white/[0.1] shadow-[0_0_20px_rgba(255,255,255,0.08)] hover:shadow-[0_0_30px_rgba(255,255,255,0.15)] transition-all disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {loading ? "Searching…" : "Find Matching Projects"}
            </button>
          </div>

          {/* ── RIGHT — results ── */}
          <div>
            {/* Feature 0: Before search — prompt message */}
            {results === null && !loading && (
              <div className={`${glass} p-10 flex flex-col items-center justify-center text-center min-h-[320px]`}>
                <Search className="w-10 h-10 text-white/20 mb-4" />
                <p className="text-white/50 text-base font-medium mb-1">
                  No projects shown yet
                </p>
                <p className="text-white/30 text-sm max-w-xs">
                  Enter your interests, choose a domain and difficulty level, then click{" "}
                  <span className="text-white/50">"Find Matching Projects"</span>
                </p>
              </div>
            )}

            {/* Loading spinner */}
            {loading && (
              <div className={`${glass} p-10 flex flex-col items-center justify-center min-h-[320px] gap-4`}>
                <div className="w-8 h-8 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                <p className="text-white/40 text-sm">Finding best projects for you…</p>
              </div>
            )}

            {/* Connection error */}
            {!loading && fetchError && (
              <div className={`${glass} p-10 flex flex-col items-center justify-center min-h-[320px] text-center gap-4`}>
                <AlertCircle className="w-10 h-10 text-red-400/60" />
                <p className="text-red-300/80 text-sm max-w-sm">{fetchError}</p>
              </div>
            )}

            {/* No results */}
            {!loading && !fetchError && results !== null && results.length === 0 && (
              <div className={`${glass} p-10 flex flex-col items-center justify-center min-h-[320px] text-center gap-3`}>
                <Search className="w-10 h-10 text-white/20" />
                <p className="text-white/50 text-base font-medium">No projects found</p>
                <p className="text-white/30 text-sm max-w-xs">
                  Try a different interest keyword or change the domain and difficulty.
                </p>
              </div>
            )}

            {/* Results */}
            {!loading && !fetchError && results !== null && results.length > 0 && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-5">
                <div className="flex items-center justify-between mb-1">
                  <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                    <BarChart3 className="w-5 h-5 text-white drop-shadow-[0_0_6px_rgba(255,255,255,0.5)]" />
                    Suggested Projects
                  </h2>
                  {/* match_source badge — useful for viva */}
                  {matchSource && (
                    <span className="text-xs text-white/30 font-mono bg-white/[0.04] border border-white/[0.08] px-2.5 py-0.5 rounded-full">
                      source: {matchSource}
                    </span>
                  )}
                </div>

                {results.map((p, i) => (
                  <motion.div
                    key={`${p.title}-${i}`}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.12 }}
                    className={`${glass} p-5`}
                  >
                    {/* Title + level badge */}
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-lg font-semibold text-white">{p.title}</h3>
                      <span className={`text-xs font-medium px-3 py-0.5 rounded-full border ${levelColor(p.level)}`}>
                        {p.level}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-white/60 text-sm leading-relaxed mb-3">{p.description}</p>

                    {/* Technology tags */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      {p.technologies.map((t) => (
                        <span
                          key={t}
                          className="text-xs px-2.5 py-0.5 rounded-full bg-white/[0.08] border border-white/[0.1] text-white/70"
                        >
                          {t}
                        </span>
                      ))}
                    </div>

                    {/* Feature 1: functional "View Details" button */}
                    <button
                      id={`view-details-${i}`}
                      onClick={() => handleViewDetails(p)}
                      className="inline-flex items-center gap-1.5 text-sm text-white/60 hover:text-white transition-colors underline underline-offset-4"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      View Details
                    </button>
                  </motion.div>
                ))}
              </motion.div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
};

export default ProjectGuidance;
