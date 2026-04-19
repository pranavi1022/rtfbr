"""
logic/keyword_matcher.py

Three-layer keyword matching:
  Layer 1 → MySQL keywords table  — exact / partial match (primary)
  Layer 2 → JSON dataset          — only on STRONG keyword hit
  Layer 3 → Generic domain-based  — always returns something meaningful

get_db_connection() is also imported by:
  - logic/project_engine.py
  - logic/skill_engine.py
  - routes/auth_routes.py
  - routes/project_routes.py

CRITICAL FIX: get_db_connection() now returns None on failure instead of
raising, so all callers can check `if conn is None` and skip safely to the
next fallback layer without blocking.
"""

import json
import os
import mysql.connector
from config import DB_CONFIG


# ── SAFE connection helper ────────────────────────────────────────────────

def get_db_connection():
    """
    Return a live MySQL connection, or None if the connection fails.

    Uses connect_timeout=5 from DB_CONFIG to fail fast rather than
    blocking the Flask thread for minutes.

    All callers MUST check:
        conn = get_db_connection()
        if conn is None:
            <skip to next fallback layer>
    """
    try:
        conn = mysql.connector.connect(
            **DB_CONFIG,
            connection_timeout=5   # belt-and-suspenders: enforce 5s timeout
        )
        print("[DB] [OK] Connection established")
        return conn
    except mysql.connector.Error as e:
        print(f"[DB] [FAIL] Connection failed (mysql): {e}")
        return None
    except Exception as e:
        print(f"[DB] [FAIL] Connection failed (unexpected): {e}")
        return None


# ── keyword matching ──────────────────────────────────────────────────────

# ── Domain → Category priority mapping ────────────────────────────────────
# When a user selects a specific domain, we should return projects from
# that domain's primary category FIRST, before falling back to keyword
# matching. This fixes the bug where all domains returned "attendance_system".

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

    Priority order (CRITICAL — this order fixes the 'all domains = same' bug):
      1. Domain-based mapping   — user picked a specific domain  (highest priority)
      2. MySQL keyword match    — interest text matches a DB keyword
      3. JSON keyword match     — interest text matches a JSON keyword
      4. Generic fallback       — domain map or default to 'portfolio'

    Returns:
        {
            "category": str,
            "domain":   str,
            "source":   "domain" | "mysql" | "json" | "generic"
        }
    """
    interest_lower = interest_text.lower().strip()
    # Split into meaningful words (length > 2) for word-level matching
    words = [w for w in interest_lower.split() if len(w) > 2]

    # ── LAYER 1 : Domain-based category (HIGHEST PRIORITY) ─────────────
    # When the user explicitly selects a domain, that domain determines
    # the project category. This is the primary fix for the bug where
    # every domain returned the same projects.
    if domain:
        domain_lower = domain.strip().lower()
        if domain_lower in DOMAIN_CATEGORY_MAP:
            fallback_category = DOMAIN_CATEGORY_MAP[domain_lower]
            print(f"[keyword_matcher] [OK] Domain map -> domain={domain!r} -> category={fallback_category!r}")
            return {
                "category": fallback_category,
                "domain":   domain,
                "source":   "domain"
            }

    # ── LAYER 2 : MySQL keywords table ─────────────────────────────────
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)

            # Try full phrase first, then each word individually
            phrases_to_try = [interest_lower] + words

            for phrase in phrases_to_try:
                print(f"[keyword_matcher] DB query: LIKE '%{phrase}%'")
                cursor.execute(
                    "SELECT category, domain FROM keywords WHERE LOWER(keyword) LIKE %s LIMIT 1",
                    (f"%{phrase}%",)
                )
                row = cursor.fetchone()
                if row:
                    cursor.close()
                    conn.close()
                    print(f"[keyword_matcher] [OK] MySQL hit -> category={row['category']!r}")
                    return {
                        "category": row["category"],
                        "domain":   row["domain"],
                        "source":   "mysql"
                    }

            cursor.close()
            conn.close()
            print(f"[keyword_matcher] [INFO] MySQL: no keyword match found -- trying JSON")
        except Exception as e:
            print(f"[keyword_matcher] MySQL query error: {e}")
    else:
        print(f"[keyword_matcher] [WARN] MySQL unavailable -- skipping to JSON layer")

    # ── LAYER 3 : JSON dataset — strong match only ──────────────────────
    # "Strong" = the keyword appears directly in the interest text OR
    # a meaningful word (len > 3) is a substring of the keyword.
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'projects_dataset.json')
        with open(json_path, 'r') as f:
            dataset = json.load(f)

        for entry in dataset:
            for keyword in entry["keywords"]:
                keyword_lower = keyword.lower()
                # Direct containment (interest text includes keyword)
                direct_hit = keyword_lower in interest_lower
                # Word-level hit: a meaningful user word is inside this keyword
                word_hit = any(w in keyword_lower for w in words if len(w) > 3)
                if direct_hit or word_hit:
                    print(f"[keyword_matcher] [OK] JSON hit -> category={entry['category']!r}")
                    return {
                        "category": entry["category"],
                        "domain":   entry.get("domain", domain or "Web Development"),
                        "source":   "json"
                    }
    except Exception as e:
        print(f"[keyword_matcher] JSON error: {e}")

    # ── LAYER 4 : Generic fallback ─────────────────────────────────────────
    # Uses the same DOMAIN_CATEGORY_MAP; defaults to "portfolio" if nothing matches.
    fallback_category = DOMAIN_CATEGORY_MAP.get(
        (domain or "").strip().lower(), "portfolio"
    )
    fallback_domain = domain or "Web Development"

    print(f"[keyword_matcher] [INFO] Generic fallback -> category={fallback_category!r}")
    return {
        "category": fallback_category,
        "domain":   fallback_domain,
        "source":   "generic"
    }


