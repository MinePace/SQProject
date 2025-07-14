import sqlite3
import bcrypt
import db.database as db
import os
import hashlib
from datetime import datetime
import time
from collections import defaultdict
import models.log as l

# ─────────────────────────────── LOGIN/REGISTER ────────────────────────────── #

def login_user(username: str, password: str):
    conn = db.get_db_connection()
    c = conn.cursor()

    username_hash = hash_username(username)
    c.execute("SELECT * FROM users WHERE username_hash = ?", (username_hash,))
    user = c.fetchone()

    if user and check_password(password, user['password_hash']):
        failed_logins.pop(username, None)
        log_data = {
            "username": username,
            "activity": "Login successful",
            "additional_info": "",
            "suspicious": 0
        }
        l.add_log(log_data)
        return user

    suspicious = 1 if is_suspicious_attempt(username) else 0
    log_data = {
            "username": username,
            "activity": "Login failed",
            "additional_info": "Invalid password or username",
            "suspicious": suspicious
        }
    l.add_log(log_data)

    time.sleep(1)
    return None

# ─────────────────────────────── BCRYPT ────────────────────────────── #

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def hash_username(username: str) -> str:
    return hashlib.sha256(username.lower().encode()).hexdigest()

def check_username(username: str, hashed: str) -> bool:
    return bcrypt.checkpw(username.encode('utf-8'), hashed.encode('utf-8'))
    
# ─────────────────────────────── SUS ACTIVITIES ────────────────────────────── #

failed_logins = defaultdict(list)

def is_suspicious_attempt(username: str) -> bool:
    now = time.time()
    failed_logins[username].append(now)
    failed_logins[username] = [t for t in failed_logins[username] if now - t <= 60]
    return len(failed_logins[username]) >= 3

