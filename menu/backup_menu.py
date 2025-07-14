from datetime import datetime
import sqlite3
from pathlib import Path
import zipfile
import utils.utils as utils
import time
import random

import models.backup as b
import models.user as u
import models.log as l

def Backup_menu(user):
    while True:
        choices = {"1", "2", "3",
                   "c", "e", "q",
                   "C", "E", "Q"}
        choice = None

        if user['role'] == "system_admin" or user['role'] == "super_admin":
            while choice not in choices:
                utils.clear_screen()
                print("\n=== Backup data Menu ===")
                print("1. [c] Create backup")
                print("2. [e] Execute backup")
                utils.print_colored("3. [q] Quit to Main Menu", "blue")

                if user["role"] == "super_admin":
                    utils.print_colored("\n=== Super Admin Only ===", "green")
                    utils.print_colored("4. [a] Appoint backup Code", "green")
                    utils.print_colored("5. [r] Revoke backup Code", "green")
                    choices.update({"4", "a", "A", "5", "r", "R"})

                choice = input("\nSelect an option: ").strip()
                if choice not in choices:
                    utils.print_colored("\n[!] Invalid option. Please try again.", "red")
                    time.sleep(0.5)
                    continue
            
            match choice:
                case 1 | "c" | "C":
                    create_backup(user)
                case 2 | "e" | "E":
                    execute_backup(user)
                case 3 | "q" | "Q":
                    utils.print_colored("[↩] Returning to Main Menu", "blue")
                    time.sleep(1)
                    return
                case 4 | "a" | "A":
                    appoint_backup(user)
                case 5 | "r" | "R":
                    revoke_backup_code(user)
            
        else:
            utils.clear_screen()
            utils.print_colored("[!] Access Denied. You do not have permission to access this menu.", "red")
            time.sleep(1.5)
            return
            
        utils.clear_screen()

