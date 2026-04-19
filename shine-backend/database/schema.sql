-- ============================================================
-- SHINE Access Point — Database Expansion Script
-- Run ONLY on shine_db
-- Safe to re-run: uses IF NOT EXISTS and IGNORE
-- ============================================================

USE shine_db;

-- ============================================================
-- STEP 0 — Clean duplicate skills from previous runs
-- ============================================================
DELETE FROM skills
WHERE id NOT IN (
    SELECT * FROM (
        SELECT MIN(id)
        FROM skills
        GROUP BY skill_name, project_type
    ) AS temp
);

-- ============================================================
-- STEP 1 — EXPANDED KEYWORDS TABLE
-- ============================================================
INSERT IGNORE INTO keywords (keyword, category, domain) VALUES

-- Attendance synonyms
('attend',              'attendance_system', 'Education'),
('presence',            'attendance_system', 'Education'),
('rollcall',            'attendance_system', 'Education'),
('roll call',           'attendance_system', 'Education'),
('absentee',            'attendance_system', 'Education'),
('biometric',           'attendance_system', 'Education'),
('face recognition',    'attendance_system', 'Education'),
('qr attendance',       'attendance_system', 'Education'),

-- Library synonyms
('borrow',              'library_system', 'Education'),
('isbn',                'library_system', 'Education'),
('catalog',             'library_system', 'Education'),
('librarian',           'library_system', 'Education'),
('book issue',          'library_system', 'Education'),
('book return',         'library_system', 'Education'),

-- Hospital synonyms
('clinic',              'hospital_system', 'Medical'),
('medicine',            'hospital_system', 'Medical'),
('health',              'hospital_system', 'Medical'),
('prescription',        'hospital_system', 'Medical'),
('pharmacy',            'hospital_system', 'Medical'),

-- Ecommerce synonyms
('shop',                'ecommerce', 'Web Development'),
('buy',                 'ecommerce', 'Web Development'),
('sell',                'ecommerce', 'Web Development'),
('e-commerce',          'ecommerce', 'Web Development'),
('product',             'ecommerce', 'Web Development'),
('checkout',            'ecommerce', 'Web Development'),
('purchase',            'ecommerce', 'Web Development'),
('marketplace',         'ecommerce', 'Web Development'),

-- Chat synonyms
('message',             'chat_app', 'Web Development'),
('talk',                'chat_app', 'Web Development'),
('messenger',           'chat_app', 'Web Development'),
('group chat',          'chat_app', 'Web Development'),
('instant message',     'chat_app', 'Web Development'),

-- Quiz synonyms
('mcq',                 'quiz_app', 'Education'),
('question',            'quiz_app', 'Education'),
('answer',              'quiz_app', 'Education'),
('assessment',          'quiz_app', 'Education'),
('grade',               'quiz_app', 'Education'),
('test portal',         'quiz_app', 'Education'),

-- Expense/Finance
('money',               'expense_tracker', 'Web Development'),
('spend',               'expense_tracker', 'Web Development'),
('income',              'expense_tracker', 'Web Development'),
('cost',                'expense_tracker', 'Web Development'),
('savings',             'expense_tracker', 'Web Development'),
('wallet',              'expense_tracker', 'Web Development'),

-- Task Manager
('reminder',            'task_manager', 'Web Development'),
('checklist',           'task_manager', 'Web Development'),
('planner',             'task_manager', 'Web Development'),
('deadline',            'task_manager', 'Web Development'),
('kanban',              'task_manager', 'Web Development'),

-- Food
('meal',                'food_ordering', 'Web Development'),
('canteen',             'food_ordering', 'Web Development'),
('menu',                'food_ordering', 'Web Development'),
('order food',          'food_ordering', 'Web Development'),

-- Employee
('staff',               'employee_management', 'Web Development'),
('salary',              'employee_management', 'Web Development'),
('leave',               'employee_management', 'Web Development'),
('worker',              'employee_management', 'Web Development'),
('department',          'employee_management', 'Web Development'),

-- AI / ML
('artificial intelligence', 'ai_project', 'Artificial Intelligence'),
('machine learning',    'ai_project', 'Artificial Intelligence'),
('deep learning',       'ai_project', 'Artificial Intelligence'),
('neural network',      'ai_project', 'Artificial Intelligence'),
('nlp',                 'ai_project', 'Artificial Intelligence'),
('natural language',    'ai_project', 'Artificial Intelligence'),
('computer vision',     'ai_project', 'Artificial Intelligence'),
('image recognition',   'ai_project', 'Artificial Intelligence'),
('chatbot',             'ai_project', 'Artificial Intelligence'),
('recommendation',      'ai_project', 'Artificial Intelligence'),

-- Data Science
('data science',        'data_science_project', 'Data Science'),
('data analysis',       'data_science_project', 'Data Science'),
('visualization',       'data_science_project', 'Data Science'),
('dashboard',           'data_science_project', 'Data Science'),
('analytics',           'data_science_project', 'Data Science'),
('prediction',          'data_science_project', 'Data Science'),
('statistics',          'data_science_project', 'Data Science'),
('dataset',             'data_science_project', 'Data Science'),

-- Cyber Security
('cyber security',      'cyber_security_project', 'Cyber Security'),
('cybersecurity',       'cyber_security_project', 'Cyber Security'),
('encryption',          'cyber_security_project', 'Cyber Security'),
('hacking',             'cyber_security_project', 'Cyber Security'),
('firewall',            'cyber_security_project', 'Cyber Security'),
('vulnerability',       'cyber_security_project', 'Cyber Security'),
('intrusion',           'cyber_security_project', 'Cyber Security'),
('network security',    'cyber_security_project', 'Cyber Security'),
('password manager',    'cyber_security_project', 'Cyber Security'),

