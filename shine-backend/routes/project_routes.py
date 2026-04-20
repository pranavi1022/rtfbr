"""
routes/project_routes.py
Endpoints:
  POST /api/project-guidance   — get project suggestions
  POST /api/project-details    — get enriched details for a specific project

Fixed:
  - dict() conversion for psycopg2 RealDictRow
  - Comment updated: PostgreSQL not MySQL
  - technologies split handles None safely
"""

import json
import os
from flask import Blueprint, request, jsonify
from logic.project_engine import get_project_suggestions
from logic.keyword_matcher import get_db_connection

project_bp = Blueprint('project', __name__)

# ── Required skills map (Feature 3) ─────────────────────────────────────
_REQUIRED_SKILLS_BY_TYPE = {
    "website": [
        {"name": "HTML",        "category": "Frontend",  "priority": "LOW",  "estimatedTime": "Est. ~1 week"},
        {"name": "CSS",         "category": "Frontend",  "priority": "LOW",  "estimatedTime": "Est. ~1 week"},
        {"name": "JavaScript",  "category": "Frontend",  "priority": "HIGH", "estimatedTime": "Est. ~2-3 weeks"},
        {"name": "React",       "category": "Frontend",  "priority": "HIGH", "estimatedTime": "Est. ~3-4 weeks"},
        {"name": "Python",      "category": "Backend",   "priority": "HIGH", "estimatedTime": "Est. ~2-3 weeks"},
        {"name": "Flask",       "category": "Backend",   "priority": "HIGH", "estimatedTime": "Est. ~1-2 weeks"},
        {"name": "PostgreSQL",  "category": "Database",  "priority": "HIGH", "estimatedTime": "Est. ~1-2 weeks"},
    ],
    "app": [
        {"name": "Java",        "category": "Android",        "priority": "HIGH", "estimatedTime": "Est. ~4-6 weeks"},
        {"name": "Kotlin",      "category": "Android",        "priority": "HIGH", "estimatedTime": "Est. ~3-4 weeks"},
        {"name": "Flutter",     "category": "Cross-Platform", "priority": "HIGH", "estimatedTime": "Est. ~3-4 weeks"},
        {"name": "React Native","category": "Cross-Platform", "priority": "HIGH", "estimatedTime": "Est. ~3-4 weeks"},
        {"name": "Firebase",    "category": "Backend",        "priority": "HIGH", "estimatedTime": "Est. ~1-2 weeks"},
        {"name": "REST API",    "category": "Integration",    "priority": "HIGH", "estimatedTime": "Est. ~1-2 weeks"},
    ],
    "other": [
        {"name": "Python",          "category": "Core",          "priority": "HIGH", "estimatedTime": "Est. ~2-3 weeks"},
        {"name": "Machine Learning","category": "AI/ML",         "priority": "HIGH", "estimatedTime": "Est. ~4-6 weeks"},
        {"name": "Pandas",          "category": "Data",          "priority": "HIGH", "estimatedTime": "Est. ~1-2 weeks"},
        {"name": "NumPy",           "category": "Data",          "priority": "LOW",  "estimatedTime": "Est. ~1 week"},
        {"name": "Matplotlib",      "category": "Visualization", "priority": "LOW",  "estimatedTime": "Est. ~1 week"},
        {"name": "scikit-learn",    "category": "AI/ML",         "priority": "HIGH", "estimatedTime": "Est. ~2-3 weeks"},
        {"name": "PostgreSQL",      "category": "Database",      "priority": "LOW",  "estimatedTime": "Est. ~1-2 weeks"},
    ],
    "gaming": [
        {"name": "Python",     "category": "Backend",    "priority": "HIGH", "estimatedTime": "Est. ~2-3 weeks"},
        {"name": "Pygame",     "category": "Game Engine","priority": "HIGH", "estimatedTime": "Est. ~2-3 weeks"},
        {"name": "JavaScript", "category": "Frontend",   "priority": "HIGH", "estimatedTime": "Est. ~2-3 weeks"},
        {"name": "Three.js",   "category": "Game Engine","priority": "HIGH", "estimatedTime": "Est. ~3-4 weeks"},
        {"name": "WebSocket",  "category": "Networking", "priority": "HIGH", "estimatedTime": "Est. ~1-2 weeks"},
    ],
}

_COMPLETION_TIME = {
    "Beginner":     "2–4 weeks",
    "Intermediate": "4–8 weeks",
    "Advanced":     "8–16 weeks",
}


