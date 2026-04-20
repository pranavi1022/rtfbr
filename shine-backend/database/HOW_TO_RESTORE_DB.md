# SHINE Database Restoration — Quick Guide

## Option A: Render Shell (Easiest)

1. Go to https://dashboard.render.com
2. Click your **shine-backend** service
3. Click the **"Shell"** tab (top right area)
4. Type and run:
   ```
   python database/run_restore.py
   ```
5. Wait ~30 seconds — you'll see row counts at the end.

---

## Option B: Run locally pointing to Render DB

1. Copy your DATABASE_URL from Render:
   - Render Dashboard → shine-db (PostgreSQL) → **Connect** tab → copy the **Internal** or **External** connection string

2. Open PowerShell in `d:\rtfbr final\shine-backend` and run:
   ```powershell
   $env:DATABASE_URL="postgresql://YOUR_ACTUAL_URL_HERE"
   python database/run_restore.py
   ```

---

## What the script does

- Creates tables: `users`, `projects`, `keywords`, `skills`,
  `skill_dependencies`, `learning_resources`, `user_activity`
- Inserts **100+ projects** across categories:
  Gaming, Web, Education, AI/ML, Mobile, Cloud, IoT,
  Cyber Security, Data Science, Blockchain, FinTech, Medical, Fitness
- Inserts **110+ keywords** with correct category mapping
- Inserts **27 skills** across 4 project types (website/app/other/gaming)
- Inserts **14 skill dependencies**
- Inserts **42 learning resources** with real URLs

---

## Render Environment Variables (must be set in Render dashboard)

| Variable         | Value                                      |
|------------------|--------------------------------------------|
| DATABASE_URL     | (auto-set by Render when you attach DB)    |
| FLASK_SECRET_KEY | shine_secret_key_2024                      |
| EMAIL_USER       | pranavigaridepally02@gmail.com             |
| EMAIL_PASS       | eckn vfql epdj evxd  ← Gmail App Password |
| SMTP_HOST        | smtp.gmail.com                             |
| SMTP_PORT        | 587                                        |

> **IMPORTANT:** EMAIL_PASS must be a **Gmail App Password** (16 chars with spaces).
> Generate at: https://myaccount.google.com/apppasswords

---

## Verification

After running, the script prints:

```
projects            → 80+ rows
keywords            → 110+ rows
skills              → 27 rows
skill_dependencies  → 14 rows
learning_resources  → 42 rows
```
