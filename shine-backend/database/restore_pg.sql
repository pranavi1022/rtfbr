-- ============================================================
-- SHINE Access Point — PostgreSQL Restoration Script
-- Run this on your Render PostgreSQL database
-- ============================================================

-- ── Drop tables in dependency order ──────────────────────────
DROP TABLE IF EXISTS user_activity CASCADE;
DROP TABLE IF EXISTS learning_resources CASCADE;
DROP TABLE IF EXISTS skill_dependencies CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS keywords CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ── USERS ─────────────────────────────────────────────────────
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    fullname      VARCHAR(150) NOT NULL,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    email         VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── PROJECTS ──────────────────────────────────────────────────
CREATE TABLE projects (
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(255) NOT NULL,
    description  TEXT         NOT NULL,
    domain       VARCHAR(100) NOT NULL,
    difficulty   VARCHAR(50)  NOT NULL,
    category     VARCHAR(100) NOT NULL,
    technologies TEXT         NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_project_title UNIQUE (title)
);
CREATE INDEX idx_projects_category   ON projects (LOWER(category));
CREATE INDEX idx_projects_difficulty ON projects (LOWER(difficulty));

-- ── KEYWORDS ──────────────────────────────────────────────────
CREATE TABLE keywords (
    id       SERIAL PRIMARY KEY,
    keyword  VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    domain   VARCHAR(100) NOT NULL,
    CONSTRAINT uq_keyword UNIQUE (keyword)
);
CREATE INDEX idx_keywords_keyword ON keywords (LOWER(keyword));

-- ── SKILLS ────────────────────────────────────────────────────
CREATE TABLE skills (
    id             SERIAL PRIMARY KEY,
    skill_name     VARCHAR(100) NOT NULL,
    project_type   VARCHAR(100) NOT NULL,
    category       VARCHAR(100) NOT NULL,
    weight         INT          DEFAULT 3,
    estimated_time VARCHAR(50)  DEFAULT '1-2 weeks',
    CONSTRAINT uq_skill_type UNIQUE (skill_name, project_type)
);

-- ── SKILL DEPENDENCIES ────────────────────────────────────────
CREATE TABLE skill_dependencies (
    id         SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL,
    depends_on VARCHAR(100) NOT NULL,
    CONSTRAINT uq_skill_dep UNIQUE (skill_name, depends_on)
);

-- ── LEARNING RESOURCES ────────────────────────────────────────
CREATE TABLE learning_resources (
    id             SERIAL PRIMARY KEY,
    skill_name     VARCHAR(100) NOT NULL,
    resource_title VARCHAR(255) NOT NULL,
    resource_link  TEXT         NOT NULL,
    difficulty     VARCHAR(50)  DEFAULT 'Beginner',
    CONSTRAINT uq_resource UNIQUE (skill_name, resource_title)
);
CREATE INDEX idx_lr_skill ON learning_resources (LOWER(skill_name));

