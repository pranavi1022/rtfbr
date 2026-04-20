"""
logic/keyword_matcher.py

Three-layer keyword matching:
  Layer 1 → Domain-based category map   — highest priority (explicit domain selection)
  Layer 2 → DB keywords table           — LIKE partial match + synonym expansion
  Layer 3 → JSON dataset                — strong keyword hit
  Layer 4 → Generic fallback            — always returns something

Synonym mapping ensures:
  game → gaming → unity → unreal → pygame → all map to game_project
  ai   → ml     → deep learning        → all map to ai_project
  etc.

get_db_connection() is imported by:
  - logic/project_engine.py
  - logic/skill_engine.py
  - routes/auth_routes.py
  - routes/project_routes.py
  - routes/history_routes.py
"""

import json
import os
from config import DB_CONFIG, DB_TYPE, DATABASE_URL

# ── Database driver imports ────────────────────────────────────────────────
if DB_TYPE == "postgresql":
    import psycopg2
    from psycopg2.extras import RealDictCursor
else:
    import mysql.connector


# ── PostgreSQL connection wrapper ─────────────────────────────────────────
# Bridges psycopg2's API to match mysql.connector's cursor(dictionary=True)
# so that ALL existing caller code works without modification.

class _PgConnWrapper:
    """Thin wrapper around a psycopg2 connection."""

    def __init__(self, conn):
        self._conn = conn

    def cursor(self, dictionary=False):
        if dictionary:
            return self._conn.cursor(cursor_factory=RealDictCursor)
        return self._conn.cursor()

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


# ── SAFE connection helper ────────────────────────────────────────────────

def get_db_connection():
    """
    Return a live database connection, or None if connection fails.
    Uses connect_timeout=5 to fail fast.
    Automatically selects PostgreSQL (Render) or MySQL (local).

    All callers MUST check:
        conn = get_db_connection()
        if conn is None:
            <skip to next fallback layer>
    """
    try:
        if DB_TYPE == "postgresql":
            # Use DATABASE_URL directly for psycopg2 (most reliable on Render)
            if DATABASE_URL:
                conn = psycopg2.connect(DATABASE_URL, connect_timeout=5,
                                        sslmode="require")
            else:
                conn = psycopg2.connect(**DB_CONFIG)
            print("[DB] [OK] PostgreSQL connection established")
            return _PgConnWrapper(conn)
        else:
            conn = mysql.connector.connect(
                **DB_CONFIG,
                connection_timeout=5
            )
            print("[DB] [OK] MySQL connection established")
            return conn
    except Exception as e:
        print(f"[DB] [FAIL] Connection failed ({DB_TYPE}): {e}")
        return None


# ── Synonym map ────────────────────────────────────────────────────────────
# Normalises user input before keyword matching so alternative words map
# to the correct category.

_SYNONYMS = {
    # Gaming synonyms
    "game":     "gaming",
    "games":    "gaming",
    "unity":    "gaming",
    "unreal":   "gaming",
    "pygame":   "gaming",
    "2d game":  "gaming",
    "3d game":  "gaming",
    "arcade":   "gaming",
    "rpg":      "gaming",
    "shooter":  "gaming",
    # AI synonyms
    "ai":           "artificial intelligence",
    "ml":           "machine learning",
    "dl":           "deep learning",
    "nlp":          "natural language processing",
    "cv":           "computer vision",
    "neural":       "neural network",
    # Web
    "web":          "web development",
    "website":      "web development",
    "frontend":     "web development",
    "backend":      "web development",
    # Mobile
    "android":      "mobile",
    "ios":          "mobile",
    "flutter":      "mobile",
    # Cloud
    "devops":       "cloud computing",
    "docker":       "cloud computing",
    "kubernetes":   "cloud computing",
    "aws":          "cloud computing",
    # Security
    "security":     "cyber security",
    "hacking":      "cyber security",
    "encryption":   "cyber security",
    # Data
    "data":         "data science",
    "analytics":    "data science",
    "pandas":       "data science",
}


