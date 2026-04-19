-- ============================================================
-- SHINE: learning_resources table
-- Run: mysql -u root -p shine_db < learning_resources.sql
-- ============================================================

CREATE TABLE IF NOT EXISTS learning_resources (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    skill_name      VARCHAR(100)  NOT NULL,
    category        VARCHAR(100)  NOT NULL DEFAULT 'General',
    resource_title  VARCHAR(255)  NOT NULL,
    resource_link   VARCHAR(500)  NOT NULL,
    difficulty      ENUM('Beginner','Intermediate','Advanced') DEFAULT 'Beginner',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_skill_name (skill_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Sample data (30+ entries across 12 skills) ──────────────

-- Python (3 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Python', 'Backend', 'Python Official Tutorial', 'https://docs.python.org/3/tutorial/', 'Beginner'),
('Python', 'Backend', 'Real Python - Intermediate Guide', 'https://realpython.com/tutorials/intermediate/', 'Intermediate'),
('Python', 'Backend', 'Python Design Patterns', 'https://refactoring.guru/design-patterns/python', 'Advanced');

-- MySQL (3 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('MySQL', 'Database', 'MySQL Official Tutorial', 'https://dev.mysql.com/doc/refman/8.0/en/tutorial.html', 'Beginner'),
('MySQL', 'Database', 'MySQL Performance Tuning', 'https://dev.mysql.com/doc/refman/8.0/en/optimization.html', 'Intermediate'),
('MySQL', 'Database', 'MySQL Indexing Best Practices', 'https://planetscale.com/courses/mysql-for-developers/indexes', 'Advanced');

-- React (3 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('React', 'Frontend', 'React Official Tutorial', 'https://react.dev/learn', 'Beginner'),
('React', 'Frontend', 'React Hooks Deep Dive', 'https://react.dev/reference/react/hooks', 'Intermediate'),
('React', 'Frontend', 'Advanced React Patterns', 'https://www.patterns.dev/react/', 'Advanced');

-- Git (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Git', 'Tools', 'Git - Getting Started', 'https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control', 'Beginner'),
('Git', 'Tools', 'Advanced Git Branching', 'https://learngitbranching.js.org/', 'Intermediate');

-- Flask (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Flask', 'Backend', 'Flask Official Tutorial', 'https://flask.palletsprojects.com/en/3.0.x/tutorial/', 'Beginner'),
('Flask', 'Backend', 'Flask REST API Development', 'https://flask-restful.readthedocs.io/en/latest/', 'Intermediate');

-- JavaScript (3 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('JavaScript', 'Frontend', 'MDN JavaScript Guide', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide', 'Beginner'),
('JavaScript', 'Frontend', 'JavaScript.info - Modern Tutorial', 'https://javascript.info/', 'Intermediate'),
('JavaScript', 'Frontend', 'You Don''t Know JS (Book Series)', 'https://github.com/getify/You-Dont-Know-JS', 'Advanced');

-- HTML (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('HTML', 'Frontend', 'MDN HTML Foundations', 'https://developer.mozilla.org/en-US/docs/Learn/HTML', 'Beginner'),
('HTML', 'Frontend', 'HTML Semantic Elements Guide', 'https://web.dev/learn/html/', 'Intermediate');

-- CSS (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('CSS', 'Frontend', 'CSS Fundamentals (web.dev)', 'https://web.dev/learn/css', 'Beginner'),
('CSS', 'Frontend', 'CSS Grid & Flexbox Mastery', 'https://css-tricks.com/snippets/css/complete-guide-grid/', 'Intermediate');

-- Java (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Java', 'Android', 'Java Official Tutorial', 'https://dev.java/learn/', 'Beginner'),
('Java', 'Android', 'Effective Java Practices', 'https://www.baeldung.com/java-tutorial', 'Intermediate');

-- Machine Learning (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Machine Learning', 'AI/ML', 'Scikit-learn Tutorial', 'https://scikit-learn.org/stable/tutorial/', 'Beginner'),
('Machine Learning', 'AI/ML', 'Stanford CS229 - ML Course', 'https://cs229.stanford.edu/', 'Advanced');

-- REST API (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('REST API', 'Integration', 'REST API Tutorial', 'https://restfulapi.net/', 'Beginner'),
('REST API', 'Integration', 'API Design Best Practices', 'https://swagger.io/resources/articles/best-practices-in-api-design/', 'Intermediate');

-- Docker (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Docker', 'DevOps', 'Docker Getting Started', 'https://docs.docker.com/get-started/', 'Beginner'),
('Docker', 'DevOps', 'Docker Compose Guide', 'https://docs.docker.com/compose/', 'Intermediate');

-- Node.js (2 resources)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Node.js', 'Backend', 'Node.js Official Learn', 'https://nodejs.org/en/learn', 'Beginner'),
('Node.js', 'Backend', 'Node.js Best Practices', 'https://github.com/goldbergyoni/nodebestpractices', 'Advanced');

-- Firebase (1 resource)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Firebase', 'Backend', 'Firebase Documentation', 'https://firebase.google.com/docs', 'Beginner');

-- Kotlin (1 resource)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Kotlin', 'Android', 'Kotlin Official Docs', 'https://kotlinlang.org/docs/getting-started.html', 'Beginner');

-- Pandas (1 resource)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('Pandas', 'Data', 'Pandas Getting Started', 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/', 'Beginner');

-- MongoDB (1 resource)
INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty) VALUES
('MongoDB', 'Database', 'MongoDB Official Tutorial', 'https://www.mongodb.com/docs/manual/tutorial/', 'Beginner');

SELECT CONCAT('Inserted ', COUNT(*), ' learning resources') AS status FROM learning_resources;
