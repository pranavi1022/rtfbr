"""
logic/project_engine.py

Architecture (3 layers):
  Layer 1 — PostgreSQL/MySQL : primary source, category + difficulty query
  Layer 2 — JSON dataset     : rich fallback ONLY when DB returns 0 results
  Layer 3 — Generic template : last resort, always returns something

Fixes:
  - RANDOM() for PostgreSQL, RAND() for MySQL
  - dict() conversion on psycopg2 RealDictRow results
  - Synonym-aware category via match_keyword
  - Clear debug logs: DB category, fallback used, source
"""

import json
import os
from logic.keyword_matcher import match_keyword, get_db_connection
from config import DB_TYPE

# SQL dialect: PostgreSQL uses RANDOM(), MySQL uses RAND()
_SQL_RANDOM = "RANDOM()" if DB_TYPE == "postgresql" else "RAND()"

# Path to the rich JSON project fallback database
_JSON_PROJECTS_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'json_projects.json'
)

# Nearest-difficulty fallback order (DB layer only)
_FALLBACK_ORDER = {
    "Beginner":     ["Beginner",     "Intermediate", "Advanced"],
    "Intermediate": ["Intermediate", "Beginner",     "Advanced"],
    "Advanced":     ["Advanced",     "Intermediate", "Beginner"],
}


# ── helpers ────────────────────────────────────────────────────────────

def _dedup(projects: list) -> list:
    """Remove duplicate projects by title (case-insensitive)."""
    seen   = set()
    unique = []
    for p in projects:
        key = p["title"].strip().lower()
        if key not in seen:
            unique.append(p)
            seen.add(key)
    return unique


def _fetch_by_category_and_difficulty(cursor, category: str, difficulty: str) -> list:
    """
    Fetch up to 10 DISTINCT projects for a given category + difficulty from DB.
    LOWER() wrappers make the query case-insensitive.
    """
    cursor.execute(
        f"""SELECT DISTINCT title, description, domain, difficulty, technologies
           FROM projects
           WHERE LOWER(category)   = LOWER(%s)
             AND LOWER(difficulty) = LOWER(%s)
           ORDER BY {_SQL_RANDOM}
           LIMIT 10""",
        (category.strip().lower(), difficulty.strip())
    )
    rows = cursor.fetchall()
    # Convert psycopg2 RealDictRow → plain dict
    return [dict(r) for r in rows]


def _load_json_projects(category: str, difficulty: str) -> list:
    """
    Load projects from local JSON dataset (Layer 2 fallback).
    Only called when DB returns 0 results.
    """
    try:
        with open(_JSON_PROJECTS_PATH, 'r', encoding='utf-8') as f:
            db = json.load(f)
    except Exception as e:
        print(f"[project_engine] JSON load error: {e}")
        return []

    collected = []
    fallback_order = _FALLBACK_ORDER.get(difficulty, [difficulty])

    # Pass 1: same category, difficulty-prioritised
    if category in db:
        for diff_level in fallback_order:
            for entry in db[category].get(diff_level, []):
                collected.append({
                    "title":        entry["title"],
                    "description":  entry["description"],
                    "technologies": ",".join(entry["technologies"]),
                    "difficulty":   diff_level,
                    "domain":       ""
                })
            if len(_dedup(collected)) >= 3:
                break

    # Pass 2: different categories, same requested difficulty
    if len(_dedup(collected)) < 3:
        for cat_name, cat_data in db.items():
            if cat_name == category or cat_name == "_meta":
                continue
            for entry in cat_data.get(difficulty, []):
                collected.append({
                    "title":        entry["title"],
                    "description":  entry["description"],
                    "technologies": ",".join(entry["technologies"]),
                    "difficulty":   difficulty,
                    "domain":       ""
                })
            if len(_dedup(collected)) >= 3:
                break

    result = _dedup(collected)[:3]
    print(f"[project_engine] JSON dataset returned {len(result)} project(s) "
          f"for category={category!r} difficulty={difficulty!r}")
    return result


# ── main public function ───────────────────────────────────────────────

