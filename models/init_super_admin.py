import utils.auth as auth
from utils.cryptography import encrypt_data, decrypt_data
import db.database as db
from datetime import datetime

def ensure_super_admin_exists():
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = 'super_admin'")
    if c.fetchone():
        return

    username_encrypt = encrypt_data("super_admin")
    username_hash = auth.hash_username("super_admin")
    role = encrypt_data("super_admin")
    password_hash = auth.hash_password("Admin_123?")
    c.execute("""
        INSERT INTO users (username, username_hash, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, (username_encrypt, username_hash, password_hash, role))
    
    user_id = c.lastrowid
    firstname_encrypt = encrypt_data("Super")
    lastname_encrypt = encrypt_data("Admin")
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        INSERT INTO user_profiles (user_id, first_name, last_name, registration_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, firstname_encrypt, lastname_encrypt, registration_date))

    conn.commit()
    conn.close()
    print(f"[✓] Super Administrator account created (username: super_admin)")
