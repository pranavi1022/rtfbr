import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FloatingPaths } from "@/components/ui/background-paths";
import { useNavigate } from "react-router-dom";
import { LogOut, Lightbulb, BarChart3, Clock, TrendingUp, Target, Zap, Rocket, Loader2, Inbox } from "lucide-react";
import { API_BASE } from "@/lib/api";

/* ── types ────────────────────────────────── */

interface ActivityItem {
  project: string;
  level: string;
  missing_skills: number;
  action: string;
}

interface ProgressItem {
  skill: string;
  percent: number;
}

/* ── static data ─────────────────────────── */

const quickTips = [
  {
    icon: Target,
    title: "Pick the Right Project",
    text: "Align your choice with your career goals, not just current trends.",
  },
  {
    icon: Zap,
    title: "Fill Your Skill Gaps",
    text: "Focus on foundational concepts before jumping into frameworks.",
  },
  {
    icon: Rocket,
    title: "Start Small, Grow Fast",
    text: "Ship an MVP first, then iterate with advanced features.",
  },
];

const cardClass =
  "rounded-2xl p-6 backdrop-blur-xl bg-white/[0.06] border border-white/[0.12] shadow-[0_8px_60px_rgba(0,0,0,0.6),0_0_15px_rgba(255,255,255,0.03)]";

/* ════════════════════════════════════════════ */