-- IoT
('iot',                 'iot_project', 'IoT'),
('internet of things',  'iot_project', 'IoT'),
('sensor',              'iot_project', 'IoT'),
('arduino',             'iot_project', 'IoT'),
('raspberry pi',        'iot_project', 'IoT'),
('smart home',          'iot_project', 'IoT'),
('automation',          'iot_project', 'IoT'),
('embedded',            'iot_project', 'IoT'),

-- Cloud Computing
('cloud',               'cloud_project', 'Cloud Computing'),
('aws',                 'cloud_project', 'Cloud Computing'),
('deployment',          'cloud_project', 'Cloud Computing'),
('devops',              'cloud_project', 'Cloud Computing'),
('docker',              'cloud_project', 'Cloud Computing'),
('kubernetes',          'cloud_project', 'Cloud Computing'),
('microservice',        'cloud_project', 'Cloud Computing'),
('serverless',          'cloud_project', 'Cloud Computing');

-- ============================================================
-- STEP 2 — EXPANDED PROJECTS TABLE
-- (3 Beginner + 3 Intermediate + 3 Advanced per category)
-- ============================================================

-- ── ATTENDANCE SYSTEM (additional) ───────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Student Register App',
 'A web form that lets a teacher register student names and mark daily attendance. Stores data in MySQL and shows a simple attendance table.',
 'Education', 'Beginner', 'attendance_system', 'HTML,CSS,Python,MySQL'),

('Class Attendance Logger',
 'Log attendance per class period. Supports multiple subjects, generates per-student percentage, and exports to CSV.',
 'Education', 'Beginner', 'attendance_system', 'HTML,CSS,Python,MySQL'),

('Attendance Report Viewer',
 'Reads attendance records from MySQL and displays colourful monthly reports. Teacher can filter by student or date range.',
 'Education', 'Beginner', 'attendance_system', 'HTML,CSS,Python,MySQL'),

('Attendance Portal with Login',
 'Teacher and student login, per-class attendance marking, defaulter list, and PDF report generation.',
 'Education', 'Intermediate', 'attendance_system', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Smart Attendance Dashboard',
 'Role-based system (admin, teacher, student). Real-time attendance charts, email notifications for low attendance, and CSV/PDF export.',
 'Education', 'Intermediate', 'attendance_system', 'HTML,CSS,JavaScript,Chart.js,Python,Flask,MySQL'),

('Geo-Fenced Attendance System',
 'Students mark attendance only within campus GPS boundary. Live map view for admin, attendance analytics dashboard.',
 'Education', 'Intermediate', 'attendance_system', 'Python,Flask,MySQL,JavaScript,Leaflet.js'),

('Face Recognition Attendance',
 'Automated attendance using OpenCV face detection. Stores face embeddings in DB, real-time marking, and admin analytics dashboard.',
 'Education', 'Advanced', 'attendance_system', 'Python,OpenCV,Flask,MySQL,NumPy,JavaScript'),

('Blockchain Attendance Ledger',
 'Tamper-proof attendance records stored on a private blockchain. Smart contracts enforce rules; admin can audit full history.',
 'Education', 'Advanced', 'attendance_system', 'Python,Flask,MySQL,JavaScript,Blockchain'),

('AI-Powered Attendance Predictor',
 'Predicts students likely to fall below attendance threshold using ML. Sends automated alerts and generates trend reports.',
 'Education', 'Advanced', 'attendance_system', 'Python,Flask,MySQL,scikit-learn,Pandas,JavaScript,React');

-- ── LIBRARY SYSTEM (additional) ───────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Book Catalogue Browser',
 'A simple searchable list of library books with title, author, and availability status stored in MySQL.',
 'Education', 'Beginner', 'library_system', 'HTML,CSS,Python,MySQL'),

('Library Issue Tracker',
 'Track which books are issued to which student. Admin can record issue and return dates and view overdue books.',
 'Education', 'Beginner', 'library_system', 'HTML,CSS,Python,MySQL'),

('Simple Book Search App',
 'Search books by title or author. Results show cover image, genre, and shelf location. Admin can add books via form.',
 'Education', 'Beginner', 'library_system', 'HTML,CSS,JavaScript,Python,MySQL'),

('Library Member Portal',
 'Member registration, book catalog with filters, issue history per member, and fines calculated automatically.',
 'Education', 'Intermediate', 'library_system', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Library Management with Notifications',
 'Full library system with due-date email reminders, reservation queue, and admin dashboard with inventory reports.',
 'Education', 'Intermediate', 'library_system', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('E-Library with PDF Viewer',
 'Digital library where users can read PDFs in-browser. Tracks reading progress, supports bookmarks, and has admin upload panel.',
 'Education', 'Intermediate', 'library_system', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Smart Library Recommendation Engine',
 'Recommends books based on borrowing history using collaborative filtering. Admin can manage users, inventory, and view analytics.',
 'Education', 'Advanced', 'library_system', 'Python,Flask,MySQL,scikit-learn,JavaScript,React'),

('RFID-Based Library System',
 'Books tagged with RFID auto-check-in/check-out at gates. Dashboard tracks real-time inventory and generates usage analytics.',
 'Education', 'Advanced', 'library_system', 'Python,Flask,MySQL,JavaScript,React,RFID'),

('Library API with Mobile App',
 'RESTful library backend with JWT auth. Mobile app built in React Native lets students search, reserve, and renew books.',
 'Education', 'Advanced', 'library_system', 'Python,Flask,MySQL,React Native,REST API,JWT');

-- ── HOSPITAL SYSTEM (additional) ──────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Patient Registration Form',
 'A simple form to register new patients with name, age, and ailment. Records stored in MySQL, admin can view patient list.',
 'Medical', 'Beginner', 'hospital_system', 'HTML,CSS,Python,MySQL'),

('Doctor Schedule Viewer',
 'Displays available doctor slots for the week. Patients can view but not book — admin manages the schedule.',
 'Medical', 'Beginner', 'hospital_system', 'HTML,CSS,Python,MySQL'),

('Basic Medical Records App',
 'Store and view patient visit records — diagnosis, prescribed medicines, and doctor notes. Simple CRUD interface.',
 'Medical', 'Beginner', 'hospital_system', 'HTML,CSS,Python,MySQL'),

