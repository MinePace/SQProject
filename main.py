import db.database as db 
import models.init_super_admin as admin
import models.traveller as t
import utils.auth as auth
import utils.utils as utils
import menu.menus as menu
import time
from cryptography.fernet import Fernet
import models.log as log
from utils.cryptography import encrypt_data, decrypt_data

def main_menu():
    utils.clear_screen()
    print("\nWelcome to the Urban Mobility Backend System")
    print("=" * 50)
    print("Please log in to continue:")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = auth.login_user(username, password)
    # user = {
    #     'username': 'super_admin',
    #     'role': 'super_admin'
    # }


    if not user:
        utils.print_colored("[!] Login failed. Invalid credentials.\n", "red")
        time.sleep(2)
        return
    else:
        user = dict(user)
        user['username'] = decrypt_data(user['username'])
        user['role'] = decrypt_data(user['role'])

    utils.print_colored("\n[✓] Login successful!", "green")

    if user["role"] in ["system_admin", "super_admin", "System Administrator", "Super Administrator"]:
        count = log.get_unread_suspicious_logs()
        if count > 0:
            utils.print_colored(f"[!] ALERT: {count} suspicious activity log(s) need review!", "red")
            input("Press Enter to acknowledge and mark as read...")
            log.mark_suspicious_logs_as_read()

    time.sleep(1)

    print(f"\n[✓] Welcome, {user['username']}! Role: {user['role']}")


    if user['role'] == "super_admin":
        menu.show_admin_menu(user)
    elif user['role'] == "system_admin":
        menu.show_admin_menu(user)
    elif user['role'] == "service_engineer":
        menu.show_service_engineer_menu(user)
    else:
        utils.print_colored("[!] Role not recognized or not implemented yet.", "red")
        time.sleep(1)

if __name__ == "__main__":
    db.setup_database()
    while True:
        main_menu()