-- ── USER ACTIVITY ─────────────────────────────────────────────
CREATE TABLE user_activity (
    id             SERIAL PRIMARY KEY,
    user_id        INT          NOT NULL,
    project_name   VARCHAR(255) NOT NULL,
    level          VARCHAR(50)  DEFAULT '',
    missing_skills INT          DEFAULT 0,
    action         VARCHAR(50)  DEFAULT 'search',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_user_activity_user_id ON user_activity (user_id);


-- ============================================================
-- KEYWORDS DATA
-- ============================================================
INSERT INTO keywords (keyword, category, domain) VALUES
-- Gaming / Game Development
('game',              'game_project',         'Game Development'),
('gaming',            'game_project',         'Game Development'),
('unity',             'game_project',         'Game Development'),
('unreal',            'game_project',         'Game Development'),
('pygame',            'game_project',         'Game Development'),
('2d game',           'game_project',         'Game Development'),
('3d game',           'game_project',         'Game Development'),
('multiplayer game',  'game_project',         'Game Development'),
('game engine',       'game_project',         'Game Development'),
('sprite',            'game_project',         'Game Development'),
('arcade game',       'game_project',         'Game Development'),
('rpg game',          'game_project',         'Game Development'),
('platformer game',   'game_project',         'Game Development'),
-- Web Development
('portfolio',         'portfolio',             'Web Development'),
('personal website',  'portfolio',             'Web Development'),
('resume site',       'portfolio',             'Web Development'),
('blog',              'blog',                  'Web Development'),
('article',           'blog',                  'Web Development'),
('news website',      'blog',                  'Web Development'),
('chat',              'chat_app',              'Web Development'),
('messaging app',     'chat_app',              'Web Development'),
('real time chat',    'chat_app',              'Web Development'),
('ecommerce',         'ecommerce',             'Web Development'),
('online shop',       'ecommerce',             'Web Development'),
('shopping cart',     'ecommerce',             'Web Development'),
('food ordering',     'food_ordering',         'Web Development'),
('restaurant app',    'food_ordering',         'Web Development'),
('expense tracker',   'expense_tracker',       'Web Development'),
('budget app',        'expense_tracker',       'Web Development'),
('todo app',          'task_manager',          'Web Development'),
('task manager',      'task_manager',          'Web Development'),
('kanban',            'task_manager',          'Web Development'),
('inventory system',  'inventory_system',      'Web Development'),
('stock management',  'inventory_system',      'Web Development'),
('employee management','employee_management',  'Web Development'),
('hr system',         'employee_management',   'Web Development'),
('hotel booking',     'hotel_booking',         'Web Development'),
('reservation system','hotel_booking',         'Web Development'),
('transport app',     'transport_system',      'Web Development'),
('ride sharing',      'transport_system',      'Web Development'),
('job portal',        'recruitment_system',    'Web Development'),
('recruitment',       'recruitment_system',    'Web Development'),
('social network',    'social_media',          'Web Development'),
('social media app',  'social_media',          'Web Development'),
('real estate',       'real_estate',           'Web Development'),
('property listing',  'real_estate',           'Web Development'),
('weather app',       'weather_app',           'Web Development'),
-- Education
('attendance',        'attendance_system',     'Education'),
('attendance system', 'attendance_system',     'Education'),
('student system',    'attendance_system',     'Education'),
('library',           'library_system',        'Education'),
('book management',   'library_system',        'Education'),
('quiz app',          'quiz_app',              'Education'),
('exam portal',       'quiz_app',              'Education'),
-- Medical
('hospital',          'hospital_system',       'Medical'),
('clinic',            'hospital_system',       'Medical'),
('patient management','hospital_system',       'Medical'),
('pharmacy',          'hospital_system',       'Medical'),
('telemedicine',      'hospital_system',       'Medical'),
-- AI / ML
('artificial intelligence','ai_project',       'Artificial Intelligence'),
('machine learning',  'ai_project',            'Artificial Intelligence'),
('deep learning',     'ai_project',            'Artificial Intelligence'),
('neural network',    'ai_project',            'Artificial Intelligence'),
('nlp',               'ai_project',            'Artificial Intelligence'),
('chatbot',           'ai_project',            'Artificial Intelligence'),
('computer vision',   'ai_project',            'Artificial Intelligence'),
('image recognition', 'ai_project',            'Artificial Intelligence'),
('recommendation system','ai_project',         'Artificial Intelligence'),
-- Data Science
('data science',      'data_science_project',  'Data Science'),
('data analysis',     'data_science_project',  'Data Science'),
('data visualization','data_science_project',  'Data Science'),
('analytics dashboard','data_science_project', 'Data Science'),
('prediction model',  'data_science_project',  'Data Science'),
-- Cyber Security
('cyber security',    'cyber_security_project','Cyber Security'),
('cybersecurity',     'cyber_security_project','Cyber Security'),
('encryption',        'cyber_security_project','Cyber Security'),
('password manager',  'cyber_security_project','Cyber Security'),
('intrusion detection','cyber_security_project','Cyber Security'),
-- IoT
('iot',               'iot_project',           'IoT'),
('internet of things','iot_project',           'IoT'),
('arduino',           'iot_project',           'IoT'),
('raspberry pi',      'iot_project',           'IoT'),
('smart home',        'iot_project',           'IoT'),
('sensor system',     'iot_project',           'IoT'),
-- Cloud
('cloud computing',   'cloud_project',         'Cloud Computing'),
('docker',            'cloud_project',         'Cloud Computing'),
('kubernetes',        'cloud_project',         'Cloud Computing'),
('devops',            'cloud_project',         'Cloud Computing'),
('aws deployment',    'cloud_project',         'Cloud Computing'),
('ci cd pipeline',    'cloud_project',         'Cloud Computing'),
-- Mobile
('mobile app',        'mobile_app',            'Mobile App Development'),
('android app',       'mobile_app',            'Mobile App Development'),
('ios app',           'mobile_app',            'Mobile App Development'),
('flutter app',       'mobile_app',            'Mobile App Development'),
('react native',      'mobile_app',            'Mobile App Development'),
-- Blockchain
('blockchain',        'blockchain_project',    'Blockchain'),
('cryptocurrency',    'blockchain_project',    'Blockchain'),
('smart contract',    'blockchain_project',    'Blockchain'),
('nft',               'blockchain_project',    'Blockchain'),
('web3',              'blockchain_project',    'Blockchain'),
-- FinTech
('fintech',           'fintech_project',       'FinTech'),
('banking app',       'fintech_project',       'FinTech'),
('payment system',    'fintech_project',       'FinTech'),
('investment tracker','fintech_project',       'FinTech'),
('digital wallet',    'fintech_project',       'FinTech'),
-- Fitness
('fitness app',       'fitness_app',           'Mobile App Development'),
('workout tracker',   'fitness_app',           'Mobile App Development'),
('gym app',           'fitness_app',           'Mobile App Development'),
-- Agriculture
('agriculture',       'agriculture_project',   'IoT'),
('smart farming',     'agriculture_project',   'IoT'),
('crop monitoring',   'agriculture_project',   'IoT')
ON CONFLICT (keyword) DO UPDATE
  SET category = EXCLUDED.category,
      domain   = EXCLUDED.domain;


-- ============================================================
-- PROJECTS DATA
-- ============================================================

-- ── Game Development ─────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Pygame Snake Game',
 'Classic snake game built with Pygame. Arrow key controls, score tracking, increasing speed, and high score stored locally.',
 'Game Development','Beginner','game_project','Python,Pygame,MySQL'),