('Clinic Appointment Manager',
 'Online appointment booking with doctor selection, date/time slot picker, and confirmation email. Admin dashboard for scheduling.',
 'Medical', 'Intermediate', 'hospital_system', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Hospital Patient Portal',
 'Patients log in to view medical history, book appointments, and download prescriptions. Doctors update records after visits.',
 'Medical', 'Intermediate', 'hospital_system', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Pharmacy Inventory System',
 'Track medicine stock, suppliers, expiry dates, and auto-reorder alerts. Integrates with hospital patient prescription module.',
 'Medical', 'Intermediate', 'hospital_system', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Telemedicine Platform',
 'Video consultation platform with patient-doctor chat, prescription upload, appointment scheduling, and payment gateway.',
 'Medical', 'Advanced', 'hospital_system', 'Python,Flask,MySQL,JavaScript,React,WebRTC'),

('Hospital AI Diagnostic Assistant',
 'Symptom-checker powered by ML that suggests probable diagnoses. Feeds into doctor review workflow with confidence scores.',
 'Medical', 'Advanced', 'hospital_system', 'Python,Flask,MySQL,scikit-learn,React,REST API'),

('Hospital ERP System',
 'End-to-end hospital ERP: patient management, billing, payroll, inventory, lab results, and analytics across every department.',
 'Medical', 'Advanced', 'hospital_system', 'Python,Flask,MySQL,JavaScript,React,Docker');

-- ── ECOMMERCE (additional) ─────────────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Simple Product Store',
 'Display products from MySQL with image, price, and category. Users can browse but cart/checkout is a future feature.',
 'Web Development', 'Beginner', 'ecommerce', 'HTML,CSS,Python,MySQL'),

('Category Filter Shop',
 'Product listing with category-based filter and price sort. Products managed by admin via a hidden dashboard.',
 'Web Development', 'Beginner', 'ecommerce', 'HTML,CSS,JavaScript,Python,MySQL'),

('Product Search Engine',
 'Live search bar that filters products as user types. Search across title, description, and category stored in MySQL.',
 'Web Development', 'Beginner', 'ecommerce', 'HTML,CSS,JavaScript,Python,MySQL'),

('Shopping Cart App',
 'Add/remove items to cart, calculate totals, and place orders. Order history saved in MySQL. User authentication required.',
 'Web Development', 'Intermediate', 'ecommerce', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('E-Commerce with Reviews',
 'Full shopping site with product ratings, user reviews, wishlist, and admin panel to manage products and orders.',
 'Web Development', 'Intermediate', 'ecommerce', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Multi-Vendor Marketplace',
 'Multiple sellers register shops; buyers browse and order from any seller. Admin approves sellers and mediates disputes.',
 'Web Development', 'Intermediate', 'ecommerce', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('E-Commerce with Payment Gateway',
 'Complete store with Razorpay/Stripe integration, order tracking emails, inventory control, and React-based frontend.',
 'Web Development', 'Advanced', 'ecommerce', 'Python,Flask,MySQL,JavaScript,React,Razorpay'),

('E-Commerce Recommendation Engine',
 'Product recommendations using collaborative filtering on purchase history. Includes A/B testing framework for offers.',
 'Web Development', 'Advanced', 'ecommerce', 'Python,Flask,MySQL,scikit-learn,JavaScript,React'),

('Headless Commerce API',
 'REST API-first commerce backend with JWT auth, GraphQL queries, Redis caching, and a React storefront.',
 'Web Development', 'Advanced', 'ecommerce', 'Python,Flask,MySQL,Redis,JavaScript,React,Docker');

-- ── PORTFOLIO ──────────────────────────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Basic HTML Resume',
 'A single-page online resume with name, education, skills, and contact info. No JavaScript required.',
 'Web Development', 'Beginner', 'portfolio', 'HTML,CSS'),

('Animated Portfolio Page',
 'Personal portfolio with CSS animations, skills section, project cards, and a mailto contact button.',
 'Web Development', 'Beginner', 'portfolio', 'HTML,CSS,JavaScript'),

('Portfolio with Photo Gallery',
 'Showcase your photos in a responsive grid with lightbox pop-ups. Admin adds images via a simple upload form.',
 'Web Development', 'Beginner', 'portfolio', 'HTML,CSS,JavaScript,Python,MySQL'),

('Portfolio with Live Projects',
 'Dynamic portfolio that fetches your GitHub repos via API and displays them as project cards with live demo links.',
 'Web Development', 'Intermediate', 'portfolio', 'HTML,CSS,JavaScript,Python,Flask,GitHub API'),

('Portfolio Blog System',
 'Portfolio combined with a blog engine. Write/edit posts in Markdown; posts stored in MySQL. Responsive design.',
 'Web Development', 'Intermediate', 'portfolio', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Portfolio CMS',
 'Content management system lets you add/edit skills, projects, and testimonials from an admin panel without touching code.',
 'Web Development', 'Intermediate', 'portfolio', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Portfolio with Analytics',
 'Portfolio site that tracks visitor count, page views, and time on page. Dashboard shows visual analytics to owner.',
 'Web Development', 'Advanced', 'portfolio', 'Python,Flask,MySQL,JavaScript,React,Chart.js'),

('Full-Stack Portfolio Platform',
 'Multi-user portfolio platform — users register, build their own portfolio, and share a public URL. Admin moderation panel.',
 'Web Development', 'Advanced', 'portfolio', 'Python,Flask,MySQL,JavaScript,React,Docker'),

('3D Interactive Portfolio',
 'Portfolio with Three.js 3D animations, WebGL effects, and API-driven content. Hosted on cloud with CI/CD pipeline.',
 'Web Development', 'Advanced', 'portfolio', 'JavaScript,React,Three.js,Python,Flask,MySQL,Docker');

-- ── QUIZ APP ───────────────────────────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Static Quiz Page',
 'A 5-question multiple-choice quiz hardcoded in HTML/JavaScript that shows final score at the end.',
 'Education', 'Beginner', 'quiz_app', 'HTML,CSS,JavaScript'),

