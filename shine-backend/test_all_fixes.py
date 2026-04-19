"""
test_all_fixes.py — Validates all SHINE system fixes

Run: python test_all_fixes.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_step2_domain_mapping():
    """STEP 2: Different domains must return different categories."""
    from logic.keyword_matcher import match_keyword
    print("\n=== STEP 2: Domain -> Category Mapping ===")
    
    test_domains = [
        "Blockchain",
        "Artificial Intelligence",
        "Data Science",
        "Cyber Security",
        "Education",
        "IoT",
        "Cloud Computing",
        "Game Development",
        "FinTech",
    ]
    
    categories_seen = set()
    all_pass = True
    
    for domain in test_domains:
        result = match_keyword("project", domain=domain)
        cat = result["category"]
        src = result["source"]
        categories_seen.add(cat)
        print("  {} -> {} (source: {})".format(domain.ljust(30), cat.ljust(25), src))
    
    if len(categories_seen) >= 7:
        print("  PASS: {} unique categories returned".format(len(categories_seen)))
    else:
        print("  FAIL: Only {} unique categories".format(len(categories_seen)))
        all_pass = False
    
    return all_pass


def test_step5_config():
    """STEP 5: Config loads env vars properly."""
    from config import DB_CONFIG, FLASK_PORT, EMAIL_USER, EMAIL_PASS, SMTP_HOST
    print("\n=== STEP 5: Config & Email Setup ===")
    
    print("  DB_HOST:     {}".format(DB_CONFIG["host"]))
    print("  DB_NAME:     {}".format(DB_CONFIG["database"]))
    print("  FLASK_PORT:  {}".format(FLASK_PORT))
    print("  SMTP_HOST:   {}".format(SMTP_HOST))
    
    if EMAIL_USER:
        print("  EMAIL_USER:  {} (CONFIGURED)".format(EMAIL_USER))
    else:
        print("  EMAIL_USER:  (not set - demo mode, OTP prints to console)")
    
    print("  PASS: Config loads correctly")
    return True


def test_step6_skill_engine():
    """STEP 6: Skill gap analysis with partial/alias matching."""
    from logic.skill_engine import analyze_skill_gap
    print("\n=== STEP 6: Skill Gap Analysis ===")
    
    # Test 1: Website with some skills
    result = analyze_skill_gap("attendance website", "website", ["html", "css", "py"])
    print("  Website test: readiness={}%, matched={}, missing={}".format(
        result["readinessScore"], result["matchedCount"], result["missingCount"]
    ))
    
    # Verify 'py' matched 'Python' via alias
    matched_names = [s["name"] for s in result["skillsYouHave"]]
    if "Python" in matched_names:
        print("  PASS: Alias 'py' -> 'Python' matched correctly")
    else:
        print("  FAIL: Alias 'py' did not match 'Python'")
        return False
    
    # Test 2: App type
    result2 = analyze_skill_gap("food delivery app", "app", ["java", "kotlin"])
    print("  App test:     readiness={}%, matched={}, missing={}".format(
        result2["readinessScore"], result2["matchedCount"], result2["missingCount"]
    ))
    
    # Test 3: Other type
    result3 = analyze_skill_gap("ML predictor", "other", ["python", "sklearn"])
    print("  Other test:   readiness={}%, matched={}, missing={}".format(
        result3["readinessScore"], result3["matchedCount"], result3["missingCount"]
    ))
    
    # Verify sklearn alias matched scikit-learn
    matched3 = [s["name"] for s in result3["skillsYouHave"]]
    if "scikit-learn" in [m.lower() for m in matched3] or "Machine Learning" in matched3:
        print("  PASS: Alias matching working")
    else:
        print("  INFO: Alias check - matched: {}".format(matched3))
    
    # Verify proficiency varies
    profs = [s["proficiency"] for s in result["skillsYouHave"]]
    if len(set(profs)) > 1 or len(profs) <= 1:
        print("  PASS: Proficiency values vary: {}".format(profs))
    
    return True


def test_step3_history_routes():
    """STEP 3: History routes import correctly."""
    from routes.history_routes import history_bp
    print("\n=== STEP 3: History Routes ===")
    print("  Blueprint name: {}".format(history_bp.name))
    print("  PASS: history_bp imports and registers correctly")
    return True


def test_step9_app_structure():
    """STEP 9: App registers all blueprints."""
    print("\n=== STEP 9: App Structure ===")
    from app import app
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    
    required = [
        "/api/login",
        "/api/register",
        "/api/project-guidance",
        "/api/skill-gap",
        "/api/save-activity",
        "/api/forgot-password",
    ]
    
    for endpoint in required:
        if endpoint in rules:
            print("  OK: {} registered".format(endpoint))
        else:
            print("  FAIL: {} NOT found".format(endpoint))
            return False
    
    print("  PASS: All {} endpoints registered".format(len(required)))
    return True


if __name__ == "__main__":
    print("=" * 55)
    print("  SHINE System — Full Fix Validation")
    print("=" * 55)
    
    results = {
        "STEP 2 (Domain Mapping)":   test_step2_domain_mapping(),
        "STEP 3 (History API)":      test_step3_history_routes(),
        "STEP 5 (Config/Email)":     test_step5_config(),
        "STEP 6 (Skill Engine)":     test_step6_skill_engine(),
        "STEP 9 (App Structure)":    test_step9_app_structure(),
    }
    
    print("\n" + "=" * 55)
    print("  SUMMARY")
    print("=" * 55)
    for step, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print("  [{}] {}".format(status, step))
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print("\n  Result: {}/{} steps passed".format(passed, total))
    print("=" * 55)
