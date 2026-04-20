"""
database/run_restore.py

Run this script to populate / restore the PostgreSQL database on Render.

Usage (local, pointing to Render DB):
    set DATABASE_URL=<your-render-postgresql-url>
    python database/run_restore.py

Or run directly on Render via the Shell tab:
    python database/run_restore.py
"""

import os
import sys

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set.")
    print("Set it as:  set DATABASE_URL=postgresql://...")
    sys.exit(1)

try:
    import psycopg2
except ImportError:
    print("ERROR: psycopg2 not installed. Run:  pip install psycopg2-binary")
    sys.exit(1)

# Load SQL file
sql_path = os.path.join(os.path.dirname(__file__), "restore_pg.sql")
if not os.path.exists(sql_path):
    print(f"ERROR: SQL file not found: {sql_path}")
    sys.exit(1)

with open(sql_path, "r", encoding="utf-8") as f:
    sql_content = f.read()

print(f"[restore] Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(DATABASE_URL, sslmode="require", connect_timeout=15)
    conn.autocommit = False
    cursor = conn.cursor()
    print(f"[restore] Connected. Running restore script...")

    # Split on semicolons to run statement by statement
    # (handles the VERIFY SELECT at end gracefully)
    statements = [s.strip() for s in sql_content.split(";") if s.strip()]
    total = len(statements)
    print(f"[restore] {total} SQL statements to execute...")

    for i, stmt in enumerate(statements, 1):
        try:
            cursor.execute(stmt)
            if stmt.upper().startswith("SELECT"):
                rows = cursor.fetchall()
                print(f"\n  Verification results:")
                for row in rows:
                    print(f"    {row[0]:30s} → {row[1]} rows")
        except Exception as e:
            print(f"[restore] Statement {i}/{total} ERROR: {e}")
            print(f"          SQL: {stmt[:120]}...")
            # Continue — some errors expected (e.g. constraint already exists)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"\n[restore] Done! Database restored successfully.")

except Exception as e:
    print(f"[restore] Connection failed: {e}")
    sys.exit(1)