('Pygame Brick Breaker',
 'Brick breaker game with multiple levels, power-ups, and a high score leaderboard stored in MySQL.',
 'Game Development','Beginner','game_project','Python,Pygame'),

('Pygame Space Shooter',
 'Side-scrolling space shooter with enemy waves, power-ups, background music, and local high score table.',
 'Game Development','Beginner','game_project','Python,Pygame,MySQL'),

('Multiplayer Tic-Tac-Toe (WebSocket)',
 'Real-time 2-player Tic-Tac-Toe over WebSocket. Flask backend handles game rooms; React frontend shows live board.',
 'Game Development','Intermediate','game_project','Python,Flask,WebSocket,JavaScript,React,MySQL'),

('2D Platformer Game',
 'Scrolling 2D platformer with multiple levels, enemy AI, collectibles, and a persistent leaderboard.',
 'Game Development','Intermediate','game_project','Python,Pygame,MySQL'),

('Multiplayer Quiz Battle',
 'Real-time quiz battle where two players answer questions simultaneously. Fastest correct answer wins the round.',
 'Game Development','Intermediate','game_project','Python,Flask,WebSocket,JavaScript,React,MySQL'),

('3D Browser Game with Three.js',
 'Interactive 3D game running in the browser using Three.js. Physics engine, animated characters, and global leaderboard.',
 'Game Development','Advanced','game_project','JavaScript,Three.js,React,WebSocket,Python,Flask,MySQL'),

('AI-Powered Chess Engine',
 'Chess game with an AI opponent using minimax + alpha-beta pruning. Difficulty levels and move history display.',
 'Game Development','Advanced','game_project','Python,Flask,JavaScript,React,MySQL'),

('Unity-Style RPG Demo',
 'Top-down RPG prototype with tile maps, NPC dialogue, inventory system, and save/load using MySQL.',
 'Game Development','Advanced','game_project','Python,Pygame,MySQL,JavaScript')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Web Development ────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Personal Portfolio Website',
 'A clean portfolio site with about, projects, skills, and contact sections. Fully responsive and deployed on GitHub Pages.',
 'Web Development','Beginner','portfolio','HTML,CSS,JavaScript'),

('Animated Portfolio with Dark Mode',
 'Portfolio with smooth scroll animations, dark/light mode toggle, typewriter effect, and a contact form backed by Flask.',
 'Web Development','Intermediate','portfolio','HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Full-Stack Portfolio CMS',
 'Dynamic portfolio where admin updates skills, projects, and bio from a dashboard. Visitors see the live site.',
 'Web Development','Advanced','portfolio','Python,Flask,MySQL,JavaScript,React,Docker'),

('Simple To-Do List',
 'Add, complete, and delete tasks. Data persisted in PostgreSQL. Minimal clean interface.',
 'Web Development','Beginner','task_manager','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Team Kanban Board',
 'Kanban board with To-Do, In Progress, and Done columns. Drag-and-drop tasks, user assignment, and real-time sync.',
 'Web Development','Intermediate','task_manager','HTML,CSS,JavaScript,Python,Flask,MySQL,WebSocket'),

('Enterprise Task REST API',
 'Fully RESTful task management API with JWT auth, role-based permissions, webhooks, and rate limiting.',
 'Web Development','Advanced','task_manager','Python,Flask,PostgreSQL,Redis,Docker,REST API,JWT'),

('Shopping Cart App',
 'Product catalogue with PostgreSQL backend, add-to-cart, order history, and user authentication.',
 'Web Development','Intermediate','ecommerce','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('E-Commerce with Payment Gateway',
 'Complete store with Razorpay integration, order tracking emails, inventory, and React frontend.',
 'Web Development','Advanced','ecommerce','Python,Flask,PostgreSQL,JavaScript,React,Razorpay'),

('Simple Product Catalogue',
 'Browse products by category with admin CRUD panel. Product images, prices, descriptions stored in PostgreSQL.',
 'Web Development','Beginner','ecommerce','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Expense Tracker App',
 'Log income and expenses by category, view monthly summaries and pie charts, export CSV reports.',
 'Web Development','Beginner','expense_tracker','HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Budget Planning Dashboard',
 'Set monthly budget goals per category, track real spending, get over-budget alerts, and view trend charts.',
 'Web Development','Intermediate','expense_tracker','HTML,CSS,JavaScript,Python,Flask,MySQL,Chart.js'),

('Real-Time Chat App',
 'Real-time messaging using Flask-SocketIO. Private rooms, online status, read receipts, and message history.',
 'Web Development','Intermediate','chat_app','Python,Flask,WebSocket,JavaScript,MySQL'),

('Advanced Messaging Platform',
 'Full-featured chat platform with group rooms, file sharing, message search, push notifications, and React frontend.',
 'Web Development','Advanced','chat_app','Python,Flask,WebSocket,JavaScript,React,MySQL,Docker')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Education ─────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Student Register App',
 'Web form for teachers to register students and mark daily attendance. Reports are saved in PostgreSQL.',
 'Education','Beginner','attendance_system','HTML,CSS,Python,Flask,PostgreSQL'),

