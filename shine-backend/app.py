"""
app.py — SHINE Access Point Backend Entry Point
Run: python app.py
Backend will start at: http://localhost:PORT (default 5000)
"""

import os
from flask import Flask
from flask_cors import CORS

from config import FLASK_PORT, FLASK_SECRET
from routes.auth_routes    import auth_bp
from routes.project_routes import project_bp
from routes.skill_routes   import skill_bp
from routes.history_routes import history_bp

app = Flask(__name__)

# ── Session secret key (from env var or fallback) ────────────────────
app.secret_key = FLASK_SECRET

# ── CORS: allow the React dev server + deployed frontend ────────────
frontend_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:5174",
    "http://localhost:8080",
    "http://localhost:8081",
    "https://rtfbr-1.onrender.com",
]

# Also allow a custom frontend URL from env (e.g., FRONTEND_URL)
custom_frontend = os.environ.get("FRONTEND_URL")
if custom_frontend:
    frontend_origins.append(custom_frontend.rstrip("/"))

CORS(
    app,
    supports_credentials=True,
    origins=frontend_origins
)

# ── Register blueprints ─────────────────────────────────────────────
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(skill_bp)
app.register_blueprint(history_bp)


# ── Health-check endpoint ───────────────────────────────────────────
@app.route('/')
def index():
    return {
        "message": "SHINE Access Point Backend is running",
        "status":  "ok",
        "version": "2.0.0"
    }


if __name__ == '__main__':
    print("=" * 55)
    print("  SHINE Access Point — Flask Backend v2.0")
    print(f"  Running at: http://localhost:{FLASK_PORT}")
    print("  Make sure MySQL is running and schema.sql was executed.")
    print("=" * 55)
    if __name__ == '__main__':
    port = int(os.environ.get("PORT", FLASK_PORT))
    app.run(host="0.0.0.0", port=port)