const Dashboard = () => {
  const navigate = useNavigate();

  const [username, setUsername]       = useState("Student");
  const [userId, setUserId]          = useState<number | null>(null);
  const [activityData, setActivity]  = useState<ActivityItem[]>([]);
  const [progressData, setProgress]  = useState<ProgressItem[]>([]);
  const [loadingActivity, setLoadingActivity] = useState(true);

  // ── Fetch user identity from session ───────────────────────────────
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/api/me`, { credentials: "include" });
        if (res.ok) {
          const data = await res.json();
          setUsername(data.username || "Student");
          setUserId(data.user_id);
        }
      } catch {
        // not logged in — Dashboard still renders with defaults
      }
    })();
  }, []);

  // ── Fetch real activity once we have userId ───────────────────────
  useEffect(() => {
    if (!userId) {
      setLoadingActivity(false);
      return;
    }
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/api/user-history/${userId}`, {
          credentials: "include",
        });
        if (res.ok) {
          const data = await res.json();
          const activities: ActivityItem[] = (data.activities || []).map(
            (a: any) => ({
              project:        a.project,
              level:          a.level || "—",
              missing_skills: a.missing_skills || 0,
              action:         a.action || "search",
            })
          );
          setActivity(activities);

          // Build progress from activity aggregation
          const categoryCounts: Record<string, number> = {};
          activities.forEach((a) => {
            const key = a.action === "skill_gap" ? "Analysis" : "Search";
            categoryCounts[key] = (categoryCounts[key] || 0) + 1;
          });
          const total = activities.length || 1;
          const progress: ProgressItem[] = Object.entries(categoryCounts).map(
            ([skill, count]) => ({
              skill,
              percent: Math.min(100, Math.round((count / total) * 100)),
            })
          );
          setProgress(progress);
        }
      } catch (err) {
        console.error("Failed to fetch activity:", err);
      } finally {
        setLoadingActivity(false);
      }
    })();
  }, [userId]);

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-black">
      <div className="absolute inset-0">
        <FloatingPaths position={1} />
        <FloatingPaths position={-1} />
      </div>

      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Top Navbar */}
        <motion.nav
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex items-center justify-between px-6 py-4 backdrop-blur-xl bg-white/[0.04] border-b border-white/[0.08]"
        >
          <h2 className="text-sm md:text-base font-semibold text-white truncate max-w-[60%]">
            Student-Centric Project Guidance and Skill Gap Analysis System
          </h2>
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-white/[0.08] border border-white/[0.12] flex items-center justify-center text-sm font-bold text-white">
              {username.charAt(0).toUpperCase()}
            </div>
            <button
              onClick={() => navigate("/")}
              className="flex items-center gap-1.5 text-sm text-white/50 hover:text-white/80 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </motion.nav>

        {/* Main Content */}
        <div className="flex-1 px-4 md:px-8 py-8 max-w-6xl mx-auto w-full space-y-8">
          {/* 1. Welcome Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <h1 className="text-3xl md:text-4xl font-bold text-white">
              Welcome back, {username}
            </h1>
            <p className="text-base md:text-lg text-white/70 mt-2">
              Explore project ideas and analyze your skill gaps
            </p>
          </motion.div>

          {/* 2. Action Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className={cardClass}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-full bg-white/[0.10] border border-white/[0.20] flex items-center justify-center shadow-[0_0_12px_rgba(255,255,255,0.08)]">
                  <Lightbulb className="w-5 h-5 text-white drop-shadow-[0_0_4px_rgba(255,255,255,0.4)]" />
                </div>
                <h3 className="text-lg font-semibold text-white">Project Guidance</h3>
              </div>
              <p className="text-sm text-white/60 mb-6 leading-relaxed">
                Describe your interests and domain expertise. The system will match you with optimal project ideas suited to your level.
              </p>
              <button
                onClick={() => navigate("/project-guidance")}
                className="w-full h-11 rounded-full bg-white/[0.08] hover:bg-white/[0.14] text-white font-semibold text-sm border border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.3)] transition-colors"
              >
                Get Project Ideas
              </button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className={cardClass}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-full bg-white/[0.10] border border-white/[0.20] flex items-center justify-center shadow-[0_0_12px_rgba(255,255,255,0.08)]">
                  <BarChart3 className="w-5 h-5 text-white drop-shadow-[0_0_4px_rgba(255,255,255,0.4)]" />
                </div>
                <h3 className="text-lg font-semibold text-white">Skill Gap Analysis</h3>
              </div>
              <p className="text-sm text-white/60 mb-6 leading-relaxed">
                Input a project description and your existing skills. Visualize your learning path through an interactive timeline.
              </p>
              <button
                onClick={() => navigate("/skill-gap")}
                className="w-full h-11 rounded-full bg-white/[0.08] hover:bg-white/[0.14] text-white font-semibold text-sm border border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.3)] transition-colors"
              >
                Analyze My Skills
              </button>
            </motion.div>
          </div>

          {/* 3. Activity + Progress (REAL DATA) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className={cardClass}
            >
              <div className="flex items-center gap-3 mb-5">
                <Clock className="w-5 h-5 text-white drop-shadow-[0_0_4px_rgba(255,255,255,0.4)]" />
                <h3 className="text-lg font-semibold text-white">Recent Activity</h3>
              </div>

              {/* Loading state */}
              {loadingActivity && (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-6 h-6 text-white/30 animate-spin" />
                </div>
              )}

              {/* Empty state */}
              {!loadingActivity && activityData.length === 0 && (
                <div className="flex flex-col items-center justify-center py-8 text-center">
                  <Inbox className="w-8 h-8 text-white/20 mb-2" />
                  <p className="text-sm text-white/40">No activity yet.</p>
                  <p className="text-xs text-white/25 mt-1">
                    Search for projects or analyze skills to see history here.
                  </p>
                </div>
              )}

              {/* Activity list */}
              {!loadingActivity && activityData.length > 0 && (
                <div className="space-y-4">
                  {activityData.slice(0, 5).map((item, idx) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]"
                    >
                      <div>
                        <p className="text-sm font-medium text-white">{item.project}</p>
                        <p className="text-xs text-white/50">
                          {item.level} · {item.action === "skill_gap" ? "Skill Gap" : "Project Search"}
                        </p>
                      </div>
                      <span className="text-xs text-white/60 whitespace-nowrap">
                        {item.missing_skills} skill{item.missing_skills !== 1 ? "s" : ""} missing
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className={cardClass}
            >
              <div className="flex items-center gap-3 mb-5">
                <TrendingUp className="w-5 h-5 text-white drop-shadow-[0_0_4px_rgba(255,255,255,0.4)]" />
                <h3 className="text-lg font-semibold text-white">Skill Progress</h3>
              </div>

              {/* Empty state */}
              {progressData.length === 0 && (
                <div className="flex flex-col items-center justify-center py-8 text-center">
                  <TrendingUp className="w-8 h-8 text-white/20 mb-2" />
                  <p className="text-sm text-white/40">No progress data yet.</p>
                  <p className="text-xs text-white/25 mt-1">
                    Complete a skill gap analysis to see insights.
                  </p>
                </div>
              )}

              {/* Progress bars */}
              {progressData.length > 0 && (
                <div className="space-y-5">
                  {progressData.map((item, idx) => (
                    <div key={idx}>
                      <div className="flex justify-between text-sm mb-1.5">
                        <span className="text-white font-medium">{item.skill}</span>
                        <span className="text-white/70">{item.percent}%</span>
                      </div>
                      <div className="h-3.5 rounded-full bg-white/[0.06] overflow-hidden border border-white/[0.15] shadow-[0_0_8px_rgba(255,255,255,0.08),inset_0_0_4px_rgba(255,255,255,0.04)]">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${item.percent}%` }}
                          transition={{ duration: 1.2, delay: 0.6 + idx * 0.15, ease: "easeOut" }}
                          className="h-full rounded-full relative overflow-hidden bg-white/[0.6] border border-white/[0.7] shadow-[0_0_6px_rgba(255,255,255,0.7),0_0_14px_rgba(255,255,255,0.4),0_0_30px_rgba(255,255,255,0.2)]"
                          style={{ backgroundImage: "linear-gradient(90deg, rgba(255,255,255,0.3), rgba(255,255,255,0.7) 80%, rgba(255,255,255,0.95) 100%)" }}
                        >
                          <div
                            className="absolute inset-0 animate-[shimmer_2s_ease-in-out_infinite]"
                            style={{
                              backgroundImage: "linear-gradient(90deg, transparent 0%, rgba(255,255,255,0) 30%, rgba(255,255,255,0.8) 50%, rgba(255,255,255,0) 70%, transparent 100%)",
                              backgroundSize: "200% 100%",
                            }}
                          />
                        </motion.div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </motion.div>
          </div>

          {/* 4. Quick Tips */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <h3 className="text-xl font-semibold text-white mb-4">Quick Tips</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {quickTips.map((tip, idx) => (
                <div key={idx} className={cardClass}>
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-9 h-9 rounded-full bg-white/[0.10] border border-white/[0.20] flex items-center justify-center shadow-[0_0_10px_rgba(255,255,255,0.06)]">
                      <tip.icon className="w-4 h-4 text-white drop-shadow-[0_0_4px_rgba(255,255,255,0.4)]" />
                    </div>
                    <h4 className="text-sm font-semibold text-white">{tip.title}</h4>
                  </div>
                  <p className="text-sm text-white/60 leading-relaxed">{tip.text}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