('Attendance Portal with Login',
 'Teacher and student login, per-class attendance marking, defaulter list generation, and PDF export.',
 'Education','Intermediate','attendance_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Face Recognition Attendance',
 'Automated attendance using OpenCV face detection. Face embeddings stored in DB with real-time marking.',
 'Education','Advanced','attendance_system','Python,OpenCV,Flask,PostgreSQL,NumPy,JavaScript'),

('Book Catalogue Browser',
 'Searchable list of library books with title, author, and availability status stored in PostgreSQL.',
 'Education','Beginner','library_system','HTML,CSS,Python,Flask,PostgreSQL'),

('Library Management with Notifications',
 'Full library system with due-date email reminders, reservation queue, and admin dashboard.',
 'Education','Intermediate','library_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Smart Library Recommendation Engine',
 'Recommends books based on borrowing history using collaborative filtering. Analytics for admin.',
 'Education','Advanced','library_system','Python,Flask,PostgreSQL,scikit-learn,JavaScript,React'),

('Database-Driven Quiz',
 'Quiz questions in PostgreSQL. Admin adds/edits questions. Students take quiz and see instant score.',
 'Education','Beginner','quiz_app','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Timed Quiz Application',
 'Countdown timer per question, auto-submit on timeout, leaderboard, and user login for history.',
 'Education','Intermediate','quiz_app','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Adaptive Quiz Engine',
 'Quiz adjusts difficulty based on previous answers. Analytics show student progress over time.',
 'Education','Advanced','quiz_app','Python,Flask,PostgreSQL,scikit-learn,JavaScript,React')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── AI / ML ────────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Sentiment Analyser',
 'Enter text and get positive/negative/neutral sentiment using NLTK. Simple Flask + HTML interface.',
 'Artificial Intelligence','Beginner','ai_project','Python,Flask,NLTK,HTML,CSS'),

('Simple Rule-Based Chatbot',
 'FAQ chatbot using keyword matching. Trained on custom Q&A pairs. Deployed as Flask web app.',
 'Artificial Intelligence','Beginner','ai_project','Python,Flask,HTML,CSS,PostgreSQL'),

('Image Classifier Demo',
 'Upload an image; classify it using a pre-trained CNN. Shows top-3 predictions with confidence scores.',
 'Artificial Intelligence','Beginner','ai_project','Python,Flask,TensorFlow,HTML,CSS'),

('ML Spam Detector',
 'Naive Bayes classifier on SMS data. Web interface to check if a message is spam or not.',
 'Artificial Intelligence','Intermediate','ai_project','Python,Flask,scikit-learn,Pandas,HTML,CSS,PostgreSQL'),

('Movie Recommendation System',
 'Collaborative filtering recommender. Enter a movie title and get 5 similar recommendations.',
 'Artificial Intelligence','Intermediate','ai_project','Python,Flask,Pandas,scikit-learn,PostgreSQL,JavaScript'),

('Handwriting Recognition App',
 'Draw a digit on canvas; trained CNN predicts the number instantly. Trained on MNIST dataset.',
 'Artificial Intelligence','Intermediate','ai_project','Python,Flask,TensorFlow,JavaScript,HTML,CSS'),

('Real-Time Object Detection',
 'Detect objects in a webcam stream using YOLO. Annotated frames streamed to browser via Flask.',
 'Artificial Intelligence','Advanced','ai_project','Python,Flask,OpenCV,YOLO,JavaScript,PostgreSQL'),

('NLP Question Answering System',
 'Upload a PDF; system answers natural-language questions using a Transformer model.',
 'Artificial Intelligence','Advanced','ai_project','Python,Flask,Transformers,PostgreSQL,JavaScript,React'),

('AI Code Review Bot',
 'Analyses Python code for errors, style, and complexity. Returns detailed review with suggestions.',
 'Artificial Intelligence','Advanced','ai_project','Python,Flask,AST,PostgreSQL,JavaScript,React')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Mobile App ─────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Simple Calculator App',
 'Basic calculator for arithmetic with Flutter. Clean material design, cross-platform.',
 'Mobile App Development','Beginner','mobile_app','Flutter,Dart'),

('Notes App',
 'Create, edit, and delete text notes. Data persisted locally using SQLite. Material design.',
 'Mobile App Development','Beginner','mobile_app','Flutter,Dart,SQLite'),

('Unit Converter App',
 'Convert between length, weight, temperature, and currency units. Offline-capable.',
 'Mobile App Development','Beginner','mobile_app','Flutter,Dart'),

('Expense Tracker Mobile App',
 'Log daily expenses by category. Monthly pie charts. Data synced with Firebase.',
 'Mobile App Development','Intermediate','mobile_app','Flutter,Dart,Firebase,Chart.js'),

('Movie Browser App',
 'Browse and search movies from TMDB API. Save favourites locally. Smooth animations.',
 'Mobile App Development','Intermediate','mobile_app','Flutter,Dart,REST API,Firebase'),

('Fitness Tracker App',
 'Log workouts, track steps, set goals, and visualise progress with charts.',
 'Mobile App Development','Intermediate','mobile_app','Flutter,Dart,Firebase,SQLite'),