# ── Domain → Category priority mapping ────────────────────────────────────
DOMAIN_CATEGORY_MAP = {
    "education":                "attendance_system",
    "medical":                  "hospital_system",
    "web development":          "portfolio",
    "artificial intelligence":  "ai_project",
    "data science":             "data_science_project",
    "cyber security":           "cyber_security_project",
    "iot":                      "iot_project",
    "cloud computing":          "cloud_project",
    "mobile app development":   "mobile_app",
    "mobile":                   "mobile_app",
    "blockchain":               "blockchain_project",
    "fintech":                  "fintech_project",
    "finance":                  "fintech_project",
    "game development":         "game_project",
    "gaming":                   "game_project",
    "ai":                       "ai_project",
    "ml":                       "ai_project",
    "cloud":                    "cloud_project",
    "security":                 "cyber_security_project",
}


def match_keyword(interest_text: str, domain: str = None) -> dict:
    """
    Accepts free-form user interest text and optional domain.

    Priority order:
      1. Domain-based mapping   — user picked a specific domain (highest priority)
      2. DB keyword match       — interest text matches a DB keyword (LIKE partial)
      3. JSON keyword match     — interest text matches a JSON keyword
      4. Generic fallback       — domain map or default to 'portfolio'

    Returns:
        {
            "category": str,
            "domain":   str,
            "source":   "domain" | "db" | "json" | "generic"
        }
    """
    interest_lower = interest_text.lower().strip()

    # Apply synonym expansion to interest text
    expanded = _SYNONYMS.get(interest_lower, interest_lower)
    for syn, replacement in _SYNONYMS.items():
        if syn in interest_lower:
            expanded = interest_lower.replace(syn, replacement)
            break

    print(f"[keyword_matcher] interest='{interest_lower}' expanded='{expanded}' domain='{domain}'")

    # Split into meaningful words (length > 2) for word-level matching
    words = [w for w in expanded.split() if len(w) > 2]

    # ── LAYER 1 : Domain-based category (HIGHEST PRIORITY) ─────────────
    if domain:
        domain_lower = domain.strip().lower()
        if domain_lower in DOMAIN_CATEGORY_MAP:
            fallback_category = DOMAIN_CATEGORY_MAP[domain_lower]
            print(f"[keyword_matcher] [DOMAIN HIT] domain={domain!r} → category={fallback_category!r}")
            return {
                "category": fallback_category,
                "domain":   domain,
                "source":   "domain"
            }

    # ── LAYER 2 : DB keywords table ────────────────────────────────────
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)

            # Try phrases: full expanded text first, then each word
            phrases_to_try = [expanded, interest_lower] + words

            for phrase in phrases_to_try:
                if not phrase or len(phrase) < 2:
                    continue
                print(f"[keyword_matcher] DB query: LIKE '%{phrase}%'")
                cursor.execute(
                    "SELECT category, domain FROM keywords WHERE LOWER(keyword) LIKE %s LIMIT 1",
                    (f"%{phrase}%",)
                )
                row = cursor.fetchone()
                if row:
                    row = dict(row)
                    cursor.close()
                    conn.close()
                    print(f"[keyword_matcher] [DB HIT] category={row['category']!r}")
                    return {
                        "category": row["category"],
                        "domain":   row["domain"],
                        "source":   "db"
                    }

            cursor.close()
            conn.close()
            print(f"[keyword_matcher] [INFO] DB: no keyword match — trying JSON")
        except Exception as e:
            print(f"[keyword_matcher] DB query error: {e}")
    else:
        print(f"[keyword_matcher] [WARN] DB unavailable — skipping to JSON layer")

    # ── LAYER 3 : JSON dataset — strong match only ──────────────────────
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'projects_dataset.json')
        with open(json_path, 'r') as f:
            dataset = json.load(f)

        for entry in dataset:
            for keyword in entry["keywords"]:
                keyword_lower = keyword.lower()
                direct_hit = keyword_lower in expanded or keyword_lower in interest_lower
                word_hit   = any(w in keyword_lower for w in words if len(w) > 3)
                if direct_hit or word_hit:
                    print(f"[keyword_matcher] [JSON HIT] category={entry['category']!r}")
                    return {
                        "category": entry["category"],
                        "domain":   entry.get("domain", domain or "Web Development"),
                        "source":   "json"
                    }
    except Exception as e:
        print(f"[keyword_matcher] JSON error: {e}")

    # ── LAYER 4 : Generic fallback ──────────────────────────────────────
    fallback_category = DOMAIN_CATEGORY_MAP.get(
        (domain or "").strip().lower(), "portfolio"
    )
    fallback_domain = domain or "Web Development"
    print(f"[keyword_matcher] [GENERIC] category={fallback_category!r}")
    return {
        "category": fallback_category,
        "domain":   fallback_domain,
        "source":   "generic"
    }
