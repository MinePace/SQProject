import sqlite3
from pathlib import Path
from utils.cryptography import encrypt_data
import bcrypt
import hashlib
from datetime import datetime
import time

def get_db_connection():
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "mobility.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def delete_users():
    db_path = Path("data")
    db_path.mkdir(exist_ok=True)

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    DROP TABLE users
    """)

    conn.commit()
    conn.close()

    print("Users deleted")
    time.sleep(2)

def delete_logs():
    db_path = Path("data")
    db_path.mkdir(exist_ok=True)

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
    DROP TABLE logs
    """)

    conn.commit()
    conn.close()

    print("Logs deleted")
    time.sleep(2)


def setup_database():
    db_path = Path("data")
    db_path.mkdir(exist_ok=True)

    conn = get_db_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username BLOB NOT NULL,
        username_hash TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER,
        first_name BLOB,
        last_name BLOB,
        registration_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)


    c.execute("""
    CREATE TABLE IF NOT EXISTS travellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name BLOB,
        last_name BLOB,
        birthday TEXT,
        gender TEXT,
        street_name BLOB,
        house_number BLOB,
        zip_code BLOB,
        city BLOB,
        email BLOB,
        mobile_phone BLOB,
        driving_license BLOB,
        registration_date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS scooters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT,
        model TEXT,
        serial_number TEXT UNIQUE,
        top_speed REAL,
        battery_capacity REAL,
        state_of_charge INTEGER,
        target_range_soc TEXT,
        location TEXT,
        out_of_service INTEGER,
        mileage REAL,
        last_maintenance_date TEXT,
        in_service_date TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        username BLOB,
        activity BLOB,
        additional_info BLOB,
        suspicious INTEGER,
        read INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS restore_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code BLOB,
        assigned_to BLOB,
        backup_file BLOB,
        used INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def delete_and_add_db():
    db_path = Path("data/mobility.db")
    if db_path.exists():
        db_path.unlink()
        print("[✓] Database file deleted.")
    else:
        print("[i] No existing database found. Creating a fresh one...")

    setup_database()
    conn = get_db_connection()
    conn.close()
    print("[✓] Database recreated and super_admin ensured.")