('Real-Time Chat Mobile App',
 'Cross-platform chat with auth, group chats, push notifications, and media sharing via Firebase.',
 'Mobile App Development','Advanced','mobile_app','Flutter,Dart,Firebase,FCM,WebSocket'),

('Ride Sharing Mobile App',
 'Uber-like app with live driver tracking, fare calculation, OTP verification, and payment gateway.',
 'Mobile App Development','Advanced','mobile_app','Flutter,Dart,Firebase,Google Maps,REST API,Stripe'),

('E-Commerce Mobile App',
 'Full-featured shopping app with product catalogue, cart, checkout, and order tracking.',
 'Mobile App Development','Advanced','mobile_app','Flutter,Dart,Firebase,Razorpay,REST API')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Cloud Computing ─────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Dockerised Flask App',
 'Package a Flask app in Docker. Includes Dockerfile, .dockerignore, and documentation.',
 'Cloud Computing','Beginner','cloud_project','Python,Flask,Docker,PostgreSQL'),

('Cloud File Storage App',
 'Upload files to AWS S3 via Flask. Files listed with download links. Env-var credentials.',
 'Cloud Computing','Beginner','cloud_project','Python,Flask,AWS,PostgreSQL,HTML,CSS'),

('Docker Compose Web Stack',
 'Flask + PostgreSQL + Nginx orchestrated with Docker Compose. One-command deployment.',
 'Cloud Computing','Intermediate','cloud_project','Python,Flask,PostgreSQL,Docker,Nginx'),

('CI/CD Pipeline with GitHub Actions',
 'Automated test-and-deploy: push triggers tests, builds Docker image, deploys to AWS EC2.',
 'Cloud Computing','Intermediate','cloud_project','Python,Flask,Docker,AWS,GitHub Actions'),

('Kubernetes Microservices App',
 'Decompose a monolith into 3 microservices on Kubernetes. Helm charts and auto-scaling.',
 'Cloud Computing','Advanced','cloud_project','Python,Flask,Docker,Kubernetes,PostgreSQL,Helm,GitHub Actions'),

('Multi-Region Disaster Recovery',
 'Flask app across two AWS regions. Route 53 health checks auto-failover on outage.',
 'Cloud Computing','Advanced','cloud_project','Python,Flask,AWS,Docker,PostgreSQL,Terraform')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── IoT ──────────────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Temperature Monitor Dashboard',
 'DHT11 sensor reads temperature; Raspberry Pi sends data to Flask. Dashboard shows live readings.',
 'IoT','Beginner','iot_project','Python,Flask,Raspberry Pi,PostgreSQL,HTML,CSS'),

('Smart Home Dashboard',
 'Control GPIO pins (lights, fans) from a web dashboard. State persisted in PostgreSQL.',
 'IoT','Intermediate','iot_project','Python,Flask,Raspberry Pi,PostgreSQL,JavaScript,HTML,CSS'),

('Smart Energy Monitor',
 'Current sensors measure appliance power. Real-time dashboard shows usage, cost, and carbon footprint.',
 'IoT','Advanced','iot_project','Python,Flask,MQTT,PostgreSQL,Raspberry Pi,React,Chart.js,Docker')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Cyber Security ──────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Password Strength Checker',
 'Enter a password and get a strength score (Weak/Fair/Strong) with improvement tips.',
 'Cyber Security','Beginner','cyber_security_project','Python,Flask,HTML,CSS,JavaScript'),

('Caesar Cipher Tool',
 'Encrypt and decrypt messages with Caesar cipher. User selects shift value, sees result in real time.',
 'Cyber Security','Beginner','cyber_security_project','Python,Flask,HTML,CSS,JavaScript'),

('Secure Password Manager',
 'Store encrypted passwords in PostgreSQL. Master password decrypts vault locally. Password generator.',
 'Cyber Security','Intermediate','cyber_security_project','Python,Flask,PostgreSQL,Cryptography,HTML,JavaScript'),

('Phishing URL Detector',
 'ML model classifies URLs as phishing or legitimate based on lexical features.',
 'Cyber Security','Intermediate','cyber_security_project','Python,Flask,scikit-learn,Pandas,PostgreSQL,HTML,CSS'),

('Intrusion Detection System',
 'Monitor network traffic, detect anomalous patterns with ML, trigger alerts with packet logging.',
 'Cyber Security','Advanced','cyber_security_project','Python,Flask,scikit-learn,Scapy,PostgreSQL,React,Docker'),

('Web Vulnerability Scanner',
 'Automated scanner checks for SQLi, XSS, CSRF, open redirects, and missing security headers.',
 'Cyber Security','Advanced','cyber_security_project','Python,Flask,PostgreSQL,JavaScript,React,Docker')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Data Science ────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('CSV Data Explorer',
 'Upload a CSV; see column statistics, data types, and preview table built with Pandas and Flask.',
 'Data Science','Beginner','data_science_project','Python,Flask,Pandas,HTML,CSS'),

('Student Grade Analyser',
 'Enter marks; app calculates mean, median, pass/fail rate, and renders grade distribution chart.',
 'Data Science','Beginner','data_science_project','Python,Flask,Pandas,Matplotlib,PostgreSQL,HTML,CSS'),