# ── EXISTING ENDPOINT ────────────────────────────────────────────────────

@project_bp.route('/api/project-guidance', methods=['POST'])
def project_guidance():
    data = request.get_json() or {}

    interest   = data.get('interest', '').strip()
    domain     = data.get('domain',   '').strip()
    difficulty = data.get('level',    '').strip()

    if not interest or not domain or not difficulty:
        return jsonify({"error": "interest, domain, and level are required"}), 400

    if difficulty not in ('Beginner', 'Intermediate', 'Advanced'):
        return jsonify({"error": "level must be Beginner, Intermediate, or Advanced"}), 400

    print(f"[API] POST /api/project-guidance  interest={interest!r} domain={domain!r} level={difficulty!r}")
    result = get_project_suggestions(interest, domain, difficulty)
    return jsonify(result), 200


# ── FEATURE 1 — PROJECT DETAILS ENDPOINT ────────────────────────────────

@project_bp.route('/api/project-details', methods=['POST'])
def project_details():
    """
    Accepts: { title, difficulty, technologies[] }
    Returns enriched project data.

    Strategy:
      1. Try to fetch from PostgreSQL by exact title match
      2. Fall back to client-provided data (from JSON project list)
      3. Generate a structured default if both miss
    """
    data         = request.get_json() or {}
    title        = data.get('title',        '').strip()
    difficulty   = data.get('difficulty',   '').strip()
    technologies = data.get('technologies', [])
    description  = data.get('description', '').strip()

    if not title:
        return jsonify({"error": "title is required"}), 400

    if difficulty not in ('Beginner', 'Intermediate', 'Advanced'):
        difficulty = 'Beginner'

    # ── Layer 1: PostgreSQL ──────────────────────────────────────────────
    db_project = None
    print(f"[API] POST /api/project-details  title={title!r}")
    conn = get_db_connection()
    if conn is None:
        print(f"[DB] DB unavailable — using client-provided data for {title!r}")
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            print(f"[DB] Querying project title={title!r}")
            cursor.execute(
                """SELECT title, description, domain, difficulty, category, technologies
                   FROM projects
                   WHERE LOWER(title) = LOWER(%s)
                   LIMIT 1""",
                (title,)
            )
            row = cursor.fetchone()
            if row:
                db_project = dict(row)
            print(f"[DB] project-details hit: {bool(db_project)}")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[project_details] DB error: {e}")

    if db_project:
        tech_raw  = db_project.get("technologies") or ""
        tech_list = [t.strip() for t in tech_raw.split(",") if t.strip()]
        project_desc = db_project["description"]
        source = "db"
    else:
        # ── Layer 2: Client-provided data ─────────────────────────────────
        project_desc = description or ""
        tech_list    = technologies or []
        source       = "json" if description else "generated"

    # ── Estimate project type from technologies ──────────────────────────
    tech_lower   = [t.lower() for t in tech_list]
    project_type = "website"
    if any(t in tech_lower for t in ["flutter", "kotlin", "java", "react native", "swift", "dart"]):
        project_type = "app"
    elif any(t in tech_lower for t in ["pygame", "three.js", "unity", "unreal", "game engine"]):
        project_type = "gaming"
    elif any(t in tech_lower for t in ["python", "pandas", "tensorflow", "scikit-learn", "opencv", "nltk"]):
        project_type = "other"

    # ── Build required_skills from type map ──────────────────────────────
    required_skills = list(_REQUIRED_SKILLS_BY_TYPE.get(project_type, _REQUIRED_SKILLS_BY_TYPE["website"]))

    # Add any extra technologies not already in the map
    known_skill_names = {s["name"].lower() for s in required_skills}
    for tech in tech_list:
        if tech.lower() not in known_skill_names:
            required_skills.append({
                "name":          tech,
                "category":      "Technology",
                "priority":      "LOW",
                "estimatedTime": "Est. ~1-2 weeks"
            })
            known_skill_names.add(tech.lower())

    estimated_time = _COMPLETION_TIME.get(difficulty, "4–8 weeks")

    return jsonify({
        "title":           title,
        "description":     project_desc or f"A {difficulty.lower()} level {title} built using {', '.join(tech_list[:3])}{'...' if len(tech_list) > 3 else ''}.",
        "difficulty":      difficulty,
        "technologies":    tech_list,
        "required_skills": required_skills,
        "estimated_time":  estimated_time,
        "project_type":    project_type,
        "match_source":    source
    }), 200
