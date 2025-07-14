import utils.auth as auth
import time
import db.database as db
from datetime import datetime
from utils.cryptography import encrypt_data, decrypt_data

def get_all_users():
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("""
        SELECT 
            u.id,
            u.username,
            u.role,
            up.first_name,
            up.last_name,
            up.registration_date
        FROM users u
        LEFT JOIN user_profiles up ON u.id = up.user_id
    """)
    users = c.fetchall()
    conn.close()

    if not users:
        return None

    return [
        {
            "id": row["id"],
            "username": decrypt_data(row["username"]),
            "role": decrypt_data(row["role"]),
            "first_name": decrypt_data(row["first_name"]) if row["first_name"] else "-",
            "last_name": decrypt_data(row["last_name"]) if row["last_name"] else "-",
            "registration_date": row["registration_date"] if row["registration_date"] else "-"
        }
        for row in users
    ]

def get_user_by_username(name):
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (name,))
    user = c.fetchone()
    conn.close()

    if user is None:
        return None

    return decrypt_user_row(user)

def decrypt_user_row(row):
    return {
        "id": row["id"],
        "username": decrypt_data(row["username"]),
        "role": decrypt_data(row["role"]),
        "first_name": decrypt_data(row["first_name"]) if "first_name" in row and row["first_name"] else None,
        "last_name": decrypt_data(row["last_name"]) if "last_name" in row and row["last_name"] else None,
        "registration_date": row["registration_date"] if "registration_date" in row and row["registration_date"] else "-"
    }

def add_user(user_data):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("""
            INSERT INTO users (username, username_hash, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (
            encrypt_data(user_data['username']),
            auth.hash_username(user_data['username']),
            auth.hash_password(user_data['password']),
            encrypt_data(user_data['role']),
        ))

        user_id = c.lastrowid

        c.execute("""
            INSERT INTO user_profiles (user_id, first_name, last_name, registration_date)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            encrypt_data(user_data['first_name']),
            encrypt_data(user_data['last_name']),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        print("User created successfully")
        time.sleep(0.5)

        conn.commit()
        return True

    except Exception as e:
        print("Error:", e)
        time.sleep(2)
        return False

    finally:
        conn.close()


def update_user(id, user_data):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("""
            UPDATE users
            SET username = ?, password = ?, role = ?
            WHERE id = ?
        """, (
            encrypt_data(user_data['username']),
            user_data['password'],
            encrypt_data(user_data['role']),
            id
        ))

        conn.commit()

        return True

    except Exception as e:
        return e
        
    finally:
        conn.close()

def delete_user(id):
    return