('Sales Trend Dashboard',
 'Upload CSV; dashboard shows trend lines, top products, and seasonal patterns using Plotly.',
 'Data Science','Intermediate','data_science_project','Python,Flask,Pandas,Plotly,PostgreSQL,HTML,JavaScript'),

('Housing Price Predictor',
 'Linear regression predicts house price from area, rooms, and location features. Web form for predictions.',
 'Data Science','Intermediate','data_science_project','Python,Flask,scikit-learn,Pandas,PostgreSQL,HTML,CSS'),

('Customer Churn Predictor',
 'Random Forest on telecom data predicts customer churn. Dashboard shows feature importance.',
 'Data Science','Advanced','data_science_project','Python,Flask,scikit-learn,Pandas,React,PostgreSQL,Docker'),

('Financial Fraud Detection',
 'Anomaly detection on transactions using Isolation Forest. Real-time alert dashboard.',
 'Data Science','Advanced','data_science_project','Python,Flask,scikit-learn,TensorFlow,Pandas,PostgreSQL,React')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Blockchain ──────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Simple Blockchain Simulator',
 'Build a basic blockchain in Python. Demonstrates hashing, blocks, chains, and proof-of-work.',
 'Blockchain','Beginner','blockchain_project','Python,Flask,HTML,CSS'),

('Cryptocurrency Price Tracker',
 'Fetch live crypto prices from CoinGecko API and display with price change indicators.',
 'Blockchain','Beginner','blockchain_project','Python,Flask,HTML,CSS,JavaScript'),

('Decentralised Voting App',
 'Blockchain-based voting with smart contracts ensuring tamper-proof votes. React DApp frontend.',
 'Blockchain','Intermediate','blockchain_project','Solidity,Python,JavaScript,React,Web3.js,Hardhat'),

('NFT Marketplace UI',
 'Browse and list NFTs. Connects to MetaMask wallet. Displays IPFS-hosted artwork.',
 'Blockchain','Intermediate','blockchain_project','JavaScript,React,Web3.js,IPFS,Solidity'),

('DeFi Lending Protocol',
 'Decentralised lending/borrowing protocol. Smart contracts handle collateral, interest, and liquidation.',
 'Blockchain','Advanced','blockchain_project','Solidity,Hardhat,JavaScript,React,Web3.js,The Graph'),

('Supply Chain Tracker',
 'Track product provenance on blockchain from manufacturer to consumer.',
 'Blockchain','Advanced','blockchain_project','Solidity,Python,Flask,React,Web3.js,IPFS,PostgreSQL')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── FinTech ─────────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('EMI Calculator',
 'Calculate loan EMI with amortisation schedule. Input loan amount, interest rate, and tenure.',
 'FinTech','Beginner','fintech_project','HTML,CSS,JavaScript,Python,Flask'),

('Personal Finance Dashboard',
 'Track income, expenses, and savings goals. Visual summary with pie charts in PostgreSQL.',
 'FinTech','Beginner','fintech_project','HTML,CSS,JavaScript,Python,PostgreSQL'),

('Digital Wallet App',
 'Send and receive money between users. Transaction history, balance display, QR code payments.',
 'FinTech','Intermediate','fintech_project','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Investment Portfolio Tracker',
 'Track stocks, mutual funds, and crypto. Calculates returns, portfolio allocation, and P&L.',
 'FinTech','Intermediate','fintech_project','HTML,CSS,JavaScript,Python,Flask,PostgreSQL,REST API'),

('Algorithmic Trading Platform',
 'Backtesting for trading strategies. Live paper trading via broker API with analytics.',
 'FinTech','Advanced','fintech_project','Python,Flask,Pandas,NumPy,React,PostgreSQL,Redis,Docker'),

('Credit Scoring Engine',
 'ML model predicts creditworthiness from financial behaviour. Explainable AI dashboard.',
 'FinTech','Advanced','fintech_project','Python,Flask,scikit-learn,Pandas,React,PostgreSQL,Docker')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Hospital / Medical ──────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Patient Registration Form',
 'Register patients with name, age, ailment. Records in PostgreSQL; admin views patient list.',
 'Medical','Beginner','hospital_system','HTML,CSS,Python,Flask,PostgreSQL'),

('Doctor Schedule Viewer',
 'View available doctor slots for the week. Admin manages availability.',
 'Medical','Beginner','hospital_system','HTML,CSS,Python,Flask,PostgreSQL'),

('Clinic Appointment Manager',
 'Online appointment booking with doctor selection, slot picker, and confirmation email.',
 'Medical','Intermediate','hospital_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Hospital Patient Portal',
 'Patients view medical history, book appointments, and download prescriptions. Doctors update records.',
 'Medical','Intermediate','hospital_system','HTML,CSS,JavaScript,Python,Flask,PostgreSQL'),

('Telemedicine Platform',
 'Video consultation platform with patient-doctor chat, prescription upload, and payment gateway.',
 'Medical','Advanced','hospital_system','Python,Flask,PostgreSQL,JavaScript,React,WebRTC'),

('Hospital ERP System',
 'End-to-end hospital ERP: patient management, billing, payroll, inventory, lab, and analytics.',
 'Medical','Advanced','hospital_system','Python,Flask,PostgreSQL,JavaScript,React,Docker')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;