def get_project_suggestions(interest: str, domain: str, difficulty: str) -> dict:
    """
    Parameters
    ----------
    interest   : free-text interest (e.g. 'gaming', 'attendance system')
    domain     : selected domain   (e.g. 'Game Development', 'Education')
    difficulty : 'Beginner' | 'Intermediate' | 'Advanced'

    Returns
    -------
    {
        'match_source':      'db' | 'json' | 'generic',
        'matched_category':  str,
        'projects':          [ {title, description, level, technologies}, ... ]
    }
    """

    # ── Step 1: resolve category via keyword matching ──────────────────
    match          = match_keyword(interest, domain)
    category       = match["category"].strip().lower()
    matched_domain = match["domain"]

    # Normalize difficulty casing
    difficulty = difficulty.strip()
    if difficulty.lower() == "beginner":
        difficulty = "Beginner"
    elif difficulty.lower() == "intermediate":
        difficulty = "Intermediate"
    elif difficulty.lower() == "advanced":
        difficulty = "Advanced"

    print(f"\n[project_engine] ── REQUEST ─────────────────────────────────")
    print(f"[project_engine]  interest   = {interest!r}")
    print(f"[project_engine]  domain     = {domain!r}")
    print(f"[project_engine]  difficulty = {difficulty!r}")
    print(f"[project_engine]  category   = {category!r}  (from keyword match, source={match['source']!r})")
    print(f"[DB category]: {category}")

    raw_projects  = []
    result_source = "generic"

    # ── Step 2 (Layer 1): DB with difficulty fallback ──────────────────
    db_error = False
    conn = get_db_connection()
    if conn is None:
        db_error = True
        print(f"[project_engine]  DB unavailable — jumping to JSON fallback")
    else:
        try:
            cursor = conn.cursor(dictionary=True)

            for diff_level in _FALLBACK_ORDER.get(difficulty, [difficulty]):
                print(f"[DB] Querying: category={category!r} difficulty={diff_level!r}")
                rows = _fetch_by_category_and_difficulty(cursor, category, diff_level)
                print(f"[DB] Rows fetched: {len(rows)} raw, {len(_dedup(rows))} unique")

                raw_projects.extend(rows)
                unique_so_far = len(_dedup(raw_projects))

                if unique_so_far >= 3:
                    print(f"[project_engine]  Got {unique_so_far} unique from DB — stopping loop")
                    break

            # Last DB resort: same domain + requested difficulty
            if not _dedup(raw_projects):
                print(f"[project_engine]  Category empty — trying domain fallback: {matched_domain!r}")
                cursor.execute(
                    f"""SELECT DISTINCT title, description, domain, difficulty, technologies
                       FROM projects
                       WHERE LOWER(domain)     = LOWER(%s)
                         AND LOWER(difficulty) = LOWER(%s)
                       ORDER BY {_SQL_RANDOM}
                       LIMIT 10""",
                    (matched_domain.strip(), difficulty.strip())
                )
                domain_rows = [dict(r) for r in cursor.fetchall()]
                print(f"[DB] Domain fallback rows: {len(domain_rows)}")
                raw_projects.extend(domain_rows)

            cursor.close()
            conn.close()

        except Exception as e:
            db_error = True
            print(f"[project_engine]  DB query error: {e}")

    db_unique = _dedup(raw_projects)
    print(f"[project_engine]  DB layer total: {len(raw_projects)} raw, {len(db_unique)} unique after dedup")

    if db_unique:
        result_source = "db"

    # ── Step 3 (Layer 2): JSON project dataset fallback ────────────────
    # Only fires when DB produced ZERO unique results
    if len(db_unique) == 0:
        print(f"[project_engine]  DB returned 0 — loading JSON fallback dataset")
        json_projects = _load_json_projects(category, difficulty)
        print(f"[JSON fallback used]: category={category!r}")

        if json_projects:
            raw_projects.extend(json_projects)
            result_source = "json"
        else:
            print(f"[project_engine]  JSON fallback empty — will use generic template")

    # ── Step 4: Deduplicate and cap at 3 ──────────────────────────────
    unique_projects = _dedup(raw_projects)[:3]
    print(f"[project_engine]  Final projects: {len(unique_projects)}  source={result_source!r}")

    # ── Step 5: Format output ──────────────────────────────────────────
    result = []
    for p in unique_projects:
        tech_raw  = p.get("technologies", "")
        tech_list = [t.strip() for t in tech_raw.split(",") if t.strip()]
        result.append({
            "title":        p["title"],
            "description":  p["description"],
            "level":        difficulty,
            "technologies": tech_list
        })

    # ── Step 6 (Layer 3): Hard generic fallback ────────────────────────
    if not result:
        result_source = "generic"
        print(f"[project_engine]  All layers empty — using generic template")
        generic_map = {
            "Beginner": {
                "title":        f"Beginner {domain} Project",
                "description":  (
                    f"A simple beginner-level {domain} project. "
                    f"Build core features with a clean interface using HTML, CSS, Python, and PostgreSQL."
                ),
                "technologies": ["HTML", "CSS", "Python", "PostgreSQL"]
            },
            "Intermediate": {
                "title":        f"Intermediate {domain} Project",
                "description":  (
                    f"A full-stack {domain} project with user authentication, "
                    f"database-backed features, and a dynamic frontend."
                ),
                "technologies": ["HTML", "CSS", "JavaScript", "Python", "Flask", "PostgreSQL"]
            },
            "Advanced": {
                "title":        f"Advanced {domain} Project",
                "description":  (
                    f"A complex {domain} system with REST APIs, analytics dashboards, "
                    f"role-based access, and scalable architecture."
                ),
                "technologies": ["Python", "Flask", "PostgreSQL", "JavaScript", "React", "Docker"]
            },
        }
        g = generic_map.get(difficulty, generic_map["Intermediate"])
        result = [{**g, "level": difficulty}]

    print(f"[project_engine] ─────────────────────────────────────────────\n")

    return {
        "match_source":     result_source,   # 'db' | 'json' | 'generic'
        "matched_category": category,
        "projects":         result
    }
