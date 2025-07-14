import time
import menu.traveller_menu
import utils.utils as utils
import models.scooter as s
import menu.manage_user as users_manage
import menu.scooter_menu as scooter
import menu.traveller_menu as traveller
import menu.log_menu as log
import menu.backup_menu as backup
import db.database as db
import menu.manage_user as users

TGREEN =  '\033[32m'
TRED = '\033[31m'
TWHITE = '\033[0m'
TBLUE = '\033[34m'
TBLACK = '\033[30m'

def show_admin_menu(user):
    is_super_admin  = user.get("role", "").lower() == "super_admin"
    is_system_admin = not is_super_admin

    while True:
        choice = None
        choices = ["1", "2", "3", "4", "5", "6", "7",
                   "t", "s", "m", "u", "l", "b", "q",
                   "T", "S", "M", "U", "L", "B", "Q"]
        if is_system_admin:
            choices += ["p", "e", "x", "P", "E", "X"]

        while choice not in choices:
            utils.clear_screen()
            print(f"\n=== {'Super Admin' if is_super_admin else 'System Admin'} Menu ===")
            print("1. [t] Traveller data")
            print("2. [s] Scooter data")
            print("3. [m] Manage users")
            print("4. [u] Users List")
            print("5. [l] Log Data")
            print("6. [b] Back-ups ")
            if is_system_admin:
                print("7. [p] Update My Password")
                print("8. [e] Edit My Account / Profile")
                print("9. [x] Delete My Account")
            utils.print_colored(f"{'7. ' if is_super_admin else '10. '}[q] Quit to Login", "blue")

            choice = input("\nSelect an option: ").strip().lower()
            if choice not in choices:
                utils.print_colored("[!] Invalid option. Please try again.", "red")
                time.sleep(0.5)

        match choice:
            case "1" | "t" | "T":
                utils.clear_screen(); traveller.traveller_data_menu(user)
            case "2" | "s" | "S":
                utils.clear_screen(); scooter.scooter_data_menu(user)
            case "3" | "m" | "M":
                utils.clear_screen(); users_manage.manage_users_menu(user)
            case "4" | "u" | "U":
                utils.clear_screen(); users.show_users()
            case "5" | "l" | "L":
                utils.clear_screen(); log.show_logs(user)
            case "6" | "b" | "B":
                utils.clear_screen(); backup.Backup_menu(user)
            case "7" | "p" | "P" if is_system_admin:
                utils.clear_screen(); users_manage.update_own_password(user)
            case "8" | "e" | "E" if is_system_admin:
                users_manage.edit_my_account(user)
            case "9" | "x" | "X" if is_system_admin:
                if users_manage.delete_my_account(user):
                    return
            case "7" | "q" | "Q" if is_super_admin:
                utils.print_colored("[↩] Logging out…", "blue")
                time.sleep(1); return
            case "10" | "q" | "Q" if is_system_admin:
                utils.print_colored("[↩] Logging out…", "blue")
                time.sleep(1); return
            
def show_service_engineer_menu(user):
    while True:
        print("\n=== Service Engineer Menu ===")
        print("1. [s] Scooter data")
        print("2. [p] Update Account Password")
        utils.print_colored("3. Exit to Login\n", "blue")

        choice = input("\nSelect an option: ").strip().lower()

        if choice == "1" or choice == "s":
            scooter.scooter_data_menu(user)

        elif choice == "2" or choice == "p":
            utils.clear_screen()
            update_password_service_engineer(user)
            utils.clear_screen()
        elif choice == "3" or choice == "q":
            utils.print_colored("[↩] Logging out...\n", "blue")
            time.sleep(1)
            break
        else:
            utils.print_colored("[!] Invalid option. Please try again.", "red")

def update_password_service_engineer(user):
    print("\n=== Update Account Password ===")

    try:
        new_password = input("Enter new password: ").strip()
        confirm_password = input("Confirm new password: ").strip()
    except (KeyboardInterrupt, EOFError):
        utils.print_colored("\n[!] Interrupted – aborting.", "red")
        return

    if new_password != confirm_password:
        utils.print_colored("[!] Passwords do not match. Please try again.", "red")
        return

    if not utils.is_valid_password(new_password):
        utils.print_colored("[!] Password does not meet security requirements.", "red")
        return

    hashed = utils.hash_password(new_password)

    try:
        conn = db.get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hashed, user["id"]))
        conn.commit()
        conn.close()
        utils.print_colored("[✓] Password updated successfully!", "green")
        
        time.sleep(1.2)
    except Exception:
        utils.print_colored("[!] Failed to update password in the database.", "red")
        time.sleep(1.2)

def update_system_engineer_password(user):
    utils.clear_screen()
    print("\n=== Update My Password ===")

    try:
        new_password = utils.prompt_password()
        if not new_password:
            utils.print_colored("[↩] Password change cancelled.", "blue")
            time.sleep(1)
            return

        hashed = utils.hash_password(new_password)

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