-- ── Fitness ─────────────────────────────────────────────────────
INSERT INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('BMI Calculator App',
 'Calculate BMI, display health category, and provide personalised diet tips.',
 'Mobile App Development','Beginner','fitness_app','HTML,CSS,JavaScript,Python,Flask'),

('Workout Logger',
 'Log workouts by type, duration, and calories burned. View history and weekly summaries.',
 'Mobile App Development','Intermediate','fitness_app','Flutter,Dart,Firebase,SQLite'),

('AI Fitness Coach App',
 'ML model analyses workout history to suggest personalised training plans and nutrition advice.',
 'Mobile App Development','Advanced','fitness_app','Flutter,Dart,Firebase,Python,Flask,scikit-learn,REST API')
ON CONFLICT (title) DO UPDATE
  SET description  = EXCLUDED.description,
      domain       = EXCLUDED.domain,
      difficulty   = EXCLUDED.difficulty,
      category     = EXCLUDED.category,
      technologies = EXCLUDED.technologies;


-- ============================================================
-- SKILLS DATA
-- ============================================================
INSERT INTO skills (skill_name, project_type, category, weight, estimated_time) VALUES
-- website
('HTML',            'website', 'Frontend',    2, '1 week'),
('CSS',             'website', 'Frontend',    2, '1 week'),
('JavaScript',      'website', 'Frontend',    4, '2-3 weeks'),
('React',           'website', 'Frontend',    3, '3-4 weeks'),
('Python',          'website', 'Backend',     4, '2-3 weeks'),
('Flask',           'website', 'Backend',     3, '1-2 weeks'),
('PostgreSQL',      'website', 'Database',    3, '1-2 weeks'),
-- app
('Java',            'app',     'Android',         4, '4-6 weeks'),
('Kotlin',          'app',     'Android',         4, '3-4 weeks'),
('React Native',    'app',     'Cross-Platform',  4, '3-4 weeks'),
('Flutter',         'app',     'Cross-Platform',  4, '3-4 weeks'),
('Firebase',        'app',     'Backend',         3, '1-2 weeks'),
('REST API',        'app',     'Integration',     3, '1-2 weeks'),
-- other (AI/ML/DS)
('Python',          'other',   'Core',            5, '2-3 weeks'),
('Machine Learning','other',   'AI/ML',           5, '4-6 weeks'),
('Pandas',          'other',   'Data',            3, '1-2 weeks'),
('NumPy',           'other',   'Data',            2, '1 week'),
('Matplotlib',      'other',   'Visualization',   2, '1 week'),
('PostgreSQL',      'other',   'Database',        2, '1-2 weeks'),
('scikit-learn',    'other',   'AI/ML',           4, '2-3 weeks'),
-- gaming
('Python',          'gaming',  'Backend',         3, '2-3 weeks'),
('Pygame',          'gaming',  'Game Engine',     4, '2-3 weeks'),
('JavaScript',      'gaming',  'Frontend',        4, '2-3 weeks'),
('Three.js',        'gaming',  'Game Engine',     4, '3-4 weeks'),
('WebSocket',       'gaming',  'Networking',      3, '1-2 weeks'),
('HTML',            'gaming',  'Frontend',        2, '1 week'),
('CSS',             'gaming',  'Frontend',        2, '1 week')
ON CONFLICT (skill_name, project_type) DO UPDATE
  SET category       = EXCLUDED.category,
      weight         = EXCLUDED.weight,
      estimated_time = EXCLUDED.estimated_time;


-- ============================================================
-- SKILL DEPENDENCIES
-- ============================================================
INSERT INTO skill_dependencies (skill_name, depends_on) VALUES
('React',          'JavaScript'),
('React',          'HTML'),
('React',          'CSS'),
('Flask',          'Python'),
('PostgreSQL',     'Python'),
('React Native',   'JavaScript'),
('Firebase',       'JavaScript'),
('Kotlin',         'Java'),
('Three.js',       'JavaScript'),
('Pygame',         'Python'),
('WebSocket',      'JavaScript'),
('scikit-learn',   'Python'),
('scikit-learn',   'Pandas'),
('Pandas',         'Python')
ON CONFLICT (skill_name, depends_on) DO NOTHING;