def create_backup(user):
    utils.clear_screen()
    if user['role'] not in ["super_admin", "system_admin"]:
        utils.print_colored("[!] Unauthorized to create backup.", "red")
        time.sleep(2)
        return

    original_path = Path("data/mobility.db")
    BASE_DIR = Path(__file__).resolve().parent
    backup_dir = BASE_DIR / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"mobility_selected_backup_{timestamp}.zip"
    backup_zip_path = backup_dir / backup_name
    temp_db_path = Path(f"temp_selected_backup_{timestamp}.db")

    if not original_path.exists():
        utils.print_colored("[!] Original database not found.", "red")
        return

    b.create_backup(original_path, temp_db_path)
    
    with zipfile.ZipFile(backup_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(temp_db_path, arcname="mobility_selected.db")

    temp_db_path.unlink()

    utils.print_colored(f"[✓] Selected tables backed up to: {backup_zip_path}", "green")
    print(f"Full backup path: {backup_zip_path.resolve()}")
    time.sleep(2)
    return backup_zip_path.name

def execute_backup(user):
    utils.clear_screen()
    print("\n=== Execute a Backup ===")
    backups = b.get_available_backups(user)
    if backups:
        for backup in backups:
            print(backup['id'], "|", backup['backup_file'], "|", backup['code'])
    else:
        utils.print_colored("No available backups were found","red")
        time.sleep(1)
        return
    print("")
    while True:
        choice = input("Enter backup ID to execute: ")
        if choice.lower() == 'q':
            utils.print_colored("[↩] Returning to Backup Menu", "blue")
            time.sleep(1)
            return
        selected_backup = next((b for b in backups if str(b['id']) == choice), None)
        if not selected_backup:
            utils.print_colored("[!] Invalid backup ID.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
        break

    code = input("Please enter the restore code to execute this backup: ")
    if code != selected_backup['code']:
        utils.print_colored("[!] Invalid restore code.", "red")
        time.sleep(1)
        return
    
    if b.execute_backup(selected_backup):
        utils.print_colored("[✓] Backup executed successfully.", "green")
        log_data = {
            "username": user['username'],
            "activity": "Execute Backup",
            "additional_info": f"Executed backup {selected_backup['backup_file']}",
            "suspicious": 0
        }
        l.add_log(log_data)
        time.sleep(0.5)
        utils.print_colored("[↩] Returning to Backup Menu", "blue")
        time.sleep(1)
    else:
        utils.print_colored(f"[!] Failed to execute backup", "red")
        log_data = {
            "username": user['username'],
            "activity": "Execute Backup",
            "additional_info": f"Failed to execute backup {selected_backup['backup_file']}",
            "suspicious": 0
        }
        time.sleep(10)
        return

def appoint_backup(user):
    utils.clear_screen()
    print("\n=== Appoint a Backup Code ===")
    backup_dir = Path(__file__).resolve().parent / "backups"
    if not backup_dir.exists():
        utils.print_colored("[!] No backup directory found.", "red")
        time.sleep(2)
        return

    backup_files = {f.name for f in backup_dir.glob("*.zip")}
    used_files = b.get_used_backups()
    available_backups = sorted(list(backup_files - used_files))

    if not available_backups:
        utils.print_colored("[!] No unassigned backups available.", "yellow")
        time.sleep(2)
        return
    
    print("\nAvailable Backups:")
    for i, fname in enumerate(available_backups, 1):
        print(f"{i}. {fname}")

    try:
        choice = int(input("\nSelect a backup to assign (by number): "))
        selected_file = available_backups[choice - 1]
    except (ValueError, IndexError):
        utils.print_colored("[!] Invalid selection.", "red")
        time.sleep(2)
        return
    
    available_users = u.get_all_users()
    system_admins = [user for user in available_users if user.get('role') == 'system_admin']

    print("\nAvailable System Admins:")
    print(f"ID | {'Username':<16} ")
    print("-" * 30)
    for sa in system_admins:
        print(f"{sa['id']:<2} | {sa['username']}")
    print("")

    while True:
        choice = input("Enter admin ID to assign this backup: ")
        selected_user = next((user for user in system_admins if str(user['id']) == choice), None)
        if not selected_user:
            utils.print_colored("[!] Invalid user ID.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
        break
    
    code = "{:08d}".format(random.randint(10000000, 99999999))


    if b.add_restore_code(code, str(selected_user['id']), selected_file):
        utils.print_colored(f"[✓] Backup code {code} assigned to {selected_user['username']} for backup {selected_file}.", "green")
        log_data = {
            "username": user['username'],
            "activity": "Appoint Backup Code",
            "additional_info": f"Assigned backup code {code} to user {selected_user['username']}",
            "suspicious": 0
        }
        l.add_log(log_data)
        time.sleep(1)
        return
    else:
        utils.print_colored("[!] Failed to assign backup code.", "red")
        time.sleep(1)
        return

def revoke_backup_code(user):
    utils.clear_screen()
    print("\n=== Revoke a Backup Code ===")
    backups = b.get_available_backups()
    if not backups:
        utils.print_colored("[!] No available backups found.", "red")
        time.sleep(2)
        return
    print("\nAvailable Backups:")
    for backup in backups:
        print(f"ID: {backup['id']} | File: {backup['backup_file']} | Code: {backup['code']}")
    print("")
    while True:
        choice = input("Enter backup ID to revoke: ")
        selected_backup = next((b for b in backups if str(b['id']) == choice), None)
        if not selected_backup:
            utils.print_colored("[!] Invalid backup ID.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
        break
    if b.revoke_restore_code(selected_backup['id']):
        utils.print_colored(f"[✓] Backup code {selected_backup['code']} revoked successfully.", "green")
        log_data = {
            "username": user['username'],
            "activity": "Revoke Backup Code",
            "additional_info": f"Revoked backup code {selected_backup['code']}",
            "suspicious": 0
        }
        l.add_log(log_data)
        time.sleep(1)
    