('DB-Driven Quiz',
 'Quiz questions stored in MySQL. Admin can add/edit questions. Students take quiz and score is shown on completion.',
 'Education', 'Beginner', 'quiz_app', 'HTML,CSS,JavaScript,Python,MySQL'),

('Category Quiz Selector',
 'Choose quiz category (Math, Science, English) from a menu. Questions fetched by category from MySQL.',
 'Education', 'Beginner', 'quiz_app', 'HTML,CSS,JavaScript,Python,MySQL'),

('Timed Quiz Application',
 'Countdown timer per question, auto-submit on timeout, leaderboard showing top scores, and user login to track history.',
 'Education', 'Intermediate', 'quiz_app', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Teacher Quiz Builder',
 'Teachers create custom quizzes, assign to classes, and view per-student results. Students get instant feedback after submission.',
 'Education', 'Intermediate', 'quiz_app', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Adaptive Quiz Engine',
 'Quiz dynamically adjusts question difficulty based on previous answers using a simple scoring algorithm.',
 'Education', 'Intermediate', 'quiz_app', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Online Exam Proctoring System',
 'Full exam portal with webcam-based proctoring (screenshot capture), randomised question order, and anti-tab-switch detection.',
 'Education', 'Advanced', 'quiz_app', 'Python,Flask,MySQL,JavaScript,React,OpenCV'),

('AI Question Generator',
 'NLP model generates quiz questions from uploaded PDF study material. Exports to printable format or online quiz mode.',
 'Education', 'Advanced', 'quiz_app', 'Python,Flask,MySQL,NLP,Transformers,React'),

('Multiplayer Quiz Game',
 'Real-time multiplayer quiz where multiple students compete simultaneously. Live score updates via WebSocket.',
 'Education', 'Advanced', 'quiz_app', 'Python,Flask,Flask-SocketIO,MySQL,JavaScript,React');

-- ── EXPENSE TRACKER (additional) ──────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Daily Spending Log',
 'Simple form to log daily expenses by category (food, transport, etc.). View monthly totals in a table.',
 'Web Development', 'Beginner', 'expense_tracker', 'HTML,CSS,Python,MySQL'),

('Budget Goal Tracker',
 'Set a monthly budget goal and log expenses. A progress bar shows how much of the budget is used.',
 'Web Development', 'Beginner', 'expense_tracker', 'HTML,CSS,JavaScript,Python,MySQL'),

('Receipt Upload Tracker',
 'Upload receipt images with expense amount and category. Admin views expenses in a sortable table.',
 'Web Development', 'Beginner', 'expense_tracker', 'HTML,CSS,Python,MySQL'),

('Multi-Category Expense Dashboard',
 'Track income and expenses across categories with monthly pie charts, bar graphs, and budget alerts.',
 'Web Development', 'Intermediate', 'expense_tracker', 'HTML,CSS,JavaScript,Chart.js,Python,Flask,MySQL'),

('Family Budget Manager',
 'Multi-user family budget app. Each member logs expenses; shared dashboard shows family totals and individual contributions.',
 'Web Development', 'Intermediate', 'expense_tracker', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Expense Sharing App',
 'Split bills between friends, track who owes what, and settle balances. Expense history with detailed breakdown.',
 'Web Development', 'Intermediate', 'expense_tracker', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('AI Expense Predictor',
 'ML model trained on past spending predicts next month\'s expenses by category. REST API backend with React dashboard.',
 'Web Development', 'Advanced', 'expense_tracker', 'Python,Flask,MySQL,scikit-learn,React,Chart.js'),

('Expense Tracker with Bank Integration',
 'Connects to bank CSV exports, auto-categorises transactions with NLP, and shows trends on an analytics dashboard.',
 'Web Development', 'Advanced', 'expense_tracker', 'Python,Flask,MySQL,NLP,React,Chart.js,Docker'),

('Financial Planning Platform',
 'Comprehensive personal finance tool — budgets, goals, debt tracker, investment tracker, and AI-based savings suggestions.',
 'Web Development', 'Advanced', 'expense_tracker', 'Python,Flask,MySQL,scikit-learn,JavaScript,React,Docker');

-- ── TASK MANAGER (additional) ─────────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Simple To-Do App',
 'Add, complete, and delete tasks from a clean interface. Data saved in MySQL so tasks persist across page refreshes.',
 'Web Development', 'Beginner', 'task_manager', 'HTML,CSS,JavaScript,Python,MySQL'),

('Priority To-Do List',
 'Assign High/Medium/Low priority to tasks. Sorted list view with colour-coded priorities and a done/undone toggle.',
 'Web Development', 'Beginner', 'task_manager', 'HTML,CSS,JavaScript,Python,MySQL'),

('Daily Planner App',
 'Organise tasks by day. Calendar-style view shows tasks per date. Simple drag-and-drop reordering.',
 'Web Development', 'Beginner', 'task_manager', 'HTML,CSS,JavaScript,Python,MySQL'),

('Team Task Board',
 'Kanban-style board with To-Do, In Progress, and Done columns. Tasks can be assigned to team members.',
 'Web Development', 'Intermediate', 'task_manager', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Project Management Tool',
 'Create projects with multiple tasks, set deadlines and assignees, receive deadline reminders via email.',
 'Web Development', 'Intermediate', 'task_manager', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Recurring Task Scheduler',
 'Set tasks that recur daily/weekly/monthly. Auto-generates new task entries and sends reminder notifications.',
 'Web Development', 'Intermediate', 'task_manager', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Full PM Suite with Gantt',
 'End-to-end project management with Gantt chart visualisation, resource allocation, milestone tracking, and team chat.',
 'Web Development', 'Advanced', 'task_manager', 'Python,Flask,MySQL,JavaScript,React,Chart.js,WebSocket'),

