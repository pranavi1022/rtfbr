"""
routes/auth_routes.py
Handles: /api/register  /api/login  /api/logout  /api/me
         /api/forgot-password  /api/verify-otp  /api/reset-password

FEATURE 5 — OTP-based password reset
  - If EMAIL_USER and EMAIL_PASS are set → sends OTP via Gmail SMTP (TLS)
  - Otherwise → prints OTP to server console (demo mode)
"""

import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from logic.keyword_matcher import get_db_connection
from config import EMAIL_USER, EMAIL_PASS, SMTP_HOST, SMTP_PORT

auth_bp = Blueprint('auth', __name__)

# ── In-memory OTP store ──────────────────────────────────────────────────
# Structure: { email: { "otp": "123456", "expires": unix_timestamp } }
_otp_store: dict = {}
OTP_TTL_SECONDS = 300   # OTP valid for 5 minutes


# ── Email helper ─────────────────────────────────────────────────────────

def _send_otp_email(to_email: str, otp: str) -> bool:
    """
    Send the OTP to the user's email via Gmail SMTP with TLS.
    Returns True on success, False on failure.
    Falls back to console print if EMAIL_USER/EMAIL_PASS are not configured.
    """
    if not EMAIL_USER or not EMAIL_PASS:
        print("\n" + "=" * 50)
        print(f"  [SHINE OTP DEMO]  Email : {to_email}")
        print(f"  [SHINE OTP DEMO]  OTP   : {otp}")
        print(f"  [SHINE OTP DEMO]  Valid for {OTP_TTL_SECONDS // 60} minutes")
        print("  (Set EMAIL_USER & EMAIL_PASS in Render env vars)")
        print("=" * 50 + "\n")
        return True

    try:
        print(f"[OTP] Attempting email to {to_email} via {SMTP_HOST}:{SMTP_PORT}")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"SHINE Password Reset OTP: {otp}"
        msg["From"]    = EMAIL_USER
        msg["To"]      = to_email

        text = (
            f"Your SHINE password reset OTP is: {otp}\n\n"
            f"This code is valid for {OTP_TTL_SECONDS // 60} minutes.\n"
            f"If you did not request this, please ignore this email."
        )

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #0a0a0a; color: #ffffff; padding: 40px;">
          <div style="max-width: 480px; margin: 0 auto; text-align: center;">
            <h2 style="color: #ffffff;">SHINE Access Point</h2>
            <p style="color: #aaaaaa;">Password Reset Request</p>
            <div style="background: #1a1a2e; border-radius: 12px; padding: 30px; margin: 24px 0;">
              <p style="color: #cccccc; margin-bottom: 16px;">Your one-time password is:</p>
              <div style="font-size: 36px; font-weight: bold; letter-spacing: 8px; color: #ffffff; font-family: monospace;">
                {otp}
              </div>
              <p style="color: #888888; font-size: 13px; margin-top: 16px;">
                Valid for {OTP_TTL_SECONDS // 60} minutes
              </p>
            </div>
            <p style="color: #666666; font-size: 12px;">
              If you didn't request a password reset, ignore this email.
            </p>
          </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls()          # Enable TLS encryption
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        print(f"[OTP] Email sent successfully to {to_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"[OTP] SMTP Authentication FAILED: {e}")
        print(f"[OTP] Make sure EMAIL_PASS is a Gmail APP PASSWORD (not regular password).")
        print(f"[OTP] Generate at: https://myaccount.google.com/apppasswords")
        print(f"[OTP] Falling back to console — OTP for {to_email}: {otp}")
        return False
    except smtplib.SMTPException as e:
        print(f"[OTP] SMTP error: {e}")
        print(f"[OTP] Falling back to console — OTP for {to_email}: {otp}")
        return False
    except Exception as e:
        print(f"[OTP] Email send FAILED (unexpected): {e}")
        print(f"[OTP] Falling back to console — OTP for {to_email}: {otp}")
        return False


# ── Auth routes ──────────────────────────────────────────────────────────

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data     = request.get_json() or {}
    fullname = data.get('fullname', '').strip()
    username = data.get('username', '').strip()
    email    = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not all([fullname, username, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    hashed = generate_password_hash(password)

    print(f"[API] POST /api/register  username={username!r}")
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable. Please try again later."}), 503
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (fullname, username, email, password_hash) VALUES (%s, %s, %s, %s)",
            (fullname, username, email, hashed)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[auth] Registered OK: {username!r}")
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        err_lower = str(e).lower()
        if "duplicate" in err_lower or "unique" in err_lower:
            if "username" in err_lower:
                return jsonify({"error": "Username already taken"}), 409
            if "email" in err_lower:
                return jsonify({"error": "Email already registered"}), 409
        print(f"[auth] register error: {e}")
        return jsonify({"error": "Registration failed. Please try again."}), 500


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data     = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    print(f"[API] POST /api/login  username={username!r}")
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable. Please try again later."}), 503
    try:
        # Use dictionary=True so _PgConnWrapper returns RealDictCursor (dict rows)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, fullname, username, password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            print(f"[auth] Login FAILED: user not found — {username!r}")
            return jsonify({"error": "Invalid username or password"}), 401

        # Convert to plain dict if it's a psycopg2 RealDictRow
        user = dict(user)

        if not check_password_hash(user["password_hash"], password):
            print(f"[auth] Login FAILED: wrong password — {username!r}")
            return jsonify({"error": "Invalid username or password"}), 401

        session['user_id']  = user['id']
        session['username'] = user['username']
        print(f"[auth] Login OK for {username!r} (id={user['id']})")

        return jsonify({
            "message": "Login successful",
            "user": {
                "id":       user["id"],
                "username": user["username"],
                "fullname": user["fullname"]
            }
        }), 200
    except Exception as e:
        print(f"[auth] login error: {e}")
        return jsonify({"error": "Login failed. Please try again."}), 500


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    print(f"[auth] Logout for user_id={session.get('user_id')}")
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route('/api/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({
        "user_id":  session['user_id'],
        "username": session['username']
    }), 200


# ── FEATURE 5 — Password Reset via OTP ───────────────────────────────────

@auth_bp.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    """
    Step 1: User submits email.
    System checks if email exists, generates OTP, sends via email.
    """
    data  = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({"error": "Email is required"}), 400

    print(f"[API] POST /api/forgot-password  email={email!r}")
    conn = get_db_connection()
    if conn is None:
        print(f"[OTP] DB unavailable — generating OTP without email validation (demo mode)")
        user = True   # skip DB check in demo
    else:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE LOWER(email) = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[auth] forgot-password DB error: {e}")
            return jsonify({"error": "Database error. Please try again."}), 500

    if not user:
        return jsonify({"error": "No account found with that email address."}), 404

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    _otp_store[email] = {
        "otp":     otp,
        "expires": time.time() + OTP_TTL_SECONDS
    }
    print(f"[OTP] Generated OTP for {email!r}")

    email_sent = _send_otp_email(email, otp)

    if EMAIL_USER and EMAIL_PASS and email_sent:
        msg = "OTP sent to your email address. Please check your inbox."
    elif EMAIL_USER and EMAIL_PASS and not email_sent:
        msg = "Failed to send email. OTP printed to server console (demo fallback)."
    else:
        msg = "OTP generated. Check server console for the OTP (demo mode)."

    return jsonify({"message": msg}), 200


@auth_bp.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    """Step 2: Verify the OTP."""
    data  = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    otp   = data.get('otp',   '').strip()

    if not email or not otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    record = _otp_store.get(email)

    if not record:
        return jsonify({"error": "No OTP was sent to this email. Please request again."}), 400

    if time.time() > record["expires"]:
        _otp_store.pop(email, None)
        return jsonify({"error": "OTP has expired. Please request a new one."}), 400

    if record["otp"] != otp:
        return jsonify({"error": "Incorrect OTP. Please try again."}), 400

    record["verified"] = True
    print(f"[OTP] Verified for {email!r}")
    return jsonify({"message": "OTP verified successfully."}), 200


@auth_bp.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Step 3: Reset the password after OTP is verified."""
    data         = request.get_json() or {}
    email        = data.get('email',        '').strip().lower()
    new_password = data.get('new_password', '').strip()

    if not email or not new_password:
        return jsonify({"error": "Email and new password are required"}), 400

    if len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    record = _otp_store.get(email)

    if not record or not record.get("verified"):
        return jsonify({"error": "Please verify your OTP before resetting the password."}), 403

    if time.time() > record["expires"]:
        _otp_store.pop(email, None)
        return jsonify({"error": "Session expired. Please start over."}), 400

    hashed = generate_password_hash(new_password)
    print(f"[API] POST /api/reset-password  email={email!r}")
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable. Cannot save new password right now."}), 503
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE LOWER(email) = %s",
            (hashed, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[auth] reset-password DB error: {e}")
        return jsonify({"error": "Failed to reset password. Please try again."}), 500

    _otp_store.pop(email, None)
    print(f"[auth] Password reset successful for {email!r}")
    return jsonify({"message": "Password reset successful. You can now log in."}), 200
