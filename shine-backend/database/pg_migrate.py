"""
database/pg_migrate.py

MASTER PostgreSQL migration script for SHINE.
Creates all tables and populates all data.

Usage:
  # Set DATABASE_URL first, then run:
  python database/pg_migrate.py

  # Or pass it inline:
  DATABASE_URL="postgresql://..." python database/pg_migrate.py
"""

import os
import sys
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "")

if not DATABASE_URL:
    # Try loading from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        DATABASE_URL = os.environ.get("DATABASE_URL", "")
    except ImportError:
        pass

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL not set. Set it as an environment variable.")
    print("  Example: DATABASE_URL='postgresql://user:pass@host:5432/dbname' python database/pg_migrate.py")
    sys.exit(1)

print(f"[MIGRATE] Connecting to PostgreSQL...")


def run():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require", connect_timeout=10)
    conn.autocommit = False
    cur = conn.cursor()

    # ── STEP 0: Create tables ─────────────────────────────────────────
    print("[MIGRATE] Creating tables...")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        username VARCHAR(100) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS keywords (
        id SERIAL PRIMARY KEY,
        keyword VARCHAR(255) NOT NULL,
        category VARCHAR(100) NOT NULL,
        domain VARCHAR(100) NOT NULL,
        UNIQUE(keyword, category)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        domain VARCHAR(100) NOT NULL,
        difficulty VARCHAR(50) NOT NULL,
        category VARCHAR(100) NOT NULL,
        technologies TEXT NOT NULL,
        UNIQUE(title, difficulty)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id SERIAL PRIMARY KEY,
        skill_name VARCHAR(100) NOT NULL,
        project_type VARCHAR(50) NOT NULL,
        category VARCHAR(100) NOT NULL,
        weight INT DEFAULT 1,
        estimated_time VARCHAR(50) DEFAULT '1-2 weeks',
        UNIQUE(skill_name, project_type)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS skill_dependencies (
        id SERIAL PRIMARY KEY,
        skill_name VARCHAR(100) NOT NULL,
        depends_on VARCHAR(100) NOT NULL,
        UNIQUE(skill_name, depends_on)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS learning_resources (
        id SERIAL PRIMARY KEY,
        skill_name VARCHAR(100) NOT NULL,
        category VARCHAR(100) NOT NULL DEFAULT 'General',
        resource_title VARCHAR(255) NOT NULL,
        resource_link VARCHAR(500) NOT NULL,
        difficulty VARCHAR(20) DEFAULT 'Beginner',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_lr_skill_name ON learning_resources (skill_name);
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_activity (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        project_name VARCHAR(255) NOT NULL,
        level VARCHAR(50) DEFAULT '',
        missing_skills INT DEFAULT 0,
        action VARCHAR(50) DEFAULT 'search',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_user_activity_user_id ON user_activity (user_id);
    """)

    conn.commit()
    print("[MIGRATE] Tables created.")

    # ── STEP 1: Keywords ──────────────────────────────────────────────
    print("[MIGRATE] Inserting keywords...")

    keywords = [
        # Attendance
        ('attend', 'attendance_system', 'Education'),
        ('attendance', 'attendance_system', 'Education'),
        ('presence', 'attendance_system', 'Education'),
        ('rollcall', 'attendance_system', 'Education'),
        ('roll call', 'attendance_system', 'Education'),
        ('absentee', 'attendance_system', 'Education'),
        ('biometric', 'attendance_system', 'Education'),
        ('face recognition', 'attendance_system', 'Education'),
        ('qr attendance', 'attendance_system', 'Education'),
        # Library
        ('library', 'library_system', 'Education'),
        ('book', 'library_system', 'Education'),
        ('borrow', 'library_system', 'Education'),
        ('isbn', 'library_system', 'Education'),
        ('catalog', 'library_system', 'Education'),
        ('librarian', 'library_system', 'Education'),
        ('book issue', 'library_system', 'Education'),
        ('book return', 'library_system', 'Education'),
        # Hospital
        ('hospital', 'hospital_system', 'Medical'),
        ('doctor', 'hospital_system', 'Medical'),
        ('patient', 'hospital_system', 'Medical'),
        ('clinic', 'hospital_system', 'Medical'),
        ('medicine', 'hospital_system', 'Medical'),
        ('health', 'hospital_system', 'Medical'),
        ('prescription', 'hospital_system', 'Medical'),
        ('pharmacy', 'hospital_system', 'Medical'),
        # Ecommerce
        ('shop', 'ecommerce', 'Web Development'),
        ('store', 'ecommerce', 'Web Development'),
        ('buy', 'ecommerce', 'Web Development'),
        ('sell', 'ecommerce', 'Web Development'),
        ('e-commerce', 'ecommerce', 'Web Development'),
        ('ecommerce', 'ecommerce', 'Web Development'),
        ('product', 'ecommerce', 'Web Development'),
        ('checkout', 'ecommerce', 'Web Development'),
        ('purchase', 'ecommerce', 'Web Development'),
        ('marketplace', 'ecommerce', 'Web Development'),
        ('cart', 'ecommerce', 'Web Development'),
        # Chat
        ('chat', 'chat_app', 'Web Development'),
        ('message', 'chat_app', 'Web Development'),
        ('talk', 'chat_app', 'Web Development'),
        ('messenger', 'chat_app', 'Web Development'),
        ('group chat', 'chat_app', 'Web Development'),
        ('instant message', 'chat_app', 'Web Development'),
        # Quiz
        ('quiz', 'quiz_app', 'Education'),
        ('mcq', 'quiz_app', 'Education'),
        ('question', 'quiz_app', 'Education'),
        ('answer', 'quiz_app', 'Education'),
        ('assessment', 'quiz_app', 'Education'),
        ('grade', 'quiz_app', 'Education'),
        ('test portal', 'quiz_app', 'Education'),
        ('exam', 'quiz_app', 'Education'),
        # Expense
        ('expense', 'expense_tracker', 'Web Development'),
        ('budget', 'expense_tracker', 'Web Development'),
        ('money', 'expense_tracker', 'Web Development'),
        ('spend', 'expense_tracker', 'Web Development'),
        ('income', 'expense_tracker', 'Web Development'),
        ('cost', 'expense_tracker', 'Web Development'),
        ('savings', 'expense_tracker', 'Web Development'),
        ('wallet', 'expense_tracker', 'Web Development'),
        # Task Manager
        ('todo', 'task_manager', 'Web Development'),
        ('task', 'task_manager', 'Web Development'),
        ('to do', 'task_manager', 'Web Development'),
        ('reminder', 'task_manager', 'Web Development'),
        ('checklist', 'task_manager', 'Web Development'),
        ('planner', 'task_manager', 'Web Development'),
        ('deadline', 'task_manager', 'Web Development'),
        ('kanban', 'task_manager', 'Web Development'),
        # Food
        ('food', 'food_ordering', 'Web Development'),
        ('restaurant', 'food_ordering', 'Web Development'),
        ('meal', 'food_ordering', 'Web Development'),
        ('canteen', 'food_ordering', 'Web Development'),
        ('menu', 'food_ordering', 'Web Development'),
        ('order food', 'food_ordering', 'Web Development'),
        # Employee
        ('employee', 'employee_management', 'Web Development'),
        ('staff', 'employee_management', 'Web Development'),
        ('salary', 'employee_management', 'Web Development'),
        ('leave', 'employee_management', 'Web Development'),
        ('worker', 'employee_management', 'Web Development'),
        ('department', 'employee_management', 'Web Development'),
        ('hr', 'employee_management', 'Web Development'),
        ('payroll', 'employee_management', 'Web Development'),
        # Portfolio
        ('portfolio', 'portfolio', 'Web Development'),
        ('resume', 'portfolio', 'Web Development'),
        ('cv', 'portfolio', 'Web Development'),
        ('personal site', 'portfolio', 'Web Development'),
        ('showcase', 'portfolio', 'Web Development'),
        # AI / ML
        ('artificial intelligence', 'ai_project', 'Artificial Intelligence'),
        ('machine learning', 'ai_project', 'Artificial Intelligence'),
        ('deep learning', 'ai_project', 'Artificial Intelligence'),
        ('neural network', 'ai_project', 'Artificial Intelligence'),
        ('nlp', 'ai_project', 'Artificial Intelligence'),
        ('natural language', 'ai_project', 'Artificial Intelligence'),
        ('computer vision', 'ai_project', 'Artificial Intelligence'),
        ('image recognition', 'ai_project', 'Artificial Intelligence'),
        ('chatbot', 'ai_project', 'Artificial Intelligence'),
        ('recommendation', 'ai_project', 'Artificial Intelligence'),
        ('ai', 'ai_project', 'Artificial Intelligence'),
        ('ml', 'ai_project', 'Artificial Intelligence'),
        # Data Science
        ('data science', 'data_science_project', 'Data Science'),
        ('data analysis', 'data_science_project', 'Data Science'),
        ('visualization', 'data_science_project', 'Data Science'),
        ('dashboard', 'data_science_project', 'Data Science'),
        ('analytics', 'data_science_project', 'Data Science'),
        ('prediction', 'data_science_project', 'Data Science'),
        ('statistics', 'data_science_project', 'Data Science'),
        ('dataset', 'data_science_project', 'Data Science'),
        # Cyber Security
        ('cyber security', 'cyber_security_project', 'Cyber Security'),
        ('cybersecurity', 'cyber_security_project', 'Cyber Security'),
        ('encryption', 'cyber_security_project', 'Cyber Security'),
        ('hacking', 'cyber_security_project', 'Cyber Security'),
        ('firewall', 'cyber_security_project', 'Cyber Security'),
        ('vulnerability', 'cyber_security_project', 'Cyber Security'),
        ('intrusion', 'cyber_security_project', 'Cyber Security'),
        ('network security', 'cyber_security_project', 'Cyber Security'),
        ('password manager', 'cyber_security_project', 'Cyber Security'),
        # IoT
        ('iot', 'iot_project', 'IoT'),
        ('internet of things', 'iot_project', 'IoT'),
        ('sensor', 'iot_project', 'IoT'),
        ('arduino', 'iot_project', 'IoT'),
        ('raspberry pi', 'iot_project', 'IoT'),
        ('smart home', 'iot_project', 'IoT'),
        ('automation', 'iot_project', 'IoT'),
        ('embedded', 'iot_project', 'IoT'),
        # Cloud
        ('cloud', 'cloud_project', 'Cloud Computing'),
        ('aws', 'cloud_project', 'Cloud Computing'),
        ('deployment', 'cloud_project', 'Cloud Computing'),
        ('devops', 'cloud_project', 'Cloud Computing'),
        ('docker', 'cloud_project', 'Cloud Computing'),
        ('kubernetes', 'cloud_project', 'Cloud Computing'),
        ('microservice', 'cloud_project', 'Cloud Computing'),
        ('serverless', 'cloud_project', 'Cloud Computing'),
        # Mobile
        ('mobile app', 'mobile_app', 'Mobile App Development'),
        ('android', 'mobile_app', 'Mobile App Development'),
        ('ios', 'mobile_app', 'Mobile App Development'),
        ('flutter', 'mobile_app', 'Mobile App Development'),
        ('react native', 'mobile_app', 'Mobile App Development'),
        ('kotlin', 'mobile_app', 'Mobile App Development'),
        ('swift', 'mobile_app', 'Mobile App Development'),
        # Blockchain
        ('blockchain', 'blockchain_project', 'Blockchain'),
        ('crypto', 'blockchain_project', 'Blockchain'),
        ('nft', 'blockchain_project', 'Blockchain'),
        ('smart contract', 'blockchain_project', 'Blockchain'),
        ('ethereum', 'blockchain_project', 'Blockchain'),
        ('web3', 'blockchain_project', 'Blockchain'),
        # Fintech
        ('fintech', 'fintech_project', 'FinTech'),
        ('banking', 'fintech_project', 'FinTech'),
        ('loan', 'fintech_project', 'FinTech'),
        ('insurance', 'fintech_project', 'FinTech'),
        ('trading', 'fintech_project', 'FinTech'),
        ('stock', 'fintech_project', 'FinTech'),
        ('investment', 'fintech_project', 'FinTech'),
        ('payment gateway', 'fintech_project', 'FinTech'),
        # ── GAMING (NEW — was missing!) ──
        ('game', 'game_project', 'Game Development'),
        ('gaming', 'game_project', 'Game Development'),
        ('unity', 'game_project', 'Game Development'),
        ('unreal', 'game_project', 'Game Development'),
        ('pygame', 'game_project', 'Game Development'),
        ('multiplayer', 'game_project', 'Game Development'),
        ('2d game', 'game_project', 'Game Development'),
        ('3d game', 'game_project', 'Game Development'),
        ('game engine', 'game_project', 'Game Development'),
        ('sprite', 'game_project', 'Game Development'),
        ('game development', 'game_project', 'Game Development'),
    ]

    for kw, cat, dom in keywords:
        cur.execute(
            "INSERT INTO keywords (keyword, category, domain) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (kw, cat, dom)
        )
    conn.commit()
    print(f"[MIGRATE] Inserted {len(keywords)} keywords.")

    # ── STEP 2: Projects ──────────────────────────────────────────────
    print("[MIGRATE] Inserting projects...")

    projects = [
        # ── ATTENDANCE SYSTEM ──
        ('Student Register App', 'A web form that lets a teacher register student names and mark daily attendance. Stores data and shows a simple attendance table.', 'Education', 'Beginner', 'attendance_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Class Attendance Logger', 'Log attendance per class period. Supports multiple subjects, generates per-student percentage, and exports to CSV.', 'Education', 'Beginner', 'attendance_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Attendance Report Viewer', 'Reads attendance records and displays colourful monthly reports. Teacher can filter by student or date range.', 'Education', 'Beginner', 'attendance_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Attendance Portal with Login', 'Teacher and student login, per-class attendance marking, defaulter list, and PDF report generation.', 'Education', 'Intermediate', 'attendance_system', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Smart Attendance Dashboard', 'Role-based system (admin, teacher, student). Real-time attendance charts, email notifications for low attendance, and CSV/PDF export.', 'Education', 'Intermediate', 'attendance_system', 'HTML,CSS,JavaScript,Chart.js,Python,Flask,PostgreSQL'),
        ('Geo-Fenced Attendance System', 'Students mark attendance only within campus GPS boundary. Live map view for admin, attendance analytics dashboard.', 'Education', 'Intermediate', 'attendance_system', 'Python,Flask,PostgreSQL,JavaScript,Leaflet.js'),
        ('Face Recognition Attendance', 'Automated attendance using OpenCV face detection. Stores face embeddings in DB, real-time marking, and admin analytics dashboard.', 'Education', 'Advanced', 'attendance_system', 'Python,OpenCV,Flask,PostgreSQL,NumPy,JavaScript'),
        ('Blockchain Attendance Ledger', 'Tamper-proof attendance records stored on a private blockchain. Smart contracts enforce rules; admin can audit full history.', 'Education', 'Advanced', 'attendance_system', 'Python,Flask,PostgreSQL,JavaScript,Blockchain'),
        ('AI-Powered Attendance Predictor', 'Predicts students likely to fall below attendance threshold using ML. Sends automated alerts and generates trend reports.', 'Education', 'Advanced', 'attendance_system', 'Python,Flask,PostgreSQL,scikit-learn,Pandas,JavaScript,React'),

        # ── LIBRARY SYSTEM ──
        ('Book Catalogue Browser', 'A simple searchable list of library books with title, author, and availability status.', 'Education', 'Beginner', 'library_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Library Issue Tracker', 'Track which books are issued to which student. Admin can record issue and return dates and view overdue books.', 'Education', 'Beginner', 'library_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Simple Book Search App', 'Search books by title or author. Results show cover image, genre, and shelf location. Admin can add books via form.', 'Education', 'Beginner', 'library_system', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Library Member Portal', 'Member registration, book catalog with filters, issue history per member, and fines calculated automatically.', 'Education', 'Intermediate', 'library_system', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Library Management with Notifications', 'Full library system with due-date email reminders, reservation queue, and admin dashboard with inventory reports.', 'Education', 'Intermediate', 'library_system', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('E-Library with PDF Viewer', 'Digital library where users can read PDFs in-browser. Tracks reading progress, supports bookmarks, and has admin upload panel.', 'Education', 'Intermediate', 'library_system', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Smart Library Recommendation Engine', 'Recommends books based on borrowing history using collaborative filtering. Admin can manage users, inventory, and view analytics.', 'Education', 'Advanced', 'library_system', 'Python,Flask,PostgreSQL,scikit-learn,JavaScript,React'),
        ('RFID-Based Library System', 'Books tagged with RFID auto-check-in/check-out at gates. Dashboard tracks real-time inventory and generates usage analytics.', 'Education', 'Advanced', 'library_system', 'Python,Flask,PostgreSQL,JavaScript,React,RFID'),
        ('Library API with Mobile App', 'RESTful library backend with JWT auth. Mobile app built in React Native lets students search, reserve, and renew books.', 'Education', 'Advanced', 'library_system', 'Python,Flask,PostgreSQL,React Native,REST API,JWT'),

        # ── HOSPITAL SYSTEM ──
        ('Patient Registration Form', 'A simple form to register new patients with name, age, and ailment. Records stored in DB, admin can view patient list.', 'Medical', 'Beginner', 'hospital_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Doctor Schedule Viewer', 'Displays available doctor slots for the week. Patients can view but not book — admin manages the schedule.', 'Medical', 'Beginner', 'hospital_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Basic Medical Records App', 'Store and view patient visit records — diagnosis, prescribed medicines, and doctor notes. Simple CRUD interface.', 'Medical', 'Beginner', 'hospital_system', 'HTML,CSS,Python,PostgreSQL'),
        ('Clinic Appointment Manager', 'Online appointment booking with doctor selection, date/time slot picker, and confirmation email. Admin dashboard for scheduling.', 'Medical', 'Intermediate', 'hospital_system', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Hospital Patient Portal', 'Patients log in to view medical history, book appointments, and download prescriptions. Doctors update records after visits.', 'Medical', 'Intermediate', 'hospital_system', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Pharmacy Inventory System', 'Track medicine stock, suppliers, expiry dates, and auto-reorder alerts. Integrates with hospital patient prescription module.', 'Medical', 'Intermediate', 'hospital_system', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Telemedicine Platform', 'Video consultation platform with patient-doctor chat, prescription upload, appointment scheduling, and payment gateway.', 'Medical', 'Advanced', 'hospital_system', 'Python,Flask,PostgreSQL,JavaScript,React,WebRTC'),
        ('Hospital AI Diagnostic Assistant', 'Symptom-checker powered by ML that suggests probable diagnoses. Feeds into doctor review workflow with confidence scores.', 'Medical', 'Advanced', 'hospital_system', 'Python,Flask,PostgreSQL,scikit-learn,React,REST API'),
        ('Hospital ERP System', 'End-to-end hospital ERP: patient management, billing, payroll, inventory, lab results, and analytics across every department.', 'Medical', 'Advanced', 'hospital_system', 'Python,Flask,PostgreSQL,JavaScript,React,Docker'),

        # ── ECOMMERCE ──
        ('Simple Product Store', 'Display products with image, price, and category. Users can browse but cart/checkout is a future feature.', 'Web Development', 'Beginner', 'ecommerce', 'HTML,CSS,Python,PostgreSQL'),
        ('Category Filter Shop', 'Product listing with category-based filter and price sort. Products managed by admin via a hidden dashboard.', 'Web Development', 'Beginner', 'ecommerce', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Product Search Engine', 'Live search bar that filters products as user types. Search across title, description, and category.', 'Web Development', 'Beginner', 'ecommerce', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Shopping Cart App', 'Add/remove items to cart, calculate totals, and place orders. Order history saved. User authentication required.', 'Web Development', 'Intermediate', 'ecommerce', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('E-Commerce with Reviews', 'Full shopping site with product ratings, user reviews, wishlist, and admin panel to manage products and orders.', 'Web Development', 'Intermediate', 'ecommerce', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Multi-Vendor Marketplace', 'Multiple sellers register shops; buyers browse and order from any seller. Admin approves sellers and mediates disputes.', 'Web Development', 'Intermediate', 'ecommerce', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('E-Commerce with Payment Gateway', 'Complete store with Razorpay/Stripe integration, order tracking emails, inventory control, and React-based frontend.', 'Web Development', 'Advanced', 'ecommerce', 'Python,Flask,PostgreSQL,JavaScript,React,Razorpay'),
        ('E-Commerce Recommendation Engine', 'Product recommendations using collaborative filtering on purchase history. Includes A/B testing framework for offers.', 'Web Development', 'Advanced', 'ecommerce', 'Python,Flask,PostgreSQL,scikit-learn,JavaScript,React'),
        ('Headless Commerce API', 'REST API-first commerce backend with JWT auth, GraphQL queries, Redis caching, and a React storefront.', 'Web Development', 'Advanced', 'ecommerce', 'Python,Flask,PostgreSQL,Redis,JavaScript,React,Docker'),

        # ── PORTFOLIO ──
        ('Basic HTML Resume', 'A single-page online resume with name, education, skills, and contact info. No JavaScript required.', 'Web Development', 'Beginner', 'portfolio', 'HTML,CSS'),
        ('Animated Portfolio Page', 'Personal portfolio with CSS animations, skills section, project cards, and a mailto contact button.', 'Web Development', 'Beginner', 'portfolio', 'HTML,CSS,JavaScript'),
        ('Portfolio with Photo Gallery', 'Showcase your photos in a responsive grid with lightbox pop-ups. Admin adds images via a simple upload form.', 'Web Development', 'Beginner', 'portfolio', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Portfolio with Live Projects', 'Dynamic portfolio that fetches your GitHub repos via API and displays them as project cards with live demo links.', 'Web Development', 'Intermediate', 'portfolio', 'HTML,CSS,JavaScript,Python,Flask,GitHub API'),
        ('Portfolio Blog System', 'Portfolio combined with a blog engine. Write/edit posts in Markdown; posts stored in DB. Responsive design.', 'Web Development', 'Intermediate', 'portfolio', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Portfolio CMS', 'Content management system lets you add/edit skills, projects, and testimonials from an admin panel without touching code.', 'Web Development', 'Intermediate', 'portfolio', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Portfolio with Analytics', 'Portfolio site that tracks visitor count, page views, and time on page. Dashboard shows visual analytics to owner.', 'Web Development', 'Advanced', 'portfolio', 'Python,Flask,PostgreSQL,JavaScript,React,Chart.js'),
        ('Full-Stack Portfolio Platform', 'Multi-user portfolio platform — users register, build their own portfolio, and share a public URL. Admin moderation panel.', 'Web Development', 'Advanced', 'portfolio', 'Python,Flask,PostgreSQL,JavaScript,React,Docker'),
        ('3D Interactive Portfolio', 'Portfolio with Three.js 3D animations, WebGL effects, and API-driven content. Hosted on cloud with CI/CD pipeline.', 'Web Development', 'Advanced', 'portfolio', 'JavaScript,React,Three.js,Python,Flask,PostgreSQL,Docker'),

        # ── QUIZ APP ──
        ('Static Quiz Page', 'A 5-question multiple-choice quiz hardcoded in HTML/JavaScript that shows final score at the end.', 'Education', 'Beginner', 'quiz_app', 'HTML,CSS,JavaScript'),
        ('DB-Driven Quiz', 'Quiz questions stored in DB. Admin can add/edit questions. Students take quiz and score is shown on completion.', 'Education', 'Beginner', 'quiz_app', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Category Quiz Selector', 'Choose quiz category (Math, Science, English) from a menu. Questions fetched by category.', 'Education', 'Beginner', 'quiz_app', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Timed Quiz Application', 'Countdown timer per question, auto-submit on timeout, leaderboard showing top scores, and user login to track history.', 'Education', 'Intermediate', 'quiz_app', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Teacher Quiz Builder', 'Teachers create custom quizzes, assign to classes, and view per-student results. Students get instant feedback after submission.', 'Education', 'Intermediate', 'quiz_app', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Adaptive Quiz Engine', 'Quiz dynamically adjusts question difficulty based on previous answers using a simple scoring algorithm.', 'Education', 'Intermediate', 'quiz_app', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Online Exam Proctoring System', 'Full exam portal with webcam-based proctoring, randomised question order, and anti-tab-switch detection.', 'Education', 'Advanced', 'quiz_app', 'Python,Flask,PostgreSQL,JavaScript,React,OpenCV'),
        ('AI Question Generator', 'NLP model generates quiz questions from uploaded PDF study material. Exports to printable format or online quiz mode.', 'Education', 'Advanced', 'quiz_app', 'Python,Flask,PostgreSQL,NLP,Transformers,React'),
        ('Multiplayer Quiz Game', 'Real-time multiplayer quiz where multiple students compete simultaneously. Live score updates via WebSocket.', 'Education', 'Advanced', 'quiz_app', 'Python,Flask,Flask-SocketIO,PostgreSQL,JavaScript,React'),

        # ── EXPENSE TRACKER ──
        ('Daily Spending Log', 'Simple form to log daily expenses by category (food, transport, etc.). View monthly totals in a table.', 'Web Development', 'Beginner', 'expense_tracker', 'HTML,CSS,Python,PostgreSQL'),
        ('Budget Goal Tracker', 'Set a monthly budget goal and log expenses. A progress bar shows how much of the budget is used.', 'Web Development', 'Beginner', 'expense_tracker', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Receipt Upload Tracker', 'Upload receipt images with expense amount and category. Admin views expenses in a sortable table.', 'Web Development', 'Beginner', 'expense_tracker', 'HTML,CSS,Python,PostgreSQL'),
        ('Multi-Category Expense Dashboard', 'Track income and expenses across categories with monthly pie charts, bar graphs, and budget alerts.', 'Web Development', 'Intermediate', 'expense_tracker', 'HTML,CSS,JavaScript,Chart.js,Python,Flask,PostgreSQL'),
        ('Family Budget Manager', 'Multi-user family budget app. Each member logs expenses; shared dashboard shows family totals and individual contributions.', 'Web Development', 'Intermediate', 'expense_tracker', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Expense Sharing App', 'Split bills between friends, track who owes what, and settle balances. Expense history with detailed breakdown.', 'Web Development', 'Intermediate', 'expense_tracker', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('AI Expense Predictor', 'ML model trained on past spending predicts next month expenses by category. REST API backend with React dashboard.', 'Web Development', 'Advanced', 'expense_tracker', 'Python,Flask,PostgreSQL,scikit-learn,React,Chart.js'),
        ('Expense Tracker with Bank Integration', 'Connects to bank CSV exports, auto-categorises transactions with NLP, and shows trends on an analytics dashboard.', 'Web Development', 'Advanced', 'expense_tracker', 'Python,Flask,PostgreSQL,NLP,React,Chart.js,Docker'),
        ('Financial Planning Platform', 'Comprehensive personal finance tool — budgets, goals, debt tracker, investment tracker, and AI-based savings suggestions.', 'Web Development', 'Advanced', 'expense_tracker', 'Python,Flask,PostgreSQL,scikit-learn,JavaScript,React,Docker'),

        # ── TASK MANAGER ──
        ('Simple To-Do App', 'Add, complete, and delete tasks from a clean interface. Data saved so tasks persist across page refreshes.', 'Web Development', 'Beginner', 'task_manager', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Priority To-Do List', 'Assign High/Medium/Low priority to tasks. Sorted list view with colour-coded priorities and a done/undone toggle.', 'Web Development', 'Beginner', 'task_manager', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Daily Planner App', 'Organise tasks by day. Calendar-style view shows tasks per date. Simple drag-and-drop reordering.', 'Web Development', 'Beginner', 'task_manager', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Team Task Board', 'Kanban-style board with To-Do, In Progress, and Done columns. Tasks can be assigned to team members.', 'Web Development', 'Intermediate', 'task_manager', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Project Management Tool', 'Create projects with multiple tasks, set deadlines and assignees, receive deadline reminders via email.', 'Web Development', 'Intermediate', 'task_manager', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Recurring Task Scheduler', 'Set tasks that recur daily/weekly/monthly. Auto-generates new task entries and sends reminder notifications.', 'Web Development', 'Intermediate', 'task_manager', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Full PM Suite with Gantt', 'End-to-end project management with Gantt chart visualisation, resource allocation, milestone tracking, and team chat.', 'Web Development', 'Advanced', 'task_manager', 'Python,Flask,PostgreSQL,JavaScript,React,Chart.js,WebSocket'),
        ('AI Task Prioritiser', 'ML model suggests task priority based on deadline, dependencies, and historical completion patterns.', 'Web Development', 'Advanced', 'task_manager', 'Python,Flask,PostgreSQL,scikit-learn,JavaScript,React'),
        ('Enterprise Task API', 'Fully RESTful task management API with JWT auth, role-based permissions, webhooks, and API rate limiting.', 'Web Development', 'Advanced', 'task_manager', 'Python,Flask,PostgreSQL,Redis,Docker,REST API,JWT'),

        # ── CHAT APP ──
        ('Static Chat UI', 'A styled chat-room look built with HTML/CSS only. No real functionality — a pure UI exercise.', 'Web Development', 'Beginner', 'chat_app', 'HTML,CSS'),
        ('Basic Chat Room', 'Simple WebSocket chat where multiple browser tabs can exchange messages in real time. No login required.', 'Web Development', 'Beginner', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,Flask-SocketIO'),
        ('Chat with Username', 'Assign a username before entering the chat room. Messages show sender name and timestamp. History stored in DB.', 'Web Development', 'Beginner', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Private Messaging App', 'User login, find other users, send private messages, and see online/offline status with read receipts.', 'Web Development', 'Intermediate', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL,Flask-SocketIO'),
        ('Group Chat with Rooms', 'Create or join named chat rooms. Messages persist. Admin can mute/kick users from rooms.', 'Web Development', 'Intermediate', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL,Flask-SocketIO'),
        ('Chat App with File Sharing', 'Send text and upload images/files in chat. Preview images inline; file links stored in DB and served via Flask.', 'Web Development', 'Intermediate', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL,Flask-SocketIO'),
        ('Encrypted Messaging Platform', 'End-to-end encrypted chat using RSA/AES. Key exchange on login; messages decrypted only on recipient device.', 'Web Development', 'Advanced', 'chat_app', 'Python,Flask,PostgreSQL,JavaScript,React,Cryptography,WebSocket'),
        ('Video Conference App', 'Multi-user video and audio calls using WebRTC with a text chat sidebar. Room links shareable by URL.', 'Web Development', 'Advanced', 'chat_app', 'Python,Flask,PostgreSQL,JavaScript,React,WebRTC'),
        ('Chat Bot Integration Platform', 'Messenger platform with plugin-based chatbot support. Bots answer FAQ, schedule meetings, and escalate to human agents.', 'Web Development', 'Advanced', 'chat_app', 'Python,Flask,PostgreSQL,JavaScript,React,NLP,WebSocket'),

        # ── EMPLOYEE MANAGEMENT ──
        ('Employee List App', 'View a list of employees with name, department, and role. Admin can add or delete records.', 'Web Development', 'Beginner', 'employee_management', 'HTML,CSS,Python,PostgreSQL'),
        ('Employee Profile Manager', 'Each employee has a profile page with photo, contact info, and designation. Admin can edit profiles.', 'Web Development', 'Beginner', 'employee_management', 'HTML,CSS,Python,PostgreSQL'),
        ('Department Organisation Chart', 'Visual org chart showing company hierarchy. Data pulled from DB; admin updates structure via form.', 'Web Development', 'Beginner', 'employee_management', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Leave Management System', 'Employees apply for leave online. Manager approves/rejects. Leave balance tracked per employee.', 'Web Development', 'Intermediate', 'employee_management', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Payroll Calculator App', 'Enter hours worked and hourly rate; system calculates gross pay, tax deductions, and net salary. Payslips downloadable.', 'Web Development', 'Intermediate', 'employee_management', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('HR Dashboard with Analytics', 'Admin dashboard showing headcount by department, attrition rate, leave trends, and salary distribution charts.', 'Web Development', 'Intermediate', 'employee_management', 'HTML,CSS,JavaScript,Chart.js,Python,Flask,PostgreSQL'),
        ('Full HRMS Platform', 'Complete HR system — recruitment, onboarding, attendance, performance reviews, payroll, and exit management.', 'Web Development', 'Advanced', 'employee_management', 'Python,Flask,PostgreSQL,JavaScript,React,Docker'),
        ('AI Employee Attrition Predictor', 'ML model predicts which employees are likely to resign based on satisfaction scores, tenure, and performance data.', 'Web Development', 'Advanced', 'employee_management', 'Python,Flask,PostgreSQL,scikit-learn,Pandas,React'),
        ('Employee Self-Service Portal', 'Employees log in to view payslips, apply for leave, update details, and access company documents. Full REST API backend.', 'Web Development', 'Advanced', 'employee_management', 'Python,Flask,PostgreSQL,JavaScript,React,Docker,REST API'),

        # ── FOOD ORDERING ──
        ('Static Menu Page', 'Beautiful HTML/CSS food menu for a single restaurant. Items grouped by category with prices.', 'Web Development', 'Beginner', 'food_ordering', 'HTML,CSS'),
        ('Restaurant Menu with DB', 'Menu items stored in DB. Admin adds/updates items via a form. Customers browse from the same page.', 'Web Development', 'Beginner', 'food_ordering', 'HTML,CSS,JavaScript,Python,PostgreSQL'),
        ('Canteen Daily Menu Poster', 'School or office canteen posts today menu. Admin updates it daily. Displays current time and meal timing.', 'Web Development', 'Beginner', 'food_ordering', 'HTML,CSS,Python,PostgreSQL'),
        ('Food Order and Bill Generator', 'Customer selects items, adds to cart, places order, and gets a printable bill. Orders saved in DB.', 'Web Development', 'Intermediate', 'food_ordering', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Restaurant Online Ordering System', 'Full table reservation + food pre-order system. User login, real-time kitchen status, and SMS notification on ready.', 'Web Development', 'Intermediate', 'food_ordering', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Multi-Restaurant Food App', 'Multiple restaurants listed; user browses menus, places orders, and tracks delivery status from a single platform.', 'Web Development', 'Intermediate', 'food_ordering', 'HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
        ('Food Delivery Platform', 'Full delivery ecosystem — restaurants, riders, and customers. Live order tracking map, payment gateway, and admin panel.', 'Web Development', 'Advanced', 'food_ordering', 'Python,Flask,PostgreSQL,JavaScript,React,Leaflet.js,Razorpay'),
        ('AI Food Recommendation Engine', 'Recommends dishes based on order history and dietary preferences using collaborative filtering. React-based frontend.', 'Web Development', 'Advanced', 'food_ordering', 'Python,Flask,PostgreSQL,scikit-learn,JavaScript,React'),
        ('Cloud Kitchen Management System', 'Multi-brand cloud kitchen backend: order routing, inventory, cost analysis, and customer loyalty program management.', 'Web Development', 'Advanced', 'food_ordering', 'Python,Flask,PostgreSQL,JavaScript,React,Docker,Redis'),

        # ── AI PROJECT ──
        ('Sentiment Analyser', 'Enter text and get a positive/negative/neutral sentiment result using a pre-trained model. Simple Flask+HTML interface.', 'Artificial Intelligence', 'Beginner', 'ai_project', 'Python,Flask,NLTK,HTML,CSS'),
        ('Image Classifier Demo', 'Upload an image and classify it into categories using a pre-trained CNN. Shows top-3 predictions with confidence.', 'Artificial Intelligence', 'Beginner', 'ai_project', 'Python,Flask,TensorFlow,HTML,CSS'),
        ('Simple Chatbot', 'Rule-based chatbot that answers predefined FAQs using keyword matching. Deployed as a Flask web app.', 'Artificial Intelligence', 'Beginner', 'ai_project', 'Python,Flask,HTML,CSS,PostgreSQL'),
        ('ML Spam Detector', 'Train a Naive Bayes classifier on SMS/email data. Web interface to type a message and check if it is spam.', 'Artificial Intelligence', 'Intermediate', 'ai_project', 'Python,Flask,scikit-learn,Pandas,HTML,CSS,PostgreSQL'),
        ('Movie Recommendation System', 'Collaborative filtering recommender trained on ratings dataset. Enter a movie title and get 5 similar recommendations.', 'Artificial Intelligence', 'Intermediate', 'ai_project', 'Python,Flask,Pandas,scikit-learn,PostgreSQL,HTML,JavaScript'),
        ('Handwriting Recognition App', 'Draw a digit on a canvas; a trained CNN predicts the number instantly. Model trained on MNIST dataset.', 'Artificial Intelligence', 'Intermediate', 'ai_project', 'Python,Flask,TensorFlow,JavaScript,HTML,CSS'),
        ('Real-Time Object Detection App', 'Detect objects in a live webcam stream using YOLO. Annotated frames streamed to the browser via Flask.', 'Artificial Intelligence', 'Advanced', 'ai_project', 'Python,Flask,OpenCV,YOLO,JavaScript,PostgreSQL'),
        ('NLP Question Answering System', 'Upload a PDF; system extracts text and answers natural-language questions using a Transformer model.', 'Artificial Intelligence', 'Advanced', 'ai_project', 'Python,Flask,Transformers,PostgreSQL,JavaScript,React'),
        ('AI Code Review Bot', 'Analyses student Python code for errors, style issues, and complexity. Returns detailed review with suggestions.', 'Artificial Intelligence', 'Advanced', 'ai_project', 'Python,Flask,AST,PostgreSQL,JavaScript,React'),

        # ── DATA SCIENCE ──
        ('CSV Data Explorer', 'Upload a CSV and instantly see column statistics, data types, and a preview table. Built with Pandas and Flask.', 'Data Science', 'Beginner', 'data_science_project', 'Python,Flask,Pandas,HTML,CSS'),
        ('Simple Bar Chart Generator', 'Upload tabular data; tool generates a bar chart using Matplotlib. Download the chart as PNG.', 'Data Science', 'Beginner', 'data_science_project', 'Python,Flask,Matplotlib,HTML,CSS'),
        ('Student Grade Analyser', 'Enter student marks; app calculates mean, median, pass/fail rate, and renders a grade distribution chart.', 'Data Science', 'Beginner', 'data_science_project', 'Python,Flask,Pandas,Matplotlib,PostgreSQL,HTML,CSS'),
        ('Sales Trend Dashboard', 'Upload monthly sales CSV; dashboard shows trend lines, top products, and seasonal patterns using Plotly.', 'Data Science', 'Intermediate', 'data_science_project', 'Python,Flask,Pandas,Plotly,PostgreSQL,HTML,JavaScript'),
        ('COVID Data Visualisation', 'Fetch public COVID dataset, clean with Pandas, and display interactive country-wise charts on a world map.', 'Data Science', 'Intermediate', 'data_science_project', 'Python,Flask,Pandas,Plotly,HTML,JavaScript'),
        ('Housing Price Predictor', 'Linear regression model predicts house price from area, rooms, and location features. Web form for predictions.', 'Data Science', 'Intermediate', 'data_science_project', 'Python,Flask,scikit-learn,Pandas,PostgreSQL,HTML,CSS'),
        ('Customer Churn Predictor', 'Train a Random Forest on telecom data to predict customer churn. Interactive dashboard shows feature importance.', 'Data Science', 'Advanced', 'data_science_project', 'Python,Flask,scikit-learn,Pandas,React,PostgreSQL,Docker'),
        ('Real-Time Stock Market Analyser', 'Stream live stock data via API, calculate moving averages, and display interactive candlestick charts.', 'Data Science', 'Advanced', 'data_science_project', 'Python,Flask,Pandas,Plotly,WebSocket,PostgreSQL,React'),
        ('Financial Fraud Detection System', 'Anomaly detection on transaction data using Isolation Forest and AutoEncoder. Real-time alert dashboard.', 'Data Science', 'Advanced', 'data_science_project', 'Python,Flask,scikit-learn,TensorFlow,Pandas,PostgreSQL,React'),

        # ── CYBER SECURITY ──
        ('Password Strength Checker', 'Enter a password and get an instant strength score (Weak/Fair/Strong) with improvement tips.', 'Cyber Security', 'Beginner', 'cyber_security_project', 'Python,Flask,HTML,CSS,JavaScript'),
        ('Caesar Cipher Tool', 'Encrypt and decrypt messages using Caesar cipher. User selects shift value; tool shows cipher text in real time.', 'Cyber Security', 'Beginner', 'cyber_security_project', 'Python,Flask,HTML,CSS,JavaScript'),
        ('Basic Port Scanner', 'Enter an IP/hostname; tool scans a port range and reports open/closed ports. Result displayed in a table.', 'Cyber Security', 'Beginner', 'cyber_security_project', 'Python,Flask,HTML,CSS'),
        ('Secure Password Manager', 'Store encrypted passwords. Master password decrypts vault locally. Clipboard copy and password generator.', 'Cyber Security', 'Intermediate', 'cyber_security_project', 'Python,Flask,PostgreSQL,Cryptography,HTML,JavaScript'),
        ('Network Traffic Analyser', 'Capture network packets with Scapy, parse protocols, and display live packet summary in a Flask dashboard.', 'Cyber Security', 'Intermediate', 'cyber_security_project', 'Python,Flask,Scapy,PostgreSQL,HTML,JavaScript'),
        ('Phishing URL Detector', 'ML model classifies URLs as phishing or legitimate based on lexical features. Web form for URL submission.', 'Cyber Security', 'Intermediate', 'cyber_security_project', 'Python,Flask,scikit-learn,Pandas,PostgreSQL,HTML,CSS'),
        ('IDS Intrusion Detection System', 'Monitor network traffic, detect anomalous patterns using ML, and trigger alerts with packet capture logging.', 'Cyber Security', 'Advanced', 'cyber_security_project', 'Python,Flask,scikit-learn,Scapy,PostgreSQL,React,Docker'),
        ('Secure File Sharing App', 'AES-encrypted file upload/download platform. Files encrypted at rest, temporary signed URLs, and audit trail.', 'Cyber Security', 'Advanced', 'cyber_security_project', 'Python,Flask,PostgreSQL,Cryptography,React,Docker'),
        ('Vulnerability Scanner', 'Automated web vulnerability scanner — checks for SQLi, XSS, CSRF, open redirects, and security headers.', 'Cyber Security', 'Advanced', 'cyber_security_project', 'Python,Flask,PostgreSQL,JavaScript,React,Docker'),

        # ── IoT ──
        ('LED Brightness Control', 'Control an LED brightness via a web slider. Arduino reads PWM signal from serial; Flask serves the control page.', 'IoT', 'Beginner', 'iot_project', 'Python,Flask,Arduino,HTML,CSS,JavaScript'),
        ('Temperature Monitor', 'DHT11 sensor reads temperature; Raspberry Pi sends data to Flask server. Dashboard shows current reading.', 'IoT', 'Beginner', 'iot_project', 'Python,Flask,Raspberry Pi,PostgreSQL,HTML,CSS'),
        ('Button-Triggered Notification', 'Press a physical button; Arduino sends signal via serial to Flask which emails or notifies the user.', 'IoT', 'Beginner', 'iot_project', 'Python,Flask,Arduino,HTML,CSS'),
        ('Smart Home Dashboard', 'Control multiple GPIO pins (lights, fans) from a web dashboard. State persisted in DB; mobile-responsive UI.', 'IoT', 'Intermediate', 'iot_project', 'Python,Flask,Raspberry Pi,PostgreSQL,JavaScript,HTML,CSS'),
        ('IoT Environment Monitor', 'Multi-sensor station feeds real-time data to a Plotly dashboard via MQTT.', 'IoT', 'Intermediate', 'iot_project', 'Python,Flask,MQTT,Raspberry Pi,PostgreSQL,JavaScript,Plotly'),
        ('Plant Watering Automation', 'Soil moisture sensor triggers water pump via relay. Web dashboard shows moisture history and manual override.', 'IoT', 'Intermediate', 'iot_project', 'Python,Flask,Arduino,PostgreSQL,JavaScript,HTML,CSS'),
        ('Smart Energy Monitor', 'Current sensors measure appliance power consumption. Real-time dashboard shows usage, cost, and carbon footprint.', 'IoT', 'Advanced', 'iot_project', 'Python,Flask,MQTT,PostgreSQL,Raspberry Pi,React,Chart.js,Docker'),
        ('Industrial Anomaly Detector', 'Vibration and temperature sensors feed ML model that detects machine anomalies before failure occurs.', 'IoT', 'Advanced', 'iot_project', 'Python,Flask,scikit-learn,MQTT,PostgreSQL,React,Docker'),
        ('Smart City Traffic System', 'Traffic sensors count vehicles per lane; ML model adjusts signal timings dynamically. Live map dashboard.', 'IoT', 'Advanced', 'iot_project', 'Python,Flask,MQTT,PostgreSQL,scikit-learn,JavaScript,React,Leaflet.js'),

        # ── CLOUD COMPUTING ──
        ('Static Site Deployment Guide', 'Deploy a simple HTML/CSS site on AWS S3. Includes step-by-step documentation and Bash setup scripts.', 'Cloud Computing', 'Beginner', 'cloud_project', 'HTML,CSS,AWS,Bash'),
        ('Dockerised Flask App', 'Package a Flask app in a Docker container and run it locally. Includes Dockerfile and documentation.', 'Cloud Computing', 'Beginner', 'cloud_project', 'Python,Flask,Docker,PostgreSQL'),
        ('Cloud File Storage App', 'Upload files to AWS S3 via a Flask web form. Files listed with download links.', 'Cloud Computing', 'Beginner', 'cloud_project', 'Python,Flask,AWS,PostgreSQL,HTML,CSS'),
        ('Docker Compose Web Stack', 'Flask + PostgreSQL + Nginx all orchestrated with Docker Compose. One command spins up the full stack.', 'Cloud Computing', 'Intermediate', 'cloud_project', 'Python,Flask,PostgreSQL,Docker,Nginx'),
        ('CI/CD Pipeline with GitHub Actions', 'Automated test-and-deploy pipeline: push to GitHub triggers tests, builds Docker image, and deploys.', 'Cloud Computing', 'Intermediate', 'cloud_project', 'Python,Flask,Docker,AWS,GitHub Actions'),
        ('Serverless API with AWS Lambda', 'Build a CRUD REST API deployed as serverless functions on AWS Lambda.', 'Cloud Computing', 'Intermediate', 'cloud_project', 'Python,AWS Lambda,DynamoDB,API Gateway,Serverless'),
        ('Kubernetes Microservices App', 'Decompose a monolith into 3 microservices deployed on Kubernetes. Includes Helm charts and auto-scaling.', 'Cloud Computing', 'Advanced', 'cloud_project', 'Python,Flask,Docker,Kubernetes,PostgreSQL,Helm,GitHub Actions'),
        ('Multi-Region Disaster Recovery', 'Flask app deployed across two AWS regions. Route 53 health checks auto-failover on region outage.', 'Cloud Computing', 'Advanced', 'cloud_project', 'Python,Flask,AWS,Docker,PostgreSQL,Terraform'),
        ('Cloud Cost Optimiser Dashboard', 'Fetches AWS Cost Explorer data, analyses spending, and surfaces optimisation recommendations.', 'Cloud Computing', 'Advanced', 'cloud_project', 'Python,Flask,AWS,PostgreSQL,JavaScript,React,Docker'),

        # ── GAME PROJECT (NEW — was completely missing!) ──
        ('Snake Game', 'Classic snake game built with Pygame. Arrow keys to move, eat food to grow, and avoid walls.', 'Game Development', 'Beginner', 'game_project', 'Python,Pygame'),
        ('Tic-Tac-Toe Game', 'Two-player Tic-Tac-Toe with a clean GUI. Option to play against a simple AI opponent.', 'Game Development', 'Beginner', 'game_project', 'Python,Pygame,HTML,CSS,JavaScript'),
        ('Memory Card Game', 'Flip cards to find matching pairs. Timer and move counter track performance. Built with JavaScript.', 'Game Development', 'Beginner', 'game_project', 'HTML,CSS,JavaScript'),
        ('Platformer Game', '2D side-scrolling platformer with jumping, enemies, and collectible coins. Level progression system.', 'Game Development', 'Intermediate', 'game_project', 'Python,Pygame,JavaScript'),
        ('Multiplayer Quiz Game', 'Real-time multiplayer quiz where players compete. WebSocket-based live scoring and leaderboard.', 'Game Development', 'Intermediate', 'game_project', 'Python,Flask,Flask-SocketIO,JavaScript,React,PostgreSQL'),
        ('Tower Defense Game', 'Strategic tower defense game with multiple tower types, enemy waves, and upgrade system.', 'Game Development', 'Intermediate', 'game_project', 'Python,Pygame,JavaScript,HTML,CSS'),
        ('3D First-Person Explorer', 'First-person 3D environment built with Three.js. Explore a procedurally generated world with dynamic lighting.', 'Game Development', 'Advanced', 'game_project', 'JavaScript,Three.js,React,WebGL'),
        ('Multiplayer Battle Arena', 'Real-time multiplayer battle game with WebSocket networking. Player matchmaking and live score tracking.', 'Game Development', 'Advanced', 'game_project', 'Python,Flask,Flask-SocketIO,JavaScript,React,PostgreSQL,Redis'),
        ('AI Game Bot with Reinforcement Learning', 'Train an AI agent to play a game using reinforcement learning. Compare human vs AI performance on dashboard.', 'Game Development', 'Advanced', 'game_project', 'Python,TensorFlow,Flask,Pygame,JavaScript,React'),
    ]

    for title, desc, domain, diff, cat, tech in projects:
        cur.execute(
            """INSERT INTO projects (title, description, domain, difficulty, category, technologies)
               VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
            (title, desc, domain, diff, cat, tech)
        )
    conn.commit()
    print(f"[MIGRATE] Inserted {len(projects)} projects.")

    # ── STEP 3: Skills ────────────────────────────────────────────────
    print("[MIGRATE] Inserting skills...")

    skills = [
        # Website
        ('HTML', 'website', 'Frontend', 2, '1 week'),
        ('CSS', 'website', 'Frontend', 2, '1 week'),
        ('JavaScript', 'website', 'Frontend', 4, '2-3 weeks'),
        ('React', 'website', 'Frontend', 3, '3-4 weeks'),
        ('Python', 'website', 'Backend', 4, '2-3 weeks'),
        ('Flask', 'website', 'Backend', 3, '1-2 weeks'),
        ('MySQL', 'website', 'Database', 3, '1-2 weeks'),
        ('PostgreSQL', 'website', 'Database', 3, '1-2 weeks'),
        ('Git', 'website', 'Tools', 2, '3-5 days'),
        # App
        ('Java', 'app', 'Android', 4, '4-6 weeks'),
        ('Kotlin', 'app', 'Android', 4, '3-4 weeks'),
        ('React Native', 'app', 'Cross-Platform', 4, '3-4 weeks'),
        ('Firebase', 'app', 'Backend', 3, '1-2 weeks'),
        ('REST API', 'app', 'Integration', 3, '1-2 weeks'),
        ('Git', 'app', 'Tools', 2, '3-5 days'),
        # Other
        ('Python', 'other', 'Core', 5, '2-3 weeks'),
        ('Machine Learning', 'other', 'AI/ML', 5, '4-6 weeks'),
        ('Pandas', 'other', 'Data', 3, '1-2 weeks'),
        ('NumPy', 'other', 'Data', 2, '1 week'),
        ('Matplotlib', 'other', 'Visualisation', 2, '1 week'),
        ('MySQL', 'other', 'Database', 2, '1-2 weeks'),
        # AI / ML
        ('Python', 'ai', 'Backend', 3, '2-3 weeks'),
        ('Machine Learning', 'ai', 'AI/ML', 5, '4-6 weeks'),
        ('TensorFlow', 'ai', 'AI/ML', 4, '3-4 weeks'),
        ('OpenCV', 'ai', 'AI/ML', 3, '2-3 weeks'),
        ('Pandas', 'ai', 'Data', 3, '1-2 weeks'),
        ('NumPy', 'ai', 'Data', 2, '1 week'),
        ('Flask', 'ai', 'Backend', 3, '1-2 weeks'),
        ('MySQL', 'ai', 'Database', 2, '1-2 weeks'),
        ('Git', 'ai', 'Tools', 2, '3-5 days'),
        # Data Science
        ('Python', 'datascience', 'Backend', 3, '2-3 weeks'),
        ('Pandas', 'datascience', 'Data', 4, '1-2 weeks'),
        ('NumPy', 'datascience', 'Data', 3, '1 week'),
        ('Matplotlib', 'datascience', 'Visualisation', 3, '1 week'),
        ('scikit-learn', 'datascience', 'AI/ML', 4, '3-4 weeks'),
        ('MySQL', 'datascience', 'Database', 2, '1-2 weeks'),
        ('Flask', 'datascience', 'Backend', 2, '1-2 weeks'),
        ('Git', 'datascience', 'Tools', 2, '3-5 days'),
        # Cyber Security
        ('Python', 'cybersecurity', 'Backend', 3, '2-3 weeks'),
        ('Networking', 'cybersecurity', 'Security', 4, '3-4 weeks'),
        ('Linux', 'cybersecurity', 'Security', 3, '2-3 weeks'),
        ('Cryptography', 'cybersecurity', 'Security', 4, '2-3 weeks'),
        ('MySQL', 'cybersecurity', 'Database', 2, '1-2 weeks'),
        ('Flask', 'cybersecurity', 'Backend', 3, '1-2 weeks'),
        ('Git', 'cybersecurity', 'Tools', 2, '3-5 days'),
        # IoT
        ('Python', 'iot', 'Backend', 3, '2-3 weeks'),
        ('Arduino', 'iot', 'Hardware', 4, '2-3 weeks'),
        ('Raspberry Pi', 'iot', 'Hardware', 4, '2-3 weeks'),
        ('MQTT', 'iot', 'Protocols', 3, '1 week'),
        ('MySQL', 'iot', 'Database', 2, '1-2 weeks'),
        ('Flask', 'iot', 'Backend', 2, '1-2 weeks'),
        ('Git', 'iot', 'Tools', 2, '3-5 days'),
        # Cloud
        ('Python', 'cloud', 'Backend', 3, '2-3 weeks'),
        ('Docker', 'cloud', 'DevOps', 4, '2-3 weeks'),
        ('AWS', 'cloud', 'Cloud', 5, '3-4 weeks'),
        ('Linux', 'cloud', 'DevOps', 3, '1-2 weeks'),
        ('MySQL', 'cloud', 'Database', 2, '1-2 weeks'),
        ('Git', 'cloud', 'Tools', 2, '3-5 days'),
        # ── GAMING (NEW) ──
        ('Python', 'gaming', 'Backend', 3, '2-3 weeks'),
        ('Pygame', 'gaming', 'Game Engine', 4, '2-3 weeks'),
        ('JavaScript', 'gaming', 'Frontend', 4, '2-3 weeks'),
        ('HTML', 'gaming', 'Frontend', 2, '1 week'),
        ('CSS', 'gaming', 'Frontend', 2, '1 week'),
        ('Three.js', 'gaming', 'Graphics', 4, '3-4 weeks'),
        ('WebSocket', 'gaming', 'Networking', 3, '1-2 weeks'),
        ('Flask', 'gaming', 'Backend', 3, '1-2 weeks'),
        ('Git', 'gaming', 'Tools', 2, '3-5 days'),
    ]

    for sname, ptype, cat, weight, etime in skills:
        cur.execute(
            """INSERT INTO skills (skill_name, project_type, category, weight, estimated_time)
               VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
            (sname, ptype, cat, weight, etime)
        )
    conn.commit()
    print(f"[MIGRATE] Inserted {len(skills)} skills.")

    # ── STEP 4: Skill Dependencies ────────────────────────────────────
    print("[MIGRATE] Inserting skill dependencies...")

    deps = [
        ('React', 'HTML'), ('React', 'CSS'), ('React', 'JavaScript'),
        ('Flask', 'Python'), ('MySQL', 'Python'), ('PostgreSQL', 'Python'),
        ('TensorFlow', 'Python'), ('Machine Learning', 'Python'),
        ('Machine Learning', 'NumPy'), ('Machine Learning', 'Pandas'),
        ('OpenCV', 'Python'), ('Matplotlib', 'Python'),
        ('scikit-learn', 'Python'), ('scikit-learn', 'NumPy'), ('scikit-learn', 'Pandas'),
        ('MQTT', 'Python'), ('Docker', 'Linux'), ('AWS', 'Linux'), ('AWS', 'Docker'),
        ('Raspberry Pi', 'Python'), ('Cryptography', 'Python'), ('Networking', 'Linux'),
        ('Kotlin', 'Java'), ('React Native', 'JavaScript'), ('Firebase', 'JavaScript'),
        ('Pygame', 'Python'), ('Three.js', 'JavaScript'), ('WebSocket', 'JavaScript'),
    ]

    for sname, dep in deps:
        cur.execute(
            "INSERT INTO skill_dependencies (skill_name, depends_on) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (sname, dep)
        )
    conn.commit()
    print(f"[MIGRATE] Inserted {len(deps)} dependencies.")

    # ── STEP 5: Learning Resources ────────────────────────────────────
    print("[MIGRATE] Inserting learning resources...")

    resources = [
        ('Python', 'Backend', 'Python Official Tutorial', 'https://docs.python.org/3/tutorial/', 'Beginner'),
        ('Python', 'Backend', 'Real Python - Intermediate Guide', 'https://realpython.com/tutorials/intermediate/', 'Intermediate'),
        ('Python', 'Backend', 'Python Design Patterns', 'https://refactoring.guru/design-patterns/python', 'Advanced'),
        ('MySQL', 'Database', 'MySQL Official Tutorial', 'https://dev.mysql.com/doc/refman/8.0/en/tutorial.html', 'Beginner'),
        ('MySQL', 'Database', 'MySQL Performance Tuning', 'https://dev.mysql.com/doc/refman/8.0/en/optimization.html', 'Intermediate'),
        ('PostgreSQL', 'Database', 'PostgreSQL Official Tutorial', 'https://www.postgresql.org/docs/current/tutorial.html', 'Beginner'),
        ('PostgreSQL', 'Database', 'PostgreSQL Performance', 'https://wiki.postgresql.org/wiki/Performance_Optimization', 'Intermediate'),
        ('React', 'Frontend', 'React Official Tutorial', 'https://react.dev/learn', 'Beginner'),
        ('React', 'Frontend', 'React Hooks Deep Dive', 'https://react.dev/reference/react/hooks', 'Intermediate'),
        ('React', 'Frontend', 'Advanced React Patterns', 'https://www.patterns.dev/react/', 'Advanced'),
        ('Git', 'Tools', 'Git - Getting Started', 'https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control', 'Beginner'),
        ('Git', 'Tools', 'Advanced Git Branching', 'https://learngitbranching.js.org/', 'Intermediate'),
        ('Flask', 'Backend', 'Flask Official Tutorial', 'https://flask.palletsprojects.com/en/3.0.x/tutorial/', 'Beginner'),
        ('Flask', 'Backend', 'Flask REST API Development', 'https://flask-restful.readthedocs.io/en/latest/', 'Intermediate'),
        ('JavaScript', 'Frontend', 'MDN JavaScript Guide', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide', 'Beginner'),
        ('JavaScript', 'Frontend', 'JavaScript.info - Modern Tutorial', 'https://javascript.info/', 'Intermediate'),
        ('JavaScript', 'Frontend', 'You Dont Know JS', 'https://github.com/getify/You-Dont-Know-JS', 'Advanced'),
        ('HTML', 'Frontend', 'MDN HTML Foundations', 'https://developer.mozilla.org/en-US/docs/Learn/HTML', 'Beginner'),
        ('HTML', 'Frontend', 'HTML Semantic Elements Guide', 'https://web.dev/learn/html/', 'Intermediate'),
        ('CSS', 'Frontend', 'CSS Fundamentals', 'https://web.dev/learn/css', 'Beginner'),
        ('CSS', 'Frontend', 'CSS Grid and Flexbox Mastery', 'https://css-tricks.com/snippets/css/complete-guide-grid/', 'Intermediate'),
        ('Java', 'Android', 'Java Official Tutorial', 'https://dev.java/learn/', 'Beginner'),
        ('Java', 'Android', 'Effective Java Practices', 'https://www.baeldung.com/java-tutorial', 'Intermediate'),
        ('Machine Learning', 'AI/ML', 'Scikit-learn Tutorial', 'https://scikit-learn.org/stable/tutorial/', 'Beginner'),
        ('Machine Learning', 'AI/ML', 'Stanford CS229 ML Course', 'https://cs229.stanford.edu/', 'Advanced'),
        ('REST API', 'Integration', 'REST API Tutorial', 'https://restfulapi.net/', 'Beginner'),
        ('REST API', 'Integration', 'API Design Best Practices', 'https://swagger.io/resources/articles/best-practices-in-api-design/', 'Intermediate'),
        ('Docker', 'DevOps', 'Docker Getting Started', 'https://docs.docker.com/get-started/', 'Beginner'),
        ('Docker', 'DevOps', 'Docker Compose Guide', 'https://docs.docker.com/compose/', 'Intermediate'),
        ('Node.js', 'Backend', 'Node.js Official Learn', 'https://nodejs.org/en/learn', 'Beginner'),
        ('Firebase', 'Backend', 'Firebase Documentation', 'https://firebase.google.com/docs', 'Beginner'),
        ('Kotlin', 'Android', 'Kotlin Official Docs', 'https://kotlinlang.org/docs/getting-started.html', 'Beginner'),
        ('Pandas', 'Data', 'Pandas Getting Started', 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/', 'Beginner'),
        ('MongoDB', 'Database', 'MongoDB Official Tutorial', 'https://www.mongodb.com/docs/manual/tutorial/', 'Beginner'),
        ('TensorFlow', 'AI/ML', 'TensorFlow Tutorials', 'https://www.tensorflow.org/tutorials', 'Beginner'),
        ('Pygame', 'Game Engine', 'Pygame Official Docs', 'https://www.pygame.org/docs/', 'Beginner'),
        ('Pygame', 'Game Engine', 'Pygame Game Tutorial', 'https://realpython.com/pygame-a-primer/', 'Intermediate'),
        ('Three.js', 'Graphics', 'Three.js Fundamentals', 'https://threejs.org/manual/#en/fundamentals', 'Beginner'),
        ('Three.js', 'Graphics', 'Three.js Journey Course', 'https://threejs-journey.com/', 'Intermediate'),
    ]

    # Clear and re-insert to avoid duplicates
    cur.execute("DELETE FROM learning_resources")
    for sname, cat, rtitle, rlink, diff in resources:
        cur.execute(
            """INSERT INTO learning_resources (skill_name, category, resource_title, resource_link, difficulty)
               VALUES (%s, %s, %s, %s, %s)""",
            (sname, cat, rtitle, rlink, diff)
        )
    conn.commit()
    print(f"[MIGRATE] Inserted {len(resources)} learning resources.")

    # ── Final report ──────────────────────────────────────────────────
    tables = ['users', 'keywords', 'projects', 'skills', 'skill_dependencies', 'learning_resources', 'user_activity']
    print("\n[MIGRATE] ── FINAL REPORT ──")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        count = cur.fetchone()[0]
        print(f"  {t}: {count} rows")

    cur.close()
    conn.close()
    print("\n[MIGRATE] ✅ Migration complete! Database is fully populated.")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"\n[MIGRATE] ❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
