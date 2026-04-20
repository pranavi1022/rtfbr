"""
logic/skill_engine.py

Analyses the gap between what a student knows and what a project requires.
Uses PostgreSQL/MySQL first, falls back to JSON dataset, then hardcoded.

Fixed:
  - dict() conversion on psycopg2 RealDictRow results
  - Duplicate skills removed (by skill_name + project_type key)
  - Weighted readiness calculated on deduplicated list
  - Learning resources fetched from DB (learning_resources table)
  - Clear debug logs: Skills, fallback used
"""

import json
import os
import random
from logic.keyword_matcher import get_db_connection


# ── Aliases for common skill short-forms ──────────────────────────────────
_SKILL_ALIASES = {
    "js":       "javascript",
    "py":       "python",
    "ts":       "typescript",
    "node":     "node.js",
    "react.js": "react",
    "vue.js":   "vue",
    "pg":       "postgresql",
    "postgres": "postgresql",
    "mongo":    "mongodb",
    "tf":       "tensorflow",
    "sklearn":  "scikit-learn",
    "rn":       "react native",
    "ml":       "machine learning",
    "dl":       "deep learning",
    "css3":     "css",
    "html5":    "html",
    "sql":      "postgresql",
    "db":       "postgresql",
}


# ── Hardcoded resource fallback (used ONLY when DB is down) ───────────────
_FALLBACK_RESOURCES: dict = {
    "HTML":             [{"title": "HTML Foundations",           "link": "https://developer.mozilla.org/en-US/docs/Learn/HTML"}],
    "CSS":              [{"title": "CSS Fundamentals",           "link": "https://web.dev/learn/css"}],
    "JavaScript":       [{"title": "JavaScript Guide (MDN)",     "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"}],
    "React":            [{"title": "React Official Docs",        "link": "https://react.dev/learn"}],
    "Python":           [{"title": "Python Official Tutorial",   "link": "https://docs.python.org/3/tutorial/"}],
    "Flask":            [{"title": "Flask Official Tutorial",    "link": "https://flask.palletsprojects.com/en/3.0.x/tutorial/"}],
    "Node.js":          [{"title": "Node.js Docs",               "link": "https://nodejs.org/en/learn"}],
    "PostgreSQL":       [{"title": "PostgreSQL Tutorial",        "link": "https://www.postgresqltutorial.com/"}],
    "MySQL":            [{"title": "MySQL Tutorial",             "link": "https://dev.mysql.com/doc/refman/8.0/en/tutorial.html"}],
    "MongoDB":          [{"title": "MongoDB University",         "link": "https://learn.mongodb.com/"}],
    "Firebase":         [{"title": "Firebase Docs",              "link": "https://firebase.google.com/docs"}],
    "Java":             [{"title": "Java Programming",           "link": "https://dev.java/learn/"}],
    "Kotlin":           [{"title": "Kotlin for Android",         "link": "https://kotlinlang.org/docs/getting-started.html"}],
    "Flutter":          [{"title": "Flutter Official Docs",      "link": "https://docs.flutter.dev/get-started/codelab"}],
    "React Native":     [{"title": "React Native Docs",          "link": "https://reactnative.dev/docs/getting-started"}],
    "Machine Learning": [{"title": "ML Crash Course (Google)",   "link": "https://developers.google.com/machine-learning/crash-course"}],
    "TensorFlow":       [{"title": "TensorFlow Tutorials",       "link": "https://www.tensorflow.org/tutorials"}],
    "scikit-learn":     [{"title": "Scikit-learn Guide",         "link": "https://scikit-learn.org/stable/user_guide.html"}],
    "Pandas":           [{"title": "Pandas User Guide",          "link": "https://pandas.pydata.org/docs/user_guide/index.html"}],
    "NumPy":            [{"title": "NumPy Quickstart",           "link": "https://numpy.org/doc/stable/user/quickstart.html"}],
    "Matplotlib":       [{"title": "Matplotlib Tutorials",       "link": "https://matplotlib.org/stable/tutorials/index.html"}],
    "Docker":           [{"title": "Docker Get Started",         "link": "https://docs.docker.com/get-started/"}],
    "Git":              [{"title": "Git Book",                   "link": "https://git-scm.com/book/en/v2"}],
    "REST API":         [{"title": "REST API Design Guide",      "link": "https://restfulapi.net/"}],
    "Pygame":           [{"title": "Pygame Documentation",       "link": "https://www.pygame.org/docs/"}],
    "Three.js":         [{"title": "Three.js Manual",            "link": "https://threejs.org/manual/#en/fundamentals"}],
    "WebSocket":        [{"title": "WebSocket API (MDN)",        "link": "https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API"}],
}


