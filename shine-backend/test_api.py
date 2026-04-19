"""
test_api.py — SHINE Access Point API Tester
============================================
Run:
    pip install requests
    python test_api.py

Make sure the Flask server is running first:
    python app.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/project-guidance"

TEST_CASES = [
    {"interest": "attendance", "domain": "Education", "level": "Beginner"},
    {"interest": "attendance", "domain": "Education", "level": "Intermediate"},
    {"interest": "attendance", "domain": "Education", "level": "Advanced"},
]

DIVIDER = "=" * 60


def run_test(payload: dict, test_number: int) -> None:
    print(f"\n{DIVIDER}")
    print(f" TEST {test_number}")
    print(DIVIDER)
    print(f"  INPUT  : interest='{payload['interest']}' | domain='{payload['domain']}' | level='{payload['level']}'")

    try:
        response = requests.post(
            BASE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
    except requests.exceptions.ConnectionError:
        print("\n  ❌  ERROR: Cannot connect to Flask server.")
        print("      Make sure 'python app.py' is running on port 5000.")
        return
    except requests.exceptions.Timeout:
        print("\n  ❌  ERROR: Request timed out.")
        return

    if response.status_code != 200:
        print(f"\n  ❌  HTTP {response.status_code}: {response.text}")
        return

    data = response.json()

    level          = payload["level"]
    source         = data.get("match_source", "N/A")
    category       = data.get("matched_category", "N/A")
    projects       = data.get("projects", [])

    print(f"\n  LEVEL     : {level}")
    print(f"  SOURCE    : {source}")        # mysql | json | generic
    print(f"  CATEGORY  : {category}")
    print(f"  COUNT     : {len(projects)} project(s) returned")

    # ── Check for duplicates ──────────────────────────────────────────
    titles = [p["title"] for p in projects]
    duplicates = [t for t in titles if titles.count(t) > 1]

    print(f"\n  PROJECTS:")
    for i, proj in enumerate(projects, start=1):
        techs = ", ".join(proj.get("technologies", []))
        print(f"    {i}. {proj['title']}")
        print(f"       Technologies : {techs}")
        print(f"       Level echoed : {proj.get('level', 'N/A')}")

    if duplicates:
        print(f"\n  ⚠️  DUPLICATES DETECTED: {set(duplicates)}")
    else:
        print(f"\n  ✅  No duplicate projects found.")


def check_level_variation(results: list) -> None:
    """Check whether different difficulty levels returned different project sets."""
    print(f"\n{DIVIDER}")
    print(" LEVEL VARIATION CHECK")
    print(DIVIDER)

    title_sets = []
    for level, titles in results:
        title_sets.append((level, set(titles)))
        print(f"  {level:15s} → {titles}")

    # Compare each pair
    levels = [r[0] for r in title_sets]
    sets   = [r[1] for r in title_sets]

    all_different = True
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            overlap = sets[i].intersection(sets[j])
            if overlap:
                print(f"\n  ⚠️  OVERLAP between {levels[i]} and {levels[j]}: {overlap}")
                all_different = False

    if all_different:
        print("\n  ✅  All three levels returned DIFFERENT project sets.")
    else:
        print("\n  ℹ️  Some overlap detected — review DB data for that category.")


def main():
    print(f"\n{'#' * 60}")
    print("  SHINE Access Point — API Test Runner")
    print(f"  Target: {BASE_URL}")
    print(f"{'#' * 60}")

    level_results = []   # [(level, [titles]), ...]

    for i, payload in enumerate(TEST_CASES, start=1):
        run_test(payload, test_number=i)

        # Collect titles to cross-check later
        try:
            resp = requests.post(BASE_URL, json=payload, timeout=10)
            if resp.status_code == 200:
                titles = [p["title"] for p in resp.json().get("projects", [])]
                level_results.append((payload["level"], titles))
        except Exception:
            pass

    # Summary variation report
    if len(level_results) == len(TEST_CASES):
        check_level_variation(level_results)

    print(f"\n{DIVIDER}")
    print(" TEST COMPLETE")
    print(DIVIDER)
    print()


if __name__ == "__main__":
    main()