('AI Task Prioritiser',
 'ML model suggests task priority based on deadline, dependencies, and historical completion patterns.',
 'Web Development', 'Advanced', 'task_manager', 'Python,Flask,MySQL,scikit-learn,JavaScript,React'),

('Enterprise Task API',
 'Fully RESTful task management API with JWT auth, role-based permissions, webhooks, and API rate limiting.',
 'Web Development', 'Advanced', 'task_manager', 'Python,Flask,MySQL,Redis,Docker,REST API,JWT');

-- ── CHAT APP (additional) ──────────────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Static Chat UI',
 'A styled chat-room look built with HTML/CSS only. No real functionality — a pure UI exercise.',
 'Web Development', 'Beginner', 'chat_app', 'HTML,CSS'),

('Basic Chat Room',
 'Simple WebSocket chat where multiple browser tabs can exchange messages in real time. No login required.',
 'Web Development', 'Beginner', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,Flask-SocketIO'),

('Chat with Username',
 'Assign a username before entering the chat room. Messages show sender name and timestamp. History stored in MySQL.',
 'Web Development', 'Beginner', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Private Messaging App',
 'User login, find other users, send private messages, and see online/offline status with read receipts.',
 'Web Development', 'Intermediate', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,MySQL,Flask-SocketIO'),

('Group Chat with Rooms',
 'Create or join named chat rooms. Messages persist in MySQL. Admin can mute/kick users from rooms.',
 'Web Development', 'Intermediate', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,MySQL,Flask-SocketIO'),

('Chat App with File Sharing',
 'Send text and upload images/files in chat. Preview images inline; file links stored in DB and served via Flask.',
 'Web Development', 'Intermediate', 'chat_app', 'HTML,CSS,JavaScript,Python,Flask,MySQL,Flask-SocketIO'),

('Encrypted Messaging Platform',
 'End-to-end encrypted chat using RSA/AES. Key exchange on login; messages decrypted only on recipient device.',
 'Web Development', 'Advanced', 'chat_app', 'Python,Flask,MySQL,JavaScript,React,Cryptography,WebSocket'),

('Video Conference App',
 'Multi-user video and audio calls using WebRTC with a text chat sidebar. Room links shareable by URL.',
 'Web Development', 'Advanced', 'chat_app', 'Python,Flask,MySQL,JavaScript,React,WebRTC'),

('Chat Bot Integration Platform',
 'Messenger platform with plugin-based chatbot support. Bots answer FAQ, schedule meetings, and escalate to human agents.',
 'Web Development', 'Advanced', 'chat_app', 'Python,Flask,MySQL,JavaScript,React,NLP,WebSocket');

-- ── EMPLOYEE MANAGEMENT (additional) ──────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Employee List App',
 'View a list of employees with name, department, and role. Admin can add or delete records.',
 'Web Development', 'Beginner', 'employee_management', 'HTML,CSS,Python,MySQL'),

('Employee Profile Manager',
 'Each employee has a profile page with photo, contact info, and designation. Admin can edit profiles.',
 'Web Development', 'Beginner', 'employee_management', 'HTML,CSS,Python,MySQL'),

('Department Organisation Chart',
 'Visual org chart showing company hierarchy. Data pulled from MySQL; admin updates structure via form.',
 'Web Development', 'Beginner', 'employee_management', 'HTML,CSS,JavaScript,Python,MySQL'),

('Leave Management System',
 'Employees apply for leave online. Manager approves/rejects. Leave balance tracked per employee in MySQL.',
 'Web Development', 'Intermediate', 'employee_management', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Payroll Calculator App',
 'Enter hours worked and hourly rate; system calculates gross pay, tax deductions, and net salary. Payslips downloadable.',
 'Web Development', 'Intermediate', 'employee_management', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('HR Dashboard with Analytics',
 'Admin dashboard showing headcount by department, attrition rate, leave trends, and salary distribution charts.',
 'Web Development', 'Intermediate', 'employee_management', 'HTML,CSS,JavaScript,Chart.js,Python,Flask,MySQL'),

('Full HRMS Platform',
 'Complete HR system — recruitment, onboarding, attendance, performance reviews, payroll, and exit management.',
 'Web Development', 'Advanced', 'employee_management', 'Python,Flask,MySQL,JavaScript,React,Docker'),

('AI Employee Attrition Predictor',
 'ML model predicts which employees are likely to resign based on satisfaction scores, tenure, and performance data.',
 'Web Development', 'Advanced', 'employee_management', 'Python,Flask,MySQL,scikit-learn,Pandas,React'),

('Employee Self-Service Portal',
 'Employees log in to view payslips, apply for leave, update details, and access company documents. Full REST API backend.',
 'Web Development', 'Advanced', 'employee_management', 'Python,Flask,MySQL,JavaScript,React,Docker,REST API');

-- ── FOOD ORDERING (additional) ────────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Static Menu Page',
 'Beautiful HTML/CSS food menu for a single restaurant. Items grouped by category with prices.',
 'Web Development', 'Beginner', 'food_ordering', 'HTML,CSS'),

('Restaurant Menu with DB',
 'Menu items stored in MySQL. Admin adds/updates items via a form. Customers browse from the same page.',
 'Web Development', 'Beginner', 'food_ordering', 'HTML,CSS,JavaScript,Python,MySQL'),

('Canteen Daily Menu Poster',
 'School or office canteen posts today\'s menu. Admin updates it daily. Displays current time and meal timing.',
 'Web Development', 'Beginner', 'food_ordering', 'HTML,CSS,Python,MySQL'),

('Food Order and Bill Generator',
 'Customer selects items, adds to cart, places order, and gets a printable bill. Orders saved in MySQL.',
 'Web Development', 'Intermediate', 'food_ordering', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Restaurant Online Ordering System',
 'Full table reservation + food pre-order system. User login, real-time kitchen status, and SMS notification on ready.',
 'Web Development', 'Intermediate', 'food_ordering', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Multi-Restaurant Food App',
 'Multiple restaurants listed; user browses menus, places orders, and tracks delivery status from a single platform.',
 'Web Development', 'Intermediate', 'food_ordering', 'HTML,CSS,JavaScript,Python,Flask,MySQL'),

('Food Delivery Platform',
 'Full delivery ecosystem — restaurants, riders, and customers. Live order tracking map, payment gateway, and admin panel.',
 'Web Development', 'Advanced', 'food_ordering', 'Python,Flask,MySQL,JavaScript,React,Leaflet.js,Razorpay'),

('AI Food Recommendation Engine',
 'Recommends dishes based on order history and dietary preferences using collaborative filtering. React-based frontend.',
 'Web Development', 'Advanced', 'food_ordering', 'Python,Flask,MySQL,scikit-learn,JavaScript,React'),

('Cloud Kitchen Management System',
 'Multi-brand cloud kitchen backend: order routing, inventory, cost analysis, and customer loyalty program management.',
 'Web Development', 'Advanced', 'food_ordering', 'Python,Flask,MySQL,JavaScript,React,Docker,Redis');

-- ── ARTIFICIAL INTELLIGENCE (new category) ───────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Sentiment Analyser',
 'Enter text and get a positive/negative/neutral sentiment result using a pre-trained model. Simple Flask+HTML interface.',
 'Artificial Intelligence', 'Beginner', 'ai_project', 'Python,Flask,NLTK,HTML,CSS'),

('Image Classifier Demo',
 'Upload an image and classify it into categories using a pre-trained CNN. Shows top-3 predictions with confidence.',
 'Artificial Intelligence', 'Beginner', 'ai_project', 'Python,Flask,TensorFlow,HTML,CSS'),

('Simple Chatbot',
 'Rule-based chatbot that answers predefined FAQs using keyword matching. Deployed as a Flask web app.',
 'Artificial Intelligence', 'Beginner', 'ai_project', 'Python,Flask,HTML,CSS,MySQL'),

('ML Spam Detector',
 'Train a Naive Bayes classifier on SMS/email data. Web interface to type a message and check if it is spam.',
 'Artificial Intelligence', 'Intermediate', 'ai_project', 'Python,Flask,scikit-learn,Pandas,HTML,CSS,MySQL'),

('Movie Recommendation System',
 'Collaborative filtering recommender trained on ratings dataset. Enter a movie title and get 5 similar recommendations.',
 'Artificial Intelligence', 'Intermediate', 'ai_project', 'Python,Flask,Pandas,scikit-learn,MySQL,HTML,JavaScript'),

('Handwriting Recognition App',
 'Draw a digit on a canvas; a trained CNN predicts the number instantly. Model trained on MNIST dataset.',
 'Artificial Intelligence', 'Intermediate', 'ai_project', 'Python,Flask,TensorFlow,JavaScript,HTML,CSS'),

('Real-Time Object Detection App',
 'Detect objects in a live webcam stream using YOLO. Annotated frames streamed to the browser via Flask.',
 'Artificial Intelligence', 'Advanced', 'ai_project', 'Python,Flask,OpenCV,YOLO,JavaScript,MySQL'),

('NLP Question Answering System',
 'Upload a PDF; system extracts text and answers natural-language questions using a Transformer model.',
 'Artificial Intelligence', 'Advanced', 'ai_project', 'Python,Flask,Transformers,MySQL,JavaScript,React'),

('AI Code Review Bot',
 'Analyses student Python code for errors, style issues, and complexity. Returns detailed review with suggestions.',
 'Artificial Intelligence', 'Advanced', 'ai_project', 'Python,Flask,AST,MySQL,JavaScript,React');

-- ── DATA SCIENCE (new category) ───────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('CSV Data Explorer',
 'Upload a CSV and instantly see column statistics, data types, and a preview table. Built with Pandas and Flask.',
 'Data Science', 'Beginner', 'data_science_project', 'Python,Flask,Pandas,HTML,CSS'),

('Simple Bar Chart Generator',
 'Upload tabular data; tool generates a bar chart using Matplotlib. Download the chart as PNG.',
 'Data Science', 'Beginner', 'data_science_project', 'Python,Flask,Matplotlib,HTML,CSS'),

('Student Grade Analyser',
 'Enter student marks; app calculates mean, median, pass/fail rate, and renders a grade distribution chart.',
 'Data Science', 'Beginner', 'data_science_project', 'Python,Flask,Pandas,Matplotlib,MySQL,HTML,CSS'),

('Sales Trend Dashboard',
 'Upload monthly sales CSV; dashboard shows trend lines, top products, and seasonal patterns using Plotly.',
 'Data Science', 'Intermediate', 'data_science_project', 'Python,Flask,Pandas,Plotly,MySQL,HTML,JavaScript'),

('COVID Data Visualisation',
 'Fetch public COVID dataset, clean with Pandas, and display interactive country-wise charts on a world map.',
 'Data Science', 'Intermediate', 'data_science_project', 'Python,Flask,Pandas,Plotly,HTML,JavaScript'),

('Housing Price Predictor',
 'Linear regression model predicts house price from area, rooms, and location features. Web form for predictions.',
 'Data Science', 'Intermediate', 'data_science_project', 'Python,Flask,scikit-learn,Pandas,MySQL,HTML,CSS'),

('Customer Churn Predictor',
 'Train a Random Forest on telecom data to predict customer churn. Interactive dashboard shows feature importance.',
 'Data Science', 'Advanced', 'data_science_project', 'Python,Flask,scikit-learn,Pandas,React,MySQL,Docker'),

('Real-Time Stock Market Analyser',
 'Stream live stock data via API, calculate moving averages, and display interactive candlestick charts.',
 'Data Science', 'Advanced', 'data_science_project', 'Python,Flask,Pandas,Plotly,WebSocket,MySQL,React'),

('Financial Fraud Detection System',
 'Anomaly detection on transaction data using Isolation Forest and AutoEncoder. Real-time alert dashboard.',
 'Data Science', 'Advanced', 'data_science_project', 'Python,Flask,scikit-learn,TensorFlow,Pandas,MySQL,React');

-- ── CYBER SECURITY (new category) ─────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Password Strength Checker',
 'Enter a password and get an instant strength score (Weak/Fair/Strong) with improvement tips. No passwords stored.',
 'Cyber Security', 'Beginner', 'cyber_security_project', 'Python,Flask,HTML,CSS,JavaScript'),

