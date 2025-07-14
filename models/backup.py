import db.database as db
from datetime import datetime
from utils.cryptography import encrypt_data, decrypt_data
import sqlite3
import time
import os
import zipfile
import shutil
from pathlib import Path

def get_available_backups(user=None):    
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT id, code, assigned_to, backup_file, used FROM restore_codes WHERE used = 0")
    backups = c.fetchall()
    conn.close()

    if not backups:
        return []

    filtered_backups = []

    for backup in backups:
        id, code, assigned_to_enc, backup_file, used = backup

        if assigned_to_enc:
            assigned_to = decrypt_data(assigned_to_enc)
        else:
            assigned_to = None

        if user:
            if user['role'] == "super_admin" and assigned_to is None:
                filtered_backups.append(backup)
            elif user['role'] == "system_admin" and assigned_to == str(user['id']):
                filtered_backups.append(backup)
        else:
            filtered_backups.append(backup)

    return [decrypt_backup_row(row) for row in filtered_backups]

def decrypt_backup_row(row):
    return {
        "id": row[0],
        "code": decrypt_data(row[1]),
        "assigned_to": decrypt_data(row[2]),
        "backup_file": decrypt_data(row[3]),
        "used": row[4]
    }


def get_used_backups():
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT backup_file FROM restore_codes")
    used_files = {decrypt_data(row[0]) for row in c.fetchall() if row[0] is not None}
    conn.close()
    return used_files

def create_backup(original_path, temp_db_path):
    src_conn = sqlite3.connect(original_path)
    dst_conn = sqlite3.connect(temp_db_path)

    try:
        src_cursor = src_conn.cursor()
        dst_cursor = dst_conn.cursor()

        tables = ["logs", "restore_codes", "scooters", "travellers", "user_profiles", "users"]

        for table in tables:
            src_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'")
            create_sql = src_cursor.fetchone()
            if not create_sql:
                continue
            dst_cursor.execute(create_sql[0])

            src_cursor.execute(f"SELECT * FROM {table}")
            rows = src_cursor.fetchall()
            if rows:
                placeholders = ", ".join(["?"] * len(rows[0]))
                dst_cursor.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)

        dst_conn.commit()
    finally:
        src_conn.close()
        dst_conn.close()

def add_restore_code(code, user_id, backup_file):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("""
            INSERT INTO restore_codes (code, assigned_to, backup_file, used)
            VALUES (?, ?, ?, ?)
        """, (encrypt_data(code), encrypt_data(user_id), encrypt_data(backup_file), False))

        conn.commit()
        conn.close()
        return True
    
    except sqlite3.Error as e:
        print(f"Error adding restore code: {e}")
        time.sleep(2)
        return False

def execute_backup(backup):
    conn = None
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM restore_codes WHERE id = ? AND used = 0", (backup['id'],))
        backup_check = c.fetchone()

        if not backup_check:
            print("Invalid or already used backup code.")
            return False

        c.execute("UPDATE restore_codes SET used = 1 WHERE id = ?", (backup['id'],))
        conn.commit()
        conn.close()

        current_dir = Path(__file__).resolve().parent
        zip_filename = backup['backup_file']
        zip_path = (current_dir / ".." / "menu" / "backups" / zip_filename).resolve()

        restore_dir = current_dir / "restored_backup"
        restore_dir.mkdir(exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(restore_dir)

        extracted_db_path = restore_dir / "mobility_selected.db"
        if not extracted_db_path.exists():
            print("Backup file does not contain expected mobility_selected.db.")
            return False

        current_db_path = (current_dir / ".." / "data" / "mobility.db").resolve()

        if current_db_path.exists():
            os.remove(current_db_path)

        shutil.move(str(extracted_db_path), str(current_db_path))

        shutil.rmtree(restore_dir)

        print("Backup restored successfully.")
        return True

    except sqlite3.Error as e:
        print(f"Database error during backup execution: {e}")
        time.sleep(2)
        return False

    except Exception as e:
        print(f"Error executing backup: {e}")
        time.sleep(2)
        return False

    finally:
        if conn:
            conn.close()


def revoke_restore_code(backup_id):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM restore_codes WHERE id = ?", (backup_id,))
        backup = c.fetchone()

        if not backup:
            return False

        c.execute("DELETE FROM restore_codes WHERE id = ?", (backup_id,))
        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Error revoking restore code: {e}")
        time.sleep(2)
        return False

    finally:
        conn.close()