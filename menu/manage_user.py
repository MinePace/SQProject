import time
import db.database as db
import utils.utils as utils
import bcrypt
import models.user as u
import utils.utils as utils
import utils.auth as auth
from utils.cryptography import encrypt_data, decrypt_data
from datetime import datetime
import utils.cryptography as crypto

# ─────────────────────────────── select user ────────────────────────────── #

def select_user(user):
    conn = db.get_db_connection()
    c = conn.cursor()

    valid_roles = {"super_admin", "system_admin", "service_engineer"}
    user_role = user.get('role', '').lower()
    if user_role not in valid_roles:
        utils.print_colored("[!] Access denied: Invalid role.", "red")
        conn.close()
        return None

    c.execute("SELECT id, username, role FROM users")
    all_users = c.fetchall()
    conn.close()

    filtered_users = []
    for row in all_users:
        try:
            role = crypto.decrypt_data(row['role'])
        except Exception:
            continue
        if user_role == "super_admin" and role in ("system_admin", "service_engineer"):
            filtered_users.append(row)
        elif user_role == "system_admin" and role == "service_engineer":
            filtered_users.append(row)

    if not filtered_users:
        utils.print_colored("[!] No users found.", "red")
        return None

    print("\nAvailable users:")
    for idx, row in enumerate(filtered_users, 1):
        try:
            username = crypto.decrypt_data(row['username'])
            role = crypto.decrypt_data(row['role'])
        except Exception:
            username = "<decryption error>"
            role = "<decryption error>"
        print(f"{idx}. ID: {row['id']}, Username: {username}, Role: {role}")

    while True:
        choice = input("Select a user by number (or Q to cancel): ").strip()
        if choice.lower() == "q":
            return None
        if not choice.isdigit():
            utils.print_colored("[!] Please enter a valid number.", "red")
            continue
        choice_num = int(choice)
        if 1 <= choice_num <= len(filtered_users):
            return filtered_users[choice_num - 1]
        else:
            utils.print_colored("[!] Invalid selection. Please choose a valid number.", "red")

# ─────────────────────────────── edit user ─────────────────────────────── #
def edit_user(current_user):
    selected = select_user(current_user)
    if not selected:
        return

    user_id  = selected["id"]
    username = decrypt_data(selected["username"])
    role     = decrypt_data(selected["role"])

    while True:
        utils.clear_screen()
        print(f"\n=== Edit User: {username} (Role: {role}) ===")
        print("1. Edit username")
        print("2. Edit password")
        print("3. Edit profile (first / last name)")
        print("Q. Quit")
        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            new_username = utils.prompt_username()
            if not new_username or new_username == username:
                utils.print_colored("[!] Username unchanged or cancelled.", "yellow")
                time.sleep(1)
                continue

            enc_username  = encrypt_data(new_username)
            username_hash = auth.hash_username(new_username)

            with db.get_db_connection() as conn:
                conn.execute(
                    "UPDATE users SET username = ?, username_hash = ? WHERE id = ?;",
                    (enc_username, username_hash, user_id)
                )

            username = new_username
            utils.print_colored("[✓] Username updated.", "green")
            time.sleep(1)

        elif choice == "2":
            new_pw = utils.prompt_password()
            if not new_pw:
                utils.print_colored("[!] Password change cancelled.", "yellow")
                time.sleep(1)
                continue

            pw_hash = auth.hash_password(new_pw)
            with db.get_db_connection() as conn:
                conn.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?;",
                    (pw_hash, user_id)
                )

            utils.print_colored("[✓] Password updated.", "green")
            time.sleep(1)

        elif choice == "3":
            new_first, new_last = utils.get_user_profile_names(user_id)
            if not new_first or not new_last:
                utils.print_colored("[!] Profile update cancelled.", "yellow")
                time.sleep(1)
                continue

            enc_first = encrypt_data(new_first)
            enc_last  = encrypt_data(new_last)
            with db.get_db_connection() as conn:
                conn.execute(
                    "UPDATE user_profiles SET first_name = ?, last_name = ? WHERE user_id = ?;",
                    (enc_first, enc_last, user_id)
                )

            utils.print_colored("[✓] Profile updated.", "green")
            time.sleep(1)

        elif choice == "q":
            break

        else:
            utils.print_colored("[!] Invalid option.", "red")
            time.sleep(1)

