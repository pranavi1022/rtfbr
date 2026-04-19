-- ============================================================
-- fix_duplicates.sql
-- Run ONLY on shine_db
-- PURPOSE: Remove duplicate project titles, keep ONE correct
--          difficulty per project, then add UNIQUE constraint.
-- ============================================================

USE shine_db;

-- ── STEP 0: Show duplicates before fixing ─────────────────
SELECT title, COUNT(*) AS cnt
FROM projects
GROUP BY title
HAVING COUNT(*) > 1
ORDER BY cnt DESC;

-- ── STEP 1: Delete duplicate rows, keep the one with the
--            LOWEST id (first inserted = canonical row) ────
DELETE p1
FROM projects p1
INNER JOIN projects p2
  ON  p2.title     = p1.title
  AND p2.id        < p1.id;

-- ── STEP 2: Spot-fix known wrong difficulties ──────────────
--   (Add more UPDATE statements here if needed)
UPDATE projects
SET difficulty = 'Intermediate'
WHERE title = 'Attendance Management System';

-- ── STEP 3: Add UNIQUE constraint on title ─────────────────
--   (Wrapped in IF NOT EXISTS logic via stored proc trick)
SET @constraint_exists = (
  SELECT COUNT(*)
  FROM information_schema.TABLE_CONSTRAINTS
  WHERE CONSTRAINT_SCHEMA = 'shine_db'
    AND TABLE_NAME         = 'projects'
    AND CONSTRAINT_NAME    = 'unique_project_title'
);

SET @sql = IF(
  @constraint_exists = 0,
  'ALTER TABLE projects ADD CONSTRAINT unique_project_title UNIQUE (title)',
  'SELECT ''unique_project_title already exists, skipped'' AS info'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ── STEP 4: Verify ─────────────────────────────────────────
SELECT title, difficulty, category
FROM projects
ORDER BY category, difficulty, title;
