"""
config.py — SHINE backend configuration

Reads all credentials and settings from environment variables (via .env file).
Falls back to hardcoded defaults so the app still works without a .env file.

Database strategy:
  - If DATABASE_URL is set (Render / production) → PostgreSQL via psycopg2
  - Otherwise → MySQL via mysql-connector-python (local development)

connect_timeout=5 tells the DB driver to fail fast (5 seconds)
instead of blocking the entire Flask thread indefinitely when the
database is slow or unreachable.
"""

import os
from urllib.parse import urlparse

# Load .env file if python-dotenv is installed (graceful skip if not)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Database ──────────────────────────────────────────────────────────
# If DATABASE_URL is set → PostgreSQL (Render production)
# Otherwise            → MySQL      (local development)

DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL:
    DB_TYPE = "postgresql"
    _parsed = urlparse(DATABASE_URL)
    DB_CONFIG = {
        "host":            _parsed.hostname,
        "port":            _parsed.port or 5432,
        "user":            _parsed.username,
        "password":        _parsed.password,
        "dbname":          _parsed.path.lstrip("/"),
        "sslmode":         "require",
        "connect_timeout": 5,
    }
else:
    DB_TYPE = "mysql"
    DB_CONFIG = {
        "host":            os.getenv("DB_HOST", "localhost"),
        "user":            os.getenv("DB_USER", "root"),
        "password":        os.getenv("DB_PASS", "root123"),
        "database":        os.getenv("DB_NAME", "shine_db"),
        "connect_timeout": 5,
    }

# ── Flask ─────────────────────────────────────────────────────────────
FLASK_PORT    = int(os.getenv("PORT", "5000"))
FLASK_SECRET  = os.getenv("FLASK_SECRET_KEY", "shine_secret_key_2024")

# ── Email OTP (Gmail SMTP) ───────────────────────────────────────────
# To use real email: set EMAIL_USER and EMAIL_PASS in .env
# Generate an App Password at: https://myaccount.google.com/apppasswords
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASS = os.getenv("EMAIL_PASS", "")
SMTP_HOST  = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT  = int(os.getenv("SMTP_PORT", "587"))
