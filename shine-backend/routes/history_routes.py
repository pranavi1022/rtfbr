"""
routes/history_routes.py

Endpoints:
  POST /api/save-activity        — save a user activity (project search / skill gap)
  GET  /api/user-history/<user_id> — fetch recent activity for a user
  GET  /api/my-history           — fetch history for logged-in user (session)

Activity is stored in PostgreSQL if available; falls back to in-memory store
so the Dashboard still works even when the database is offline.

Fixed:
  - dict() conversion on psycopg2 RealDictRow
  - commit() ensured after INSERT
  - _ensure_table only called once at startup (not per request)
  - Correct user_id handling from session and request body
  - Timestamp serialized to string safely
"""

from flask import Blueprint, request, jsonify, session
from logic.keyword_matcher import get_db_connection
from config import DB_TYPE
import time

history_bp = Blueprint('history', __name__)

# ── In-memory fallback store ─────────────────────────────────────────────
# { user_id (int): [ { project, level, missing_skills, action, timestamp } ] }
_memory_history: dict = {}
MAX_HISTORY_PER_USER = 20

# Track whether the DB table has been confirmed to exist this session
_table_ensured = False


def _ensure_table():
    """Create user_activity table if it doesn't exist (runs once at startup)."""
    global _table_ensured
    if _table_ensured:
        return
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        if DB_TYPE == "postgresql":
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_activity (
                    id             SERIAL PRIMARY KEY,
                    user_id        INT          NOT NULL,
                    project_name   VARCHAR(255) NOT NULL,
                    level          VARCHAR(50)  DEFAULT '',
                    missing_skills INT          DEFAULT 0,
                    action         VARCHAR(50)  DEFAULT 'search',
                    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_activity_user_id
                ON user_activity (user_id)
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_activity (
                    id             INT AUTO_INCREMENT PRIMARY KEY,
                    user_id        INT          NOT NULL,
                    project_name   VARCHAR(255) NOT NULL,
                    level          VARCHAR(50)  DEFAULT '',
                    missing_skills INT          DEFAULT 0,
                    action         VARCHAR(50)  DEFAULT 'search',
                    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX          idx_user_id (user_id)
                )
            """)
        conn.commit()
        cursor.close()
        conn.close()
        _table_ensured = True
        print("[history] user_activity table confirmed/created")
    except Exception as e:
        print(f"[history] Table creation error: {e}")


# Call at module load time so it's ready before first request
_ensure_table()


# ── Save Activity ────────────────────────────────────────────────────────

@history_bp.route('/api/save-activity', methods=['POST'])
def save_activity():
    """
    Save a user activity.
    Body: { project, level, missing_skills, action, user_id (optional) }
    user_id is read from session first, then request body as fallback.
    """
    data = request.get_json() or {}

    # Get user_id from session (primary) or body (fallback)
    user_id = session.get('user_id')
    if not user_id:
        user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user_id        = int(user_id)
    project        = data.get('project', '').strip()
    level          = data.get('level', '').strip()
    missing_skills = data.get('missing_skills', 0)
    action         = data.get('action', 'search')  # 'search' | 'skill_gap'

    if not project:
        return jsonify({"error": "project is required"}), 400

    print(f"[history] Saving activity: user_id={user_id} project={project!r} action={action!r}")

    # Try Database first
    saved_to_db = False
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO user_activity (user_id, project_name, level, missing_skills, action)
                   VALUES (%s, %s, %s, %s, %s)""",
                (user_id, project, level, int(missing_skills), action)
            )
            conn.commit()
            cursor.close()
            conn.close()
            saved_to_db = True
            print(f"[history] Activity saved to DB for user_id={user_id}: {project!r}")
        except Exception as e:
            print(f"[history] DB save error: {e}")

    # Always save to in-memory too (for instant fetching without DB)
    if user_id not in _memory_history:
        _memory_history[user_id] = []

    _memory_history[user_id].insert(0, {
        "project":        project,
        "level":          level,
        "missing_skills": missing_skills,
        "action":         action,
        "timestamp":      str(int(time.time()))
    })

    # Trim to last N
    _memory_history[user_id] = _memory_history[user_id][:MAX_HISTORY_PER_USER]

    return jsonify({
        "message": "Activity saved",
        "source":  "db" if saved_to_db else "memory"
    }), 201


# ── Fetch User History ───────────────────────────────────────────────────

@history_bp.route('/api/user-history/<int:user_id>', methods=['GET'])
def get_user_history(user_id: int):
    """Return the last 10 activities for a user. DB first, memory fallback."""
    activities = []
    source     = "memory"

    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """SELECT project_name AS project, level, missing_skills, action,
                          created_at AS timestamp
                   FROM user_activity
                   WHERE user_id = %s
                   ORDER BY created_at DESC
                   LIMIT 10""",
                (user_id,)
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if rows:
                activities = []
                for r in rows:
                    r = dict(r)
                    activities.append({
                        "project":        r["project"],
                        "level":          r["level"] or "",
                        "missing_skills": r["missing_skills"] or 0,
                        "action":         r["action"] or "search",
                        "timestamp":      str(r["timestamp"]) if r["timestamp"] else ""
                    })
                source = "db"
                print(f"[history] Fetched {len(activities)} rows from DB for user_id={user_id}")
        except Exception as e:
            print(f"[history] DB fetch error: {e}")

    # Fallback to memory
    if not activities and user_id in _memory_history:
        activities = _memory_history[user_id][:10]
        source = "memory"
        print(f"[history] Fetched {len(activities)} rows from memory for user_id={user_id}")

    return jsonify({
        "activities": activities,
        "source":     source
    }), 200


# ── Fetch current user's history (uses session) ─────────────────────────

@history_bp.route('/api/my-history', methods=['GET'])
def get_my_history():
    """Convenience endpoint: uses session user_id."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"activities": [], "source": "none"}), 200
    return get_user_history(int(user_id))
