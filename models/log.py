import db.database as db
from datetime import datetime
from utils.cryptography import encrypt_data, decrypt_data

def add_log(log_data):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")

        c.execute("""
            INSERT INTO logs (date, time, username, activity, additional_info, suspicious, read)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (
            date,
            time,
            encrypt_data(log_data['username']),
            encrypt_data(log_data['activity']),
            encrypt_data(log_data['additional_info']),
            log_data['suspicious']
        ))

        conn.commit()
        conn.close()
        return True

    except Exception:
        return False

def get_logs():
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    logs = c.fetchall()
    conn.close()

    if logs is None:
        return None

    return [decrypt_log_row(row) for row in logs]

def decrypt_log_row(row):
    return {
        "id": row[0],
        "date": row[1],
        "time": row[2],
        "username": decrypt_if_needed(row[3]),
        "activity": decrypt_if_needed(row[4]),
        "additional_info": decrypt_if_needed(row[5]),
        "suspicious": row[6]
    }

def is_encrypted(value):
    return isinstance(value, str) and value.startswith("gAAA")

def decrypt_if_needed(value):
    return decrypt_data(value) if is_encrypted(value) else value

def get_unread_suspicious_logs():
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as count FROM logs WHERE suspicious = 1 AND read = 0")
    count = c.fetchone()["count"]
    conn.close()
    return count

def mark_suspicious_logs_as_read():
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE logs SET read = 1 WHERE suspicious = 1 AND read = 0")
    conn.commit()
    conn.close()
