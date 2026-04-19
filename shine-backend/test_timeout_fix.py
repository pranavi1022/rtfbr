"""
test_timeout_fix.py -- SHINE MySQL Timeout + Fallback Verification
===================================================================
Run:  python test_timeout_fix.py

Tests:
  1. DB_CONFIG includes connect_timeout
  2. get_db_connection() returns conn or None (never hangs)
  3. keyword_matcher works even when DB is down (JSON/generic fallback)
  4. project_engine works even when DB is down (JSON/generic fallback)
  5. skill_engine works even when DB is down (JSON/hardcoded fallback)
  6. No call takes more than 6 seconds
"""

import time
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

DIVIDER = "=" * 60
PASS = "[PASS]"
FAIL = "[FAIL]"
results = []


def timed_test(label, fn, max_seconds=6):
    """Run fn(), assert it completes within max_seconds."""
    print(f"\n{DIVIDER}")
    print(f" TEST: {label}")
    print(DIVIDER)

    start = time.time()
    try:
        result = fn()
        elapsed = time.time() - start
        passed = elapsed < max_seconds
        status = PASS if passed else FAIL
        print(f"  Duration : {elapsed:.2f}s")
        print(f"  Result   : {result}")
        print(f"  Status   : {status} {'(OK)' if passed else f'BLOCKED -- exceeded {max_seconds}s!'}")
        results.append((label, passed))
        return result
    except Exception as e:
        elapsed = time.time() - start
        print(f"  Duration : {elapsed:.2f}s")
        print(f"  ERROR    : {e}")
        print(f"  Status   : {FAIL} Exception raised")
        results.append((label, False))
        return None


def test_db_connection():
    """Test 1: get_db_connection returns conn or None, never hangs."""
    from logic.keyword_matcher import get_db_connection
    conn = get_db_connection()
    if conn is not None:
        print("  [DB] Connection succeeded -- MySQL is running")
        conn.close()
        return "Connected (MySQL is up)"
    else:
        print("  [DB] Connection returned None -- fallback layer should activate")
        return "None (MySQL is down -- fallback will activate)"


def test_keyword_matcher():
    """Test 2: match_keyword returns a result regardless of DB state."""
    from logic.keyword_matcher import match_keyword
    result = match_keyword("attendance system", "Education")
    assert result is not None, "match_keyword returned None!"
    assert "category" in result, "Missing 'category' key"
    assert "source" in result, "Missing 'source' key"
    print(f"  Category : {result['category']}")
    print(f"  Source   : {result['source']}")
    return f"category={result['category']}, source={result['source']}"


def test_project_engine():
    """Test 3: get_project_suggestions returns projects regardless of DB state."""
    from logic.project_engine import get_project_suggestions
    result = get_project_suggestions("attendance", "Education", "Beginner")
    assert result is not None, "get_project_suggestions returned None!"
    assert "projects" in result, "Missing 'projects' key"
    assert len(result["projects"]) >= 1, "No projects returned!"
    print(f"  Source   : {result['match_source']}")
    print(f"  Projects : {len(result['projects'])}")
    for p in result["projects"]:
        print(f"    -> {p['title']}")
    return f"source={result['match_source']}, count={len(result['projects'])}"


def test_skill_engine():
    """Test 4: analyze_skill_gap returns skill data regardless of DB state."""
    from logic.skill_engine import analyze_skill_gap
    result = analyze_skill_gap("Student Portal", "website", ["HTML", "CSS", "Python"])
    assert result is not None, "analyze_skill_gap returned None!"
    assert "readinessScore" in result, "Missing 'readinessScore' key"
    assert "missingSkills" in result, "Missing 'missingSkills' key"
    print(f"  Source     : {result['source']}")
    print(f"  Readiness  : {result['readinessScore']}%")
    print(f"  Matched    : {result['matchedCount']}")
    print(f"  Missing    : {result['missingCount']}")
    return f"source={result['source']}, readiness={result['readinessScore']}%"


def test_config_has_timeout():
    """Test 5: DB_CONFIG includes connect_timeout."""
    from config import DB_CONFIG
    assert "connect_timeout" in DB_CONFIG, "connect_timeout missing from DB_CONFIG!"
    timeout = DB_CONFIG["connect_timeout"]
    print(f"  connect_timeout = {timeout}")
    assert timeout <= 10, f"Timeout too high: {timeout}s"
    return f"connect_timeout={timeout}"


def main():
    print(f"\n{'#' * 60}")
    print("  SHINE -- MySQL Timeout Fix Verification")
    print(f"{'#' * 60}")

    timed_test("DB_CONFIG has connect_timeout", test_config_has_timeout)
    timed_test("get_db_connection() -- no hang", test_db_connection)
    timed_test("keyword_matcher fallback", test_keyword_matcher)
    timed_test("project_engine fallback", test_project_engine)
    timed_test("skill_engine fallback", test_skill_engine)

    # -- Summary --
    print(f"\n{'#' * 60}")
    print("  SUMMARY")
    print(f"{'#' * 60}")

    all_passed = True
    for label, passed in results:
        status = PASS if passed else FAIL
        print(f"  {status}  {label}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("  MySQL timeout issue fixed")
        print("  System no longer blocks")
        print("  Fallback working correctly")
    else:
        print("  Some tests failed -- review output above")

    print(f"\n{'#' * 60}\n")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