-- ============================================================
-- LEARNING RESOURCES
-- ============================================================
INSERT INTO learning_resources (skill_name, resource_title, resource_link, difficulty) VALUES
('HTML',            'HTML Foundations',              'https://developer.mozilla.org/en-US/docs/Learn/HTML',                       'Beginner'),
('HTML',            'HTML Full Course (freeCodeCamp)','https://www.freecodecamp.org/learn/2022/responsive-web-design/',           'Beginner'),
('CSS',             'CSS Fundamentals',              'https://web.dev/learn/css',                                                  'Beginner'),
('CSS',             'CSS Tricks Complete Guide',     'https://css-tricks.com/guides/',                                             'Intermediate'),
('JavaScript',      'JavaScript Guide (MDN)',        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',              'Beginner'),
('JavaScript',      'JavaScript.info',               'https://javascript.info/',                                                   'Intermediate'),
('React',           'React Official Docs',           'https://react.dev/learn',                                                    'Intermediate'),
('React',           'React Full Course (Scrimba)',   'https://scrimba.com/learn/learnreact',                                       'Intermediate'),
('Python',          'Python Official Tutorial',      'https://docs.python.org/3/tutorial/',                                        'Beginner'),
('Python',          'Python for Beginners (freeCodeCamp)','https://www.youtube.com/watch?v=rfscVS0vtbw',                          'Beginner'),
('Flask',           'Flask Official Tutorial',       'https://flask.palletsprojects.com/en/3.0.x/tutorial/',                      'Intermediate'),
('Flask',           'Flask Mega-Tutorial',           'https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world','Intermediate'),
('PostgreSQL',      'PostgreSQL Tutorial',           'https://www.postgresqltutorial.com/',                                        'Beginner'),
('PostgreSQL',      'PostgreSQL Docs',               'https://www.postgresql.org/docs/current/',                                   'Intermediate'),
('MySQL',           'MySQL Tutorial',                'https://dev.mysql.com/doc/refman/8.0/en/tutorial.html',                      'Beginner'),
('Node.js',         'Node.js Docs',                 'https://nodejs.org/en/learn',                                                'Intermediate'),
('MongoDB',         'MongoDB University',            'https://learn.mongodb.com/',                                                  'Beginner'),
('Firebase',        'Firebase Docs',                 'https://firebase.google.com/docs',                                           'Beginner'),
('Java',            'Java Programming (Oracle)',     'https://dev.java/learn/',                                                    'Beginner'),
('Kotlin',          'Kotlin for Android',            'https://kotlinlang.org/docs/getting-started.html',                          'Intermediate'),
('Flutter',         'Flutter Official Docs',         'https://docs.flutter.dev/get-started/codelab',                              'Beginner'),
('Flutter',         'Flutter Tutorial (freeCodeCamp)','https://www.youtube.com/watch?v=VPvVD8t02U8',                              'Beginner'),
('React Native',    'React Native Docs',             'https://reactnative.dev/docs/getting-started',                              'Intermediate'),
('Machine Learning','ML Crash Course (Google)',      'https://developers.google.com/machine-learning/crash-course',               'Beginner'),
('Machine Learning','Scikit-learn Tutorial',         'https://scikit-learn.org/stable/tutorial/',                                  'Intermediate'),
('Pandas',          'Pandas User Guide',             'https://pandas.pydata.org/docs/user_guide/index.html',                      'Beginner'),
('Pandas',          'Pandas Tutorial (Kaggle)',      'https://www.kaggle.com/learn/pandas',                                       'Beginner'),
('NumPy',           'NumPy Quickstart',              'https://numpy.org/doc/stable/user/quickstart.html',                         'Beginner'),
('Matplotlib',      'Matplotlib Tutorials',          'https://matplotlib.org/stable/tutorials/index.html',                        'Beginner'),
('scikit-learn',    'Scikit-learn User Guide',       'https://scikit-learn.org/stable/user_guide.html',                           'Intermediate'),
('TensorFlow',      'TensorFlow Tutorials',          'https://www.tensorflow.org/tutorials',                                       'Intermediate'),
('Pygame',          'Pygame Documentation',          'https://www.pygame.org/docs/',                                               'Beginner'),
('Pygame',          'Pygame Beginners Guide',        'https://realpython.com/pygame-a-primer/',                                    'Beginner'),
('Three.js',        'Three.js Manual',               'https://threejs.org/manual/#en/fundamentals',                               'Intermediate'),
('WebSocket',       'WebSocket API (MDN)',            'https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API',           'Intermediate'),
('Docker',          'Docker Get Started',             'https://docs.docker.com/get-started/',                                      'Beginner'),
('Docker',          'Docker Tutorial (freeCodeCamp)', 'https://www.youtube.com/watch?v=fqMOX6JJhGo',                              'Beginner'),
('Git',             'Git Book',                       'https://git-scm.com/book/en/v2',                                           'Beginner'),
('REST API',        'REST API Design Guide',          'https://restfulapi.net/',                                                   'Intermediate'),
('Solidity',        'Solidity Docs',                  'https://docs.soliditylang.org/',                                           'Advanced'),
('OpenCV',          'OpenCV Python Tutorials',        'https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html',                 'Intermediate'),
('AWS',             'AWS Getting Started',            'https://aws.amazon.com/getting-started/',                                   'Intermediate'),
('Kubernetes',      'Kubernetes Docs',                'https://kubernetes.io/docs/tutorials/',                                     'Advanced')
ON CONFLICT (skill_name, resource_title) DO UPDATE
  SET resource_link = EXCLUDED.resource_link,
      difficulty    = EXCLUDED.difficulty;


-- ============================================================
-- VERIFY
-- ============================================================
SELECT 'projects'          AS tbl, COUNT(*) FROM projects          UNION ALL
SELECT 'keywords',                  COUNT(*) FROM keywords          UNION ALL
SELECT 'skills',                    COUNT(*) FROM skills            UNION ALL
SELECT 'skill_dependencies',        COUNT(*) FROM skill_dependencies UNION ALL
SELECT 'learning_resources',        COUNT(*) FROM learning_resources;
