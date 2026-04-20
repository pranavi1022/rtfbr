"""
app.py — SHINE Access Point Backend
Deployed on Render with gunicorn
"""

import os
import sys

# Force print to flush immediately (critical for Render/gunicorn logs)
import functools
print = functools.partial(print, flush=True)

print("[BOOT] Starting SHINE backend...")
print(f"[BOOT] Python version: {sys.version}")
print(f"[BOOT] Working directory: {os.getcwd()}")
print(f"[BOOT] DATABASE_URL set: {bool(os.environ.get('DATABASE_URL'))}")
print(f"[BOOT] PORT: {os.environ.get('PORT', 'not set')}")

# ── Step 1: Flask ────────────────────────────────────────────────────
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
print("[BOOT] Flask app created")

# ── Step 2: Config ───────────────────────────────────────────────────
try:
    from config import FLASK_PORT, FLASK_SECRET, DB_TYPE, DB_CONFIG
    app.secret_key = FLASK_SECRET
    print(f"[BOOT] Config loaded: DB_TYPE={DB_TYPE}")
    print(f"[BOOT] DB host={DB_CONFIG.get('host')}, dbname={DB_CONFIG.get('dbname', DB_CONFIG.get('database'))}")
except Exception as e:
    print(f"[BOOT] ERROR loading config: {e}")
    DB_TYPE = "unknown"
    app.secret_key = "fallback_secret"

# ── Step 3: CORS ─────────────────────────────────────────────────────
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://rtfbr-1.onrender.com",                    # Frontend on Render
            "https://shine-backend-08ll.onrender.com",         # Backend (for testing)
            "http://localhost:5173",                           # Local Vite dev
            "http://localhost:3000",                           # Fallback local
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    },
    r"/*": {
        "origins": "*"  # Allow root routes without CORS restrictions
    }
})
print("[BOOT] CORS configured")

# ── Step 4: Register blueprints ──────────────────────────────────────
try:
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    print("[BOOT] auth_bp registered")
except Exception as e:
    print(f"[BOOT] ERROR registering auth_bp: {e}")

try:
    from routes.project_routes import project_bp
    app.register_blueprint(project_bp)
    print("[BOOT] project_bp registered")
except Exception as e:
    print(f"[BOOT] ERROR registering project_bp: {e}")

try:
    from routes.skill_routes import skill_bp
    app.register_blueprint(skill_bp)
    print("[BOOT] skill_bp registered")
except Exception as e:
    print(f"[BOOT] ERROR registering skill_bp: {e}")

try:
    from routes.history_routes import history_bp
    app.register_blueprint(history_bp)
    print("[BOOT] history_bp registered")
except Exception as e:
    print(f"[BOOT] ERROR registering history_bp: {e}")

# ── Root route ───────────────────────────────────────────────────────
@app.route('/')
def index():
    return jsonify({
        "message": "SHINE Backend is running",
        "status": "ok",
        "db_type": DB_TYPE
    })

# ── Test route ───────────────────────────────────────────────────────
@app.route('/api/test')
def api_test():
    try:
        from logic.keyword_matcher import get_db_connection
        conn = get_db_connection()
        if conn is not None:
            conn.close()
            return jsonify({"status": "ok", "database": "connected", "db_type": DB_TYPE})
        else:
            return jsonify({"status": "error", "database": "not connected", "db_type": DB_TYPE}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ── Print all registered routes ──────────────────────────────────────
print("[BOOT] Registered routes:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.methods} {rule.rule}")

print("[BOOT] App ready!")

# ── Local dev server ─────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"[BOOT] Starting dev server on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)