# ─────────────────────────────── manage users ────────────────────────────── #
def manage_users_menu(current_user):
    while True:
        utils.clear_screen()
        print("=== Manage Users ===")
        print("1. [a] Add user")
        print("2. [e] Edit user")
        print("3. [d] Delete user")
        print("4. [r] Reset user password (temporary)")
        utils.print_colored("5. [q] Quit to main menu\n", "blue")
        choice = input("Select an option: ").strip().lower()

        if choice in ("1", "a"):
            add_user(current_user)
            print("\n[✓] User added successfully!")
            time.sleep(1)
            utils.clear_screen()
        elif choice in ("2", "e"):
            edit_user(current_user)
            print("\n[✓] User edited successfully!")
            time.sleep(1)
            utils.clear_screen()
        elif choice in ("3", "d"):
            delete_user(current_user)
            print("\n[✓] User deleted successfully!")
            time.sleep(1)
            utils.clear_screen()
            continue
        elif choice in ("4", "r"):
            reset_temp_password_menu(current_user)
            print("\n[✓] Temporary password reset successfully!")
            time.sleep(1)
            utils.clear_screen()
            continue
        elif choice in ("5", "q"):
            utils.print_colored("[↩] Returning to Main Menu...\n", "blue")
            time.sleep(1)
            utils.clear_screen()
            break
        else:
            utils.print_colored("[!] Invalid option. Please try again.", "red")
            time.sleep(1)

# ─────────────────────────────── show users ────────────────────────────── #
def show_users():
    print("\n=== All User Data ===")
    users = u.get_all_users()
    if users:
        print(f"{'ID':<3} | {'Username':<16} | {'Role':<16} | {'First Name':<12} | {'Last Name':<12} | Registered")
        print("-" * 85)
        for user in users:
            print(f"{user['id']:<3} | {user['username']:<16} | {user['role']:<16} | "
                  f"{(user['first_name'] or '-'): <12} | {(user['last_name'] or '-'): <12} | {user['registration_date']}")
        input("\nPress Enter to continue...")
    else:
        utils.print_colored("[!] No users found.", "red")
        input("Press Enter to continue...")

    utils.print_colored("[↩] Returning to Main Menu...\n", "blue")
    time.sleep(1)
    utils.clear_screen()

# ─────────────────────────────── delete user ────────────────────────────── #

def delete_user(current_user):
    selected = select_user(current_user)
    if not selected:
        return

    user_id = selected["id"]
    username = decrypt_data(selected["username"])

    confirm = input(f"\nAre you sure you want to delete user '{username}'? [y/N]: ").strip().lower()
    if confirm != "y":
        utils.print_colored("[↩] Cancelled deletion.", "yellow")
        time.sleep(1)
        return

    with db.get_db_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

    utils.print_colored(f"[✓] User '{username}' and profile deleted.", "green")
    time.sleep(1)


