"""
migrate_learning_resources.py
Creates the learning_resources table and inserts sample data.
Run: python migrate_learning_resources.py
"""

import mysql.connector
import sys

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "shine_db",
    "connect_timeout": 5,
}

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
    except Exception as e:
        print(f"[FAIL] Cannot connect to MySQL: {e}")
        sys.exit(1)

    # ── Step 1: Create table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_resources (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            skill_name      VARCHAR(100)  NOT NULL,
            category        VARCHAR(100)  NOT NULL DEFAULT 'General',
            resource_title  VARCHAR(255)  NOT NULL,
            resource_link   VARCHAR(500)  NOT NULL,
            difficulty      ENUM('Beginner','Intermediate','Advanced') DEFAULT 'Beginner',
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_skill_name (skill_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    print("[OK] Table learning_resources created (or already exists)")

    # ── Step 2: Check existing data ──
    cursor.execute("SELECT COUNT(*) FROM learning_resources")
    existing = cursor.fetchone()[0]
    if existing > 0:
        print(f"[SKIP] Table already has {existing} rows — skipping inserts")
    else:
        inserts = [
            # Python
            ("Python","Backend","Python Official Tutorial","https://docs.python.org/3/tutorial/","Beginner"),
            ("Python","Backend","Real Python - Intermediate Guide","https://realpython.com/tutorials/intermediate/","Intermediate"),
            ("Python","Backend","Python Design Patterns","https://refactoring.guru/design-patterns/python","Advanced"),
            # MySQL
            ("MySQL","Database","MySQL Official Tutorial","https://dev.mysql.com/doc/refman/8.0/en/tutorial.html","Beginner"),
            ("MySQL","Database","MySQL Performance Tuning","https://dev.mysql.com/doc/refman/8.0/en/optimization.html","Intermediate"),
            ("MySQL","Database","MySQL Indexing Best Practices","https://planetscale.com/courses/mysql-for-developers/indexes","Advanced"),
            # React
            ("React","Frontend","React Official Tutorial","https://react.dev/learn","Beginner"),
            ("React","Frontend","React Hooks Deep Dive","https://react.dev/reference/react/hooks","Intermediate"),
            ("React","Frontend","Advanced React Patterns","https://www.patterns.dev/react/","Advanced"),
            # Git
            ("Git","Tools","Git - Getting Started","https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control","Beginner"),
            ("Git","Tools","Advanced Git Branching","https://learngitbranching.js.org/","Intermediate"),
            # Flask
            ("Flask","Backend","Flask Official Tutorial","https://flask.palletsprojects.com/en/3.0.x/tutorial/","Beginner"),
            ("Flask","Backend","Flask REST API Development","https://flask-restful.readthedocs.io/en/latest/","Intermediate"),
            # JavaScript
            ("JavaScript","Frontend","MDN JavaScript Guide","https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide","Beginner"),
            ("JavaScript","Frontend","JavaScript.info - Modern Tutorial","https://javascript.info/","Intermediate"),
            ("JavaScript","Frontend","You Don't Know JS (Book Series)","https://github.com/getify/You-Dont-Know-JS","Advanced"),
            # HTML
            ("HTML","Frontend","MDN HTML Foundations","https://developer.mozilla.org/en-US/docs/Learn/HTML","Beginner"),
            ("HTML","Frontend","HTML Semantic Elements Guide","https://web.dev/learn/html/","Intermediate"),
            # CSS
            ("CSS","Frontend","CSS Fundamentals (web.dev)","https://web.dev/learn/css","Beginner"),
            ("CSS","Frontend","CSS Grid and Flexbox Mastery","https://css-tricks.com/snippets/css/complete-guide-grid/","Intermediate"),
            # Java
            ("Java","Android","Java Official Tutorial","https://dev.java/learn/","Beginner"),
            ("Java","Android","Effective Java Practices","https://www.baeldung.com/java-tutorial","Intermediate"),
            # Machine Learning
            ("Machine Learning","AI/ML","Scikit-learn Tutorial","https://scikit-learn.org/stable/tutorial/","Beginner"),
            ("Machine Learning","AI/ML","Stanford CS229 - ML Course","https://cs229.stanford.edu/","Advanced"),
            # REST API
            ("REST API","Integration","REST API Tutorial","https://restfulapi.net/","Beginner"),
            ("REST API","Integration","API Design Best Practices","https://swagger.io/resources/articles/best-practices-in-api-design/","Intermediate"),
            # Docker
            ("Docker","DevOps","Docker Getting Started","https://docs.docker.com/get-started/","Beginner"),
            ("Docker","DevOps","Docker Compose Guide","https://docs.docker.com/compose/","Intermediate"),
            # Node.js
            ("Node.js","Backend","Node.js Official Learn","https://nodejs.org/en/learn","Beginner"),
            ("Node.js","Backend","Node.js Best Practices","https://github.com/goldbergyoni/nodebestpractices","Advanced"),
            # Firebase
            ("Firebase","Backend","Firebase Documentation","https://firebase.google.com/docs","Beginner"),
            # Kotlin
            ("Kotlin","Android","Kotlin Official Docs","https://kotlinlang.org/docs/getting-started.html","Beginner"),
            # Pandas
            ("Pandas","Data","Pandas Getting Started","https://pandas.pydata.org/docs/getting_started/intro_tutorials/","Beginner"),
            # MongoDB
            ("MongoDB","Database","MongoDB Official Tutorial","https://www.mongodb.com/docs/manual/tutorial/","Beginner"),
        ]
        cursor.executemany(
            "INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES (%s,%s,%s,%s,%s)",
            inserts,
        )
        conn.commit()
        print(f"[OK] Inserted {len(inserts)} rows")

    # ── Verify ──
    cursor.execute("SELECT COUNT(*) FROM learning_resources")
    total = cursor.fetchone()[0]
    print(f"\n[OK] Total rows: {total}")

    cursor.execute(
        "SELECT skill_name, resource_title, difficulty FROM learning_resources ORDER BY skill_name LIMIT 10"
    )
    print(f"\n{'Skill':<22} {'Title':<45} {'Difficulty'}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"  {row[0]:<20} {row[1]:<43} {row[2]}")

    cursor.close()
    conn.close()
    print("\n[DONE] Migration complete!")


if __name__ == "__main__":
    main()