def fetch_learning_resources(skill_name: str) -> list:
    """
    Fetch learning resources for a skill from the learning_resources table.
    Case-insensitive match. Falls back to _FALLBACK_RESOURCES if DB down.

    Returns: [ { "title": str, "link": str }, ... ]
    """
    resources = []

    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT resource_title, resource_link
                   FROM learning_resources
                   WHERE LOWER(skill_name) = LOWER(%s)
                   ORDER BY CASE difficulty
                     WHEN 'Beginner'     THEN 1
                     WHEN 'Intermediate' THEN 2
                     WHEN 'Advanced'     THEN 3
                     ELSE 4 END""",
                (skill_name.strip(),)
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in rows:
                row = dict(row)
                resources.append({
                    "title": row["resource_title"],
                    "link":  row["resource_link"],
                })

            if resources:
                print(f"[skill_engine] [OK] DB resources for '{skill_name}': {len(resources)} found")
                return resources

        except Exception as e:
            print(f"[skill_engine] DB resource query error for '{skill_name}': {e}")

    # Fallback: hardcoded resources (safety net)
    fallback = _FALLBACK_RESOURCES.get(skill_name, [])
    if fallback:
        print(f"[skill_engine] [FALLBACK] Using hardcoded resources for '{skill_name}': {len(fallback)}")
    return fallback


# ── Feature 3: hardcoded required skills per project type ─────────────────
_HARDCODED_REQUIRED_SKILLS: dict = {
    "website": [
        {"skill_name": "HTML",       "category": "Frontend",    "weight": 2, "estimated_time": "1 week"},
        {"skill_name": "CSS",        "category": "Frontend",    "weight": 2, "estimated_time": "1 week"},
        {"skill_name": "JavaScript", "category": "Frontend",    "weight": 4, "estimated_time": "2-3 weeks"},
        {"skill_name": "React",      "category": "Frontend",    "weight": 3, "estimated_time": "3-4 weeks"},
        {"skill_name": "Python",     "category": "Backend",     "weight": 4, "estimated_time": "2-3 weeks"},
        {"skill_name": "Flask",      "category": "Backend",     "weight": 3, "estimated_time": "1-2 weeks"},
        {"skill_name": "PostgreSQL", "category": "Database",    "weight": 3, "estimated_time": "1-2 weeks"},
    ],
    "app": [
        {"skill_name": "Java",         "category": "Android",        "weight": 4, "estimated_time": "4-6 weeks"},
        {"skill_name": "Kotlin",       "category": "Android",        "weight": 4, "estimated_time": "3-4 weeks"},
        {"skill_name": "Flutter",      "category": "Cross-Platform", "weight": 4, "estimated_time": "3-4 weeks"},
        {"skill_name": "React Native", "category": "Cross-Platform", "weight": 4, "estimated_time": "3-4 weeks"},
        {"skill_name": "Firebase",     "category": "Backend",        "weight": 3, "estimated_time": "1-2 weeks"},
        {"skill_name": "REST API",     "category": "Integration",    "weight": 3, "estimated_time": "1-2 weeks"},
    ],
    "other": [
        {"skill_name": "Python",          "category": "Core",          "weight": 5, "estimated_time": "2-3 weeks"},
        {"skill_name": "Machine Learning","category": "AI/ML",         "weight": 5, "estimated_time": "4-6 weeks"},
        {"skill_name": "Pandas",          "category": "Data",          "weight": 3, "estimated_time": "1-2 weeks"},
        {"skill_name": "NumPy",           "category": "Data",          "weight": 2, "estimated_time": "1 week"},
        {"skill_name": "Matplotlib",      "category": "Visualization", "weight": 2, "estimated_time": "1 week"},
        {"skill_name": "scikit-learn",    "category": "AI/ML",         "weight": 4, "estimated_time": "2-3 weeks"},
        {"skill_name": "PostgreSQL",      "category": "Database",      "weight": 2, "estimated_time": "1-2 weeks"},
    ],
    "gaming": [
        {"skill_name": "Python",     "category": "Backend",    "weight": 3, "estimated_time": "2-3 weeks"},
        {"skill_name": "Pygame",     "category": "Game Engine","weight": 4, "estimated_time": "2-3 weeks"},
        {"skill_name": "JavaScript", "category": "Frontend",   "weight": 4, "estimated_time": "2-3 weeks"},
        {"skill_name": "Three.js",   "category": "Game Engine","weight": 4, "estimated_time": "3-4 weeks"},
        {"skill_name": "WebSocket",  "category": "Networking", "weight": 3, "estimated_time": "1-2 weeks"},
        {"skill_name": "HTML",       "category": "Frontend",   "weight": 2, "estimated_time": "1 week"},
        {"skill_name": "CSS",        "category": "Frontend",   "weight": 2, "estimated_time": "1 week"},
    ],
}


def _dedup_skills(skills: list) -> list:
    """Remove duplicate skills — keyed on (skill_name, project_type)."""
    seen   = set()
    unique = []
    for skill in skills:
        key = (skill["skill_name"].lower(), skill.get("project_type", "").lower())
        if key not in seen:
            unique.append(skill)
            seen.add(key)
    return unique


def analyze_skill_gap(project_description: str, project_type: str, user_skills: list) -> dict:
    """
    Parameters
    ----------
    project_description : user-supplied project name / description
    project_type        : 'website' | 'app' | 'other' | 'gaming'
    user_skills         : list of skill strings the student already knows

    Returns a rich result dict consumed by the React frontend.
    """
    project_type_lower = project_type.lower()
    user_skills_lower  = [s.strip().lower() for s in user_skills]
    raw_skills         = []
    source             = "db"

    print(f"\n[skill_engine] ── REQUEST ──────────────────────────────────")
    print(f"[skill_engine]  project      = {project_description!r}")
    print(f"[skill_engine]  project_type = {project_type_lower!r}")
    print(f"[skill_engine]  user_skills  = {user_skills_lower}")

    # ── Layer 1: Database ────────────────────────────────────────────
    conn = get_db_connection()
    if conn is None:
        print(f"[skill_engine] [WARN] DB unavailable — skipping to JSON/hardcoded fallback")
        source = "json"
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            print(f"[DB] Querying skills: project_type={project_type_lower!r}")
            cursor.execute(
                """SELECT skill_name, project_type, category, weight, estimated_time
                   FROM skills WHERE LOWER(project_type) = LOWER(%s)""",
                (project_type_lower,)
            )
            rows = cursor.fetchall()
            raw_skills = [dict(r) for r in rows]
            print(f"[DB] Rows fetched: {len(raw_skills)} skill(s)")
            print(f"[Skills from DB]: {[s['skill_name'] for s in raw_skills]}")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[skill_engine] DB query error: {e}")
            source = "json"

    # ── Layer 2: JSON fallback ────────────────────────────────────────────
    if not raw_skills:
        print(f"[skill_engine] DB returned nothing — trying JSON dataset")
        source = "json"
        try:
            json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'skills_dataset.json')
            with open(json_path, 'r') as f:
                skills_data = json.load(f)

            type_key  = project_type_lower if project_type_lower in skills_data else "website"
            type_data = skills_data[type_key]
            print(f"[JSON fallback used]: project_type={type_key!r}")

            for category, cat_data in type_data.items():
                if category in ("dependencies", "learning_resources"):
                    continue
                for skill in cat_data.get("skills", []):
                    weight = cat_data.get("weights", {}).get(skill, 1)
                    raw_skills.append({
                        "skill_name":     skill,
                        "project_type":   project_type_lower,
                        "category":       category,
                        "weight":         weight,
                        "estimated_time": "1-2 weeks"
                    })
            print(f"[skill_engine] JSON gave {len(raw_skills)} skill(s)")
        except Exception as e:
            print(f"[skill_engine] JSON fallback error: {e}")

    # ── Layer 3: Hardcoded fallback ───────────────────────────────────────
    if not raw_skills:
        print(f"[skill_engine] Both DB and JSON empty — using hardcoded for '{project_type_lower}'")
        source = "hardcoded"
        hardcoded_key = project_type_lower if project_type_lower in _HARDCODED_REQUIRED_SKILLS else "website"
        for entry in _HARDCODED_REQUIRED_SKILLS[hardcoded_key]:
            raw_skills.append({**entry, "project_type": project_type_lower})

    # ── Deduplication ─────────────────────────────────────────────────
    required_skills = _dedup_skills(raw_skills)

    # ── Helper: check if user has this skill ──────────────────────────
    def _user_has_skill(required_lower: str) -> bool:
        """Case-insensitive, partial, alias-aware skill matching."""
        for u in user_skills_lower:
            u_expanded = _SKILL_ALIASES.get(u, u)
            r_expanded = _SKILL_ALIASES.get(required_lower, required_lower)
            if u_expanded == r_expanded:
                return True
            if r_expanded in u_expanded or u_expanded in r_expanded:
                return True
        return False

    # ── Skill comparison ──────────────────────────────────────────────
    matched = []
    missing = []

    for skill_row in required_skills:
        skill_name  = skill_row["skill_name"]
        skill_lower = skill_name.lower()
        is_matched  = _user_has_skill(skill_lower)

        if is_matched:
            weight      = skill_row.get("weight", 1)
            base        = min(85, 55 + weight * 7)
            jitter      = random.randint(-3, 5)
            proficiency = max(60, min(90, base + jitter))
            matched.append({
                "name":        skill_name,
                "category":    skill_row["category"],
                "proficiency": proficiency
            })
        else:
            weight    = skill_row.get("weight", 1)
            resources = fetch_learning_resources(skill_name)
            missing.append({
                "name":          skill_name,
                "category":      skill_row["category"],
                "priority":      "HIGH" if weight >= 3 else "LOW",
                "estimatedTime": f"Est. ~{skill_row.get('estimated_time', '1-2 weeks')}",
                "resources":     resources,
            })

    print(f"[Skills]: matched={len(matched)}, missing={len(missing)}")

    # ── Dependency ordering ───────────────────────────────────────────
    dependency_order = {}
    try:
        conn2 = get_db_connection()
        if conn2 is not None:
            cursor2 = conn2.cursor(dictionary=True)
            print("[DB] Querying skill_dependencies table")
            cursor2.execute("SELECT skill_name, depends_on FROM skill_dependencies")
            deps = cursor2.fetchall()
            print(f"[DB] {len(deps)} dependency row(s)")
            for d in deps:
                d = dict(d)
                dependency_order.setdefault(d["skill_name"], []).append(d["depends_on"])
            cursor2.close()
            conn2.close()
        else:
            print("[skill_engine] Skipping dependency ordering — DB unavailable")
    except Exception as e:
        print(f"[skill_engine] Dependency query error: {e}")

    def dep_depth(skill_name: str) -> int:
        return len(dependency_order.get(skill_name, []))

    missing.sort(key=lambda s: dep_depth(s["name"]))

    # ── Weighted readiness score ──────────────────────────────────────
    total_weight   = sum(s.get("weight", 1) for s in required_skills)
    matched_weight = sum(
        s.get("weight", 1) for s in required_skills
        if _user_has_skill(s["skill_name"].lower())
    )
    readiness = round((matched_weight / total_weight) * 100) if total_weight > 0 else 0

    # ── Level classification ──────────────────────────────────────────
    if readiness >= 70:
        level = "Advanced"
    elif readiness >= 40:
        level = "Intermediate"
    else:
        level = "Beginner"

    # ── Category breakdown ────────────────────────────────────────────
    categories: dict = {}
    for skill_row in required_skills:
        cat = skill_row["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "matched": 0}
        categories[cat]["total"] += 1
        if _user_has_skill(skill_row["skill_name"].lower()):
            categories[cat]["matched"] += 1

    category_breakdown = [
        {
            "category":   cat,
            "percentage": round((v["matched"] / v["total"]) * 100) if v["total"] > 0 else 0
        }
        for cat, v in categories.items()
    ]

    # ── Learning path ─────────────────────────────────────────────────
    learning_path = []
    for ms in missing:
        for res in ms.get("resources", []):
            learning_path.append({
                "skill":       ms["name"],
                "title":       res["title"],
                "description": f"Learn {ms['name']} — {res['title']}",
                "link":        res["link"]
            })

    print(f"[skill_engine] ── RESULT: readiness={readiness}% level={level!r} source={source!r}")
    print(f"[skill_engine] ─────────────────────────────────────────────\n")

    return {
        "projectName":       project_description,
        "level":             level,
        "readinessScore":    readiness,
        "totalRequired":     len(required_skills),
        "matchedCount":      len(matched),
        "missingCount":      len(missing),
        "skillsYouHave":     matched,
        "missingSkills":     missing,
        "learningPath":      learning_path,
        "categoryBreakdown": category_breakdown,
        "source":            source
    }