('Caesar Cipher Tool',
 'Encrypt and decrypt messages using Caesar cipher. User selects shift value; tool shows cipher text in real time.',
 'Cyber Security', 'Beginner', 'cyber_security_project', 'Python,Flask,HTML,CSS,JavaScript'),

('Basic Port Scanner',
 'Enter an IP/hostname; tool scans a port range and reports open/closed ports. Result displayed in a table.',
 'Cyber Security', 'Beginner', 'cyber_security_project', 'Python,Flask,HTML,CSS'),

('Secure Password Manager',
 'Store encrypted passwords in MySQL. Master password decrypts vault locally. Clipboard copy and password generator.',
 'Cyber Security', 'Intermediate', 'cyber_security_project', 'Python,Flask,MySQL,Cryptography,HTML,JavaScript'),

('Network Traffic Analyser',
 'Capture network packets with Scapy, parse protocols, and display live packet summary in a Flask dashboard.',
 'Cyber Security', 'Intermediate', 'cyber_security_project', 'Python,Flask,Scapy,MySQL,HTML,JavaScript'),

('Phishing URL Detector',
 'ML model classifies URLs as phishing or legitimate based on lexical features. Web form for URL submission.',
 'Cyber Security', 'Intermediate', 'cyber_security_project', 'Python,Flask,scikit-learn,Pandas,MySQL,HTML,CSS'),