def add_user(current_user):

    current_role = current_user.get("role", "").lower()
    if current_role == "super_admin":
        allowed_roles = ["system_admin", "service_engineer"]
    elif current_role == "system_admin":
        allowed_roles = ["service_engineer"]
    else:
        utils.print_colored("[!] You are not allowed to add users.", "red")
        time.sleep(1.5)
        return

    while True:
        utils.clear_screen()
        print("\n=== Create New User ===")
        for i, r in enumerate(allowed_roles, 1):
            print(f"{i}. {r}")
        choice = input("Select role (Q=cancel): ").strip().lower()
        if choice == "q":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(allowed_roles):
            new_role = allowed_roles[int(choice) - 1]
            break
        utils.print_colored("[!] Invalid choice.", "red")

    new_username = utils.prompt_username()
    if not new_username:
        return

    new_password = utils.prompt_password()
    if not new_password:
        return

    first_name, last_name = utils.get_user_profile_names(None)
    if not first_name or not last_name:
        return

    try:
        enc_username  = encrypt_data(new_username)
        enc_role      = encrypt_data(new_role)
        enc_first     = encrypt_data(first_name)
        enc_last      = encrypt_data(last_name)

        with db.get_db_connection() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO users (username, username_hash, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, (
                enc_username,
                auth.hash_username(new_username),
                auth.hash_password(new_password),
                enc_role
            ))
            user_id = c.lastrowid
            c.execute("""
                INSERT INTO user_profiles (user_id, first_name, last_name, registration_date)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                enc_first,
                enc_last,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()

        utils.print_colored("[✓] User and profile created successfully.", "green")
        time.sleep(1)

    except Exception as e:
        utils.print_colored(f"[!] Failed to add user: {e}", "red")
        time.sleep(2)


# ─────────────────────────────── reset_temp_pw ────────────────────────────── #
def reset_temp_password_menu(current_user):
    selected = select_user(current_user)
    if not selected:
        return

    user_id = selected["id"]
    username = decrypt_data(selected["username"])

    utils.clear_screen()
    print(f"\n=== Reset Password for: {username} ===")

    new_pw = utils.prompt_password()
    if not new_pw:
        utils.print_colored("[↩] Password reset cancelled.", "blue")
        time.sleep(1)
        return

    pw_hash = auth.hash_password(new_pw)

    with db.get_db_connection() as conn:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (pw_hash, user_id))

    utils.print_colored(f"[✓] Password reset successfully for user '{username}'.", "green")
    time.sleep(1)

# ─────────────────────────────── system-admin self-service ────────────────────────────── #

def edit_my_account(user):
    user_id  = user["id"]
    username = user["username"]

    while True:
        utils.clear_screen()
        print(f"\n=== Edit My Account ({username}) ===")
        print("1. Change username")
        print("2. Update profile (first / last name)")
        print("Q. Back")
        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            new_username = utils.prompt_username()
            if not new_username or new_username == username:
                utils.print_colored("[↩] Username unchanged.", "blue")
                time.sleep(1)
                continue

            enc_username  = encrypt_data(new_username)
            username_hash = auth.hash_username(new_username)

            with db.get_db_connection() as conn:
                conn.execute(
                    "UPDATE users SET username = ?, username_hash = ? WHERE id = ?",
                    (enc_username, username_hash, user_id)
                )

            user["username"] = new_username
            username = new_username
            utils.print_colored("[✓] Username updated.", "green")
            time.sleep(1)

        elif choice == "2":
            first, last = utils.get_user_profile_names(None)
            if not first or not last:
                utils.print_colored("[↩] Profile update cancelled.", "blue")
                time.sleep(1)
                continue

            enc_first = encrypt_data(first)
            enc_last  = encrypt_data(last)

            with db.get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM user_profiles WHERE user_id = ?", (user_id,))
                if cur.fetchone():
                    cur.execute(
                        "UPDATE user_profiles SET first_name = ?, last_name = ? WHERE user_id = ?",
                        (enc_first, enc_last, user_id)
                    )
                else:
                    cur.execute(
                        """INSERT INTO user_profiles
                           (user_id, first_name, last_name, registration_date)
                           VALUES (?, ?, ?, ?)""",
                        (user_id, enc_first, enc_last,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    )

            utils.print_colored("[✓] Profile updated.", "green")
            time.sleep(1)

        elif choice == "q":
            return
        else:
            utils.print_colored("[!] Invalid option.", "red")
            time.sleep(1)


def delete_my_account(user):
    utils.clear_screen()
    confirm = input("❗  Delete your own account and log out? [y/N]: ").strip().lower()
    if confirm != "y":
        utils.print_colored("[↩] Deletion cancelled.", "blue")
        time.sleep(1)
        return False

    user_id  = user["id"]
    username = decrypt_data(user["username"])

    with db.get_db_connection() as conn:
        conn.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))

    utils.print_colored(f"[✓] Account '{username}' deleted.", "green")
    time.sleep(1.2)
    return True

def update_own_password(user):
    utils.clear_screen()
    print("\n=== Update My Password ===")

    try:
        new_password = utils.prompt_password()
        if not new_password:
            utils.print_colored("[↩] Password change cancelled.", "blue")
            time.sleep(1)
            return

        hashed = auth.hash_password(new_password)

        with db.get_db_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (hashed, user["id"])
            )

        utils.print_colored("[✓] Password updated successfully!", "green")
        time.sleep(1)

    except Exception as e:
        utils.print_colored(f"[!] Failed to update password: {e}", "red")
        time.sleep(2)


