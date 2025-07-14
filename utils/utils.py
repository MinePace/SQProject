import os
import sys
import platform
from datetime import datetime
import db.database as db
import bcrypt

# ──────────────────── UTILS ──────────────────── #

def print_colored(text: str, color: str) -> None:
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def remove_last_line():
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[F")

    sys.stdout.write("\033[J")
    sys.stdout.flush()
    

def _safe_input(valid_choices: set[str], prompt: str = "Select an option: ") -> str:
    while True:
        try:
            choice = input(prompt).strip().lower()[:2]
        except (EOFError, KeyboardInterrupt):
            print_colored("\n[!] Interrupted - exiting…", "red")
            raise SystemExit

        if choice in valid_choices:
            return choice
        print_colored("[!] Invalid option. Please try again.", "red")

# ─────────────────── USERNAME ───────────────────

_ALLOWED_USER_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz0123456789_'."
)
def is_valid_username(name: str) -> bool:
    name = name.lower()
    print(f"Validating username: {name}")
    print(8 <= len(name) <= 10 and(name[0].isalpha() or name[0] == "_") and all(ch in _ALLOWED_USER_CHARS for ch in name))
    return (8 <= len(name) <= 10 and(name[0].isalpha() or name[0] == "_") and all(ch in _ALLOWED_USER_CHARS for ch in name))

def check_db_duplicate(username):
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE lower(username) = ? LIMIT 1", (username.lower(),))
    user = c.fetchone()
    return user is None

# ─────────────────── PASSWORD ───────────────────

_SPECIALS = set("~!@#$%&_-+=`|\\(){}[]:;'<>,.?/")
def is_valid_password(pwd: str) -> bool:
    if not (12 <= len(pwd) <= 30):
        return False
    kinds = {
        "lower": any(c.islower() for c in pwd),
        "upper": any(c.isupper() for c in pwd),
        "digit": any(c.isdigit() for c in pwd),
        "spec": any(c in _SPECIALS for c in pwd),
    }
    if not all(kinds.values()):
        return False

    return all(ch.isalnum() or ch in _SPECIALS for ch in pwd)

# ─────────────────────────────── PROMPTS ────────────────────────────── #

def prompt_username():
    while True:
        try:
            name = input("Username (8-10 chars, a-z 0-9 _'.) [Q=cancel]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print_colored("\n[!] Interrupted - aborting.", "red")
            return None
        if name.lower() == "q":
            print_colored("[↩] BACK", "blue")
            return None
        if is_valid_username(name):
            if not check_db_duplicate(name):
                print_colored("[!] Username already in use, try again.", "red")
                continue
            return name.lower()
        print_colored("[!] Invalid username, try again.", "red")

def prompt_password():
    while True:
        try:
            pwd = input("Password (12-30 chars, mix Aa1! ) [Q=cancel]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print_colored("\n[!] Interrupted - aborting.", "red")
            return None
        if pwd.lower() == "q":
            print_colored("[↩] BACK", "blue")
            return None
        if is_valid_password(pwd):
            return pwd
        print_colored("[!] Weak or invalid password, try again.", "red")

# ─────────────────────────────── HASH / ADD DB ────────────────────────────── #

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def add_to_db(username, password, role):
    hashp = hash_password(password)
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username.lower(), hashp, role))
    conn.commit()

# ─────────────────────────────── SHOW ALL SYSTEM ADMINS ────────────────────────────── #

def show_all_system_admins():
    conn = db.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE role = 'system_admin'")
    admins = c.fetchall()
    conn.close()

    if not admins:
        print_colored("[!] No System Admins found.", "red")
        return

    print("\n=== System Admins ===")
    for admin in admins:
        print(f"Username: {admin[0]}")
    print("\n")

# ─────────────────────────────── is valid first/last name ────────────────────────────── #

def is_valid_name(name: str) -> bool:
    return name.isalpha() and 1 <= len(name) <= 30

# ─────────────────────────────── add user profile ────────────────────────────── #

def get_user_profile_names(user_id):
    while True:
        try:
            first = input("Enter first name (1-30 letters only) [Q=cancel]: ").strip()
            if first.lower() == "q":
                print_colored("[↩] BACK", "blue")
                return None, None
            if not is_valid_name(first):
                print_colored("[!] Invalid first name. Letters only, max 30 characters.", "red")
                continue

            last = input("Enter last name (1-30 letters only) [Q=cancel]: ").strip()
            if last.lower() == "q":
                print_colored("[↩] BACK", "blue")
                return None, None
            if not is_valid_name(last):
                print_colored("[!] Invalid last name. Letters only, max 30 characters.", "red")
                continue

            return first, last
        except (KeyboardInterrupt, EOFError):
            print_colored("\n[!] Interrupted – aborting.", "red")
            return None, None

def add_user_profile(user, first_name, last_name):
    conn = db.get_db_connection()
    c = conn.cursor()
    hashed_first_name = hash_password(first_name)
    hashed_last_name = hash_password(last_name)
    c.execute("INSERT INTO user_profiles (user_id, first_name, last_name, registration_date) VALUES (?, ?, ? ?)",
        (user["id"], hashed_first_name, hashed_last_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))