('IDS — Intrusion Detection System',
 'Monitor network traffic, detect anomalous patterns using ML, and trigger alerts with packet capture logging.',
 'Cyber Security', 'Advanced', 'cyber_security_project', 'Python,Flask,scikit-learn,Scapy,MySQL,React,Docker'),

('Secure File Sharing App',
 'AES-encrypted file upload/download platform. Files encrypted at rest, temporary signed URLs, and audit trail.',
 'Cyber Security', 'Advanced', 'cyber_security_project', 'Python,Flask,MySQL,Cryptography,React,Docker'),

('Vulnerability Scanner',
 'Automated web vulnerability scanner — checks for SQLi, XSS, CSRF, open redirects, and security headers.',
 'Cyber Security', 'Advanced', 'cyber_security_project', 'Python,Flask,MySQL,JavaScript,React,Docker');

-- ── IoT (new category) ────────────────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('LED Brightness Control',
 'Control an LED brightness via a web slider. Arduino reads PWM signal from serial; Flask serves the control page.',
 'IoT', 'Beginner', 'iot_project', 'Python,Flask,Arduino,HTML,CSS,JavaScript'),

('Temperature Monitor',
 'DHT11 sensor reads temperature; Raspberry Pi sends data to Flask server. Dashboard shows current reading.',
 'IoT', 'Beginner', 'iot_project', 'Python,Flask,Raspberry Pi,MySQL,HTML,CSS'),

('Button-Triggered Notification',
 'Press a physical button; Arduino sends signal via serial to Flask which emails or notifies the user.',
 'IoT', 'Beginner', 'iot_project', 'Python,Flask,Arduino,HTML,CSS'),

('Smart Home Dashboard',
 'Control multiple GPIO pins (lights, fans) from a web dashboard. State persisted in MySQL; mobile-responsive UI.',
 'IoT', 'Intermediate', 'iot_project', 'Python,Flask,Raspberry Pi,MySQL,JavaScript,HTML,CSS'),

('IoT Environment Monitor',
 'Multi-sensor station (temperature, humidity, air quality) feeds real-time data to a Plotly dashboard via MQTT.',
 'IoT', 'Intermediate', 'iot_project', 'Python,Flask,MQTT,Raspberry Pi,MySQL,JavaScript,Plotly'),

('Plant Watering Automation',
 'Soil moisture sensor triggers water pump via relay. Web dashboard shows moisture history and manual override.',
 'IoT', 'Intermediate', 'iot_project', 'Python,Flask,Arduino,MySQL,JavaScript,HTML,CSS'),

('Smart Energy Monitor',
 'Current sensors measure appliance power consumption. Real-time dashboard shows usage, cost, and carbon footprint.',
 'IoT', 'Advanced', 'iot_project', 'Python,Flask,MQTT,MySQL,Raspberry Pi,React,Chart.js,Docker'),

('Industrial Anomaly Detector',
 'Vibration and temperature sensors feed ML model that detects machine anomalies before failure occurs.',
 'IoT', 'Advanced', 'iot_project', 'Python,Flask,scikit-learn,MQTT,MySQL,React,Docker'),

('Smart City Traffic System',
 'Traffic sensors count vehicles per lane; ML model adjusts signal timings dynamically. Live map dashboard.',
 'IoT', 'Advanced', 'iot_project', 'Python,Flask,MQTT,MySQL,scikit-learn,JavaScript,React,Leaflet.js');

-- ── CLOUD COMPUTING (new category) ────────────────────────────────────
INSERT IGNORE INTO projects (title, description, domain, difficulty, category, technologies) VALUES
('Static Site Deployment Guide',
 'Deploy a simple HTML/CSS site on AWS S3 / Netlify. Includes step-by-step documentation and Bash setup scripts.',
 'Cloud Computing', 'Beginner', 'cloud_project', 'HTML,CSS,AWS,Bash'),

('Dockerised Flask App',
 'Package a Flask app in a Docker container and run it locally. Includes Dockerfile, .dockerignore, and documentation.',
 'Cloud Computing', 'Beginner', 'cloud_project', 'Python,Flask,Docker,MySQL'),

