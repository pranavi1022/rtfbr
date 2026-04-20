"""
app.py — SHINE Access Point Backend Entry Point
Deployed on Render with gunicorn app:app
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

from config import FLASK_PORT, FLASK_SECRET, DB_TYPE, DB_CONFIG
from routes.auth_routes    import auth_bp
from routes.project_routes import project_bp
from routes.skill_routes   import skill_bp
from routes.history_routes import history_bp

app = Flask(__name__)

# ── Session secret key ──────────────────────────────────────────────
app.secret_key = FLASK_SECRET

# ── CORS: allow frontend origins ────────────────────────────────────
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://rtfbr-1.onrender.com",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5174",
    ],
    "supports_credentials": True
}})

# ── Register blueprints (routes already have /api prefix) ───────────
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(skill_bp)
app.register_blueprint(history_bp)

print(f"[APP] DB_TYPE = {DB_TYPE}")
print(f"[APP] DB_CONFIG host = {DB_CONFIG.get('host', 'N/A')}")
print(f"[APP] DB_CONFIG dbname = {DB_CONFIG.get('dbname', DB_CONFIG.get('database', 'N/A'))}")


# ── Root health-check ───────────────────────────────────────────────
@app.route('/')
def index():
    return jsonify({
        "message": "SHINE Access Point Backend is running",
        "status": "ok",
        "db_type": DB_TYPE,
        "version": "2.1.0"
    })


# ── Test endpoint ───────────────────────────────────────────────────
@app.route('/api/test')
def api_test():
    from logic.keyword_matcher import get_db_connection
    conn = get_db_connection()
    if conn is not None:
        conn.close()
        return jsonify({"status": "ok", "database": "connected", "db_type": DB_TYPE})
    else:
        return jsonify({"status": "error", "database": "not connected", "db_type": DB_TYPE}), 500


if __name__ == '__main__':
    print("=" * 55)
    print("  SHINE Access Point — Flask Backend v2.1")
    print(f"  DB_TYPE: {DB_TYPE}")
    print(f"  Running at: http://localhost:{FLASK_PORT}")
    print("=" * 55)
    port = int(os.environ.get("PORT", FLASK_PORT))
    app.run(host="0.0.0.0", port=port)