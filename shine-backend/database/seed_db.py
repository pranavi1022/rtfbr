"""
database/seed_db.py

Auto-seeds the PostgreSQL database on first startup.
Called from app.py at boot time.

Logic:
  1. Check if tables exist and have data
  2. If empty → create tables + insert all seed data
  3. If already populated → skip (idempotent)

This runs in a background thread so it does NOT block Flask startup.
"""

import threading
import os

def _seed():
    """Run the full DB seed. Safe to call repeatedly (uses ON CONFLICT DO NOTHING / DO UPDATE)."""
    print("[SEED] Starting database seed check...")
    try:
        from config import DB_TYPE, DATABASE_URL, DB_CONFIG
        if DB_TYPE != "postgresql":
            print("[SEED] Not PostgreSQL — skipping auto-seed")
            return

        import psycopg2
        conn_str = DATABASE_URL if DATABASE_URL else None
        if not conn_str:
            print("[SEED] No DATABASE_URL — skipping auto-seed")
            return

        conn = psycopg2.connect(conn_str, sslmode="require", connect_timeout=15)
        conn.autocommit = False
        cur = conn.cursor()

        # ── Create tables ────────────────────────────────────────────────
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            SERIAL PRIMARY KEY,
                fullname      VARCHAR(150) NOT NULL,
                username      VARCHAR(80)  NOT NULL UNIQUE,
                email         VARCHAR(150) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id           SERIAL PRIMARY KEY,
                title        VARCHAR(255) NOT NULL,
                description  TEXT         NOT NULL,
                domain       VARCHAR(100) NOT NULL,
                difficulty   VARCHAR(50)  NOT NULL,
                category     VARCHAR(100) NOT NULL,
                technologies TEXT         NOT NULL,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT uq_project_title UNIQUE (title)
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_projects_category   ON projects (LOWER(category))")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_projects_difficulty ON projects (LOWER(difficulty))")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS keywords (
                id       SERIAL PRIMARY KEY,
                keyword  VARCHAR(150) NOT NULL,
                category VARCHAR(100) NOT NULL,
                domain   VARCHAR(100) NOT NULL,
                CONSTRAINT uq_keyword UNIQUE (keyword)
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords (LOWER(keyword))")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id             SERIAL PRIMARY KEY,
                skill_name     VARCHAR(100) NOT NULL,
                project_type   VARCHAR(100) NOT NULL,
                category       VARCHAR(100) NOT NULL,
                weight         INT          DEFAULT 3,
                estimated_time VARCHAR(50)  DEFAULT '1-2 weeks',
                CONSTRAINT uq_skill_type UNIQUE (skill_name, project_type)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS skill_dependencies (
                id         SERIAL PRIMARY KEY,
                skill_name VARCHAR(100) NOT NULL,
                depends_on VARCHAR(100) NOT NULL,
                CONSTRAINT uq_skill_dep UNIQUE (skill_name, depends_on)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS learning_resources (
                id             SERIAL PRIMARY KEY,
                skill_name     VARCHAR(100) NOT NULL,
                resource_title VARCHAR(255) NOT NULL,
                resource_link  TEXT         NOT NULL,
                difficulty     VARCHAR(50)  DEFAULT 'Beginner',
                CONSTRAINT uq_resource UNIQUE (skill_name, resource_title)
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_lr_skill ON learning_resources (LOWER(skill_name))")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_activity (
                id             SERIAL PRIMARY KEY,
                user_id        INT          NOT NULL,
                project_name   VARCHAR(255) NOT NULL,
                level          VARCHAR(50)  DEFAULT '',
                missing_skills INT          DEFAULT 0,
                action         VARCHAR(50)  DEFAULT 'search',
                created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_user_activity_user_id ON user_activity (user_id)")

        conn.commit()
        print("[SEED] Tables created/verified.")

        # ── Check if already seeded ──────────────────────────────────────
        cur.execute("SELECT COUNT(*) FROM projects")
        project_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM keywords")
        keyword_count = cur.fetchone()[0]

        print(f"[SEED] Current counts — projects: {project_count}, keywords: {keyword_count}")

        if project_count >= 50 and keyword_count >= 80:
            print("[SEED] Data already populated — skipping seed insert.")
            cur.close()
            conn.close()
            return

        print("[SEED] Seeding data now...")

        # ── KEYWORDS ─────────────────────────────────────────────────────
        keywords = [
            # Gaming
            ('game',              'game_project',          'Game Development'),
            ('gaming',            'game_project',          'Game Development'),
            ('unity',             'game_project',          'Game Development'),
            ('unreal',            'game_project',          'Game Development'),
            ('pygame',            'game_project',          'Game Development'),
            ('2d game',           'game_project',          'Game Development'),
            ('3d game',           'game_project',          'Game Development'),
            ('multiplayer game',  'game_project',          'Game Development'),
            ('game engine',       'game_project',          'Game Development'),
            ('sprite',            'game_project',          'Game Development'),
            ('arcade game',       'game_project',          'Game Development'),
            ('rpg game',          'game_project',          'Game Development'),
            ('platformer',        'game_project',          'Game Development'),
            ('game development',  'game_project',          'Game Development'),
            # Web
            ('portfolio',         'portfolio',              'Web Development'),
            ('personal website',  'portfolio',              'Web Development'),
            ('resume site',       'portfolio',              'Web Development'),
            ('blog',              'blog',                   'Web Development'),
            ('chat',              'chat_app',               'Web Development'),
            ('messaging app',     'chat_app',               'Web Development'),
            ('real time chat',    'chat_app',               'Web Development'),
            ('ecommerce',         'ecommerce',              'Web Development'),
            ('online shop',       'ecommerce',              'Web Development'),
            ('shopping cart',     'ecommerce',              'Web Development'),
            ('food ordering',     'food_ordering',          'Web Development'),
            ('restaurant app',    'food_ordering',          'Web Development'),
            ('expense tracker',   'expense_tracker',        'Web Development'),
            ('budget app',        'expense_tracker',        'Web Development'),
            ('todo app',          'task_manager',           'Web Development'),
            ('task manager',      'task_manager',           'Web Development'),
            ('kanban',            'task_manager',           'Web Development'),
            ('inventory system',  'inventory_system',       'Web Development'),
            ('stock management',  'inventory_system',       'Web Development'),
            ('employee management','employee_management',   'Web Development'),
            ('hr system',         'employee_management',    'Web Development'),
            ('hotel booking',     'hotel_booking',          'Web Development'),
            ('reservation system','hotel_booking',          'Web Development'),
            ('transport app',     'transport_system',       'Web Development'),
            ('job portal',        'recruitment_system',     'Web Development'),
            ('recruitment',       'recruitment_system',     'Web Development'),
            ('social network',    'social_media',           'Web Development'),
            ('real estate',       'real_estate',            'Web Development'),
            ('weather app',       'weather_app',            'Web Development'),
            # Education
            ('attendance',        'attendance_system',      'Education'),
            ('attendance system', 'attendance_system',      'Education'),
            ('student system',    'attendance_system',      'Education'),
            ('library',           'library_system',         'Education'),
            ('book management',   'library_system',         'Education'),
            ('quiz app',          'quiz_app',               'Education'),
            ('exam portal',       'quiz_app',               'Education'),
            # Medical
            ('hospital',          'hospital_system',        'Medical'),
            ('clinic',            'hospital_system',        'Medical'),
            ('patient management','hospital_system',        'Medical'),
            ('pharmacy',          'hospital_system',        'Medical'),
            ('telemedicine',      'hospital_system',        'Medical'),
            # AI/ML
            ('artificial intelligence','ai_project',        'Artificial Intelligence'),
            ('machine learning',  'ai_project',             'Artificial Intelligence'),
            ('deep learning',     'ai_project',             'Artificial Intelligence'),
            ('neural network',    'ai_project',             'Artificial Intelligence'),
            ('nlp',               'ai_project',             'Artificial Intelligence'),
            ('chatbot',           'ai_project',             'Artificial Intelligence'),
            ('computer vision',   'ai_project',             'Artificial Intelligence'),
            ('image recognition', 'ai_project',             'Artificial Intelligence'),
            ('recommendation system','ai_project',          'Artificial Intelligence'),
            # Data Science
            ('data science',      'data_science_project',   'Data Science'),
            ('data analysis',     'data_science_project',   'Data Science'),
            ('data visualization','data_science_project',   'Data Science'),
            ('analytics dashboard','data_science_project',  'Data Science'),
            ('prediction model',  'data_science_project',   'Data Science'),
            # Cyber Security
            ('cyber security',    'cyber_security_project', 'Cyber Security'),
            ('cybersecurity',     'cyber_security_project', 'Cyber Security'),
            ('encryption',        'cyber_security_project', 'Cyber Security'),
            ('password manager',  'cyber_security_project', 'Cyber Security'),
            ('intrusion detection','cyber_security_project','Cyber Security'),
            # IoT
            ('iot',               'iot_project',            'IoT'),
            ('internet of things','iot_project',            'IoT'),
            ('arduino',           'iot_project',            'IoT'),
            ('raspberry pi',      'iot_project',            'IoT'),
            ('smart home',        'iot_project',            'IoT'),
            ('sensor system',     'iot_project',            'IoT'),
            # Cloud
            ('cloud computing',   'cloud_project',          'Cloud Computing'),
            ('docker',            'cloud_project',          'Cloud Computing'),
            ('kubernetes',        'cloud_project',          'Cloud Computing'),
            ('devops',            'cloud_project',          'Cloud Computing'),
            ('aws deployment',    'cloud_project',          'Cloud Computing'),
            # Mobile
            ('mobile app',        'mobile_app',             'Mobile App Development'),
            ('android app',       'mobile_app',             'Mobile App Development'),
            ('ios app',           'mobile_app',             'Mobile App Development'),
            ('flutter app',       'mobile_app',             'Mobile App Development'),
            ('react native',      'mobile_app',             'Mobile App Development'),
            # Blockchain
            ('blockchain',        'blockchain_project',     'Blockchain'),
            ('cryptocurrency',    'blockchain_project',     'Blockchain'),
            ('smart contract',    'blockchain_project',     'Blockchain'),
            ('nft',               'blockchain_project',     'Blockchain'),
            ('web3',              'blockchain_project',     'Blockchain'),
            # FinTech
            ('fintech',           'fintech_project',        'FinTech'),
            ('banking app',       'fintech_project',        'FinTech'),
            ('payment system',    'fintech_project',        'FinTech'),
            ('investment tracker','fintech_project',        'FinTech'),
            ('digital wallet',    'fintech_project',        'FinTech'),
            # Fitness
            ('fitness app',       'fitness_app',            'Mobile App Development'),
            ('workout tracker',   'fitness_app',            'Mobile App Development'),
            ('gym app',           'fitness_app',            'Mobile App Development'),
            # Agriculture
            ('agriculture',       'agriculture_project',    'IoT'),
            ('smart farming',     'agriculture_project',    'IoT'),
        ]
        cur.executemany(
            """INSERT INTO keywords (keyword, category, domain) VALUES (%s, %s, %s)
               ON CONFLICT (keyword) DO UPDATE SET category=EXCLUDED.category, domain=EXCLUDED.domain""",
            keywords
        )
        conn.commit()
        print(f"[SEED] Keywords inserted: {len(keywords)}")

        # ── PROJECTS ─────────────────────────────────────────────────────
        projects = [
            # Gaming — Beginner
            ('Pygame Snake Game','Classic snake game with Pygame. Arrow key controls, score tracking, and high score stored in DB.','Game Development','Beginner','game_project','Python,Pygame,PostgreSQL'),
            ('Pygame Brick Breaker','Brick breaker with multiple levels, power-ups, and a leaderboard stored in PostgreSQL.','Game Development','Beginner','game_project','Python,Pygame,PostgreSQL'),
            ('Pygame Space Shooter','Side-scrolling space shooter with enemy waves, power-ups, and local high score table.','Game Development','Beginner','game_project','Python,Pygame,PostgreSQL'),
            # Gaming — Intermediate
            ('Multiplayer Tic-Tac-Toe','Real-time 2-player Tic-Tac-Toe over WebSocket. Flask backend handles game rooms; React frontend shows live board.','Game Development','Intermediate','game_project','Python,Flask,WebSocket,JavaScript,React,PostgreSQL'),
            ('2D Platformer Game','Scrolling 2D platformer with multiple levels, enemy AI, collectibles, and a leaderboard.','Game Development','Intermediate','game_project','Python,Pygame,PostgreSQL'),
            ('Multiplayer Quiz Battle','Real-time quiz battle where two players answer questions simultaneously. Fastest correct answer wins.','Game Development','Intermediate','game_project','Python,Flask,WebSocket,JavaScript,React,PostgreSQL'),
            # Gaming — Advanced
            ('3D Browser Game with Three.js','Interactive 3D game in the browser with Three.js physics engine and global leaderboard.','Game Development','Advanced','game_project','JavaScript,Three.js,React,WebSocket,Python,Flask,PostgreSQL'),
            ('AI-Powered Chess Engine','Chess game with AI opponent using minimax + alpha-beta pruning. Difficulty levels and move history.','Game Development','Advanced','game_project','Python,Flask,JavaScript,React,PostgreSQL'),
            ('AI Game Bot with Reinforcement Learning','Train an AI agent to play a game using reinforcement learning. Compare human vs AI on dashboard.','Game Development','Advanced','game_project','Python,TensorFlow,Flask,Pygame,JavaScript,React'),
            # Web — Beginner
            ('Personal Portfolio Website','Clean portfolio site with about, projects, skills, and contact sections. Fully responsive.','Web Development','Beginner','portfolio','HTML,CSS,JavaScript'),
            ('Simple To-Do List','Add, complete, and delete tasks. Data persisted in PostgreSQL. Minimal clean interface.','Web Development','Beginner','task_manager','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Simple Product Catalogue','Browse products by category with admin CRUD panel. Products stored in PostgreSQL.','Web Development','Beginner','ecommerce','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Expense Tracker App','Log income and expenses by category, view monthly summaries and pie charts, export CSV.','Web Development','Beginner','expense_tracker','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Daily Spending Log','Simple form to log daily expenses by category. View monthly totals in a table.','Web Development','Beginner','expense_tracker','HTML,CSS,Python,Flask,PostgreSQL'),
            # Web — Intermediate
            ('Animated Portfolio with Dark Mode','Portfolio with scroll animations, dark/light mode, typewriter effect, and contact form.','Web Development','Intermediate','portfolio','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Team Kanban Board','Kanban board with To-Do, In Progress, Done columns. Drag-and-drop and real-time sync.','Web Development','Intermediate','task_manager','HTML,CSS,JavaScript,Python,Flask,PostgreSQL,WebSocket'),
            ('Shopping Cart App','Product catalogue, add-to-cart, order history, and user authentication with PostgreSQL.','Web Development','Intermediate','ecommerce','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Real-Time Chat App','Real-time messaging using Flask-SocketIO. Private rooms, online status, and message history.','Web Development','Intermediate','chat_app','Python,Flask,WebSocket,JavaScript,PostgreSQL'),
            ('Budget Planning Dashboard','Set monthly budget goals, track spending, get over-budget alerts, and view trend charts.','Web Development','Intermediate','expense_tracker','HTML,CSS,JavaScript,Python,Flask,PostgreSQL,Chart.js'),
            # Web — Advanced
            ('Full-Stack Portfolio CMS','Dynamic portfolio where admin updates skills, projects, and bio from a dashboard.','Web Development','Advanced','portfolio','Python,Flask,PostgreSQL,JavaScript,React,Docker'),
            ('Enterprise Task REST API','RESTful task management API with JWT auth, role-based permissions, webhooks, and rate limiting.','Web Development','Advanced','task_manager','Python,Flask,PostgreSQL,Redis,Docker,REST API,JWT'),
            ('E-Commerce with Payment Gateway','Complete store with Razorpay integration, order tracking emails, and React frontend.','Web Development','Advanced','ecommerce','Python,Flask,PostgreSQL,JavaScript,React,Razorpay'),
            ('Advanced Messaging Platform','Full-featured chat with group rooms, file sharing, search, push notifications, and React frontend.','Web Development','Advanced','chat_app','Python,Flask,WebSocket,JavaScript,React,PostgreSQL,Docker'),
            # Education — Beginner
            ('Student Register App','Web form for teachers to register students and mark daily attendance. Reports in PostgreSQL.','Education','Beginner','attendance_system','HTML,CSS,Python,Flask,PostgreSQL'),
            ('Book Catalogue Browser','Searchable list of library books with title, author, and availability stored in PostgreSQL.','Education','Beginner','library_system','HTML,CSS,Python,Flask,PostgreSQL'),
            ('Database-Driven Quiz','Quiz questions in PostgreSQL. Admin adds questions. Students take quiz and see score.','Education','Beginner','quiz_app','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            # Education — Intermediate
            ('Attendance Portal with Login','Teacher and student login, per-class attendance marking, defaulter list, and PDF export.','Education','Intermediate','attendance_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Library Management with Notifications','Full library system with due-date email reminders, reservation queue, and admin dashboard.','Education','Intermediate','library_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Timed Quiz Application','Countdown timer per question, auto-submit, leaderboard, and user login for history.','Education','Intermediate','quiz_app','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            # Education — Advanced
            ('Face Recognition Attendance','Automated attendance using OpenCV face detection. Face embeddings stored in DB.','Education','Advanced','attendance_system','Python,OpenCV,Flask,PostgreSQL,NumPy,JavaScript'),
            ('Smart Library Recommendation Engine','Recommends books based on borrowing history using collaborative filtering.','Education','Advanced','library_system','Python,Flask,PostgreSQL,scikit-learn,JavaScript,React'),
            ('Adaptive Quiz Engine','Quiz adjusts difficulty based on previous answers. Analytics show student progress.','Education','Advanced','quiz_app','Python,Flask,PostgreSQL,scikit-learn,JavaScript,React'),
            # AI/ML
            ('Sentiment Analyser','Enter text and get positive/negative/neutral sentiment using NLTK. Flask + HTML interface.','Artificial Intelligence','Beginner','ai_project','Python,Flask,NLTK,HTML,CSS'),
            ('Simple Rule-Based Chatbot','FAQ chatbot using keyword matching. Trained on custom Q&A pairs. Flask web app.','Artificial Intelligence','Beginner','ai_project','Python,Flask,HTML,CSS,PostgreSQL'),
            ('Image Classifier Demo','Upload an image; classify with pre-trained CNN. Shows top-3 predictions with confidence.','Artificial Intelligence','Beginner','ai_project','Python,Flask,TensorFlow,HTML,CSS'),
            ('ML Spam Detector','Naive Bayes classifier on SMS data. Web interface checks if a message is spam.','Artificial Intelligence','Intermediate','ai_project','Python,Flask,scikit-learn,Pandas,HTML,CSS,PostgreSQL'),
            ('Movie Recommendation System','Collaborative filtering recommender. Enter movie title, get 5 similar recommendations.','Artificial Intelligence','Intermediate','ai_project','Python,Flask,Pandas,scikit-learn,PostgreSQL,JavaScript'),
            ('Handwriting Recognition App','Draw a digit on canvas; trained CNN predicts instantly. Trained on MNIST dataset.','Artificial Intelligence','Intermediate','ai_project','Python,Flask,TensorFlow,JavaScript,HTML,CSS'),
            ('Real-Time Object Detection','Detect objects in webcam stream using YOLO. Annotated frames streamed via Flask.','Artificial Intelligence','Advanced','ai_project','Python,Flask,OpenCV,YOLO,JavaScript,PostgreSQL'),
            ('NLP Question Answering System','Upload PDF; system answers natural-language questions using a Transformer model.','Artificial Intelligence','Advanced','ai_project','Python,Flask,Transformers,PostgreSQL,JavaScript,React'),
            ('AI Code Review Bot','Analyses Python code for errors, style, and complexity. Returns detailed review.','Artificial Intelligence','Advanced','ai_project','Python,Flask,AST,PostgreSQL,JavaScript,React'),
            # Mobile
            ('Simple Calculator App','Basic calculator for arithmetic with Flutter. Clean material design, cross-platform.','Mobile App Development','Beginner','mobile_app','Flutter,Dart'),
            ('Notes App','Create, edit, delete text notes. Data persisted with SQLite. Material design.','Mobile App Development','Beginner','mobile_app','Flutter,Dart,SQLite'),
            ('Unit Converter App','Convert between length, weight, temperature, and currency units. Offline-capable.','Mobile App Development','Beginner','mobile_app','Flutter,Dart'),
            ('Expense Tracker Mobile App','Log daily expenses by category. Monthly pie charts. Data synced with Firebase.','Mobile App Development','Intermediate','mobile_app','Flutter,Dart,Firebase,Chart.js'),
            ('Movie Browser App','Browse and search movies from TMDB API. Save favourites locally. Smooth animations.','Mobile App Development','Intermediate','mobile_app','Flutter,Dart,REST API,Firebase'),
            ('Fitness Tracker App','Log workouts, track steps, set goals, and visualise progress with charts.','Mobile App Development','Intermediate','mobile_app','Flutter,Dart,Firebase,SQLite'),
            ('Real-Time Chat Mobile App','Cross-platform chat with auth, group chats, push notifications, and media sharing.','Mobile App Development','Advanced','mobile_app','Flutter,Dart,Firebase,FCM,WebSocket'),
            ('Ride Sharing Mobile App','Uber-like app with live driver tracking, fare calculation, OTP, and payment gateway.','Mobile App Development','Advanced','mobile_app','Flutter,Dart,Firebase,Google Maps,REST API,Stripe'),
            ('E-Commerce Mobile App','Full-featured shopping app with catalogue, cart, checkout, and order tracking.','Mobile App Development','Advanced','mobile_app','Flutter,Dart,Firebase,Razorpay,REST API'),
            # Cloud
            ('Dockerised Flask App','Package a Flask app in Docker. Includes Dockerfile and documentation.','Cloud Computing','Beginner','cloud_project','Python,Flask,Docker,PostgreSQL'),
            ('Cloud File Storage App','Upload files to AWS S3 via Flask. Files listed with download links.','Cloud Computing','Beginner','cloud_project','Python,Flask,AWS,PostgreSQL,HTML,CSS'),
            ('Docker Compose Web Stack','Flask + PostgreSQL + Nginx orchestrated with Docker Compose. One-command deployment.','Cloud Computing','Intermediate','cloud_project','Python,Flask,PostgreSQL,Docker,Nginx'),
            ('CI/CD Pipeline with GitHub Actions','Automated test-and-deploy: push triggers tests, builds Docker image, deploys to EC2.','Cloud Computing','Intermediate','cloud_project','Python,Flask,Docker,AWS,GitHub Actions'),
            ('Kubernetes Microservices App','Decompose monolith into 3 microservices on Kubernetes. Helm charts and auto-scaling.','Cloud Computing','Advanced','cloud_project','Python,Flask,Docker,Kubernetes,PostgreSQL,Helm,GitHub Actions'),
            ('Multi-Region Disaster Recovery','Flask app across two AWS regions. Route 53 health checks auto-failover on outage.','Cloud Computing','Advanced','cloud_project','Python,Flask,AWS,Docker,PostgreSQL,Terraform'),
            # IoT
            ('Temperature Monitor Dashboard','DHT11 sensor reads temperature; Raspberry Pi sends to Flask. Dashboard shows live readings.','IoT','Beginner','iot_project','Python,Flask,Raspberry Pi,PostgreSQL,HTML,CSS'),
            ('Smart Home Dashboard','Control GPIO pins (lights, fans) from a web dashboard. State persisted in PostgreSQL.','IoT','Intermediate','iot_project','Python,Flask,Raspberry Pi,PostgreSQL,JavaScript,HTML,CSS'),
            ('Smart Energy Monitor','Current sensors measure appliance power. Real-time dashboard shows usage and cost.','IoT','Advanced','iot_project','Python,Flask,MQTT,PostgreSQL,Raspberry Pi,React,Chart.js,Docker'),
            # Cyber Security
            ('Password Strength Checker','Enter a password and get strength score (Weak/Fair/Strong) with improvement tips.','Cyber Security','Beginner','cyber_security_project','Python,Flask,HTML,CSS,JavaScript'),
            ('Caesar Cipher Tool','Encrypt and decrypt messages with Caesar cipher. User selects shift value.','Cyber Security','Beginner','cyber_security_project','Python,Flask,HTML,CSS,JavaScript'),
            ('Secure Password Manager','Store encrypted passwords in PostgreSQL. Master password decrypts vault locally.','Cyber Security','Intermediate','cyber_security_project','Python,Flask,PostgreSQL,Cryptography,HTML,JavaScript'),
            ('Phishing URL Detector','ML model classifies URLs as phishing or legitimate based on lexical features.','Cyber Security','Intermediate','cyber_security_project','Python,Flask,scikit-learn,Pandas,PostgreSQL,HTML,CSS'),
            ('Intrusion Detection System','Monitor network traffic, detect anomalous patterns with ML, trigger alerts.','Cyber Security','Advanced','cyber_security_project','Python,Flask,scikit-learn,Scapy,PostgreSQL,React,Docker'),
            ('Web Vulnerability Scanner','Automated scanner checks for SQLi, XSS, CSRF, open redirects, and missing headers.','Cyber Security','Advanced','cyber_security_project','Python,Flask,PostgreSQL,JavaScript,React,Docker'),
            # Data Science
            ('CSV Data Explorer','Upload CSV; see column statistics, data types, and preview table with Pandas.','Data Science','Beginner','data_science_project','Python,Flask,Pandas,HTML,CSS'),
            ('Student Grade Analyser','Enter marks; calculate mean, median, pass/fail rate, and grade distribution chart.','Data Science','Beginner','data_science_project','Python,Flask,Pandas,Matplotlib,PostgreSQL,HTML,CSS'),
            ('Sales Trend Dashboard','Upload CSV; dashboard shows trend lines, top products, and seasonal patterns.','Data Science','Intermediate','data_science_project','Python,Flask,Pandas,Plotly,PostgreSQL,HTML,JavaScript'),
            ('Housing Price Predictor','Linear regression predicts house price from area, rooms, and location features.','Data Science','Intermediate','data_science_project','Python,Flask,scikit-learn,Pandas,PostgreSQL,HTML,CSS'),
            ('Customer Churn Predictor','Random Forest on telecom data predicts customer churn. Dashboard shows feature importance.','Data Science','Advanced','data_science_project','Python,Flask,scikit-learn,Pandas,React,PostgreSQL,Docker'),
            ('Financial Fraud Detection','Anomaly detection on transactions using Isolation Forest. Real-time alert dashboard.','Data Science','Advanced','data_science_project','Python,Flask,scikit-learn,TensorFlow,Pandas,PostgreSQL,React'),
            # Medical
            ('Patient Registration Form','Register patients with name, age, ailment. Records in PostgreSQL; admin views list.','Medical','Beginner','hospital_system','HTML,CSS,Python,Flask,PostgreSQL'),
            ('Doctor Schedule Viewer','View available doctor slots for the week. Admin manages availability.','Medical','Beginner','hospital_system','HTML,CSS,Python,Flask,PostgreSQL'),
            ('Clinic Appointment Manager','Online appointment booking with doctor selection, slot picker, and confirmation email.','Medical','Intermediate','hospital_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Hospital Patient Portal','Patients view medical history, book appointments, and download prescriptions.','Medical','Intermediate','hospital_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Telemedicine Platform','Video consultation platform with patient-doctor chat and payment gateway.','Medical','Advanced','hospital_system','Python,Flask,PostgreSQL,JavaScript,React,WebRTC'),
            ('Hospital ERP System','End-to-end hospital ERP: patient management, billing, payroll, inventory, and analytics.','Medical','Advanced','hospital_system','Python,Flask,PostgreSQL,JavaScript,React,Docker'),
            # Blockchain
            ('Simple Blockchain Simulator','Build a basic blockchain in Python. Demonstrates hashing, blocks, and proof-of-work.','Blockchain','Beginner','blockchain_project','Python,Flask,HTML,CSS'),
            ('Cryptocurrency Price Tracker','Fetch live crypto prices from CoinGecko API and display with price change indicators.','Blockchain','Beginner','blockchain_project','Python,Flask,HTML,CSS,JavaScript'),
            ('Decentralised Voting App','Blockchain-based voting with smart contracts ensuring tamper-proof votes.','Blockchain','Intermediate','blockchain_project','Solidity,Python,JavaScript,React,Web3.js,Hardhat'),
            ('NFT Marketplace UI','Browse and list NFTs. Connects to MetaMask wallet. Displays IPFS-hosted artwork.','Blockchain','Intermediate','blockchain_project','JavaScript,React,Web3.js,IPFS,Solidity'),
            ('DeFi Lending Protocol','Decentralised lending/borrowing protocol. Smart contracts handle collateral and interest.','Blockchain','Advanced','blockchain_project','Solidity,Hardhat,JavaScript,React,Web3.js,The Graph'),
            ('Supply Chain Tracker on Blockchain','Track product provenance on blockchain from manufacturer to consumer.','Blockchain','Advanced','blockchain_project','Solidity,Python,Flask,React,Web3.js,IPFS,PostgreSQL'),
            # FinTech
            ('EMI Calculator','Calculate loan EMI with amortisation schedule. Input loan amount and interest rate.','FinTech','Beginner','fintech_project','HTML,CSS,JavaScript,Python,Flask'),
            ('Personal Finance Dashboard','Track income, expenses, and savings goals. Visual summary with pie charts.','FinTech','Beginner','fintech_project','HTML,CSS,JavaScript,Python,PostgreSQL'),
            ('Digital Wallet App','Send and receive money between users. Transaction history and QR code payments.','FinTech','Intermediate','fintech_project','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),
            ('Investment Portfolio Tracker','Track stocks, mutual funds, and crypto. Calculates returns and P&L.','FinTech','Intermediate','fintech_project','HTML,CSS,JavaScript,Python,Flask,PostgreSQL,REST API'),
            ('Algorithmic Trading Platform','Backtesting for trading strategies. Live paper trading via broker API with analytics.','FinTech','Advanced','fintech_project','Python,Flask,Pandas,NumPy,React,PostgreSQL,Redis,Docker'),
            ('Credit Scoring Engine','ML model predicts creditworthiness. Explainable AI dashboard shows key factors.','FinTech','Advanced','fintech_project','Python,Flask,scikit-learn,Pandas,React,PostgreSQL,Docker'),
            # Fitness
            ('BMI Calculator App','Calculate BMI, display health category, and provide personalised diet tips.','Mobile App Development','Beginner','fitness_app','HTML,CSS,JavaScript,Python,Flask'),
            ('Workout Logger','Log workouts by type, duration, and calories burned. View history and weekly summaries.','Mobile App Development','Intermediate','fitness_app','Flutter,Dart,Firebase,SQLite'),
            ('AI Fitness Coach App','ML model analyses workout history to suggest personalised training plans.','Mobile App Development','Advanced','fitness_app','Flutter,Dart,Firebase,Python,Flask,scikit-learn,REST API'),
        ]
        cur.executemany(
            """INSERT INTO projects (title, description, domain, difficulty, category, technologies)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (title) DO UPDATE
               SET description=EXCLUDED.description, domain=EXCLUDED.domain,
                   difficulty=EXCLUDED.difficulty, category=EXCLUDED.category,
                   technologies=EXCLUDED.technologies""",
            projects
        )
        conn.commit()
        print(f"[SEED] Projects inserted: {len(projects)}")

        # ── SKILLS ───────────────────────────────────────────────────────
        skills = [
            ('HTML',            'website', 'Frontend',       2, '1 week'),
            ('CSS',             'website', 'Frontend',       2, '1 week'),
            ('JavaScript',      'website', 'Frontend',       4, '2-3 weeks'),
            ('React',           'website', 'Frontend',       3, '3-4 weeks'),
            ('Python',          'website', 'Backend',        4, '2-3 weeks'),
            ('Flask',           'website', 'Backend',        3, '1-2 weeks'),
            ('PostgreSQL',      'website', 'Database',       3, '1-2 weeks'),
            ('Java',            'app',     'Android',        4, '4-6 weeks'),
            ('Kotlin',          'app',     'Android',        4, '3-4 weeks'),
            ('React Native',    'app',     'Cross-Platform', 4, '3-4 weeks'),
            ('Flutter',         'app',     'Cross-Platform', 4, '3-4 weeks'),
            ('Firebase',        'app',     'Backend',        3, '1-2 weeks'),
            ('REST API',        'app',     'Integration',    3, '1-2 weeks'),
            ('Python',          'other',   'Core',           5, '2-3 weeks'),
            ('Machine Learning','other',   'AI/ML',          5, '4-6 weeks'),
            ('Pandas',          'other',   'Data',           3, '1-2 weeks'),
            ('NumPy',           'other',   'Data',           2, '1 week'),
            ('Matplotlib',      'other',   'Visualization',  2, '1 week'),
            ('PostgreSQL',      'other',   'Database',       2, '1-2 weeks'),
            ('scikit-learn',    'other',   'AI/ML',          4, '2-3 weeks'),
            ('Python',          'gaming',  'Backend',        3, '2-3 weeks'),
            ('Pygame',          'gaming',  'Game Engine',    4, '2-3 weeks'),
            ('JavaScript',      'gaming',  'Frontend',       4, '2-3 weeks'),
            ('Three.js',        'gaming',  'Game Engine',    4, '3-4 weeks'),
            ('WebSocket',       'gaming',  'Networking',     3, '1-2 weeks'),
            ('HTML',            'gaming',  'Frontend',       2, '1 week'),
            ('CSS',             'gaming',  'Frontend',       2, '1 week'),
        ]
        cur.executemany(
            """INSERT INTO skills (skill_name, project_type, category, weight, estimated_time)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (skill_name, project_type) DO UPDATE
               SET category=EXCLUDED.category, weight=EXCLUDED.weight,
                   estimated_time=EXCLUDED.estimated_time""",
            skills
        )
        conn.commit()
        print(f"[SEED] Skills inserted: {len(skills)}")

        # ── SKILL DEPENDENCIES ───────────────────────────────────────────
        deps = [
            ('React',       'JavaScript'), ('React',       'HTML'),
            ('React',       'CSS'),        ('Flask',        'Python'),
            ('PostgreSQL',  'Python'),     ('React Native', 'JavaScript'),
            ('Firebase',    'JavaScript'), ('Kotlin',       'Java'),
            ('Three.js',    'JavaScript'), ('Pygame',       'Python'),
            ('WebSocket',   'JavaScript'), ('scikit-learn', 'Python'),
            ('scikit-learn','Pandas'),     ('Pandas',       'Python'),
        ]
        cur.executemany(
            """INSERT INTO skill_dependencies (skill_name, depends_on) VALUES (%s, %s)
               ON CONFLICT (skill_name, depends_on) DO NOTHING""",
            deps
        )
        conn.commit()
        print(f"[SEED] Skill dependencies inserted: {len(deps)}")

        # ── LEARNING RESOURCES ───────────────────────────────────────────
        resources = [
            ('HTML',            'HTML Foundations',              'https://developer.mozilla.org/en-US/docs/Learn/HTML',                  'Beginner'),
            ('HTML',            'HTML Full Course (freeCodeCamp)','https://www.freecodecamp.org/learn/2022/responsive-web-design/',      'Beginner'),
            ('CSS',             'CSS Fundamentals',              'https://web.dev/learn/css',                                            'Beginner'),
            ('CSS',             'CSS Tricks Complete Guide',     'https://css-tricks.com/guides/',                                       'Intermediate'),
            ('JavaScript',      'JavaScript Guide (MDN)',        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',        'Beginner'),
            ('JavaScript',      'JavaScript.info',               'https://javascript.info/',                                             'Intermediate'),
            ('React',           'React Official Docs',           'https://react.dev/learn',                                             'Intermediate'),
            ('React',           'React Full Course (Scrimba)',   'https://scrimba.com/learn/learnreact',                                 'Intermediate'),
            ('Python',          'Python Official Tutorial',      'https://docs.python.org/3/tutorial/',                                  'Beginner'),
            ('Python',          'Python for Beginners',         'https://www.youtube.com/watch?v=rfscVS0vtbw',                          'Beginner'),
            ('Flask',           'Flask Official Tutorial',       'https://flask.palletsprojects.com/en/3.0.x/tutorial/',                 'Intermediate'),
            ('Flask',           'Flask Mega-Tutorial',           'https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world','Intermediate'),
            ('PostgreSQL',      'PostgreSQL Tutorial',           'https://www.postgresqltutorial.com/',                                  'Beginner'),
            ('PostgreSQL',      'PostgreSQL Docs',               'https://www.postgresql.org/docs/current/',                             'Intermediate'),
            ('MySQL',           'MySQL Tutorial',                'https://dev.mysql.com/doc/refman/8.0/en/tutorial.html',                'Beginner'),
            ('Node.js',         'Node.js Docs',                 'https://nodejs.org/en/learn',                                          'Intermediate'),
            ('MongoDB',         'MongoDB University',            'https://learn.mongodb.com/',                                           'Beginner'),
            ('Firebase',        'Firebase Docs',                 'https://firebase.google.com/docs',                                     'Beginner'),
            ('Java',            'Java Programming',             'https://dev.java/learn/',                                              'Beginner'),
            ('Kotlin',          'Kotlin for Android',            'https://kotlinlang.org/docs/getting-started.html',                    'Intermediate'),
            ('Flutter',         'Flutter Official Docs',         'https://docs.flutter.dev/get-started/codelab',                        'Beginner'),
            ('Flutter',         'Flutter Tutorial (freeCodeCamp)','https://www.youtube.com/watch?v=VPvVD8t02U8',                        'Beginner'),
            ('React Native',    'React Native Docs',             'https://reactnative.dev/docs/getting-started',                        'Intermediate'),
            ('Machine Learning','ML Crash Course (Google)',      'https://developers.google.com/machine-learning/crash-course',         'Beginner'),
            ('Machine Learning','Scikit-learn Tutorial',         'https://scikit-learn.org/stable/tutorial/',                           'Intermediate'),
            ('Pandas',          'Pandas User Guide',             'https://pandas.pydata.org/docs/user_guide/index.html',                'Beginner'),
            ('Pandas',          'Pandas Tutorial (Kaggle)',      'https://www.kaggle.com/learn/pandas',                                 'Beginner'),
            ('NumPy',           'NumPy Quickstart',              'https://numpy.org/doc/stable/user/quickstart.html',                   'Beginner'),
            ('Matplotlib',      'Matplotlib Tutorials',          'https://matplotlib.org/stable/tutorials/index.html',                  'Beginner'),
            ('scikit-learn',    'Scikit-learn User Guide',       'https://scikit-learn.org/stable/user_guide.html',                    'Intermediate'),
            ('TensorFlow',      'TensorFlow Tutorials',          'https://www.tensorflow.org/tutorials',                                'Intermediate'),
            ('Pygame',          'Pygame Documentation',          'https://www.pygame.org/docs/',                                        'Beginner'),
            ('Pygame',          'Pygame Beginners Guide',        'https://realpython.com/pygame-a-primer/',                             'Beginner'),
            ('Three.js',        'Three.js Manual',               'https://threejs.org/manual/#en/fundamentals',                         'Intermediate'),
            ('WebSocket',       'WebSocket API (MDN)',            'https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API',    'Intermediate'),
            ('Docker',          'Docker Get Started',             'https://docs.docker.com/get-started/',                               'Beginner'),
            ('Docker',          'Docker Tutorial (freeCodeCamp)', 'https://www.youtube.com/watch?v=fqMOX6JJhGo',                       'Beginner'),
            ('Git',             'Git Book',                       'https://git-scm.com/book/en/v2',                                    'Beginner'),
            ('REST API',        'REST API Design Guide',          'https://restfulapi.net/',                                            'Intermediate'),
            ('OpenCV',          'OpenCV Python Tutorials',        'https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html',          'Intermediate'),
            ('AWS',             'AWS Getting Started',            'https://aws.amazon.com/getting-started/',                            'Intermediate'),
            ('Kubernetes',      'Kubernetes Docs',                'https://kubernetes.io/docs/tutorials/',                              'Advanced'),
        ]
        cur.executemany(
            """INSERT INTO learning_resources (skill_name, resource_title, resource_link, difficulty)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (skill_name, resource_title) DO UPDATE
               SET resource_link=EXCLUDED.resource_link, difficulty=EXCLUDED.difficulty""",
            resources
        )
        conn.commit()
        print(f"[SEED] Learning resources inserted: {len(resources)}")

        # ── Final verification ───────────────────────────────────────────
        for tbl in ('projects', 'keywords', 'skills', 'skill_dependencies', 'learning_resources'):
            cur.execute(f"SELECT COUNT(*) FROM {tbl}")
            count = cur.fetchone()[0]
            print(f"[SEED]   {tbl:30s} → {count} rows")

        cur.close()
        conn.close()
        print("[SEED] Database seeding COMPLETE.")

    except Exception as e:
        print(f"[SEED] ERROR during seeding: {e}")
        import traceback
        traceback.print_exc()


def seed_in_background():
    """Spawn the seed in a daemon thread so Flask startup isn't blocked."""
    t = threading.Thread(target=_seed, daemon=True)
    t.start()
    print("[SEED] Seed thread launched in background.")