('Cloud File Storage App',
 'Upload files to AWS S3 via a Flask web form. Files listed with download links. Credentials managed via env vars.',
 'Cloud Computing', 'Beginner', 'cloud_project', 'Python,Flask,AWS,MySQL,HTML,CSS'),

('Docker Compose Web Stack',
 'Flask + MySQL + Nginx all orchestrated with Docker Compose. One command spins up the full application stack.',
 'Cloud Computing', 'Intermediate', 'cloud_project', 'Python,Flask,MySQL,Docker,Nginx'),

('CI/CD Pipeline with GitHub Actions',
 'Automated test-and-deploy pipeline: push to GitHub triggers tests, builds Docker image, and deploys to AWS EC2.',
 'Cloud Computing', 'Intermediate', 'cloud_project', 'Python,Flask,Docker,AWS,GitHub Actions'),

('Serverless API with AWS Lambda',
 'Build a CRUD REST API deployed as serverless functions on AWS Lambda with DynamoDB as the database.',
 'Cloud Computing', 'Intermediate', 'cloud_project', 'Python,AWS Lambda,DynamoDB,API Gateway,Serverless'),

('Kubernetes Microservices App',
 'Decompose a monolith into 3 microservices deployed on a Kubernetes cluster. Includes Helm charts and auto-scaling.',
 'Cloud Computing', 'Advanced', 'cloud_project', 'Python,Flask,Docker,Kubernetes,MySQL,Helm,GitHub Actions'),

('Multi-Region Disaster Recovery',
 'Flask app deployed across two AWS regions. Route 53 health checks auto-failover on region outage.',
 'Cloud Computing', 'Advanced', 'cloud_project', 'Python,Flask,AWS,Docker,MySQL,Terraform'),

('Cloud Cost Optimiser Dashboard',
 'Fetches AWS Cost Explorer data, analyses spending by service and tag, and surfaces optimisation recommendations.',
 'Cloud Computing', 'Advanced', 'cloud_project', 'Python,Flask,AWS,MySQL,JavaScript,React,Docker');

-- ============================================================
-- STEP 3 — SKILLS FOR NEW DOMAINS
-- ============================================================

INSERT IGNORE INTO skills (skill_name, project_type, category, weight, estimated_time) VALUES
-- AI / ML project type
('Python',          'ai',        'Backend',      3, '2-3 weeks'),
('Machine Learning','ai',        'AI/ML',        5, '4-6 weeks'),
('TensorFlow',      'ai',        'AI/ML',        4, '3-4 weeks'),
('OpenCV',          'ai',        'AI/ML',        3, '2-3 weeks'),
('Pandas',          'ai',        'Data',         3, '1-2 weeks'),
('NumPy',           'ai',        'Data',         2, '1 week'),
('Flask',           'ai',        'Backend',      3, '1-2 weeks'),
('MySQL',           'ai',        'Database',     2, '1-2 weeks'),
('Git',             'ai',        'Tools',        2, '3-5 days'),

-- Data Science project type
('Python',          'datascience','Backend',     3, '2-3 weeks'),
('Pandas',          'datascience','Data',        4, '1-2 weeks'),
('NumPy',           'datascience','Data',        3, '1 week'),
('Matplotlib',      'datascience','Visualisation',3,'1 week'),
('scikit-learn',    'datascience','AI/ML',       4, '3-4 weeks'),
('MySQL',           'datascience','Database',    2, '1-2 weeks'),
('Flask',           'datascience','Backend',     2, '1-2 weeks'),
('Git',             'datascience','Tools',       2, '3-5 days'),

-- Cyber Security project type
('Python',          'cybersecurity','Backend',   3, '2-3 weeks'),
('Networking',      'cybersecurity','Security',  4, '3-4 weeks'),
('Linux',           'cybersecurity','Security',  3, '2-3 weeks'),
('Cryptography',    'cybersecurity','Security',  4, '2-3 weeks'),
('MySQL',           'cybersecurity','Database',  2, '1-2 weeks'),
('Flask',           'cybersecurity','Backend',   3, '1-2 weeks'),
('Git',             'cybersecurity','Tools',     2, '3-5 days'),

-- IoT project type
('Python',          'iot',       'Backend',      3, '2-3 weeks'),
('Arduino',         'iot',       'Hardware',     4, '2-3 weeks'),
('Raspberry Pi',    'iot',       'Hardware',     4, '2-3 weeks'),
('MQTT',            'iot',       'Protocols',    3, '1 week'),
('MySQL',           'iot',       'Database',     2, '1-2 weeks'),
('Flask',           'iot',       'Backend',      2, '1-2 weeks'),
('Git',             'iot',       'Tools',        2, '3-5 days'),

-- Cloud project type
('Python',          'cloud',     'Backend',      3, '2-3 weeks'),
('Docker',          'cloud',     'DevOps',       4, '2-3 weeks'),
('AWS',             'cloud',     'Cloud',        5, '3-4 weeks'),
('Linux',           'cloud',     'DevOps',       3, '1-2 weeks'),
('MySQL',           'cloud',     'Database',     2, '1-2 weeks'),
('Git',             'cloud',     'Tools',        2, '3-5 days');

-- ============================================================
-- STEP 4 — ADDITIONAL SKILL DEPENDENCIES
-- ============================================================

INSERT IGNORE INTO skill_dependencies (skill_name, depends_on) VALUES
('TensorFlow',      'Python'),
('Machine Learning','Python'),
('Machine Learning','NumPy'),
('Machine Learning','Pandas'),
('OpenCV',          'Python'),
('Matplotlib',      'Python'),
('scikit-learn',    'Python'),
('scikit-learn',    'NumPy'),
('scikit-learn',    'Pandas'),
('MQTT',            'Python'),
('Docker',          'Linux'),
('AWS',             'Linux'),
('AWS',             'Docker'),
('Raspberry Pi',    'Python'),
('Cryptography',    'Python'),
('Networking',      'Linux');
